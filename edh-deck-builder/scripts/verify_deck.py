"""Vérifie une liste de deck Commander au format deckstats via l'API Scryfall.

Usage : python verify_deck.py deck.txt [--bracket N] [--max-prix PRIX] [--seuil PRIX] [--devise EUR|USD] [--no-prices]

--seuil : seuil de mise en évidence des cartes chères ; par défaut, celui du profil
          (prix.seuil_mise_en_evidence de PROFIL.md), 30 si le profil est illisible.
--devise : EUR (Cardmarket) ou USD (TCGplayer), les deux prix fournis par Scryfall ; par défaut
           celle du profil (prix.devise), EUR si le profil est illisible.
--max-prix (ancien nom : --max-eur) : budget par carte, dans la devise retenue.

Contrôles : total de 100 cartes, singleton, légalité Commander,
disponibilité en papier, identité couleur, nombre de Game Changers.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

SCRYFALL_COLLECTION = "https://api.scryfall.com/cards/collection"
LINE_RE = re.compile(r"^\s*(\d+)x?\s+(?:\[[^\]]*\]\s*)?(.+?)\s*$")
# Suffixe d'impression deckstats : « (SLD) 2683 », « (PLIST) ELD-281 »…
PRINTING_RE = re.compile(r"\s+\([A-Za-z0-9]+\)\s+\S+$")
HIGHLIGHT_EUR = 30.0  # seuil de secours si le profil est illisible (informatif)
PROFILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "PROFIL.md")


def load_profile():
    """Profil de l'utilisateur (bloc JSON de PROFIL.md), ou None s'il est illisible."""
    try:
        text = open(PROFILE_PATH, encoding="utf-8").read()
        m = re.search(r"```json\s*\n(.*?)\n```", text, re.S)
        return json.loads(m.group(1)) if m else None
    except (OSError, ValueError):
        return None


# Devises : celles dont Scryfall fournit le prix (clé du prix, source, symbole court).
DEVISES = {"EUR": ("eur", "Cardmarket", "€"), "USD": ("usd", "TCGplayer", "$")}


def profile_currency():
    """Devise du profil, et vrai si c'est la valeur de secours (EUR)."""
    d = ((load_profile() or {}).get("prix") or {}).get("devise")
    return (d, False) if d in DEVISES else ("EUR", True)


CURRENCY = profile_currency()[0]


def set_currency(code):
    """Change la devise de toutes les fonctions de prix (option --devise des scripts)."""
    global CURRENCY
    if code not in DEVISES:
        raise ValueError(f"devise inconnue : {code} (EUR ou USD)")
    CURRENCY = code


def currency_source():
    return DEVISES[CURRENCY][1]


def currency_symbol():
    return DEVISES[CURRENCY][2]


def profile_threshold():
    """Seuil de mise en évidence du profil, et vrai si c'est la valeur de secours."""
    p = load_profile() or {}
    v = (p.get("prix") or {}).get("seuil_mise_en_evidence")
    if isinstance(v, (int, float)) and not isinstance(v, bool) and v >= 0:
        return float(v), False
    return HIGHLIGHT_EUR, True


MAX_GAME_CHANGERS = {1: 0, 2: 0, 3: 3}
# Sections qui ne font pas partie des 100 cartes (leurs cartes sont vérifiées quand même).
SPARE_SECTIONS = {"sideboard", "maybeboard"}
PLAIN_HEADERS = {"commander", "sideboard", "maybeboard", "deck", "main"}


def parse_deck(path):
    """Retourne (cartes du deck, cartes hors deck), chacune en (quantité, nom, est_commandant)."""
    entries, spares = [], []
    section = "main"
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if line.startswith("//"):
                section = line[2:].strip().lower()
                continue
            # Titres sans « // » reconnus par l'import deckstats : « Commander », « Sideboard ».
            if line.lower().rstrip(":") in PLAIN_HEADERS:
                section = line.lower().rstrip(":")
                continue
            target = spares if section in SPARE_SECTIONS else entries
            is_commander = section == "commander" or "!commander" in line.lower()
            line = line.split(" #", 1)[0]
            line = PRINTING_RE.sub("", line)
            match = LINE_RE.match(line)
            if not match:
                print(f"Ligne ignorée (format non reconnu) : {raw.rstrip()}")
                continue
            target.append((int(match.group(1)), match.group(2), is_commander))
    return entries, spares


def fetch_cards(names):
    """Interroge Scryfall par lots de 75 noms. Retourne (cartes par nom, introuvables)."""
    found, missing = {}, []
    unique = list(dict.fromkeys(names))
    for i in range(0, len(unique), 75):
        batch = unique[i:i + 75]
        body = json.dumps({"identifiers": [{"name": n} for n in batch]}).encode()
        req = urllib.request.Request(
            SCRYFALL_COLLECTION,
            data=body,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "edh-deck-builder/1.0",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
        for card in data.get("data", []):
            found[card["name"].lower()] = card
            # Les cartes doubles peuvent être écrites avec une seule face.
            front = card["name"].split(" // ")[0].lower()
            found.setdefault(front, card)
        missing += [m.get("name", "?") for m in data.get("not_found", [])]
        time.sleep(0.1)  # Scryfall demande une pause entre les requêtes

    # Cartes Aventure, cartes doubles… : Scryfall ne trouve parfois que la face avant.
    still_missing = []
    for name in missing:
        front = name.split(" // ")[0]
        card = search_card(f'!"{front}"') if front != name else None
        if card:
            found[name.lower()] = card
        else:
            still_missing.append(name)
    return found, still_missing


def search_card(query):
    """Première carte d'une recherche Scryfall, ou None si aucun résultat."""
    url = "https://api.scryfall.com/cards/search?" + urllib.parse.urlencode(
        {"q": query, "unique": "cards"}
    )
    req = urllib.request.Request(
        url, headers={"Accept": "application/json", "User-Agent": "edh-deck-builder/1.0"}
    )
    time.sleep(0.1)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)["data"][0]
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise


def fmt_price(value):
    return f"<1 {CURRENCY}" if value < 1 else f"~{value:.0f} {CURRENCY}"


def card_price(card):
    """Ordre de prix dans la devise retenue : impression renvoyée par Scryfall, sinon la moins chère qui a un prix."""
    key = DEVISES[CURRENCY][0]
    price = card.get("prices", {}).get(key) or card.get("prices", {}).get(key + "_foil")
    if price:
        return float(price)
    return cheapest_price(card)


def cheapest_price(card):
    """Prix de l'impression papier la moins chère dans la devise retenue, ou None si inconnu."""
    key = DEVISES[CURRENCY][0]
    url = "https://api.scryfall.com/cards/search?" + urllib.parse.urlencode(
        {"q": f'oracleid:{card["oracle_id"]} game:paper', "unique": "prints", "order": key, "dir": "asc"}
    )
    req = urllib.request.Request(
        url, headers={"Accept": "application/json", "User-Agent": "edh-deck-builder/1.0"}
    )
    time.sleep(0.1)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            prints = json.load(resp).get("data", [])
    except urllib.error.HTTPError:
        return None
    prices = [float(c["prices"][key]) for c in prints if c.get("prices", {}).get(key)]
    return min(prices) if prices else None


# Anciens noms, gardés pour les scripts et notes qui les emploient encore.
card_eur, cheapest_eur, fmt_eur = card_price, cheapest_price, fmt_price


COLORS = "WUBRG"
BASIC_TYPES = {"Plains": "W", "Island": "U", "Swamp": "B", "Mountain": "R", "Forest": "G"}


def card_text(card):
    text = card.get("oracle_text", "") or ""
    for face in card.get("card_faces", []):
        text += " " + (face.get("oracle_text", "") or "")
    return text


def produced_colors(card, identity):
    """Couleurs que la carte peut produire (terrains, rocks, créatures à mana, fetchs)."""
    produced = set(card.get("produced_mana", [])) & set(COLORS)
    if produced:
        return produced
    if "Land" in card.get("type_line", ""):
        text = card_text(card)
        if "Search your library for" in text:
            if "basic land card" in text:
                return set(identity)
            return {c for t, c in BASIC_TYPES.items() if t in text} & set(identity)
    return set()


def mana_report(entries, cards, identity):
    """Sources de mana par couleur, symboles de mana demandés, courbe et nombre de terrains.

    Une carte multicolore compte comme source de chacune de ses couleurs : on compare donc,
    pour chaque couleur, la part des producteurs de mana qui la donnent (couverture) à la
    part des symboles de cette couleur dans les coûts.
    """
    sources = {c: 0 for c in identity}
    restricted = {c: 0 for c in identity}
    restricted_names = []
    pips = {c: 0 for c in identity}
    producers = 0
    curve, lands, spells_mv = {}, 0, []
    for qty, name, is_cmd in entries:
        card = cards.get(name.lower())
        if not card:
            continue
        is_land = "Land" in card.get("type_line", "").split("//")[0]
        colors = produced_colors(card, identity) & set(identity)
        is_restricted = "spend this mana only" in card_text(card).lower()
        if colors:
            producers += qty
            if is_restricted:
                restricted_names.append(name)
            for c in colors:
                sources[c] += qty
                if is_restricted:
                    restricted[c] += qty
        if is_land:
            lands += qty
            continue
        cost = card.get("mana_cost") or " ".join(f.get("mana_cost", "") for f in card.get("card_faces", [])[:1])
        for c in identity:
            pips[c] += cost.count("{" + c + "}") + cost.count("/" + c + "}") + cost.count("{" + c + "/")
        if not is_cmd:
            mv = int(card.get("cmc", 0))
            curve[min(mv, 7)] = curve.get(min(mv, 7), 0) + qty
            spells_mv += [card.get("cmc", 0)] * qty

    warnings = []
    total_pips = sum(pips.values()) or 1
    lines = ["Base de mana :"]
    lines.append(f"  Terrains : {lands} ; producteurs de mana colorés (terrains, rocks, dorks…) : {producers}")
    for c in sorted(identity, key=COLORS.index):
        p_share = 100 * pips[c] / total_pips
        coverage = 100 * sources[c] / (producers or 1)
        extra = f", dont {restricted[c]} à mana restreint" if restricted[c] else ""
        lines.append(f"  {c} : {sources[c]} sources, soit {coverage:.0f} % des producteurs{extra} ; "
                     f"{pips[c]} symboles ({p_share:.0f} % des symboles)")
        if pips[c] and sources[c] - restricted[c] < 12:
            warnings.append(f"seulement {sources[c] - restricted[c]} sources de {c} sans restriction "
                            f"(viser au moins 12 à 15 pour une couleur jouée)")
        if pips[c] and coverage + 10 < p_share:
            warnings.append(f"le {c} est donné par {coverage:.0f} % des producteurs seulement, "
                            f"pour {p_share:.0f} % des symboles")
    if restricted_names:
        lines.append("  Mana restreint (« Spend this mana only… », inutilisable pour certains paiements) : "
                     + ", ".join(restricted_names))
    avg = sum(spells_mv) / len(spells_mv) if spells_mv else 0
    lines.append("  Courbe (hors terrains et commandant) : "
                 + ", ".join(f"{k if k < 7 else '7+'}: {v}" for k, v in sorted(curve.items()))
                 + f" ; valeur de mana moyenne {avg:.2f}")
    if lands < 33 or lands > 40:
        warnings.append(f"{lands} terrains : hors de la fourchette habituelle (33 à 40)")
    for w in warnings:
        lines.append(f"  Attention : {w}")
    return "\n".join(lines)


def pairing_errors(cmd_cards):
    """Vérifie qu'une paire de commandants a le droit d'être associée."""
    if len(cmd_cards) <= 1:
        return []
    if len(cmd_cards) > 2:
        return ["Plus de deux commandants : impossible."]
    (n1, c1), (n2, c2) = cmd_cards

    def info(c):
        text = card_text(c)
        kw = {k.lower() for k in c.get("keywords", [])}
        m_with = re.search(r"Partner with ([^(\n]+?)(?: \(|\n|$)", text)
        m_var = re.search(r"Partner\u2014([^(\n]+?)(?: \(|\n|$)", text)
        return {
            "with": m_with.group(1).strip() if m_with else None,
            "variant": m_var.group(1).strip() if m_var else None,
            "partner": "partner" in kw and not m_with and not m_var,
            "friends": "friends forever" in kw,
            "choose_bg": "choose a background" in kw,
            "background": "Background" in c.get("type_line", ""),
            "companion": "doctor's companion" in kw,
            "doctor": "Time Lord Doctor" in c.get("type_line", ""),
        }

    a, b = info(c1), info(c2)
    ok = (
        (a["partner"] and b["partner"])
        or (a["with"] and a["with"].lower() == c2["name"].lower() and b["with"] and b["with"].lower() == c1["name"].lower())
        or (a["variant"] and a["variant"] == b["variant"])
        or (a["friends"] and b["friends"])
        or (a["choose_bg"] and b["background"]) or (b["choose_bg"] and a["background"])
        or (a["companion"] and b["doctor"]) or (b["companion"] and a["doctor"])
    )
    if ok:
        return []
    return [f"Paire de commandants non autorisée : {n1} et {n2}. Il faut deux cartes avec « Partner », "
            f"un « Partner with » qui désigne l'autre, la même variante « Partner—… », « Friends forever » "
            f"des deux côtés, « Choose a Background » avec un Background, ou « Doctor's companion » avec un Docteur."]


def exists_in_paper(card):
    """Le champ games ne vaut que pour l'impression renvoyée : vérifier toutes les impressions."""
    if "paper" in card.get("games", []):
        return True
    return search_card(f'oracleid:{card["oracle_id"]} game:paper') is not None


def allows_any_number(card):
    text = card.get("oracle_text", "") or ""
    for face in card.get("card_faces", []):
        text += face.get("oracle_text", "")
    return "any number of cards named" in text or "Basic" in card.get("type_line", "")


def check_card(name, card, identity):
    """Erreurs de légalité, de disponibilité papier et d'identité couleur d'une carte."""
    errors = []
    legality = card.get("legalities", {}).get("commander")
    if legality != "legal":
        errors.append(f"{name} : non légale en Commander ({legality}).")
    if not exists_in_paper(card):
        errors.append(f"{name} : carte uniquement numérique.")
    if not set(card.get("color_identity", [])) <= identity:
        errors.append(f"{name} : hors de l'identité couleur du commandant.")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("deck")
    parser.add_argument("--bracket", type=int, default=None)
    parser.add_argument("--max-prix", "--max-eur", dest="max_prix", type=float, default=None,
                        help="budget par carte fixé par l'utilisateur : chaque carte au-dessus devient une erreur")
    parser.add_argument("--devise", choices=sorted(DEVISES), default=None,
                        help="devise des prix ; par défaut celle du profil")
    parser.add_argument("--seuil", type=float, default=None,
                        help="seuil de mise en évidence ; par défaut celui du profil")
    parser.add_argument("--no-prices", action="store_true", help="ne pas calculer les prix (plus rapide)")
    args = parser.parse_args()
    if args.devise:
        set_currency(args.devise)
    sys.stdout.reconfigure(encoding="utf-8")

    entries, spares = parse_deck(args.deck)
    errors = []

    total = sum(q for q, _, _ in entries)
    if total != 100:
        errors.append(f"Total = {total} cartes (attendu : 100, commandant(s) compris).")

    commanders = [n for _, n, c in entries if c]
    if not commanders:
        errors.append("Aucun commandant trouvé (section Commander vide ou absente).")

    try:
        cards, missing = fetch_cards([n for _, n, _ in entries + spares])
    except Exception as exc:  # réseau indisponible, API en panne…
        print(f"Impossible de joindre Scryfall : {exc}")
        print(f"Total compté localement : {total} cartes.")
        sys.exit(2)

    for name in missing:
        errors.append(f"Carte introuvable sur Scryfall (nom à vérifier) : {name}")

    errors += pairing_errors([(n, cards[n.lower()]) for n in commanders if n.lower() in cards])
    identity = set()
    for name in commanders:
        card = cards.get(name.lower())
        if card:
            identity |= set(card.get("color_identity", []))

    game_changers = []
    for qty, name, _ in entries:
        card = cards.get(name.lower())
        if not card:
            continue
        errors += check_card(name, card, identity)
        if qty > 1 and not allows_any_number(card):
            errors.append(f"{name} : {qty} exemplaires (singleton).")
        if card.get("game_changer"):
            game_changers.append(name)

    # Le maybeboard ne compte pas dans les 100, mais ses cartes doivent être jouables.
    for _, name, _ in spares:
        card = cards.get(name.lower())
        if card:
            errors += [f"[Maybeboard] {e}" for e in check_card(name, card, identity)]

    limit = MAX_GAME_CHANGERS.get(args.bracket)
    if limit is not None and len(game_changers) > limit:
        errors.append(
            f"{len(game_changers)} Game Changers pour un bracket {args.bracket} "
            f"(maximum {limit}) : {', '.join(game_changers)}"
        )

    if not args.no_prices:
        priced, unknown, deck_eur = [], [], 0.0
        for qty, name, _ in entries:
            card = cards.get(name.lower())
            if not card or "Basic Land" in card.get("type_line", ""):
                continue
            eur = card_price(card)
            if eur is None:
                unknown.append(name)
                continue
            deck_eur += eur * qty
            priced.append((eur, name))
        priced.sort(reverse=True)
        print(f"Ordre de prix du deck ({currency_source()} via Scryfall, indicatif) : environ {round(deck_eur, -1 if deck_eur >= 100 else 0):.0f} {CURRENCY}"
              + (f" ; sans prix : {', '.join(unknown)}" if unknown else ""))
        if args.seuil is not None:
            seuil, secours = args.seuil, False
        else:
            seuil, secours = profile_threshold()
        expensive = [(e, n) for e, n in priced if e >= seuil]
        print(f"Cartes à {seuil:.0f} {CURRENCY} ou plus"
              + (" (seuil de secours : profil illisible)" if secours else "") + " : "
              + (", ".join(f"{n} (~{e:.0f} {CURRENCY})" for e, n in expensive) or "aucune"))
        if args.max_prix is not None:
            for e, n in priced:
                if e > args.max_prix:
                    errors.append(f"{n} : ~{e:.0f} {CURRENCY}, au-dessus du budget de {args.max_prix:.0f} {CURRENCY} par carte.")
        spare_prices = []
        for _, name, _ in spares:
            card = cards.get(name.lower())
            eur = card_price(card) if card else None
            spare_prices.append(f"{name} ({fmt_price(eur)})" if eur is not None else f"{name} (prix inconnu)")
        if spare_prices:
            print("Maybeboard : " + ", ".join(spare_prices))

    print(mana_report(entries, cards, identity))
    print(f"Total : {total} cartes")
    print(f"Identité couleur : {''.join(sorted(identity)) or 'incolore'}")
    print(f"Game Changers ({len(game_changers)}) : {', '.join(game_changers) or 'aucun'}")
    if errors:
        print(f"\n{len(errors)} erreur(s) :")
        for e in errors:
            print(f"- {e}")
        sys.exit(1)
    print("\nAucune erreur : le deck est légal et complet.")


if __name__ == "__main__":
    main()
