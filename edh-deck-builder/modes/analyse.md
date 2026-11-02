# Mode analyse d'un deck existant

L'utilisateur garde son deck : l'objectif est de l'améliorer par petites touches, pas de le remplacer. Les principes du profil s'appliquent comme en création.

## A. Les questions d'entrée

En un seul message court, numéroté, et seulement pour ce que sa demande ne dit pas déjà :

1. **L'objectif**, en laissant le choix ouvert : améliorer le deck à niveau égal, le faire monter ou descendre de bracket (lequel), comprendre pourquoi il perd (contre quoi, comment), **réduire son coût** (jusqu'à quel montant, ou quelles cartes viser), **améliorer un precon selon une règle** (voir plus bas), **repérer les nouveautés** des éditions récentes qui servent ses synergies (depuis quand : par défaut les 12 derniers mois, ou depuis une édition qu'il nomme), ou autre chose. Plusieurs objectifs peuvent se combiner.
2. **Le bracket visé**, et s'il doit rester le même (sinon, le `bracket_defaut` du profil, annoncé en une ligne), et éventuellement la **puissance visée** sur 10.
3. **Le budget** pour les cartes à ajouter (celui du profil, sinon aucun) : un plafond, jamais un objectif à atteindre.
4. **Les cartes intouchables** (facultatif) : celles qu'il veut garder quoi qu'il arrive.

S'il a déjà tout précisé (« bracket 2, doit le rester, passe-le en revue »), ne pose aucune question et passe au diagnostic. Une seule exception : l'intention d'un deck hors des sentiers battus (voir ci-dessous), qui peut justifier une question après la lecture des cartes.

**Un lien deckstats ne suffit pas** : deckstats protège ses pages contre les lecteurs automatiques (défi Cloudflare, erreur 403, testé sur un deck public), donc tu ne peux lire ni la liste ni les notes depuis un lien. Si l'utilisateur en donne un, n'essaie pas de contourner la protection : demande-lui de coller l'export de la liste (bouton Export, « Copy for Deckstats ») et, s'il en a, ses notes.

**La liste** peut arriver dans plusieurs formats : export deckstats (`//Commander`, `//Main`), format d'import (`Sideboard`, `Commander` en fin de liste), ou simple liste. Si le commandant n'est pas identifiable, demande-le.

## B. Le diagnostic

1. **Script de vérification** sur la liste telle quelle (voir `reference/verification.md`) : total, singleton, ban list, identité couleur, Game Changers au regard du bracket visé.
2. **Lecture des cartes** : lance `python scripts/card_texts.py <fichier> --no-lands` pour avoir le texte Oracle exact de toutes les cartes, puis identifie le thème réel du deck, tel qu'il est construit, à partir de ces textes.
   **Un thème inhabituel est un choix, pas une erreur.** Compare le thème réel à l'usage courant du commandant. S'il s'en écarte (par exemple un deck d'Atraxa, Praetors' Voice construit sur les marqueurs stun plutôt que sur le poison ou les +1/+1), considère que l'utilisateur sort volontairement des sentiers battus : les échanges doivent **renforcer ce thème**, jamais le ramener vers la version standard du commandant. Une carte qui paraît faible dans l'absolu peut être un pilier de ce thème ; ne la sors pas pour une carte « classique » du commandant.
   Si tu n'es pas sûr que l'écart soit voulu, ou de la synergie visée (par exemple, les marqueurs stun servent-ils à contrôler les menaces adverses, ou à protéger ses propres permanents ?), **pose une courte question avant de proposer les échanges** : l'intention du deck et l'effet recherché, en une ou deux questions au plus. Mieux vaut un échange de plus que des conseils qui défont le deck.
   **Les contraintes implicites se demandent, elles ne se devinent pas.** Si la liste suggère une contrainte que l'utilisateur n'a pas dite (toutes les cartes légales dans un format, aucune carte au-dessus d'un certain prix, aucune carte d'une édition, pas de Command Tower ni de Sol Ring…), elle vient peut-être de sa collection, de son budget ou d'un choix de format. **Ne l'applique pas d'office** : pose la question avant les échanges, en citant les explications possibles (par exemple : « deck construit avec ta collection ? format Standard voulu ? »). S'il n'est pas là pour répondre, propose les échanges sans la contrainte, et signale ceux qui la respecteraient.
3. **Répartition par rôle**, comparée aux repères de construction (`modes/creation.md`, étape 3) : où le deck manque (souvent ramp, pioche ou interaction) et où il déborde.
4. **Cohérence** : cartes qui ne servent ni le thème, ni l'axe secondaire, ni les fondamentaux ; thèmes trop nombreux.
5. **Combos et locks** : lance `find_combos.py` (voir `reference/verification.md`). Une combo infinie ou un verrou présent se signale toujours. Il se corrige (échange proposé) si le principe correspondant du profil est actif ou si le bracket l'interdit ; sinon, mentionne-le simplement, en précisant que le bracket l'autorise. **Dis toujours quelle règle impose le retrait** : le principe du profil, le bracket, ou les deux. Si c'est le principe seul, précise que le bracket l'autoriserait, pour que l'utilisateur sache qu'il peut lever le principe pour ce deck. Note aussi les combos à une carte près, pour ne pas en compléter une par inadvertance avec les cartes qui entrent.
6. **Courbe de mana et base de mana** : courbe trop haute, nombre de terrains, sources de chaque couleur (la section « Base de mana » du script donne ces chiffres). Ici, un avertissement ne se corrige pas en silence : il devient un point du diagnostic et, si besoin, un échange proposé (par exemple `Sort : Island → Entre : Swamp`). Relance le script sur la liste mise à jour pour vérifier que l'échange règle le problème.
7. **Bracket** : conformité au bracket visé (Game Changers, règles du bracket vérifiées comme dans `reference/verification.md`). Pour une baisse de bracket, identifie précisément ce qui fait dépasser.

## C. La réponse

1. **Le diagnostic en bref** (5 à 8 lignes) : le thème du deck, ses forces, ses 2 ou 3 faiblesses principales, et la conformité au bracket. Les problèmes de règles (carte illégale, hors couleur, combo infinie interdite par le profil ou le bracket, bracket dépassé) passent en premier.
2. **La répartition par rôle** actuelle, sur une ou deux lignes, avec les écarts aux repères.
3. **Les échanges proposés**, du plus important au moins important, une ligne chacun : `Sort : X → Entre : Y`, et pourquoi. **Pas de nombre fixe** : sans règle de l'utilisateur, améliore le deck au mieux dans sa configuration (bracket, thème, budget), avec tous les échanges qui l'améliorent **nettement**. Classe-les en paliers pour qu'il puisse juger : **essentiels** (ce qui corrige une faiblesse majeure), **recommandés**, puis **optionnels** (gains marginaux ou affaire de goût). Au-delà d'une quinzaine d'échanges, livre la liste mise à jour avec les deux premiers paliers et présente le palier optionnel à part, sans l'appliquer. Dis toujours s'il reste des pistes que tu n'as pas retenues. N'ajoute pas d'échange pour atteindre un nombre : si trois échanges suffisent, propose-en trois. Un échange garde l'équilibre (une carte sort, une carte entre) ; ajouter un terrain se fait aux dépens d'un sort, et inversement. Les cartes intouchables ne sortent jamais. Les cartes qui entrent respectent l'identité couleur, le bracket et le budget. **Ne choisis pas les cartes entrantes par popularité** : pour les rôles liés au thème, cherche les candidates avec `synergy_search.py` (voir `modes/exploration.md`) et retiens celle qui sert le mieux la mécanique du deck, même peu jouée ; signale-la alors comme « peu jouée », avec la raison de son choix. Si le diagnostic révèle une piste inhabituelle que le commandant permet et que le deck n'exploite pas, mentionne-la en une ligne à la fin, comme une idée à explorer : ne l'impose pas dans les échanges, sauf si l'utilisateur le demande.
4. **La liste mise à jour** avec tous les échanges appliqués, au format d'import (voir `reference/format_import.md`), vérifiée par le script. Contrôle aussi les échanges avec `python scripts/diff_decks.py <origine> <revision>` : il liste les cartes sorties et entrées, vérifie qu'il y en a autant de chaque côté et donne le coût approximatif des cartes ajoutées, à indiquer dans la réponse. L'utilisateur peut refuser un échange : refais alors la liste sans lui.
5. **Le contrôle** et **le rappel d'import**, comme en création (`modes/creation.md`, étape 5, points 4 et 6), avec la puissance **avant et après** les échanges. Un maybeboard est possible, pour les échanges écartés mais intéressants.

## Améliorer un precon selon une règle

Ne traite une liste comme un precon que si l'utilisateur le dit. Si elle ressemble à un precon non modifié sans qu'il l'ait précisé, demande-lui confirmation avant d'appliquer cette section. L'utilisateur part d'un deck Commander préconstruit et fixe une règle : un nombre exact d'échanges (« change 10 cartes », « 15 cartes »), un périmètre (« seulement la base de mana »), un budget total pour l'amélioration, ou une combinaison. **Sa règle** (nombre d'échanges, périmètre, budget) **passe avant tout le reste**.

1. **La liste d'origine** : demande-lui de la coller. S'il ne peut pas et nomme seulement le precon, cherche la liste officielle sur le web (annonce de Wizards of the Coast ou fiche de l'édition), fais-lui confirmer que c'est la bonne version, et vérifie-la avec le script (100 cartes).
2. **La règle, sans ambiguïté** : si elle est floue, pose une seule question avant de commencer. Par exemple, « 10 cartes » : exactement 10, ou 10 au maximum ? **« La base de mana » comprend ce que liste `base_de_mana` dans le profil** ; « terrains seulement » est le cas plus strict.
3. **Garde l'identité du precon** : son commandant et son thème restent, sauf demande contraire. Le but est de rendre le deck plus solide, pas d'en faire un autre.
4. **Juger un terrain par ce qu'il apporte, pas seulement par sa vitesse** : remplace en priorité les terrains lents *et* peu utiles (terrain engagé qui ne donne que deux couleurs dans un deck à plus de couleurs, terrain utilitaire sans rapport avec le deck). Un terrain qui arrive engagé reste un bon choix s'il compense : dans un deck à 4 ou 5 couleurs, un terrain qui produit n'importe quelle couleur vaut souvent mieux qu'un double terrain rapide. L'objectif est d'avoir chaque couleur en quantité suffisante pour jouer ses sorts à temps : appuie-toi sur la section « Base de mana » du script.
5. **L'ordre des priorités habituel pour un precon**, dans les limites de la règle : la base de mana (terrains qui arrivent engagés, sources mal réparties), puis l'interaction et la pioche qui manquent, puis les cartes hors thème ou trop faibles, remplacées par des cartes du thème. Le diagnostic (B) dit où le deck perd le plus.
6. **Le bracket** : un precon est en général en bracket 2. Ne le fais pas monter sans le dire : signale tout Game Changer ajouté et vérifie le bracket visé avec le script.
7. **Vérifie la règle avec le script de comparaison**, en donnant la contrainte :
   `python scripts/diff_decks.py <origine> <revision> --expected <N>` pour un nombre exact d'échanges, et `--mana-base` si seule la base de mana doit changer : le script applique la définition `base_de_mana` du profil, et `--lands-only` si l'utilisateur limite aux terrains. Une erreur signalée se corrige avant de livrer.
8. **La réponse** suit le point C, avec en plus : la règle rappelée en une ligne (pour « la base de mana », reprends telle quelle la définition affichée par `diff_decks.py`, « Base de mana retenue : … », sans la reformuler ni en omettre une catégorie), le nombre d'échanges effectués, et le coût approximatif total de l'amélioration donné par le script.

## Réduire le coût (si l'utilisateur le demande)

1. Pars de l'ordre de prix donné par le script : les cartes les plus chères sont les premières candidates, en commençant par celles qui dépassent le seuil du profil (`prix.seuil_mise_en_evidence`).
2. Pour chacune, cherche une remplaçante **dans le même rôle**, nettement moins chère, qui sert autant que possible le thème : un sort de protection par un autre, un double terrain par un double terrain moins cher, etc. Vérifie son prix avec le script plutôt que de mémoire.
3. Garde une carte chère si elle n'a pas d'équivalent proche et qu'elle porte le deck : dis-le plutôt que de proposer un échange qui affaiblit nettement le deck.
4. Présente les échanges comme au point C.3, avec le prix approximatif de chaque carte et l'économie totale estimée : `Sort : X (~65 €) → Entre : Y (~2 €)` (dans la devise du profil).

## Les nouveautés (si l'utilisateur le demande)

Les cartes récentes sont souvent postérieures à tes connaissances : ne t'appuie jamais sur ta mémoire pour elles, et ne cite que des cartes dont tu as lu le texte Oracle dans les résultats de recherche.

1. **Traduis les synergies du deck en recherches** : 3 à 6 requêtes en syntaxe Scryfall, tirées du texte du commandant et des moteurs du deck (par exemple `o:"don't own"` pour un deck de vol, `t:elf` pour une tribu, `o:"whenever" o:"attacks"` pour des déclencheurs d'attaque).
2. **Lance le script** pour chaque requête :
   `python scripts/search_new_cards.py --identity <identité> --since <AAAA-MM-JJ> --query '<requête>' --bracket <n> [--max-prix <budget>]` (prix dans la devise du profil).
   Il ne renvoie que des cartes **nouvelles** depuis la date (pas les rééditions), légales en Commander, en papier, dans l'identité couleur, et sans Game Changer en bracket 1-2. Sans accès à Scryfall, fais les mêmes recherches sur le web et dis que la liste peut être incomplète.
3. **Trie sévèrement** : écarte les cartes déjà dans le deck, celles qui ouvrent avec une carte du deck une combo infinie ou un verrou interdits par le profil ou le bracket (autorisés, signale-les), et celles qui ne battent pas la carte la plus faible de leur rôle. Une nouveauté n'entre que si elle améliore le deck, pas parce qu'elle est nouvelle.
4. **Présente-les** dans les échanges proposés (point C.3), marquées « nouveauté », avec l'édition et sa date de sortie : `Sort : X → Entre : Y (nouveauté, édition, date)`. Les nouveautés intéressantes mais pas assez fortes pour entrer vont au maybeboard, 5 au maximum.

## Avec la collection

Si l'utilisateur joint son export ManaBox en révision, demande laquelle des trois options de `modes/collection.md` il veut, sauf si sa demande le dit déjà. Avec les options 1 et 2, propose des échanges avec des cartes qu'il possède (option 1 : seulement celles-là), et indique pour chaque échange si la carte entrante est possédée, en proxy seulement ou à acquérir. Avec l'option 3, propose les meilleurs échanges, puis fais le bilan de la liste révisée.

## D. Les notes de jeu

Une fois les échanges validés, **réécris les notes de jeu de zéro**, comme dans `modes/notes.md`, sur la base de la dernière liste validée. Ne repars pas d'anciennes notes pour les corriger, même si l'utilisateur les colle : quelques échanges suffisent à changer le plan de jeu, les synergies ou les pièges, et des notes rapiécées gardent des références à des cartes sorties. Vérifie que chaque `[[Nom de carte]]` figure dans la liste finale.

Si l'utilisateur demande seulement des notes pour un deck existant, sans analyse, applique directement `modes/notes.md` sur sa liste.
