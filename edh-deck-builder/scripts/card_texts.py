"""Affiche le texte Oracle exact de toutes les cartes d'une liste, via Scryfall.

Usage : python card_texts.py deck.txt [--only "Carte 1" "Carte 2" ...] [--no-lands]

À lancer avant d'écrire la stratégie, les synergies ou les notes de jeu : on s'appuie
sur le texte réel des cartes, pas sur la mémoire.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_deck import fetch_cards, parse_deck  # noqa: E402


def describe(card):
    faces = card.get("card_faces") if "oracle_text" not in card else None
    parts = []
    for f in faces or [card]:
        line = f"{f.get('name', card['name'])} {f.get('mana_cost', '')}".strip()
        line += f" | {f.get('type_line', card.get('type_line', ''))}"
        if f.get("power") is not None:
            line += f" | {f['power']}/{f['toughness']}"
        if f.get("loyalty"):
            line += f" | loyauté {f['loyalty']}"
        text = (f.get("oracle_text") or "").replace("\n", " / ")
        parts.append(f"{line}\n  {text}")
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("--only", nargs="*", default=None, help="limiter à ces cartes")
    ap.add_argument("--no-lands", action="store_true", help="ignorer les terrains")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    entries, spares = parse_deck(a.deck)
    names = [n for _, n, _ in entries + spares]
    if a.only:
        wanted = {n.lower() for n in a.only}
        names = [n for n in names if n.lower() in wanted] + [n for n in a.only if n.lower() not in {x.lower() for x in names}]
    try:
        cards, missing = fetch_cards(names)
    except Exception as exc:
        print(f"Impossible de joindre Scryfall : {exc}")
        sys.exit(2)
    for name in dict.fromkeys(names):
        card = cards.get(name.lower())
        if not card:
            continue
        if a.no_lands and "Land" in card.get("type_line", "").split("//")[0]:
            continue
        print("- " + describe(card))
    if missing:
        print("\nIntrouvables (nom à vérifier) : " + ", ".join(missing))


if __name__ == "__main__":
    main()
