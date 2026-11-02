# edh-deck-builder

Un **skill pour Claude** qui construit, analyse et améliore des decks **Magic: The Gathering Commander (EDH)** de 100 cartes, en papier : listes vérifiées (légalité, bracket, combos, prix) et prêtes à importer dans deckstats.net, ManaBox, Moxfield ou Archidekt, puis notes de jeu.

## Installer

1. Dans Claude, **Paramètres → Capacités** : active l'exécution de code et l'accès réseau sortant, puis autorise ces domaines : `api.scryfall.com`, `backend.commanderspellbook.com`, `github.com`, `raw.githubusercontent.com`, `release-assets.githubusercontent.com` (et `objects.githubusercontent.com` si une mise à jour échoue au téléchargement).
2. Télécharge `edh-deck-builder.skill` dans la dernière version de la page **[Releases](https://github.com/m3t3orshark/edh-deck-builder/releases)** (section *Assets*).
3. **Personnaliser → Skills → +** : importe ce fichier.
4. Ouvre une nouvelle conversation et parle de ton deck : le skill t'accueille et te propose de régler tes préférences en une minute.

## Utiliser

Dis **« aide »** à tout moment pour voir ce que le skill sait faire. Le [mode d'emploi](edh-deck-builder/docs/MODE_EMPLOI.md) détaille tout.

## Mettre à jour

Dis **« fais la mise à jour de edh-deck-builder »** : Claude vérifie ici s'il existe une nouvelle version, te résume les nouveautés, vérifie le fichier, garde tes réglages et te présente la mise à jour à installer d'un clic. Les nouveautés de chaque version sont dans [CHANGELOG.md](CHANGELOG.md).

## Documentation

- [Présentation](edh-deck-builder/docs/README.md)
- [Mode d'emploi](edh-deck-builder/docs/MODE_EMPLOI.md)
- [Documentation de développement](edh-deck-builder/docs/DOC_DEV.md)

La documentation est en français ; une version anglaise est prévue. Le skill répond en français ou en anglais.

## Mentions

edh-deck-builder est un contenu de fan non officiel, autorisé dans le cadre de la politique sur le contenu de fans (Fan Content Policy) de Wizards of the Coast. Il n'est ni approuvé ni soutenu par Wizards. Certaines parties des contenus utilisés sont la propriété de Wizards of the Coast. ©Wizards of the Coast LLC. Le dépôt ne contient aucune image ni aucun texte de carte : les données viennent de Scryfall et de Commander Spellbook au moment de l'utilisation.

Tous droits réservés pour l'instant (pas de licence).
