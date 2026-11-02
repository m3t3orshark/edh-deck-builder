# Mode création

L'utilisateur part d'un commandant, sans liste. Étapes 1 à 6 ; l'étape 6 (notes de jeu) est dans `modes/notes.md`.

## Étape 1 : le questionnaire

Si l'utilisateur n'a pas déjà tout donné, pose ces questions **en un seul message court**, numérotées, pour qu'il puisse répondre en vrac. Ne repose pas une question dont la réponse est déjà dans sa demande.

1. **Commandant** : nom de la carte (et partenaire ou *background* s'il y en a un). **Avec deux commandants, vérifie la paire avant tout** : écris un petit fichier avec la ligne `Commander` suivie des deux noms et lance `python scripts/verify_deck.py <fichier> --no-prices` ; il signale une paire non autorisée (ignore les autres erreurs, dues au fichier incomplet). Une paire refusée ne se construit pas : **réponds en texte, sans outil de boutons de choix** : explique pourquoi (la capacité qui manque), puis propose les alternatives valides sous forme de liste numérotée, et demande laquelle construire (le premier commandant seul avec le second dans les 99 si les couleurs le permettent, ou un vrai partenaire qui couvre les mêmes couleurs). Avec une paire valide, la stratégie exploite les deux commandants, ou dit clairement lequel porte le thème et à quoi sert l'autre.
2. **Bracket visé** (1 à 5), seulement si le profil n'a pas de `bracket_defaut` ; sinon applique-le et annonce-le en une ligne. La **puissance visée** ne se demande pas : c'est une tranche (détendu, équilibré, affûté) qui vient de la demande ou du profil (`puissance_defaut`) ; sans cible, tu donnes seulement la puissance estimée et sa tranche (`reference/puissance.md`).
   - 1 Exhibition : thème avant tout, très faible puissance.
   - 2 Core : niveau d'un precon, aucun Game Changer.
   - 3 Upgraded : deck amélioré, 3 Game Changers maximum.
   - 4 Optimized : très puissant, Game Changers sans limite.
   - 5 cEDH : compétitif (rarement compatible avec les principes du profil ; le signaler si choisi).
3. **Thème ou stratégie** : déjà choisi, ou « à proposer ».
4. **Budget** : celui du profil (`budget_defaut`), sinon aucun. Seulement s'il en fixe un autre (par carte ou total). Un budget est un **plafond, pas un objectif** : ne choisis jamais une carte plus chère pour s'en approcher.
5. **Contraintes particulières** (facultatif) : cartes à inclure absolument, cartes à éviter.
6. **Sa collection** (facultatif) : s'il joint un export ManaBox, ou en parle, demande laquelle des trois options il veut, sauf si sa demande le dit déjà (voir `modes/collection.md`) ; les classeurs à compter viennent du profil. Sans export ni demande, pas de contrôle de collection.

Les règles exactes des brackets (Game Changers, destruction massive de terrains, extra-tours) évoluent aussi : vérifie-les en même temps que la ban list.

## Étape 2 : analyse du commandant et choix du thème

Lis attentivement le texte du commandant : récupère son texte Oracle exact avec `python scripts/card_texts.py <fichier> --only "<commandant>"` (le fichier peut ne contenir que la ligne du commandant), ou sur Scryfall par le web si le script ne tourne pas. Identifie ce qu'il récompense : type de sort, de permanent, d'événement (attaque, mort, entrée en jeu, pioche, sacrifice…), ses couleurs et ce qu'elles permettent.

**Si le thème est connu** : vérifie qu'il colle au commandant. S'il y a un décalage important, dis-le en une phrase et propose un ajustement, puis continue.

**Si le thème est « à proposer »** : présente **2 à 4 stratégies** possibles, chacune en 2 ou 3 lignes :
- le plan de jeu en une phrase ;
- le moteur de synergie principal ;
- comment le deck gagne (sans combo infinie si le profil ou le bracket l'interdit) ;
- le niveau de puissance réaliste et les points faibles.

**Pistes inhabituelles** (selon `pistes_inhabituelles` du profil) : avec `proposer`, propose parmi ces stratégies au moins une piste inhabituelle, que le texte du commandant permet mais que peu de joueurs exploitent ; avec `mettre_en_avant`, plusieurs ; avec `ne_pas_proposer`, aucune. Par exemple, Atraxa, Praetors' Voice prolifère tous les marqueurs : au lieu du poison ou des +1/+1, des marqueurs stun sur les permanents adverses. Signale honnêtement leur niveau de puissance, et le risque de glisser vers un verrou si la piste contrôle les adversaires (principe `pas_de_verrou`). Une piste inhabituelle ne s'impose jamais.

Puis attends son choix avant de construire. Ne construis pas plusieurs decks d'avance : c'est long et il n'en gardera qu'un.

## Étape 3 : construction

Pars de cette structure, puis ajuste selon la courbe de mana, le commandant et le bracket. Ce sont des repères, pas des quotas : une carte de ramp qui sert aussi le thème compte double.

| Catégorie | Repère |
| --- | --- |
| Terrains | 35 à 38 (moins si la courbe est basse et la ramp abondante) |
| Ramp | 9 à 12 |
| Pioche / avantage de cartes | 9 à 12 |
| Removal ciblé | 7 à 10 |
| Board wipes | 2 à 4 (selon que le thème les supporte) |
| Thème et synergie | le reste, environ 25 à 30 |

Repères par bracket :
- **Brackets 1-2** : pas de Game Changers, interaction modérée, tuteurs rares.
- **Bracket 3** : 3 Game Changers au maximum, choisis pour servir le thème.
- **Bracket 4** : courbe plus basse, interaction efficace et bon marché, ramp rapide. Toujours dans le respect des principes du profil (combos, verrous).

Pour la base de mana : terrains de base en proportion des symboles de mana, puis terrains utilitaires et doubles terrains adaptés au nombre de couleurs. Sans contrainte budgétaire, tu peux proposer les meilleurs doubles terrains (fetchs, shocks, etc.).

## Étape 4 : vérification

Suis `reference/verification.md` : scripts de vérification, combos, texte des cartes, puis puissance (`reference/puissance.md`). Corrige tout avant de livrer.

## Étape 5 : proposition de la liste

Cette réponse sert à faire **valider** la liste : elle doit aider l'utilisateur à juger si le deck lui convient, sans le noyer. Le guide de jeu détaillé vient après la validation (`modes/notes.md`).

Structure de la réponse :

1. **La stratégie en bref** : **6 lignes au plus**, c'est une limite, pas une indication. Le plan de jeu, comment le deck gagne, et les 2 ou 3 synergies qui portent le deck, en une phrase chacune. N'énumère pas les cartes par catégorie (la liste et la répartition par rôle sont là pour ça) : cite au plus 4 ou 5 cartes clés au total. Relis-toi et coupe si tu dépasses. **Avant d'envoyer, compte les noms de cartes de ce paragraphe** : au-delà de 5, remplace les énumérations par la catégorie qu'elles illustrent (« les voleurs qui se déclenchent en attaquant », « le vol de permanents ») ; les noms précis sont dans la liste. Juste assez pour que l'utilisateur voie la logique du deck et puisse dire « oui » ou « change ça ».
2. **La répartition par rôle** : une ou deux lignes qui donnent le nombre de cartes par rôle (terrains, ramp, pioche, removal, board wipes, protection, thème, axe secondaire, finishers). Comme deckstats trie lui-même par type, c'est ici, et pas dans la liste, que l'utilisateur voit l'équilibre du deck. Chaque carte compte dans un seul rôle, son rôle principal.
3. **La liste au format deckstats**, dans un seul bloc de code, prête à copier-coller dans l'import de deckstats (format : `reference/format_import.md`).
4. **Le contrôle** : une ou deux lignes qui disent précisément quels contrôles ont été faits et comment (script, ou vérification manuelle) : total de 100 cartes, singleton, ban list, Game Changers, identité couleur, combos (présentes et à une carte près), puis l'ordre de prix du deck et les cartes au-dessus du seuil du profil, à titre indicatif, et la **puissance estimée sur 10** (voir `reference/puissance.md`), avec l'écart à la puissance visée s'il y en a une. Ce qui n'a pas pu être vérifié est nommé explicitement. N'écris jamais « légalité vérifiée » de façon globale si un des contrôles a manqué.
5. **Le maybeboard expliqué** (seulement s'il existe) : une ligne par carte, qui dit quelle carte du deck elle remplacerait et pourquoi. Les cartes elles-mêmes sont dans la section `Sideboard` du bloc (voir `reference/format_import.md`).
6. **Le rappel d'import** : une phrase qui rappelle d'utiliser uniquement l'import « Paste your decklist » de deckstats (pas l'autre fenêtre d'ajout) ; le même bloc s'importe aussi tel quel dans ManaBox (import texte d'un deck) et dans Moxfield ou Archidekt (import de texte), commandant reconnu, puis, s'il y a un maybeboard, de déplacer les cartes du sideboard vers le maybeboard. Termine en une phrase : une fois la liste validée, tu prépares les notes de jeu à coller dans deckstats (`modes/notes.md`).
