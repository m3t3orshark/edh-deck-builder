"""Cherche sur Commander Spellbook les combos présentes dans un deck et celles à une carte près.

Usage : python find_combos.py deck.txt [--max-almost 15]

Nécessite l'accès réseau à backend.commanderspellbook.com.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_deck import parse_deck  # noqa: E402

API = "https://backend.commanderspellbook.com/find-my-combos"
HEADERS = {"User-Agent": "edh-deck-builder/1.0", "Accept": "application/json"}


def post(body, content_type):
    req = urllib.request.Request(API, data=body, headers={**HEADERS, "Content-Type": content_type})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def query(entries):
    commanders = [{"card": n, "quantity": q} for q, n, c in entries if c]
    main = [{"card": n, "quantity": q} for q, n, c in entries if not c]
    try:
        return post(json.dumps({"commanders": commanders, "main": main}).encode(), "application/json")
    except urllib.error.HTTPError:
        # Repli : liste texte, au format attendu par le site.
        text = "// Commander\n" + "\n".join(f"{c['quantity']} {c['card']}" for c in commanders)
        text += "\n// Main\n" + "\n".join(f"{c['quantity']} {c['card']}" for c in main)
        return post(text.encode(), "text/plain")


def card_names(variant):
    return [u.get("card", {}).get("name", "?") for u in variant.get("uses", [])]


def results(variant):
    names = [p.get("feature", {}).get("name", "?") for p in variant.get("produces", [])]
    return ", ".join(names[:3]) or "?"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("--max-almost", type=int, default=15)
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    entries, _ = parse_deck(a.deck)
    deck = {n.lower() for _, n, _ in entries}
    try:
        data = query(entries)
    except Exception as exc:
        print(f"Commander Spellbook injoignable ({exc}). Vérifie l'accès à backend.commanderspellbook.com.")
        sys.exit(2)
    res = data.get("results", data)

    included = res.get("included", [])
    print(f"Combos présentes dans le deck : {len(included)}")
    for v in included:
        print(f"- {' + '.join(card_names(v))} → {results(v)} [{v.get('bracketTag', '?')}]")

    almost = res.get("almostIncluded", [])
    print(f"\nCombos à une carte près : {len(almost)}")
    for v in almost[: a.max_almost]:
        names = card_names(v)
        missing = [n for n in names if n.lower() not in deck and n.split(" // ")[0].lower() not in deck]
        present = [n for n in names if n not in missing]
        with_cards = f"avec {' + '.join(present)}" if present else "seule ou avec des cartes génériques du deck"
        print(f"- manque {', '.join(missing) or '?'} ({with_cards}) → {results(v)}")
    if len(almost) > a.max_almost:
        print(f"… et {len(almost) - a.max_almost} autres.")
    sys.exit(1 if included else 0)


if __name__ == "__main__":
    main()
