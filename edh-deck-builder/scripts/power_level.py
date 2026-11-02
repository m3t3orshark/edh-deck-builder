"""Indicateurs de puissance d'un deck Commander, et note sur 10 pour cinq critères mesurables.

Usage : python power_level.py deck.txt

Le sixième critère (conditions de victoire) et la note finale relèvent du jugement :
voir reference/puissance.md. Les détections reposent sur le texte Oracle (heuristiques) :
la liste des cartes comptées dans chaque catégorie est affichée pour pouvoir la contester.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_deck import card_text, fetch_cards, parse_deck  # noqa: E402

BASIC_TYPES = ("plains", "island", "swamp", "mountain", "forest")


def interp(x, points):
    """Interpolation linéaire sur une liste de (valeur, note) triée par valeur."""
    if x <= points[0][0]:
        return points[0][1]
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return points[-1][1]


def is_land(card):
    return "Land" in card.get("type_line", "").split("//")[0]


def classify(card):
    """Rôles détectés pour une carte (une carte peut en avoir plusieurs)."""
    t = card_text(card).lower()
    roles = set()
    land = is_land(card)
    if land:
        if re.search(r"enters( the battlefield)? tapped", t):
            conditional = any(k in t for k in ("unless", "if you control", "if you don't", "you may pay"))
            roles.add("terrain_engage_conditionnel" if conditional else "terrain_engage")
        return roles
    if card.get("produced_mana") or "treasure token" in t or (
        "search your library for" in t and ("land" in t or any(b in t for b in BASIC_TYPES))
    ):
        roles.add("ramp")
        if card.get("produced_mana") and card.get("cmc", 9) <= 1:
            roles.add("mana_rapide")
    if re.search(r"\bdraws? (a|two|three|four|x|that many|cards?)", t) or "draw cards equal" in t or "draw a card" in t:
        multi = re.search(r"draws? (two|three|four|x|that many|cards)|draw cards equal", t)
        engine = re.search(r"(whenever|at the beginning of)[^.]*draw", t)
        roles.add("pioche" if (multi or engine) else "pioche_simple")
    if "pioche" not in roles and "pioche_simple" not in roles and re.search(
        r"(look at|reveal) the top .{0,200}?into your hand", t, re.S
    ):
        roles.add("pioche_simple")  # sélection de cartes du type Fact or Fiction ; le vol se juge à part
    if re.search(r"search your library for (a|an|up to \w+) (card|instant|sorcery|creature|artifact|enchantment|planeswalker)", t):
        roles.add("tuteur")
    if re.search(r"(destroy|exile) all|each creature|all creatures get -|damage to each creature|each opponent sacrifices (a|two) creature", t):
        roles.add("wipe")
    if re.search(r"(destroy|exile) (target|up to \w+ target|another target|each nonland permanent target)|counter target|"
                 r"deals? (\d+|x) damage to (any target|target creature|target planeswalker)|gain control of target|"
                 r"return target (nonland permanent|creature|permanent) to its owner's hand|target opponent sacrifices", t):
        roles.add("interaction")
    if re.search(r"from your graveyard (to|onto)|return (target|up to \w+ target|a|an) [^.]*card[^.]* from your graveyard|"
                 r"cast [^.]* from your graveyard", t):
        roles.add("recursion")
    if re.search(r"\b(hexproof|indestructible|shroud|phase out|protection from)\b", t):
        roles.add("protection")
    return roles


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        sys.exit("Usage : python power_level.py deck.txt")
    entries, _ = parse_deck(sys.argv[1])
    try:
        cards, missing = fetch_cards([n for _, n, _ in entries])
    except Exception as exc:
        print(f"Impossible de joindre Scryfall : {exc}")
        sys.exit(2)

    buckets = {k: [] for k in ["ramp", "mana_rapide", "pioche", "pioche_simple", "tuteur", "interaction", "wipe",
                                "recursion", "protection", "terrain_engage", "terrain_engage_conditionnel"]}
    mvs = []
    for qty, name, is_cmd in entries:
        c = cards.get(name.lower())
        if not c:
            continue
        for r in classify(c):
            buckets[r].append(name)
        if not is_land(c) and not is_cmd:
            mvs += [c.get("cmc", 0)] * qty

    n = {k: len(v) for k, v in buckets.items()}
    avg = sum(mvs) / len(mvs) if mvs else 0
    tapped = n["terrain_engage"] + 0.25 * n["terrain_engage_conditionnel"]

    s_mv = interp(avg, [(2.6, 10), (3.0, 7), (3.4, 5), (3.8, 3), (4.2, 1)])
    s_ramp = interp(n["ramp"], [(6, 1), (10, 4), (14, 7), (18, 10)])
    vitesse = min(10, 0.5 * s_mv + 0.5 * s_ramp + 0.5 * min(n["mana_rapide"], 3))
    pioche = n["pioche"] + 0.5 * n["pioche_simple"]
    regularite = min(10, interp(pioche, [(5, 1), (9, 4), (13, 7), (18, 10)]) + min(n["tuteur"], 3))
    interaction = max(1, interp(n["interaction"], [(4, 1), (8, 4), (12, 7), (16, 10)]) - (1 if n["wipe"] == 0 else 0))
    resilience = interp(n["recursion"] + n["protection"], [(0, 1), (3, 3), (6, 6), (10, 10)])
    base = interp(tapped, [(0, 10), (4, 8), (8, 6), (12, 4), (16, 2)])

    scores = [("Vitesse", vitesse, f"valeur de mana moyenne {avg:.2f}, {n['ramp']} ramp dont {n['mana_rapide']} mana rapide"),
              ("Régularité", regularite, f"{n['pioche']} moteurs ou pioches multiples, {n['pioche_simple']} pioches simples (comptées pour moitié), {n['tuteur']} tuteurs"),
              ("Interaction", interaction, f"{n['interaction']} removal ou contresorts, {n['wipe']} board wipes"),
              ("Résilience", resilience, f"{n['recursion']} cartes de récursion, {n['protection']} de protection"),
              ("Base de mana", base, f"{n['terrain_engage']} terrains engagés, {n['terrain_engage_conditionnel']} engagés sous condition")]
    print("Indicateurs de puissance (heuristiques, à contester si besoin) :")
    for label, sc, detail in scores:
        print(f"- {label} : {sc:.1f}/10 ({detail})")
    moyenne = sum(s for _, s, _ in scores) / len(scores)
    print(f"Moyenne des cinq critères mesurés : {moyenne:.1f}/10")
    print("Critère 6, conditions de victoire : à évaluer (voir reference/puissance.md).")
    print("\nDétail des cartes comptées :")
    for k in ["ramp", "mana_rapide", "pioche", "pioche_simple", "tuteur", "interaction", "wipe", "recursion", "protection",
              "terrain_engage", "terrain_engage_conditionnel"]:
        if buckets[k]:
            print(f"- {k} ({len(buckets[k])}) : {', '.join(buckets[k])}")
    if missing:
        print("\nIntrouvables : " + ", ".join(missing))


if __name__ == "__main__":
    main()
