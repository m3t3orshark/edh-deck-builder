"""Liste complète des cartes qui servent les synergies d'un commandant, axe par axe.

Contrairement aux sites de statistiques, la sélection ne dépend pas de la popularité :
chaque axe est une recherche Scryfall exhaustive. La popularité (rang EDHREC fourni par
Scryfall) est seulement affichée, pour repérer les cartes peu jouées.

Usage :
  python synergy_search.py --identity wubg --axes axes.txt --out synergies.md [--bracket 2] [--commander "Nom"]
  python synergy_search.py --commanders [--identity wub] --axes axes.txt --out commandants.md
      (--commanders : ne cherche que des cartes pouvant être commandant ; l'identité devient
       facultative et sert de plafond de couleurs si elle est donnée)

axes.txt : une ligne par recherche, « Nom de l'axe :: requête Scryfall ». Plusieurs lignes
peuvent porter le même nom d'axe : leurs résultats sont fusionnés. Lignes vides et
lignes commençant par # ignorées. Exemple :
  Marqueurs stun :: o:"stun counter"
  Prolifération :: o:proliferate
  Prolifération :: o:"additional counter"
"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import OrderedDict
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_deck as vd  # noqa: E402  (devise du profil)

API = "https://api.scryfall.com/cards/search"
HEADERS = {"User-Agent": "edh-deck-builder/1.0", "Accept": "application/json"}
RARE_PLAY = 10000  # au-delà de ce rang EDHREC (ou sans rang), la carte est « peu jouée »


def search(q, cap=700):
    url = API + "?" + urllib.parse.urlencode({"q": q, "unique": "cards", "order": "cmc"})
    cards = []
    while url and len(cards) < cap:
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=30) as r:
                data = json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return []
            detail = e.read()[:200].decode("utf-8", "replace")
            raise RuntimeError(f"requête refusée par Scryfall ({e.code}) : {detail}")
        cards += data.get("data", [])
        url = data.get("next_page")
        time.sleep(0.1)
    return cards


def oracle(c):
    faces = c.get("card_faces")
    if faces and "oracle_text" not in c:
        return " // ".join(f.get("oracle_text", "") for f in faces)
    return c.get("oracle_text", "")


def cost(c):
    if c.get("mana_cost"):
        return c["mana_cost"]
    faces = c.get("card_faces") or []
    return faces[0].get("mana_cost", "") if faces else ""


def popularity(c):
    rank = c.get("edhrec_rank")
    if rank is None:
        return "jamais classée (pépite potentielle)"
    if rank > RARE_PLAY:
        return f"peu jouée (rang {rank})"
    return f"rang {rank}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--identity", default=None)
    ap.add_argument("--commanders", action="store_true", help="ne garder que les cartes pouvant être commandant")
    ap.add_argument("--axes", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--bracket", type=int, default=None)
    ap.add_argument("--commander", default=None, help="exclut le commandant de la liste")
    ap.add_argument("--devise", choices=sorted(vd.DEVISES), default=None)
    a = ap.parse_args()
    if a.devise:
        vd.set_currency(a.devise)
    sys.stdout.reconfigure(encoding="utf-8")

    axes = OrderedDict()
    for line in open(a.axes, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#") or "::" not in line:
            continue
        name, query = (x.strip() for x in line.split("::", 1))
        axes.setdefault(name, []).append(query)

    if not a.identity and not a.commanders:
        sys.exit("--identity est requis (sauf avec --commanders).")
    base = "legal:commander game:paper -t:stickers -t:attraction"  # hors des 100 cartes
    if a.identity:
        base = f"id<={a.identity} " + base
    if a.commanders:
        base = "is:commander " + base
    if a.bracket is not None and a.bracket <= 2:
        base += " -is:gamechanger"
    seen_axes = {}
    title = "Commandants possibles" if a.commanders else "Cartes synergiques"
    ident = f"Identité {a.identity.upper()}" if a.identity else "Toutes couleurs"
    out = [f"# {title}{f' : {a.commander}' if a.commander else ''}", "",
           f"{ident}{f', bracket {a.bracket}' if a.bracket else ''}. "
           "Sélection exhaustive par recherche de texte, indépendante de la popularité. "
           f"« Peu jouée » : au-delà du rang EDHREC {RARE_PLAY}.", ""]
    summary = []
    for name, queries in axes.items():
        found = OrderedDict()
        for q in queries:
            try:
                for c in search(f"({q}) {base}"):
                    if a.commander and c["name"].lower() == a.commander.lower():
                        continue
                    found.setdefault(c["name"], c)
            except RuntimeError as exc:
                print(f"[{name}] {q} : {exc}")
        cards = sorted(found.values(), key=lambda c: (c.get("cmc", 0), c["name"]))
        rare = sum(1 for c in cards if (c.get("edhrec_rank") or 10**9) > RARE_PLAY)
        summary.append(f"- {name} : {len(cards)} cartes, dont {rare} peu jouées"
                       + (" ; ATTENTION : axe trop large (plus de 150 cartes), resserre la requête sur ce qui "
                          "interagit vraiment avec le commandant, puis relance" if len(cards) > 150 else ""))
        out += [f"## {name} ({len(cards)} cartes, dont {rare} peu jouées)", "",
                "Requête(s) : " + " ; ".join(f"`{q}`" for q in queries), ""]
        for c in cards:
            others = [x for x in seen_axes.get(c["name"], []) if x != name]
            gc = " | GAME CHANGER" if c.get("game_changer") else ""
            key, sym = vd.DEVISES[vd.CURRENCY][0], vd.currency_symbol()
            eur = c.get("prices", {}).get(key)
            price = f" | ~{float(eur):.0f} {sym}" if eur and float(eur) >= 1 else (f" | <1 {sym}" if eur else "")
            text = oracle(c).replace("\n", " / ")
            text = text if len(text) <= 220 else text[:217] + "…"
            also = f" | aussi : {', '.join(others)}" if others else ""
            colors = "".join(c.get("color_identity", [])) or "C"
            idt = f" | identité {colors}" if a.commanders else ""
            out.append(f"- **{c['name']}** {cost(c)} | {c.get('type_line', '')}{idt} | {popularity(c)}{price}{gc}{also}  \n  {text}")
            seen_axes.setdefault(c["name"], []).append(name)
        out.append("")
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("\n".join(summary))
    print(f"Total : {len(seen_axes)} cartes différentes. Liste écrite dans {a.out}")


if __name__ == "__main__":
    main()
