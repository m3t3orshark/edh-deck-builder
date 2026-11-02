# Collection (ManaBox, Archidekt, Moxfield)

L'utilisateur peut joindre l'export CSV de sa collection. Trois formats sont reconnus automatiquement par le script, chacun validé par un export réel :

- **ManaBox** (onglet Collection, menu en haut à droite, Export, CSV) : classeurs, listes d'envies (ignorées) et proxies (colonne Proxy).
- **Archidekt** (Collection, Export, CSV ; garder les champs par défaut, Oracle ID en plus si possible) : ni classeurs ni listes dans l'export ; pas de champ proxy : une **étiquette** (« Collection labels ») dont le nom contient « proxy » marque un proxy.
- **Moxfield** (Collection, export CSV) : pas de classeurs dans l'export ; un proxy est une carte marquée **« Playtest Card »**. Pas d'identifiant Scryfall : le script retrouve chaque carte par son édition et son numéro (à défaut par son nom) ; une carte introuvable est signalée.

Il n'existe pas d'API : l'export est à joindre à chaque conversation. Lis-le toujours avec le script, jamais à la main. **Bon à savoir pour une migration** (constaté le 02/11) : Moxfield refuse le CSV de ManaBox mais accepte celui d'Archidekt ; un import fait perdre les classeurs et transforme les listes d'envies en cartes possédées, et l'import Archidekt → Moxfield a perdu les quantités et une carte. Si l'utilisateur vient de migrer, signale ces risques en une phrase.

## Ce que veut dire « posséder une carte »

Une carte est **possédée dès qu'il en existe au moins un exemplaire réel** dans les classeurs comptés, toutes éditions et langues confondues. **Qu'elle soit déjà dans un deck monté ne compte pas** : l'utilisateur peut la jouer en proxy dans ses autres decks. Le contrôle ne cherche donc pas où sont les cartes, il compare une liste à la collection telle qu'elle était à la date de l'export.

**Un proxy n'est pas un exemplaire possédé** (sauf si `collection.proxies_possedes` vaut `true` dans le profil : ajoute alors `--proxies-possedes`). Une carte présente dans la collection seulement en proxy est une carte **en test** : elle **manque** comme les autres cartes non possédées, et le bilan précise seulement qu'elle est déjà jouée en proxy (achat à décider).

## Le script

- `python scripts/collection.py <export.csv> summary` : nombre de cartes possédées, cartes en proxy seulement, classeurs, et **date du dernier ajout** (colonne `Added`), qui indique la fraîcheur de l'export.
- `python scripts/collection.py <export.csv> pool --identity <couleurs> --bracket <n> --out pool.txt` : les cartes possédées (proxies exclus), légales en Commander, dans l'identité couleur du commandant (sans Game Changer en bracket 1-2), triées par type et valeur de mana. Les terrains de base sont considérés comme toujours disponibles.
- `python scripts/collection.py <export.csv> check <deck.txt>` : les cartes du deck déjà possédées, puis **un seul total des cartes manquantes**, détaillé en deux parties (déjà jouées en proxy ; ni possédées ni en proxy), avec le coût approximatif de l'ensemble.
- Options : `--only-binders "Commun" "Prénom"` et `--exclude-binders "Nom"` (plusieurs noms à la suite), `--proxies-possedes`. **Classeurs à compter** : ceux de `collection.classeurs` dans le profil, sans poser la question (`--only-binders` avec ces noms). Le classeur au nom d'une autre personne ne lui appartient pas : si l'export contient des classeurs absents du profil, demande lesquels compter avant de commencer. Les listes ManaBox (listes d'envies) sont toujours ignorées.

Le nom Scryfall de chaque carte vient de l'identifiant d'impression de l'export (ou, pour Moxfield, de son édition et de son numéro) : peu importe la langue de ses cartes, la liste livrée reste en noms anglais. **Classeurs** : seulement avec ManaBox ; avec Archidekt et Moxfield, toutes les lignes comptent et le script le dit (les options de classeurs sont ignorées).

## Quand faire le contrôle

**Le contrôle (`check`) se fait sur demande**, pas d'office après chaque liste : un bilan de collection alourdirait toutes les réponses.

- **D'office**, seulement quand la collection est la source du deck : options 1 et 2 ci-dessous.
- **Sur demande claire** : « compare avec ma collection », « qu'est-ce que j'ai déjà ? », « qu'est-ce qu'il me manque ? », ou l'option 3. Il s'applique alors à n'importe quelle liste : créée, révisée, améliorée, ou collée telle quelle.
- **Un export joint sans consigne** n'est pas une demande de contrôle : demande laquelle des trois options l'utilisateur veut.
- **Pas de rappel** en fin de réponse (« je peux comparer à ta collection ») : le mode d'emploi présente la fonction.

Quand un contrôle a lieu, la ligne de contrôle donne la date de la collection (« collection au 31/07/2025, dernier ajout ») ; si l'export a plus de trois mois, signale-le en une phrase, des cartes récentes peuvent manquer.

## Les trois options

1. **Uniquement mes cartes** : construis le deck exclusivement à partir de `pool.txt` (plus les terrains de base). Lis le texte des candidates avec `card_texts.py --only` avant de choisir. Si la collection ne suffit pas pour un rôle (par exemple pas assez de removal), dis-le clairement plutôt que de mettre une carte faible sans prévenir, et propose de passer à l'option 2 pour ce rôle. Contrôle final : `check` doit indiquer 0 carte manquante (une carte en proxy seulement manque).
2. **En priorité mes cartes** : pars de `pool.txt` et ne complète avec des cartes hors collection que là où elles apportent nettement plus. Livre ensuite le résultat de `check`.
3. **Le meilleur deck, puis le bilan** : construis sans tenir compte de la collection, puis lance `check` et livre le bilan. La collection ne change rien au deck.

Le bilan indique combien de cartes du deck sont déjà possédées, puis **combien manquent au total**, en précisant lesquelles sont déjà jouées en proxy, avec le coût approximatif. **N'écris jamais « aucune carte à acquérir » ou « rien ne manque » s'il reste des cartes en proxy seulement** : l'utilisateur ne les possède pas.
