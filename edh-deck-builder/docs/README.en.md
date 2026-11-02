# edh-deck-builder

*[Version française](README.md)*

A skill for Claude that builds, reviews and improves Magic: The Gathering decks for the **EDH / Commander** format, for paper players who want solid, consistent decks without spending hours on them, ready to import into deckstats.net, ManaBox, Moxfield or Archidekt.

## The idea

Building a Commander deck takes hours: finding 99 cards that serve a commander, balancing ramp, card draw and interaction, checking the ban list and the bracket rules, then typing everything into a tool. This skill does that work while asking few questions, and delivers:

- a **100-card list** ready to paste into deckstats, ManaBox, Moxfield or Archidekt;
- a **short explanation** of the strategy, so you can decide with full knowledge;
- once the list is approved, **play notes** to paste into the Deck Notes window of deckstats.

It can also **review an existing deck**: improve it, move it to another bracket, lower its cost, upgrade a precon under a rule ("10 cards", "mana base only"…) or bring in cards from the latest sets.

## The principles

Each user has a **profile**: their preferences, set once in a panel the first time they use the skill. Without settings, the skill starts from neutral defaults. The play principles:

- **The official bracket rules, by default**: infinite combos and locks are only banned where the bracket bans them. The profile can ban them whatever the bracket, for games that are played to the end; when a combo is removed for that reason, the skill says the bracket alone would have allowed it. In every case, a combo, a lock or heavy control present in the deck is pointed out.
- **Synergy before raw power** (on by default, can be turned off): one main theme, at most one secondary axis.
- **The bracket is respected**: Game Changers counted, bracket rules checked.
- **Paper cards only**, **up-to-date ban list**, **strict color identity**, **exactly 100 cards**.

And one principle of method: **nothing is stated from memory when it can be checked**. Legality, Game Changers, card text, combos, the mana base and prices go through scripts that query Scryfall and Commander Spellbook. The list format was tested by real imports in each tool.

## What you need

- Claude with skills, **code execution** turned on and **network access** to `api.scryfall.com`, `backend.commanderspellbook.com` and, for updates, the GitHub domains (see the user guide, section 1).
- For your collection: the **ManaBox** app and its CSV export. For lists: a **deckstats.net**, **Moxfield** or **Archidekt** account, or the ManaBox app (optional: the list is readable as is).

## What the skill can do

| Need | What the skill does |
|---|---|
| Build a deck | Short questionnaire, commander analysis, build, checks, importable list |
| Review a deck | Diagnosis (roles, mana base, combos, bracket, power, cost), swaps ranked in tiers |
| Upgrade a precon | Following your rule: number of swaps, mana base only, budget |
| Lower the cost | Replacements in the same role, savings in figures |
| New cards | Search for recent cards that serve the deck's synergies |
| Explore synergies | Every card that serves a commander, by axis, with no popularity filter, including little-played gems |
| Find a commander | From a theme or a mechanic, 10 commanders explained (and the rejected ones, with the reason), more on request |
| Power level | A score out of 10 on top of the bracket, based on six named criteria |
| Help | "Help EDH" shows the list of possible requests, with an example for each |
| Settings | A visual panel for your preferences, saved in one click; update to a new version without losing your profile; profile export in one line |
| Play notes | Game plan, opening hand, synergies, rules pitfalls, combos to avoid |
| ManaBox collection | Only my cards, my cards first, or best deck then a shopping list; on request, any list compared with your collection (owned, proxy only, to acquire) |

## What it does not do

- It does not read a deckstats link (the site blocks automated readers): paste the export instead.
- It does not connect to ManaBox (no public API): attach the CSV export instead.
- It does not track which deck your cards are in: a card you own once counts for all your decks, the other copy can be a proxy.
- It speaks **French** or **English**, chosen in the profile (and it answers in the language of your own sentences if you switch); card names stay in English. The documentation exists in French and English, except the developer documentation (French only). Prices are in **euros** (Cardmarket) or **dollars** (TCGplayer), chosen in the profile: those are the two currencies Scryfall provides, with no conversion to others. Lists import into deckstats, ManaBox, Moxfield and Archidekt; other tools will come once their import has been tested. For collections, only the ManaBox export is read.
- It does not replace your judgment: it suggests, you decide.

## Further reading

- **[User guide](MODE_EMPLOI.en.md)**: install the skill and use it day to day.
- **[Developer documentation](DOC_DEV.md)** (French): architecture, scripts, validated rules and tests.
