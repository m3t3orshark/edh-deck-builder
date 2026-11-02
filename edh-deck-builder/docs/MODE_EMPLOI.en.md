# User guide

*[Version française](MODE_EMPLOI.md)* · *Updated with every version of the skill.* This guide lets you get started on your own, without knowing the skill's history.

## 1. Install the skill

1. In Claude, open **Settings → Capabilities** and turn on **code execution**. Skills need it.
2. Still in Capabilities, turn on **outbound network access**, then add these domains to the **additional allowed domains**:
   - `api.scryfall.com` (cards, legality, prices);
   - `backend.commanderspellbook.com` (combo detection);
   - `github.com`, `raw.githubusercontent.com` and `release-assets.githubusercontent.com` (updates from the official repository; also add `objects.githubusercontent.com` if an update fails to download).
3. Download the `edh-deck-builder.skill` file of the latest version from the repository's **Releases** page (https://github.com/m3t3orshark/edh-deck-builder/releases), *Assets* section. Go to **Customize → Skills**, click **+** (or **Add**), choose to import a skill and select that file (it is a zip archive; rename it to `.zip` if the import refuses it). If someone sends it to you in a Claude conversation, the save button on the file does the same.
4. Check that the skill is turned on. If another skill with the same name exists (from a plugin, for example), turn it off to avoid conflicts.

A newly added domain can take a few messages to work. If Claude says Scryfall cannot be reached, open a new conversation.

**Moving to a new version without losing your settings**: do not install a received file directly, because installing a `.skill` file replaces the whole skill, profile included. Instead, attach it to a conversation and write "update my skill with this file". Claude carries your profile over into the new version, tells you which settings are kept and which are new, and gives you a single file to install. A version Claude rebuilt for you (after "set my EDH profile") already contains your profile: that one installs directly. After any installation, open a new conversation.

**The simplest way**: say "update EDH". Claude checks the official repository for a new version; if there is one, it summarizes what's new, downloads it, checks that it has not been altered, carries your profile over, and gives you the card to install in one click. "Is there an EDH update?" only checks. The GitHub domains above must be allowed.

**Backup**: "export my EDH profile" gives you one line to keep. Pasting it into a conversation recreates your profile on any version.

## 1 bis. What you can ask

At any time, say **"help EDH"**: Claude shows the list of possible requests, with an example for each. These are examples to reuse or adapt; a request in your own words works too:

| To… | Example |
|---|---|
| Build a deck | "Build me a deck with [commander], bracket 2" |
| Find a commander | "Which commanders for a [stun, theft, artifacts…] theme?" |
| Find cards | "Which cards go with [commander]?" |
| Review or improve a deck | "Review this deck" (with the list); "Why does my deck lose?" |
| Upgrade a precon | "Improve only the mana base, 10 swaps at most" |
| Use my collection | "Only with my cards" (with the ManaBox export); "Check my collection for this deck" |
| Play | "Write the play notes"; "Does [card] trigger with [card]?" |
| My settings | "Set my EDH profile"; "Export my EDH profile" |
| Maintenance | "Is there an EDH update?"; "Update EDH"; "Update my skill with this file"; "Make a blank copy to share" |
| This list | "Help EDH" |

## 2. First use

The skill you receive can be **blank** (nobody has set it up yet) or **already set up** (your own copy, or a copy prepared for you).

**With a blank skill**, your first message, whatever it is ("build me a deck with Atraxa", "hello"), starts the welcome:

1. **Claude introduces itself in three short sentences**, in the language of your first message: what the skill does, and that its settings take one minute, once and for all.
2. **The settings panel appears**, filled in with neutral values. In it, you set:
   - your **first name**, your **language** (French or English, prefilled with the language of your first message) and, in French only, the **form of address** (tu or vous);
   - your **play principles**: synergy before power is checked by default; "never infinite combos" and "never locks" are unchecked, which means only the official bracket rules apply: check them to ban combos or locks whatever the bracket;
   - your default **bracket** and **power**, used when you don't specify: power is chosen by range, *casual* (1-3), *balanced* (4-7) or *sharp* (8-10) (leave "none" to be asked for the bracket every time; without a default power, it is only estimated);
   - your **default budget**, if you have one: it is a ceiling per deck, not an amount to spend;
   - **unusual ideas**: don't suggest them, suggest them without imposing, or highlight them;
   - your **ManaBox binders**: attach your collection export to this first message so they appear in the panel, and check the ones that hold your cards;
   - what **the mana base** includes when you ask to touch only that (lands only by default; you can add rocks, mana creatures, Treasures, ramp and land tutors), your **currency** (euro with Cardmarket prices, or dollar with TCGplayer prices) and the **price threshold** above which a card is flagged.
3. **Click "Save"**: Claude prepares your version of the skill and gives you the file.
4. **Click the save button on the file card**: your skill is set up. Then open a new conversation so it takes effect.

In a hurry? Say so, and Claude starts right away with the neutral values (official bracket rules for combos and locks, no budget, mana base limited to lands, bracket asked for each deck); it will offer to set your profile later. You can always change everything with "set my EDH profile".

**With a skill already set up**, there is no welcome: Claude uses the profile directly. Still check your settings once with "set my EDH profile".

**To share the skill** with someone, ask "make a blank copy to share": Claude produces a version without your settings or your name, and that person gets the welcome above. Don't send them your own copy: it contains your profile. And don't install the blank copy on your own account: it would replace your profile.

## 3. Build a deck

Describe what you want, in one sentence or more. Claude only asks the questions it has no answer to: commander, bracket, theme, budget, constraints.

Examples:

> Build me a deck with Nathan Drake, Treasure Hunter. Bracket 2, theft theme, no budget.

> Which strategies with Atraxa, Grand Unifier? Show me the best ones before building.

**Two commanders** (Partner, Background…): give both names. Claude first checks that the pair is allowed; if not, it explains why and suggests valid alternatives.

You receive a **strategy at a glance**, the **role breakdown** (lands, ramp, card draw…), the **list** and a **check** line (legality, combos, prices). Ask for changes as often as you like. When the list suits you, say so: Claude then writes the play notes.

## 4. Review or improve a deck

Paste your deck list or attach it as a file (a deckstats or ManaBox export works) and say what you're after. You can combine several goals. If a card name is not recognized (set suffix, typo), Claude corrects it from Scryfall and tells you each correction.

> Review this deck, it's bracket 2 and must stay there.

> Why does this deck lose against aggro decks?

> Lower the cost of this deck without weakening it too much.

> Which cards from the last year would fit this deck?

Claude suggests every swap that clearly improves your deck in its setup ("Out: X → In: Y"), with no fixed number, ranked in tiers: **essential**, **recommended**, then **optional**. Then the updated list. If you want a precise number ("10 swaps at most"), say so. Suggested cards are not picked for their popularity: a little-played card that serves the deck's mechanic better can come in, and it is flagged as such. If an unusual idea fits the deck, Claude mentions it at the end, without imposing it.

**Combos**: Claude looks for combos present in the deck. If one must go, it says why: your bracket bans it, or your profile bans combos whatever the bracket (it then says the bracket alone would have allowed it). If nothing bans it, it stays, and it is pointed out. The same goes for locks; heavy control that opponents can break is allowed but always pointed out, with the ways out.

**An off-the-beaten-path deck is respected**: if your deck plays a mechanic that is unusual for its commander (Atraxa and stun counters, for example), Claude strengthens it instead of steering it back to the classic version. If it is unsure of your intent, it first asks one or two short questions about the effect you want. You can refuse a swap: it redoes the list without it.

**Upgrading a precon under a rule**: say it's a precon and give your rule (number of swaps, mana base only, budget): it comes before everything else. Claude only treats a list as a precon if you say so, or after asking you to confirm.

> Here is my precon. Improve only the mana base, 10 cards at most. It must stay in bracket 2.

What "the mana base" includes depends on your profile: **lands only** by default, or also rocks, mana creatures, Treasure makers, ramp spells and land tutors if you checked them in your settings. The answer restates the definition applied. Say "lands only" to be stricter for one request.

## 5. Explore a commander's synergies

To see **every** card that serves a commander's mechanics, not only the most played:

> Give me every card with synergy with Atraxa, Praetors' Voice, ranked by synergy. Include unusual ideas, stun counters for example.

You receive a file with the full list, axis by axis, and for each card its text, price and popularity ("little played", "never ranked"). In the answer, Claude highlights the little-played gems and points out false friends and combo or lock risks. You can then ask it to build a deck from one axis, or to cross the list with your collection.

## 6. Find a commander for a theme

You have a mechanic in mind but no commander? Suggest the theme:

> Which commanders for a stun counter deck?

> I want to steal my opponents' spells, blue-black if possible. Which commanders?

You receive at most 10 commanders, from the strongest to the most original, each with its colors, how it plays the theme and its popularity, plus the full list in a file. Claude favors commanders that repeat the effect every turn, not those that only do it once when they enter. It also lists the commanders **set aside, with the reason**: you can still pick one if you like it, and Claude will explain how to make up for its weaknesses. If nothing appeals to you, just ask for **other choices** ("other commanders", "more original", "in green"): you get a new series, with no repeats.

## 7. Play notes

Once a list is approved, Claude delivers notes in Markdown, in a block to copy. In deckstats, open the **Deck Notes** window, paste the block and save. Card names between `[[ ]]` become hover links.

For a deck you already built: "Here is my approved list, write me the play notes."

## 8. Import the list (deckstats, ManaBox, Moxfield, Archidekt)

**Only use "Paste your decklist"** in deckstats, not the other add-deck window: it does not recognize the format and gives 103 cards with no commander.

The delivered list looks like this, to paste as is:

```
1 Sol Ring
...
5 Island

Sideboard
1 Maze of Ith

Commander
1 Nathan Drake, Treasure Hunter
```

- The **commander comes last**: that's on purpose, otherwise the whole deck becomes the commander.
- The cards under **Sideboard** are the maybeboard suggestions: after the import, move them to the maybeboard in deckstats.
- deckstats sorts the cards by type itself.

**In ManaBox**, the same block works: from the decks screen, the floating button at the bottom, text import, then paste the list. The commander is recognized, and the cards under `Sideboard` land in the sideboard, from where you can move them. ManaBox can also import a deck from its deckstats link.

**In Moxfield**, the same block works too: create a Commander deck and paste the list into the text import. The commander(s) and the sideboard are recognized. Moxfield picks the printing of each card itself: it may show a version with an alternate name (for example Tymna the Weaver as "Cecil Harvey", a Final Fantasy printing). It's the same card; change the printing in Moxfield if you prefer another look.

**In Archidekt**, likewise: create a Commander deck and paste the list into the text import. Commander, partners and sideboard are recognized. Archidekt sorts the cards into its own role categories; rearrange them as you like.

## 9. Use your ManaBox collection

In ManaBox: **Collection** tab, top-right menu, **Export**, **CSV** format. Attach the file to the conversation. Claude gives the date of the export's latest addition, so you know how recent the compared collection is.

**Building with your collection**: three options, to state in your request (otherwise Claude offers them).

1. **Only my cards**: the deck is built from your collection alone (plus basic lands). If a role lacks cards, Claude says so.
2. **My cards first**: your collection first, then the best missing cards, with their prices.
3. **The best deck, then the check**: the ideal deck, then what you already own and what you need to buy.

**Comparing any list with your collection**: Claude doesn't do it automatically, to keep answers short. Ask when you need it, with the export attached: "what do I already own in this list?", "compare this deck with my collection", "what am I missing?". It works for a deck Claude just built, reviewed or improved, and for a list you paste.

The check gives:

- the cards **already owned**: you have at least one copy, whatever the edition or language, or whether the card is already in another deck (you can play it as a proxy);
- the cards **you are missing**, with their approximate price, pointing out those you already play as proxies (for example to test a deck before buying): for those, buying is your call.

So a proxy does not count as an owned card. If your playgroup works differently, check "Count proxies as owned" in your settings.

ManaBox **lists** (such as a wishlist) are ignored: they are not owned cards. If your export contains several binders, Claude asks which ones to count, unless a preference is already saved in your skill.

## 10. Your settings

Say "set my EDH profile": Claude shows a panel with your settings (language, form of address, play principles, default bracket and power, budget, unusual ideas, ManaBox binders, proxies counted or not, what the mana base includes, currency and price threshold). Change them, click "Save": Claude rebuilds the skill with your new profile and gives you the file; click its save button to update your skill. You can also ask in writing ("set my default power to 6"). If you save without changing anything, Claude tells you and rebuilds nothing: your installed skill is already up to date.

**Language**: Claude answers in your profile's language. If you write your own sentences in the other language, it answers in that one; a card name, a list or card text quoted in English doesn't count. You can also ask ("answer in English").

Your defaults apply when you don't specify, and Claude says so in one line ("bracket 2: your default setting"). What you specify in your request always comes first.

**For someone else**: everyone has their own copy of the skill. The simplest is a blank copy (see "First use").

## 11. Power level

On top of the bracket, each deck gets an **estimated power out of 10**, based on six criteria: speed, consistency, interaction, resilience, mana base and win conditions. The bracket says what the deck is allowed to contain; power says how strong it is within its category (an unmodified precon sits around 4). You can ask "what is this deck's power level?", aim for a range ("bracket 2, balanced"; ranges: casual 1-3, balanced 4-7, sharp 8-10), or see the power before and after a review.

## 12. Good to know

- **Prices** are orders of magnitude, not exact prices: they help estimate a deck's total to stay within a budget. They are in your profile's currency: euros (Cardmarket prices) or dollars (TCGplayer prices), both provided by Scryfall. For the exact price of a card or edition, check Cardmarket or TCGplayer. Cards above your profile's threshold (30 by default) are flagged, but not replaced unless you ask. A budget given in the other currency is not converted: Claude asks which currency to work in.
- **A deckstats link is not enough**: paste the list export (Export, then "Copy for Deckstats").
- **Combos**: the skill looks for every combo present and every combo one card away; it removes or keeps the former according to your bracket and profile (see section 4), and lists in the notes the cards that would complete one.
- **Rules questions** ("Does Hylda trigger with Stop Cold?"): Claude first reads the official text of the named cards, and their rulings if needed, then answers quoting it.
- **If something goes wrong**, just tell Claude ("the list has 103 cards on import", "the commander isn't recognized"): it will fix it.
