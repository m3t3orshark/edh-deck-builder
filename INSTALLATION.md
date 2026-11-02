# Installer le skill EDH dans Claude

*[English version](INSTALLATION.en.md)*

Compte une dizaine de minutes, une seule fois. Il te faut un compte Claude, sur ordinateur (claude.ai dans le navigateur, ou l'application Claude pour Mac ou Windows). Les réglages et l'installation se font sur ordinateur.

Un skill, c'est un ensemble d'instructions et d'outils que Claude utilise tout seul quand ta demande le concerne. Celui-ci s'occupe des decks Magic Commander : il les construit, les analyse, vérifie les cartes sur Scryfall et prépare des listes à importer dans deckstats, ManaBox, Moxfield ou Archidekt.

## Étape 1 : préparer Claude

Le skill a besoin d'exécuter de petits programmes et d'interroger quelques sites. Dans Claude, ouvre **Paramètres**, puis **Capacités** :

1. Active **l'exécution de code et la création de fichiers**.
2. Active **l'accès réseau** (sorties vers Internet).
3. Dans la liste des domaines autorisés, ajoute un par un :
    - `api.scryfall.com` : les cartes, la ban list, les prix ;
    - `backend.commanderspellbook.com` : la détection des combos ;
    - `github.com`, `raw.githubusercontent.com` et `release-assets.githubusercontent.com` : les mises à jour du skill.

Un domaine ajouté peut mettre quelques messages à fonctionner : en cas de doute, ouvre une nouvelle conversation.

## Étape 2 : télécharger le skill

1. Ouvre la page des versions : [github.com/m3t3orshark/edh-deck-builder/releases](https://github.com/m3t3orshark/edh-deck-builder/releases).
2. Sous la version marquée **Latest** (la plus récente, en haut), descends jusqu'à la section **Assets**.
3. Clique sur **edh-deck-builder.skill** : le fichier arrive dans tes Téléchargements.

Ne télécharge pas les autres fichiers de la liste (`.sha256`, *Source code*) : ils servent aux mises à jour, pas à l'installation. Pas besoin de compte GitHub.

## Étape 3 : l'installer dans Claude

1. Dans Claude, ouvre **Personnaliser**, puis **Skills**.
2. Clique sur **+** (ou **Ajouter**) et choisis d'importer un skill.
3. Sélectionne le fichier `edh-deck-builder.skill` de tes Téléchargements.
4. Vérifie que le skill **edh-deck-builder** apparaît dans la liste et qu'il est activé.

## Étape 4 : le premier message et tes réglages

1. Ouvre une **nouvelle conversation** et écris simplement ce que tu veux, par exemple : « Monte-moi un deck Commander avec [ton commandant préféré] ».
2. Claude se présente en trois phrases, puis affiche un **panneau de réglages**. Remplis-le :
    - ton **prénom**, ta **langue** et le **ton** (tutoiement ou vouvoiement) ;
    - tes **principes de jeu** : coche « jamais de combo infinie » ou « jamais de verrou » si ta table ne les aime pas ; sinon, seules les règles du bracket s'appliquent ;
    - ton **bracket**, ta **puissance** et ton **budget** par défaut (tu peux laisser vide : Claude demandera) ;
    - si tu as une collection ManaBox, les **classeurs** à compter ;
    - ta **devise** (euro avec les prix Cardmarket, ou dollar) et le prix à partir duquel une carte est signalée.
3. Clique sur **Enregistrer**. Claude prépare ton skill réglé et affiche une carte **« Mettre à jour edh-deck-builder »** : clique dessus.
4. Ouvre une **nouvelle conversation** : tes réglages sont en place.

Pas le temps ? Dis « je préfère commencer tout de suite » : Claude travaille avec des réglages neutres, et tu règles ton profil plus tard avec « règle mon profil EDH ».

## Au quotidien

Dis **« aide EDH »** à tout moment : Claude affiche la liste de ce que tu peux demander, avec un exemple pour chaque cas. Tu peux aussi formuler ta demande librement. Quelques exemples :

- « Monte-moi un deck avec Atraxa, bracket 2 »
- « Analyse ce deck » (en collant ta liste ou en joignant le fichier)
- « Seulement avec mes cartes » (en joignant l'export de ta collection : ManaBox, Archidekt ou Moxfield)
- « Est-ce que [carte] se déclenche avec [carte] ? »
- « Prépare les notes de jeu »

La liste livrée se colle telle quelle dans deckstats (import « Paste your decklist »), ManaBox, Moxfield ou Archidekt.

## Mettre à jour

Dis **« fais la mise à jour EDH »**. Claude vérifie s'il existe une nouvelle version et, s'il y en a une, te résume les nouveautés et affiche une carte **« Mettre à jour edh-deck-builder »** : clique dessus, puis ouvre une nouvelle conversation. Tes réglages sont gardés. « Y a-t-il une mise à jour EDH ? » vérifie seulement.

N'installe jamais à la main un fichier `.skill` reçu de quelqu'un : il remplacerait tes réglages par les siens. Joins-le plutôt à une conversation et dis « mets à jour mon skill avec ce fichier ».

## En cas de souci

| Ce que tu vois | Ce qu'il faut faire |
| --- | --- |
| Claude dit que Scryfall, Commander Spellbook ou GitHub est injoignable | Vérifie les domaines de l'étape 1, puis ouvre une nouvelle conversation |
| Claude répond sans utiliser le skill | Vérifie qu'edh-deck-builder est activé (étape 3) et nomme ta demande : « aide EDH », « deck Commander » |
| Tu as perdu tes réglages | Dis « règle mon profil EDH » et refais-les ; pour les sauvegarder, « exporte mon profil EDH » donne une ligne à garder |
| Autre chose | Signale le problème dans l'onglet [Issues](https://github.com/m3t3orshark/edh-deck-builder/issues) du dépôt, avec une capture d'écran |
