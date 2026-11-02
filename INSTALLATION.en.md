# Install the EDH skill in Claude

*[Version française](INSTALLATION.md)*

Allow about ten minutes, once. You need a Claude account, on a computer (claude.ai in the browser, or the Claude app for Mac or Windows). Settings and installation are done on a computer.

A skill is a set of instructions and tools that Claude uses on its own when your request calls for it. This one handles Magic Commander decks: it builds and reviews them, checks the cards on Scryfall and prepares lists to import into deckstats, ManaBox, Moxfield or Archidekt.

## Step 1: set up Claude

The skill needs to run small programs and query a few websites. In Claude, open **Settings**, then **Capabilities**:

1. Turn on **code execution and file creation**.
2. Turn on **network access** (outbound connections).
3. In the list of allowed domains, add one by one:
    - `api.scryfall.com`: cards, ban list, prices;
    - `backend.commanderspellbook.com`: combo detection;
    - `github.com`, `raw.githubusercontent.com` and `release-assets.githubusercontent.com`: skill updates.

A newly added domain can take a few messages to work: if in doubt, open a new conversation.

## Step 2: download the skill

1. Open the releases page: [github.com/m3t3orshark/edh-deck-builder/releases](https://github.com/m3t3orshark/edh-deck-builder/releases).
2. Under the version marked **Latest** (the most recent, at the top), scroll down to the **Assets** section.
3. Click **edh-deck-builder.skill**: the file goes to your Downloads.

Don't download the other files in the list (`.sha256`, *Source code*): they are used for updates, not for installation. No GitHub account needed.

## Step 3: install it in Claude

1. In Claude, open **Customize**, then **Skills**.
2. Click **+** (or **Add**) and choose to import a skill.
3. Select the `edh-deck-builder.skill` file from your Downloads.
4. Check that the **edh-deck-builder** skill appears in the list and is turned on.

## Step 4: your first message and your settings

1. Open a **new conversation** and simply write what you want, for example: "Build me a Commander deck with [your favorite commander]".
2. Claude introduces itself in three sentences, then shows a **settings panel**. Fill it in:
    - your **first name** and your **language** (the form of address only applies in French);
    - your **play principles**: check "never infinite combos" or "never locks" if your table dislikes them; otherwise only the bracket rules apply;
    - your default **bracket**, **power** and **budget** (you can leave them empty: Claude will ask);
    - if you have a ManaBox collection, the **binders** to count;
    - your **currency** (euro with Cardmarket prices, or dollar) and the price above which a card is flagged.
3. Click **Save**. Claude prepares your configured skill and shows an **"Update edh-deck-builder"** card: click it.
4. Open a **new conversation**: your settings are in place.

No time? Say "I'd rather start right away": Claude works with neutral settings, and you set your profile later with "set my EDH profile".

## Day to day

Say **"help EDH"** at any time: Claude shows the list of what you can ask, with an example for each. You can also phrase your request freely. A few examples:

- "Build me a deck with Atraxa, bracket 2"
- "Review this deck" (pasting your list or attaching the file)
- "Only with my cards" (attaching your ManaBox export)
- "Does [card] trigger with [card]?"
- "Write the play notes"

The delivered list pastes as is into deckstats ("Paste your decklist" import), ManaBox, Moxfield or Archidekt.

## Update

Say **"update EDH"**. Claude checks for a new version and, if there is one, summarizes what's new and shows an **"Update edh-deck-builder"** card: click it, then open a new conversation. Your settings are kept. "Is there an EDH update?" only checks.

Never install by hand a `.skill` file received from someone: it would replace your settings with theirs. Instead, attach it to a conversation and say "update my skill with this file".

## Troubleshooting

| What you see | What to do |
| --- | --- |
| Claude says Scryfall, Commander Spellbook or GitHub cannot be reached | Check the domains from step 1, then open a new conversation |
| Claude answers without using the skill | Check that edh-deck-builder is turned on (step 3) and name your request: "help EDH", "Commander deck" |
| You lost your settings | Say "set my EDH profile" and set them again; to back them up, "export my EDH profile" gives you one line to keep |
| Anything else | Report the problem in the repository's [Issues](https://github.com/m3t3orshark/edh-deck-builder/issues) tab, with a screenshot |
