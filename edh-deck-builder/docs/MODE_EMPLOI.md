# Mode d'emploi

*[English version](MODE_EMPLOI.en.md)* · *Validée le 31 octobre 2026, revue le 1er novembre 2026, mise à jour avec chaque version du skill.* Ce guide permet de démarrer seul, sans connaître l'historique du skill.

## 1. Installer le skill

1. Dans Claude, ouvre **Paramètres → Capacités** et active **l'exécution de code** (« Exécuter du code dans le cloud »). Les skills en ont besoin.
2. Toujours dans Capacités, active **l'accès réseau sortant**, puis ajoute ces domaines dans **Domaines supplémentaires autorisés** :
   - `api.scryfall.com` (cartes, légalité, prix) ;
   - `backend.commanderspellbook.com` (détection des combos) ;
   - `github.com`, `raw.githubusercontent.com` et `release-assets.githubusercontent.com` (mises à jour depuis le dépôt officiel ; ajoute aussi `objects.githubusercontent.com` si une mise à jour échoue au téléchargement).
3. Télécharge le fichier `edh-deck-builder.skill` de la dernière version sur la page **Releases** du dépôt (https://github.com/m3t3orshark/edh-deck-builder/releases), section *Assets*. Va dans **Personnaliser → Skills**, clique sur **+** (ou **Ajouter**), choisis d'importer un skill et sélectionne ce fichier (c'est une archive zip ; renomme-le en `.zip` si l'import le refuse). Si quelqu'un te l'envoie dans une conversation Claude, le bouton d'enregistrement sur le fichier fait la même chose.
4. Vérifie que le skill est activé. Si un autre skill du même nom existe (par exemple celui d'un plugin), désactive-le pour éviter les conflits.

Un domaine ajouté peut mettre quelques messages à fonctionner. Si Claude indique que Scryfall est injoignable, ouvre une nouvelle conversation.

**Passer à une nouvelle version sans perdre tes réglages** : n'installe pas directement le fichier reçu, car installer un fichier `.skill` remplace tout le skill, profil compris. Joins-le plutôt à une conversation et écris « mets à jour mon skill avec ce fichier ». Claude reporte ton profil dans la nouvelle version, te dit quels réglages sont gardés et lesquels sont nouveaux, et te présente un seul fichier à installer. Une version que Claude a reconstruite pour toi (après « règle mon profil EDH ») contient déjà ton profil : celle-là s'installe directement. Après une installation, ouvre une nouvelle conversation.

**Le plus simple** : dis « fais la mise à jour EDH ». Claude vérifie sur le dépôt officiel s'il existe une nouvelle version ; s'il y en a une, il te résume les nouveautés, la télécharge, vérifie qu'elle n'a pas été altérée, y reporte ton profil, et te présente la carte à installer d'un clic. « Y a-t-il une mise à jour EDH ? » vérifie seulement. Il faut avoir autorisé les domaines de GitHub (ci-dessus).

**Sauvegarde de secours** : « exporte mon profil EDH » te donne une ligne à conserver. La recoller dans une conversation recrée ton profil sur n'importe quelle version.

## 1 bis. Ce que tu peux demander

À tout moment, dis **« aide EDH »** : Claude affiche la liste des demandes possibles, avec un exemple pour chacune. Ce sont des exemples à reprendre ou à adapter, une demande formulée librement fonctionne aussi :

| Pour… | Exemple à dire |
|---|---|
| Construire un deck | « Monte-moi un deck avec [commandant], bracket 2 » |
| Trouver un commandant | « Quels commandants pour un thème [stun, vol, artefacts…] ? » |
| Trouver des cartes | « Quelles cartes vont avec [commandant] ? » |
| Analyser ou améliorer un deck | « Analyse ce deck » (avec la liste) ; « Pourquoi mon deck perd ? » |
| Améliorer un precon | « Améliore seulement la base de mana, 10 échanges maximum » |
| Utiliser ma collection | « Seulement avec mes cartes » (avec l'export de ta collection : ManaBox, Archidekt ou Moxfield) ; « Fais le bilan de ma collection pour ce deck » |
| Jouer | « Prépare les notes de jeu » ; « Est-ce que [carte] se déclenche avec [carte] ? » |
| Mes réglages | « Règle mon profil EDH » ; « Exporte mon profil EDH » |
| Entretien | « Y a-t-il une mise à jour EDH ? » ; « Fais la mise à jour EDH » ; « Mets à jour mon skill avec ce fichier » ; « Prépare une copie vierge à partager » |
| Cette liste | « Aide EDH » |

## 2. Première utilisation

Le skill que tu reçois peut être **vierge** (personne ne l'a encore réglé) ou **déjà réglé** (par exemple ta propre copie, ou une copie préparée pour toi).

**Avec un skill vierge**, ton premier message, quel qu'il soit (« monte-moi un deck avec Atraxa », « bonjour »), déclenche l'accueil :

1. **Claude se présente en trois phrases courtes**, dans la langue de ton premier message : ce que fait le skill, et que ses réglages se font une fois pour toutes, en une minute.
2. **Le panneau de réglages s'affiche**, prérempli avec des valeurs neutres. Tu y indiques :
   - ton **prénom**, ta **langue** (français ou anglais, préremplie avec celle de ton premier message) et, en français, le **ton** (tutoiement ou vouvoiement) ;
   - tes **principes de jeu** : la synergie avant la puissance est cochée par défaut ; « jamais de combo infinie » et « jamais de verrou » sont décochés, ce qui veut dire que seules les règles officielles du bracket s'appliquent : coche-les pour les bannir quel que soit le bracket ;
   - ton **bracket** et ta **puissance par défaut**, utilisés quand tu ne précises rien : la puissance se choisit par tranche, *détendu* (1-3), *équilibré* (4-7) ou *affûté* (8-10) (laisse « aucun » pour qu'on te demande le bracket à chaque fois ; sans puissance par défaut, elle est seulement estimée) ;
   - ton **budget par défaut**, si tu en as un : c'est un plafond par deck, pas une somme à dépenser ;
   - les **pistes inhabituelles** : ne pas en proposer, en proposer sans les imposer, ou les mettre en avant ;
   - tes **classeurs ManaBox** : joins ton export de collection à ce premier message pour qu'ils apparaissent dans le panneau, et coche ceux qui contiennent tes cartes ;
   - ce que comprend **la base de mana** quand tu demandes de ne toucher qu'à elle (les terrains seulement par défaut ; tu peux y ajouter rocks, dorks, Trésors, ramp et tuteurs de terrain), ta **devise** (euro avec les prix Cardmarket, ou dollar avec les prix TCGplayer) et le **seuil de prix** à partir duquel une carte est signalée.
3. **Tu cliques sur « Enregistrer »** : Claude prépare ta version du skill et te présente le fichier.
4. **Tu cliques sur le bouton d'enregistrement du fichier** : ton skill est réglé. Ouvre ensuite une nouvelle conversation pour qu'il soit pris en compte.

Tu es pressé ? Dis-le, et Claude commence tout de suite avec les valeurs neutres (règles officielles du bracket pour les combos et les verrous, pas de budget, base de mana réduite aux terrains, bracket demandé à chaque deck) ; il te proposera de régler ton profil plus tard. Et tu pourras toujours tout changer avec « règle mon profil EDH ».

**Avec un skill déjà réglé**, il n'y a pas d'accueil : Claude utilise directement le profil. Vérifie quand même une fois tes réglages avec « règle mon profil EDH ».

**Pour partager le skill** avec quelqu'un, demande « prépare une copie vierge à partager » : Claude produit une version sans tes réglages ni ton prénom, et la personne aura l'accueil ci-dessus. Ne lui envoie pas ta propre copie : elle contient ton profil. Et n'installe pas la copie vierge sur ton propre compte : elle remplacerait ton profil.

## 3. Créer un deck

Décris ce que tu veux, en une phrase ou plus. Claude ne pose que les questions dont il n'a pas la réponse : commandant, bracket, thème, budget, contraintes.

Exemples :

> Monte-moi un deck avec Nathan Drake, Treasure Hunter. Bracket 2, thème vol, pas de budget.

> Quelles stratégies avec Atraxa, Grand Unifier ? Propose-moi les meilleures avant de construire.

**Deux commandants** (Partner, Background…) : donne les deux noms. Claude vérifie d'abord que la paire est autorisée ; sinon, il explique pourquoi et propose des alternatives valides.

Tu reçois une **stratégie en bref**, la **répartition par rôle** (terrains, ramp, pioche…), la **liste** et une ligne de **contrôle** (légalité, combos, prix). Demande des changements autant que tu veux. Quand la liste te convient, dis-le : Claude prépare alors les notes de jeu.

## 4. Analyser ou améliorer un deck

Colle la liste de ton deck ou joins-la en fichier (l'export deckstats ou ManaBox convient) et dis ce que tu cherches. Tu peux combiner plusieurs objectifs. Si un nom de carte n'est pas reconnu (suffixe d'édition, faute de frappe), Claude le corrige d'après Scryfall et te dit chaque correction.

> Passe en revue ce deck, il est en bracket 2 et doit le rester.

> Pourquoi ce deck perd-il contre les decks aggro ?

> Réduis le coût de ce deck sans trop l'affaiblir.

> Quelles nouveautés de la dernière année iraient dans ce deck ?

Claude propose tous les échanges qui améliorent nettement ton deck dans sa configuration (« Sort : X → Entre : Y »), sans nombre fixe, classés en paliers : **essentiels**, **recommandés**, puis **optionnels**. Puis la liste mise à jour. Si tu veux un nombre précis (« 10 échanges au plus »), dis-le. Les cartes proposées ne sont pas choisies pour leur popularité : une carte peu jouée qui sert mieux la mécanique du deck peut entrer, et elle est signalée comme telle. Si une piste inhabituelle s'offre au deck, Claude la mentionne en fin de réponse, sans l'imposer.

**Les combos** : Claude cherche les combos présentes dans le deck. Si une doit sortir, il dit pourquoi : ton bracket l'interdit, ou ton profil les bannit quel que soit le bracket (il précise alors que le bracket seul l'aurait permise). Si rien ne l'interdit, elle reste, et il la signale. Il en va de même pour les verrous ; le contrôle lourd que les adversaires peuvent casser est permis mais toujours signalé, avec ce qui permet d'en sortir.

**Un deck hors des sentiers battus est respecté** : si ton deck joue une mécanique inhabituelle pour son commandant (Atraxa et les marqueurs stun, par exemple), Claude la renforce au lieu de la ramener vers la version classique. S'il n'est pas sûr de ton intention, il te pose d'abord une ou deux questions courtes sur l'effet recherché. Tu peux refuser un échange : il refait la liste sans lui.

**Améliorer un precon selon une règle** : précise que c'est un precon et ta règle (nombre d'échanges, base de mana seule, budget) : elle passe avant tout le reste. Claude ne traite une liste comme un precon que si tu le dis, ou après t'avoir demandé confirmation.

> Voici mon precon. Améliore uniquement la base de mana, en 10 cartes maximum. Il doit rester en bracket 2.

Ce que comprend « la base de mana » dépend de ton profil : **les terrains seulement** par défaut, ou aussi les rocks, créatures à mana, créateurs de Trésors, sorts de ramp et tuteurs de terrain si tu les as cochés dans tes réglages. La réponse rappelle la définition appliquée. Dis « terrains seulement » pour être plus strict le temps d'une demande.

## 5. Explorer les synergies d'un commandant

Pour voir **toutes** les cartes qui servent les mécaniques d'un commandant, pas seulement les plus jouées :

> Donne-moi toutes les cartes synergiques avec Atraxa, Praetors' Voice, classées par synergie. Inclue des pistes inhabituelles, par exemple les marqueurs stun.

Tu reçois un fichier avec la liste complète, axe par axe, et pour chaque carte son texte, son prix et sa popularité (« peu jouée », « jamais classée »). Dans la réponse, Claude met en avant les pépites peu jouées, signale les faux amis et les risques de combo ou de verrou. Tu peux ensuite lui demander de construire un deck à partir d'un axe, ou de croiser la liste avec ta collection.

## 6. Trouver un commandant pour un thème

Tu as une idée de mécanique mais pas de commandant ? Propose le thème :

> Quels commandants pour un deck de marqueurs stun ?

> Je veux voler les sorts de mes adversaires, en bleu-noir de préférence. Quels commandants ?

Tu reçois 10 commandants au plus, des plus solides aux plus originaux, chacun avec ses couleurs, la façon dont il joue le thème et sa popularité, plus la liste complète dans un fichier. Claude privilégie les commandants qui relancent l'effet chaque tour, pas ceux qui ne le font qu'une fois en arrivant. Il liste aussi les commandants **écartés, avec la raison** : tu peux quand même en choisir un s'il te plaît, et Claude t'expliquera comment compenser ses faiblesses. Si rien ne te parle, demande simplement **d'autres choix** (« d'autres commandants », « plus original », « en vert ») : tu reçois une nouvelle série, sans répétition.

## 7. Les notes de jeu

Après validation d'une liste, Claude livre des notes en Markdown, dans un bloc à copier. Dans deckstats, ouvre la fenêtre **Deck Notes**, colle le bloc et enregistre. Les noms de cartes entre `[[ ]]` deviennent des liens survolables.

Pour un deck déjà construit : « Voici ma liste validée, fais-moi les notes de jeu. »

## 8. Importer la liste (deckstats, ManaBox, Moxfield, Archidekt)

**Utilise uniquement « Paste your decklist »** dans deckstats, pas l'autre fenêtre d'ajout de deck : elle ne reconnaît pas le format et donne 103 cartes sans commandant.

La liste livrée a cette forme, à coller telle quelle :

```
1 Sol Ring
...
5 Island

Sideboard
1 Maze of Ith

Commander
1 Nathan Drake, Treasure Hunter
```

- Le **commandant vient en dernier** : c'est voulu, sinon tout le deck passe en commandant.
- Les cartes sous **Sideboard** sont les suggestions du maybeboard : après l'import, déplace-les vers le maybeboard dans deckstats.
- deckstats trie lui-même les cartes par type.

**Dans ManaBox**, le même bloc fonctionne : depuis l'écran des decks, bouton flottant en bas, import texte, puis colle la liste. Le commandant est reconnu, et les cartes sous `Sideboard` arrivent dans la réserve, d'où tu peux les déplacer. ManaBox sait aussi importer un deck depuis son lien deckstats.

**Dans Moxfield**, le même bloc fonctionne aussi : crée un deck au format Commander et colle la liste dans l'import de texte. Le ou les commandants et le sideboard sont reconnus. Moxfield choisit lui-même l'impression de chaque carte : il peut afficher une version à nom alternatif (par exemple Tymna the Weaver sous le nom « Cecil Harvey », impression Final Fantasy). C'est la même carte ; change l'impression dans Moxfield si tu préfères un autre visuel.

**Dans Archidekt**, même chose : crée un deck Commander et colle la liste dans l'import de texte. Commandant, partenaires et sideboard sont reconnus. Archidekt range lui-même les cartes dans ses catégories de rôle ; réorganise-les à ta guise.

## 9. Utiliser ta collection (ManaBox, Archidekt, Moxfield)

Joins à la conversation l'export CSV de ta collection. Claude reconnaît le format tout seul :

- **ManaBox** : onglet **Collection**, menu en haut à droite, **Exporter**, format **CSV**. Tes classeurs et tes listes d'envies sont reconnus.
- **Archidekt** : **Collection**, **Export**, format CSV (garde les champs cochés par défaut). Pour marquer un proxy, donne-lui une étiquette (« Collection labels ») nommée par exemple `Proxy`.
- **Moxfield** : **Collection**, export CSV. Pour marquer un proxy, active **« Playtest Card »** sur la carte.

Archidekt et Moxfield n'exportent pas de classeurs : toute la collection compte. Si tu as migré ta collection d'un outil à l'autre, vérifie-la : un import perd les classeurs, transforme une liste d'envies en cartes possédées, et peut perdre des quantités (Moxfield refuse d'ailleurs le CSV de ManaBox, mais accepte celui d'Archidekt). Claude indique la date du dernier ajout de l'export, pour que tu saches de quand date la collection comparée.

**Construire avec ta collection** : trois options, à préciser dans ta demande (sinon Claude te les propose).

1. **Uniquement mes cartes** : le deck est construit avec ta collection seule (terrains de base en plus). Si un rôle manque de cartes, Claude le dit.
2. **En priorité mes cartes** : ta collection d'abord, puis les meilleures cartes manquantes, avec leur prix.
3. **Le meilleur deck, puis le bilan** : le deck idéal, puis le bilan de ce que tu as déjà et de ce qu'il faut acheter.

**Comparer n'importe quelle liste à ta collection** : Claude ne le fait pas d'office, pour garder des réponses courtes. Demande-le quand tu en as besoin, avec l'export joint : « qu'est-ce que j'ai déjà dans cette liste ? », « compare ce deck avec ma collection », « qu'est-ce qu'il me manque ? ». Ça marche pour un deck que Claude vient de créer, de réviser ou d'améliorer, comme pour une liste que tu colles.

Le bilan donne :

- les cartes **déjà possédées** : tu en as au moins un exemplaire, peu importe l'édition, la langue, ou si la carte est déjà dans un autre deck (tu peux la jouer en proxy) ;
- les cartes **qui te manquent**, avec leur prix approximatif, en précisant celles que tu joues déjà en proxy (par exemple pour tester un deck avant d'acheter) : pour celles-là, l'achat est à décider.

Un proxy ne compte donc pas comme une carte possédée. Si ton groupe de jeu fonctionne autrement, coche « Compter les proxies comme possédés » dans tes réglages.

Les **listes** ManaBox (comme une liste d'envies) sont ignorées : ce ne sont pas des cartes possédées. Si ton export contient plusieurs classeurs, Claude demande lesquels compter, sauf préférence déjà enregistrée dans ton skill.

## 10. Tes réglages

Dis « règle mon profil EDH » : Claude affiche un panneau avec tes réglages (langue, ton, principes de jeu, bracket et puissance par défaut, budget, pistes inhabituelles, classeurs ManaBox, proxies comptés ou non, ce que comprend la base de mana, devise et seuil de prix). Modifie, clique sur « Enregistrer » : Claude reconstruit le skill avec ton nouveau profil et te présente le fichier ; clique sur son bouton d'enregistrement pour mettre ton skill à jour. Tu peux aussi le demander par écrit (« passe ma puissance par défaut à 6 »). Si tu enregistres sans rien avoir changé, Claude te le dit et ne reconstruit rien : ton skill installé est déjà à jour.

**La langue** : Claude répond dans la langue de ton profil. Si tu écris tes propres phrases dans l'autre langue, il te répond dans celle-ci ; un nom de carte, une liste ou un texte de carte cité en anglais ne compte pas. Tu peux aussi le demander (« réponds en anglais »).

Tes valeurs par défaut s'appliquent quand tu ne précises rien, et Claude l'annonce en une ligne (« bracket 2 : ton réglage par défaut »). Ce que tu précises dans ta demande passe toujours avant.

**Pour une autre personne** : chacun a sa propre copie du skill. Le plus simple est une copie vierge (voir « Première utilisation »).

## 11. Le niveau de puissance

En plus du bracket, chaque deck reçoit une **puissance estimée sur 10**, fondée sur six critères : vitesse, régularité, interaction, résilience, base de mana et conditions de victoire. Le bracket dit ce que le deck a le droit de contenir ; la puissance dit sa force dans sa catégorie (un precon non modifié tourne autour de 4). Tu peux demander « quel est le niveau de puissance de ce deck ? », viser une tranche (« bracket 2, équilibré » ; tranches : détendu 1-3, équilibré 4-7, affûté 8-10), ou voir la puissance avant et après une révision.

## 12. Bon à savoir

- **Les prix** sont des ordres de grandeur, pas des prix exacts : ils servent à estimer le total d'un deck pour tenir un budget. Ils sont dans la devise de ton profil : euros (prix Cardmarket) ou dollars (prix TCGplayer), tous deux fournis par Scryfall. Pour le prix précis d'une carte ou d'une édition, consulte Cardmarket ou TCGplayer. Les cartes au-dessus du seuil de ton profil (30 par défaut) sont signalées, sans être remplacées sauf si tu le demandes. Un budget donné dans l'autre devise n'est pas converti : Claude te demande dans quelle devise travailler.
- **Un lien deckstats ne suffit pas** : colle l'export de la liste (Export, puis « Copy for Deckstats »).
- **Les combos** : le skill cherche toutes les combos présentes et celles à une carte près ; il retire ou garde les premières selon ton bracket et ton profil (voir section 4), et liste dans les notes les cartes qui en compléteraient une.
- **Les questions de règles** (« Est-ce que Hylda se déclenche avec Stop Cold ? ») : Claude lit d'abord le texte officiel des cartes nommées, et ses rulings si besoin, puis répond en le citant.
- **En cas de souci**, dis-le simplement à Claude (« la liste fait 103 cartes à l'import », « le commandant n'est pas reconnu ») : il saura corriger.
