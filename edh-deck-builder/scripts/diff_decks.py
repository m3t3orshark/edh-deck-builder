"""Compare une liste d'origine et sa version révisée : cartes sorties, entrées, nombre d'échanges
et coût approximatif des cartes ajoutées (devise du profil : EUR Cardmarket ou USD TCGplayer, via Scryfall ;
--devise pour une autre).

Usage : python diff_decks.py origine.txt revision.txt [--expected N] [--mana-base [--categories ...]] [--lands-only]

--expected N  : vérifie qu'il y a exactement N échanges (contrainte de l'utilisateur).
--mana-base   : vérifie que seules des cartes de base de mana sortent et entrent. La base de mana est
                celle du profil (base_de_mana de PROFIL.md), parmi : terrains, rocks, dorks, tresors,
                ramp, tuteurs_de_terrain. Profil illisible : les six catégories.
--categories  : remplace la définition du profil pour cette comparaison (avec --mana-base).
--lands-only  : terrains seulement (équivaut à --mana-base --categories terrains).

Les six catégories réunies acceptent exactement les mêmes cartes que l'ancienne version du script
(terrain, carte qui produit du mana, qui va chercher un terrain ou qui crée un Trésor) ; « ramp »
reçoit ce qui produit du mana sans être un terrain, un rock ni un dork (rituels, auras…), et aussi
les recherches de terrain qui le mettent sur le champ de bataille.
"""
import argparse
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_deck as vd  # noqa: E402
from verify_deck import card_price, fetch_cards, fmt_price, load_profile, parse_deck  # noqa: E402

CATEGORIES = ("terrains", "rocks", "dorks", "tresors", "ramp", "tuteurs_de_terrain")
LABELS = {"terrains": "terrain", "rocks": "rock", "dorks": "créature à mana", "tresors": "créateur de Trésors",
          "ramp": "ramp", "tuteurs_de_terrain": "tuteur de terrain"}


def mana_categories(card):
    """Catégories de base de mana d'une carte (ensemble vide si elle n'en fait pas partie)."""
    cats = set()
    front = card.get("type_line", "").split("//")[0]
    if "Land" in front:
        cats.add("terrains")
    if card.get("produced_mana") and "Land" not in front:
        if "Creature" in front:
            cats.add("dorks")
        elif "Artifact" in front:
            cats.add("rocks")
        else:
            cats.add("ramp")
    text = card.get("oracle_text", "") + " ".join(f.get("oracle_text", "") for f in card.get("card_faces", []))
    low = text.lower()
    basic_types = ("plains", "island", "swamp", "mountain", "forest")
    if "search your library for" in low and ("land" in low or any(t in low for t in basic_types)):
        cats.add("tuteurs_de_terrain")
        if "onto the battlefield" in low:
            cats.add("ramp")
    if "treasure token" in low:
        cats.add("tresors")
    return cats


def is_mana_card(card, allowed=CATEGORIES):
    """Vrai si la carte appartient à au moins une des catégories retenues."""
    return bool(mana_categories(card) & set(allowed))


def profile_mana_base():
    """Catégories de base_de_mana du profil, et vrai si c'est la valeur de secours (les six)."""
    p = load_profile() or {}
    mb = p.get("base_de_mana")
    if isinstance(mb, list) and mb and set(mb) <= set(CATEGORIES):
        return [c for c in CATEGORIES if c in mb], False
    return list(CATEGORIES), True


def counts(path):
    entries, _ = parse_deck(path)
    c = Counter()
    for qty, name, _ in entries:
        c[name] += qty
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("origine")
    ap.add_argument("revision")
    ap.add_argument("--expected", type=int, default=None)
    ap.add_argument("--lands-only", action="store_true")
    ap.add_argument("--mana-base", action="store_true")
    ap.add_argument("--categories", nargs="+", choices=CATEGORIES, default=None)
    ap.add_argument("--devise", choices=sorted(vd.DEVISES), default=None)
    a = ap.parse_args()
    if a.devise:
        vd.set_currency(a.devise)
    sys.stdout.reconfigure(encoding="utf-8")

    old, new = counts(a.origine), counts(a.revision)
    out = old - new
    inc = new - old
    n_out, n_in = sum(out.values()), sum(inc.values())
    cards, _ = fetch_cards(list(out) + list(inc))

    def eur(name):
        card = cards.get(name.lower())
        return card_price(card) if card else None

    errors = []
    print(f"Sorties ({n_out}) :")
    for name, q in sorted(out.items()):
        print(f"- {q} {name}")
    total = 0.0
    print(f"Entrées ({n_in}) :")
    for name, q in sorted(inc.items()):
        e = eur(name)
        total += (e or 0) * q
        print(f"- {q} {name} ({fmt_price(e) if e is not None else 'prix inconnu'})")
    print(f"Coût approximatif des cartes ajoutées : environ {round(total):.0f} {vd.CURRENCY}")

    if n_out != n_in:
        errors.append(f"{n_out} sorties pour {n_in} entrées : chaque échange doit être une carte pour une carte.")
    if a.expected is not None and n_in != a.expected:
        errors.append(f"{n_in} échanges au lieu des {a.expected} demandés.")
    if a.lands_only:
        for name in list(out) + list(inc):
            card = cards.get(name.lower())
            if card and "Land" not in card.get("type_line", "").split("//")[0]:
                errors.append(f"{name} n'est pas un terrain, alors que seule la base de mana doit changer.")
    if a.mana_base:
        if a.categories:
            allowed, secours = [c for c in CATEGORIES if c in a.categories], False
        else:
            allowed, secours = profile_mana_base()
        print("Base de mana retenue : " + ", ".join(allowed)
              + (" (profil illisible : les six catégories)" if secours else ""))
        for name in list(out) + list(inc):
            card = cards.get(name.lower())
            if card and not is_mana_card(card, allowed):
                errors.append(f"{name} ne fait pas partie de la base de mana ("
                              + ", ".join(LABELS[c] for c in allowed)
                              + "), alors que seule la base de mana doit changer.")
    if errors:
        print("\nErreur(s) :")
        for e in errors:
            print(f"- {e}")
        sys.exit(1)
    print("\nÉchanges conformes à la contrainte.")


if __name__ == "__main__":
    main()
