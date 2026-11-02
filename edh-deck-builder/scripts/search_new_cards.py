"""Cherche sur Scryfall les cartes récentes qui correspondent aux synergies d'un deck.

Usage :
  python search_new_cards.py --identity ubr --since 2025-10-01 --query 'o:"you don\\'t own"' [--bracket 2] [--max-prix 20] [--devise EUR|USD]

--query reçoit la syntaxe de recherche Scryfall (o:, t:, kw:…). Le script ajoute lui-même :
identité couleur, légalité Commander, papier, date de sortie, une seule impression par carte,
exclut les rééditions (seules les cartes nouvelles depuis la date sortent) et les Game Changers en bracket 1-2.
"""
import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_deck as vd  # noqa: E402  (devise du profil)

API = "https://api.scryfall.com/cards/search"
HEADERS = {"User-Agent": "edh-deck-builder/1.0", "Accept": "application/json"}


def search(q):
    url = API + "?" + urllib.parse.urlencode({"q": q, "order": "released", "dir": "desc", "unique": "cards"})
    cards = []
    while url:
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=30) as r:
                data = json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return []  # aucune carte trouvée
            raise
        cards += data.get("data", [])
        url = data.get("next_page") if len(cards) < 175 else None
        time.sleep(0.1)
    return cards


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--identity", required=True, help="identité couleur du commandant, ex. ubr")
    ap.add_argument("--since", required=True, help="date de sortie minimale AAAA-MM-JJ")
    ap.add_argument("--query", required=True, help="filtre Scryfall lié aux synergies")
    ap.add_argument("--bracket", type=int, default=3)
    ap.add_argument("--max-prix", type=float, default=None, help="prix maximal par carte, dans la devise retenue")
    ap.add_argument("--max-usd", type=float, default=None, help="ancien nom : prix maximal en USD (impose la devise USD)")
    ap.add_argument("--devise", choices=sorted(vd.DEVISES), default=None)
    a = ap.parse_args()
    if a.max_usd is not None:
        a.devise, a.max_prix = "USD", a.max_usd
    if a.devise:
        vd.set_currency(a.devise)

    q = f"({a.query}) id<={a.identity} legal:commander game:paper date>={a.since} not:reprint"
    if a.bracket <= 2:
        q += " -is:gamechanger"
    try:
        cards = search(q)
    except Exception as e:
        print(f"Recherche impossible ({e}). Vérifie l'accès à api.scryfall.com.")
        sys.exit(2)

    shown = 0
    for c in cards:
        key = vd.DEVISES[vd.CURRENCY][0]
        usd = c.get("prices", {}).get(key) or c.get("prices", {}).get(key + "_foil")
        if a.max_prix is not None and usd and float(usd) > a.max_prix:
            continue
        faces = c.get("card_faces") or [c]
        text = " // ".join(f.get("oracle_text", "") for f in faces).replace("\n", " ")
        cost = " // ".join(f.get("mana_cost", "") for f in faces if f.get("mana_cost"))
        gc = " [GAME CHANGER]" if c.get("game_changer") else ""
        print(f"- {c['name']} {cost} | {c.get('type_line','')} | {c.get('set_name','')} ({c.get('released_at','')}) | "
              f"{usd or '?'} {vd.CURRENCY}{gc}\n  {text}")
        shown += 1
    print(f"\n{shown} carte(s). Requête : {q}")


if __name__ == "__main__":
    main()
