"""Lit un export de collection ManaBox (CSV) et le croise avec Scryfall.

Usage :
  python collection.py <export.csv> summary
  python collection.py <export.csv> pool --identity ubr [--bracket 2] [--out pool.txt]
  python collection.py <export.csv> check <deck.txt>

Options communes :
  --exclude-binders "Nom1" "Nom2"  ignore ces classeurs
  --only-binders "Nom1" "Nom2"     ne garde que ces classeurs (l'option peut aussi être répétée)
  --proxies-possedes               compte les proxies comme des cartes possédées (par défaut, non)
Une carte est possédée dès qu'il en existe au moins un exemplaire réel, toutes éditions et langues
confondues ; qu'elle soit déjà dans un deck monté ne change rien. Un proxy n'est pas un exemplaire
possédé : check compte les cartes présentes « en proxy seulement » parmi les cartes manquantes,
en les signalant (cartes en test, achat à décider). Les listes ManaBox (Binder Type « list », ex. une liste d'envies) sont toujours ignorées.
La date du dernier ajout (colonne Added) indique la fraîcheur de l'export.
"""
import argparse
import csv
import json
import os
import sys
import time
import urllib.request
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_deck as vd  # noqa: E402
from verify_deck import card_price, fetch_cards, fmt_price, parse_deck  # noqa: E402

HEADERS = {"User-Agent": "edh-deck-builder/1.0", "Accept": "application/json", "Content-Type": "application/json"}
BASICS = {"plains", "island", "swamp", "mountain", "forest", "wastes"}


def truthy(v):
    return str(v).strip().lower() in {"true", "1", "yes", "oui"}


def load_export(path, exclude=(), only=(), proxies_owned=False):
    """Retourne {scryfall_id: quantité} des exemplaires possédés, {scryfall_id: quantité} des proxies
    (vide si les proxies comptent comme possédés), des statistiques de lecture et la date du dernier ajout."""
    owned = defaultdict(int)
    proxies = defaultdict(int)
    skipped = defaultdict(int)
    last_added = ""
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            binder = row.get("Binder Name", "")
            qty = int(row.get("Quantity") or 1)
            if (row.get("Binder Type") or "").lower() == "list":
                skipped[f"liste « {binder} »"] += qty
                continue
            if only and binder not in only:
                skipped[f"classeur « {binder} » (non retenu)"] += qty
                continue
            if binder in exclude:
                skipped[f"classeur « {binder} » (exclu)"] += qty
                continue
            last_added = max(last_added, (row.get("Added") or "")[:10])
            sid = row.get("Scryfall ID")
            if not sid:
                continue
            if truthy(row.get("Proxy")) and not proxies_owned:
                proxies[sid] += qty
            else:
                owned[sid] += qty
    return owned, proxies, skipped, last_added


def fmt_total(value):
    return f"moins de 1 {vd.CURRENCY}" if value < 1 else f"environ {round(value):.0f} {vd.CURRENCY}"


def fmt_date(iso):
    """2025-07-31 -> 31/07/2025 ; chaîne vide si inconnue."""
    return f"{iso[8:10]}/{iso[5:7]}/{iso[:4]}" if len(iso) == 10 else ""


def fetch_by_ids(ids):
    """Récupère les cartes Scryfall par identifiant d'impression, par lots de 75."""
    cards = {}
    ids = list(ids)
    for i in range(0, len(ids), 75):
        body = json.dumps({"identifiers": [{"id": x} for x in ids[i:i + 75]]}).encode()
        req = urllib.request.Request("https://api.scryfall.com/cards/collection", data=body, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=60) as r:
            for c in json.load(r).get("data", []):
                cards[c["id"]] = c
        time.sleep(0.1)
    return cards


def by_oracle(owned, cards):
    """Regroupe les quantités par carte (nom Oracle), toutes impressions confondues."""
    agg = {}
    for sid, qty in owned.items():
        c = cards.get(sid)
        if not c:
            continue
        key = c["name"].lower()
        if key not in agg:
            agg[key] = {"card": c, "qty": 0}
        agg[key]["qty"] += qty
    return agg


def front(name):
    return name.split(" // ")[0].strip().lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("export")
    ap.add_argument("command", choices=["summary", "pool", "check"])
    ap.add_argument("deck", nargs="?")
    ap.add_argument("--identity", default=None)
    ap.add_argument("--bracket", type=int, default=None)
    ap.add_argument("--out", default=None)
    # action="extend" : « --only-binders A --only-binders B » garde A et B (sans cela, B écrasait A)
    ap.add_argument("--exclude-binders", nargs="*", action="extend", default=[])
    ap.add_argument("--only-binders", nargs="*", action="extend", default=[])
    ap.add_argument("--proxies-possedes", action="store_true",
                    help="compte les proxies comme des cartes possédées (réglage collection.proxies_possedes du profil)")
    ap.add_argument("--devise", choices=sorted(vd.DEVISES), default=None)
    a = ap.parse_args()
    if a.devise:
        vd.set_currency(a.devise)
    sys.stdout.reconfigure(encoding="utf-8")

    owned, proxies, skipped, last_added = load_export(a.export, a.exclude_binders, a.only_binders, a.proxies_possedes)
    try:
        cards = fetch_by_ids(set(owned) | set(proxies))
    except Exception as exc:
        print(f"Impossible de joindre Scryfall : {exc}")
        sys.exit(2)
    agg = by_oracle(owned, cards)
    agg_proxy = {k: v for k, v in by_oracle(proxies, cards).items() if k not in agg}
    total = sum(v["qty"] for v in agg.values())
    ignored = "; ".join(f"{k} : {v}" for k, v in skipped.items())
    date = fmt_date(last_added)
    print(f"Collection{f' (dernier ajout le {date})' if date else ''} : {total} cartes possédées, "
          f"{len(agg)} cartes différentes"
          + (f" ; {len(agg_proxy)} cartes présentes en proxy seulement" if agg_proxy else "")
          + (" (proxies comptés comme possédés)" if a.proxies_possedes else "")
          + (f" (ignoré : {ignored})" if ignored else ""))

    if a.command == "summary":
        binders = defaultdict(int)
        with open(a.export, encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                binders[(row.get("Binder Name", ""), row.get("Binder Type", ""))] += int(row.get("Quantity") or 1)
        for (b, t), q in sorted(binders.items()):
            print(f"- {b} ({t}) : {q} cartes")
        return

    if a.command == "pool":
        if not a.identity:
            sys.exit("--identity est requis pour pool (ex. --identity ubr).")
        ident = set(a.identity.upper())
        rows = []
        for v in agg.values():
            c = v["card"]
            if c.get("legalities", {}).get("commander") != "legal":
                continue
            if not set(c.get("color_identity", [])) <= ident:
                continue
            if front(c["name"]) in BASICS:
                continue
            gc = c.get("game_changer", False)
            if a.bracket is not None and a.bracket <= 2 and gc:
                continue
            faces = c.get("card_faces") or [c]
            cost = c.get("mana_cost") or faces[0].get("mana_cost", "")
            rows.append((c.get("type_line", ""), c.get("cmc", 0), c["name"], cost, v["qty"], gc))
        rows.sort(key=lambda r: (r[0].split(" — ")[0], r[1], r[2]))
        lines = [f"{n} {cost} | {t}{' | GAME CHANGER' if gc else ''}{f' | x{q}' if q > 1 else ''}"
                 for t, _, n, cost, q, gc in rows]
        print(f"Cartes jouables dans l'identité {a.identity.upper()} : {len(lines)}")
        if a.out:
            with open(a.out, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            print(f"Liste écrite dans {a.out}")
        else:
            print("\n".join(lines))
        return

    # check : quelles cartes du deck sont possédées, en proxy seulement, ou à acquérir
    if not a.deck:
        sys.exit("Indique le fichier du deck pour check.")
    entries, _ = parse_deck(a.deck)
    owned_front = {front(k) for k in agg}
    proxy_front = {front(k) for k in agg_proxy}
    have, proxied, missing = [], [], []
    for qty, name, _ in entries:
        if front(name) in BASICS:
            continue
        f = front(name)
        (have if f in owned_front else proxied if f in proxy_front else missing).append((qty, name))
    deck_cards, _ = fetch_cards([n for _, n in proxied + missing])

    def listing(title, rows):
        cost = 0.0
        print(f"{title} : {sum(q for q, _ in rows)} cartes")
        for qty, name in sorted(rows, key=lambda x: x[1]):
            c = deck_cards.get(name.lower())
            e = card_price(c) if c else None
            cost += (e or 0) * qty
            print(f"- {qty} {name} ({fmt_price(e) if e is not None else 'prix inconnu'})")
        if rows:
            print(f"  coût approximatif : {fmt_total(cost)}")
        return cost

    n_have, n_proxy, n_missing = (sum(q for q, _ in rows) for rows in (have, proxied, missing))
    print(f"\nDéjà en ta possession (au moins un exemplaire réel, toutes éditions) : {n_have} cartes "
          "(terrains de base non comptés)")
    print(f"Cartes qui te manquent : {n_proxy + n_missing}"
          + (f", dont {n_proxy} déjà jouée(s) en proxy (en test, achat à décider)" if n_proxy else ""))
    c1 = listing("- manquantes, déjà en proxy", proxied) if proxied else 0.0
    c2 = listing("- manquantes, ni possédées ni en proxy", missing) if missing else 0.0
    if n_proxy + n_missing:
        print(f"Coût approximatif de toutes les cartes manquantes : {fmt_total(c1 + c2)}")


if __name__ == "__main__":
    main()
