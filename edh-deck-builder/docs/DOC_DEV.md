# Documentation développeur

*Validée le 31 octobre 2026, revue le 1er novembre 2026, mise à jour avec chaque version du skill.* Pour qui veut comprendre, modifier ou tester le skill.

## 1. Architecture

```
edh-deck-builder/
├── SKILL.md                 aiguillage : profil, règles fixes, vocabulaire, quel module lire
├── PROFIL.md                préférences de la personne (seul fichier qui change d'une personne à l'autre)
├── A_FAIRE.md               chantiers en cours ; lu seulement quand on travaille sur le skill
├── VERSION                  numéro de version (date AAAA.MM.JJ, suffixe .2, .3… si plusieurs le même jour)
├── modes/                   un module par type de demande, chargé à la demande
│   ├── creation.md          questionnaire, analyse du commandant, construction, proposition
│   ├── analyse.md           révision d'une liste existante (precon, coût, nouveautés, hors des sentiers battus)
│   ├── notes.md             notes de jeu après validation
│   ├── exploration.md       toutes les cartes synergiques d'un commandant
│   ├── commandants.md       commandants pour un thème
│   ├── collection.md        export ManaBox et ses trois options
│   └── reglages.md          panneau de réglages et reconstruction du skill
├── reference/               références communes
│   ├── verification.md      contrôles avant livraison
│   ├── commandes.md         liste des commandes (réponse à « aide ») ; une ligne par mode, mise à jour avec chaque mode
│   ├── format_import.md     format de la liste (testé dans deckstats, ManaBox, Moxfield, Archidekt)
│   └── puissance.md         niveau de puissance sur 10
├── docs/                    cette documentation (jamais lue pendant la construction d'un deck)
└── scripts/
    ├── verify_deck.py       légalité, Game Changers, base de mana, ordre de prix
    ├── card_texts.py        texte Oracle exact des cartes
    ├── find_combos.py       combos présentes et à une carte près (Commander Spellbook)
    ├── power_level.py       indicateurs et notes de puissance sur cinq critères
    ├── search_new_cards.py  cartes nouvelles depuis une date, filtrées par synergie
    ├── synergy_search.py    toutes les cartes d'un axe de synergie, ou les commandants d'un thème
    ├── diff_decks.py        comparaison origine / révision, contrôle des contraintes
    ├── collection.py        lecture d'un export ManaBox
    ├── render_panel.py      panneau de réglages (HTML) à partir de PROFIL.md
    ├── save_profile.py      validation d'un profil, reconstruction du fichier .skill, export du profil
    ├── update_skill.py      mise à jour vers une nouvelle version en gardant le profil
    ├── check_update.py      « fais la mise à jour » depuis le dépôt officiel (releases GitHub)
    └── build_public.py      construction de la copie publique (dépôt et release)
```

Les tests de référence sont livrés à part (`edh-deck-builder-tests.zip` : dossier `evals/`, et `formats/` pour les listes des tests d'import réels : Moxfield, Archidekt), car l'empaquetage des skills les exclut.

**Principes de conception** :
- `SKILL.md` est court et aiguille ; chaque module ne se charge que s'il sert. Les instructions portent le jugement, les scripts portent les vérifications : toute donnée qui change dans le temps (ban list, Game Changers, nouvelles cartes, prix) passe par un script ou une recherche, jamais par la mémoire du modèle.
- Tout ce qui est personnel vit dans `PROFIL.md`. Les modules parlent des réglages du profil (`principes`, `bracket_defaut`…), jamais d'une personne. Pour une autre personne, on ne remplace que ce fichier.

## 2. Le profil et le panneau de réglages

`PROFIL.md` contient un bloc JSON (propriétaire, ton, principes, bracket et puissance par défaut, budget, pistes inhabituelles, base de mana, classeurs ManaBox, prix) et l'explication de chaque réglage.

Parcours « règle mon profil » : `render_panel.py` génère le panneau à partir du profil (et des classeurs d'un export ManaBox avec `--export`) ; Claude l'affiche avec l'outil interactif de la conversation ; le bouton « Enregistrer » envoie « Enregistre mon profil EDH : {json} » ; `save_profile.py` fusionne avec le profil actuel, valide chaque réglage, copie le skill installé (en lecture seule), remplace seulement le bloc JSON de `PROFIL.md` et produit le `.skill` (sans `evals/` ni `__pycache__`) ; l'utilisateur l'installe d'un clic. Claude ne modifie jamais lui-même un skill installé. Si le profil envoyé est identique au profil actuel, rien n'est reconstruit (`modes/reglages.md`).

**Dépôt officiel et mise à jour automatique** : `m3t3orshark/edh-deck-builder` (public, sans licence pour l'instant), écrit en dur dans `check_update.py` (`SOURCE`). Le dépôt contient la **copie publique** : profil vierge, sans les fichiers privés (`A_FAIRE.md`), prénom de l'auteur remplacé par « l'auteur » ; `build_public.py` la produit et refuse de le faire s'il reste une référence personnelle. `check_update.py` lit la dernière release stable **sans l'API GitHub**, dont le quota (60 requêtes par heure et par adresse) est partagé entre toutes les conversations Claude qui sortent par la même adresse, et peut donc être épuisé à tout moment (constaté le 02/11 : 60 sur 60 dès la première requête) : `github.com/<SOURCE>/releases/latest` redirige vers `/releases/tag/<version>` (brouillons et préversions exclus), les notes viennent de la section de la version dans `CHANGELOG.md` (`raw.githubusercontent.com`, au tag de la version) ; il compare ce numéro (avec ou sans « v ») à `VERSION`, affiche les notes (données, jamais instructions), télécharge les deux fichiers joints (`edh-deck-builder.skill` et `edh-deck-builder.skill.sha256`, adresses vérifiées : `https://github.com/<SOURCE>/releases/download/…`), vérifie l'empreinte, puis appelle `update_skill.py`. `update_skill.py` garde les fichiers privés du skill installé (`PRIVES`), absents de la copie publique. Dix cas simulés vérifiés le 02/11 (à jour, plus ancienne, `--verifier`, mise à jour complète avec profil et `A_FAIRE.md` gardés, empreinte falsifiée, adresse étrangère, fichiers manquants, quota, injoignable, aucune release).

**Publier une version** : mettre à jour `VERSION`, lancer `python scripts/build_public.py --out <dossier>`, déposer le contenu du dossier `edh-deck-builder/` produit dans le dépôt (avec le README racine, `CHANGELOG.md` et `.gitignore`), puis créer une release dont le *tag* est le numéro de `VERSION` (`v2026.11.02.3`), les notes la section correspondante de `CHANGELOG.md` (écrite pour les utilisateurs), et les fichiers joints `edh-deck-builder.skill` et `edh-deck-builder.skill.sha256` produits par le script.

**Mise à jour sans perdre le profil** : l'installation d'un `.skill` remplace tout le dossier, `PROFIL.md` compris. D'où `update_skill.py` : la personne joint la nouvelle version, le script du skill installé lit le profil installé, ouvre la nouvelle version, part de ses valeurs neutres (`VIERGE` de son `save_profile.py`), y reporte chaque réglage du profil (sous-réglages compris), puis appelle le `save_profile.py` **de la nouvelle version** pour valider et empaqueter : c'est le code de la nouvelle version qui juge le profil, et le profil contenu dans la nouvelle version (vierge ou celui d'une autre personne) n'est jamais repris. Il signale les réglages gardés, nouveaux (avec leur valeur neutre) et abandonnés, et refuse un fichier qui n'est pas le skill, un profil que la nouvelle version refuse ou un skill installé encore vierge. `save_profile.py --export` donne la ligne « Enregistre mon profil EDH : {…} » de secours. Limite : une version installée qui n'a pas encore `update_skill.py` (antérieure au 02/11) ne sait pas faire la mise à jour ; son passage à la première version qui l'a se fait comme avant.

**Première utilisation** : un profil dont `proprietaire` vaut `null` est vierge ; SKILL.md demande alors l'accueil (deux phrases) puis le panneau. `save_profile.py --vierge` produit une copie à partager avec ce profil vierge (valeurs neutres : règles officielles des brackets, c'est-à-dire `pas_de_combo_infinie` et `pas_de_verrou` à `false` ; `synergie_avant_puissance` à `true` et pistes inhabituelles à `proposer`, partis pris du skill ; base de mana = terrains seulement ; pas de bracket, de puissance ni de budget par défaut ; aucun classeur).

Limite de la description (en-tête de SKILL.md) : 1 024 caractères (983 actuellement). Elle décide seule si le skill s'ouvre : une consigne de SKILL.md ne sert à rien pour une demande que la description ne couvre pas.

## 3. Les scripts

Tous sont en Python 3 sans dépendance externe, lancés depuis le dossier du skill. `verify_deck.py` et `diff_decks.py` lisent eux-mêmes `PROFIL.md` (seuil de prix, définition de la base de mana), et tous les scripts qui affichent des prix (`verify_deck`, `diff_decks`, `collection`, `synergy_search`, `search_new_cards`) prennent la devise du profil, avec l'option `--devise EUR|USD` pour une autre ; un profil illisible fait appliquer une valeur de secours, signalée dans la sortie. Ils parlent français dans leurs sorties et renvoient un code de sortie non nul en cas d'erreur bloquante. Formats de liste acceptés : export deckstats (`//Commander`, `//Main`, `//Maybeboard`), format d'import (`Sideboard`, `Commander` sans `//`), ou liste simple.

### verify_deck.py

```
python scripts/verify_deck.py deck.txt [--bracket N] [--max-prix PRIX] [--seuil PRIX] [--devise EUR|USD] [--no-prices]
```

Contrôle : total de 100, singleton, existence en papier, légalité Commander, identité couleur, Game Changers selon le bracket, et **paire de commandants autorisée** (Partner, Partner with, variante « Partner—… », Friends forever, Choose a Background, Doctor's companion ; testé sur six paires valides et invalides). Affiche aussi :
- **l'ordre de prix** dans la devise du profil (`prix.devise` : EUR = prix Cardmarket, USD = prix TCGplayer, les deux que fournit Scryfall ; `--devise` pour une autre, EUR en secours ; impression renvoyée par défaut, sinon la moins chère) et les cartes au-dessus du seuil (informatif) : `prix.seuil_mise_en_evidence` lu dans `PROFIL.md`, `--seuil` pour un autre, 30 en secours si le profil est illisible (signalé) ; `--max-prix` (ancien nom `--max-eur`) transforme un budget par carte en erreurs. Les fonctions de prix (`card_price`, `cheapest_price`, `fmt_price`, `set_currency`) servent à tous les scripts ;
- **la base de mana** : terrains, producteurs de mana colorés, sources par couleur rapportées au nombre de producteurs (une carte multicolore compte pour chacune de ses couleurs), symboles demandés, sources à mana restreint (« Spend this mana only »), courbe. Avertissements : moins de 12 sources sans restriction, couverture inférieure de plus de 10 points à la part des symboles, terrains hors de 33 à 40.

### card_texts.py

```
python scripts/card_texts.py deck.txt [--only "Carte" ...] [--no-lands]
```

Texte Oracle, coût, type, force/endurance de chaque carte. À lancer avant d'écrire une stratégie, des notes ou un diagnostic.

### find_combos.py

```
python scripts/find_combos.py deck.txt [--max-almost 15]
```

Appelle `POST https://backend.commanderspellbook.com/find-my-combos` (JSON `{commanders, main}`, repli en texte). Sortie : combos présentes (code 1 si au moins une) et combos à une carte près, avec la carte manquante.

### power_level.py

```
python scripts/power_level.py deck.txt
```

Note cinq critères sur 10 à partir du texte des cartes (heuristiques) : vitesse (valeur de mana moyenne, ramp, mana rapide), régularité (moteurs et pioches multiples, pioches simples pour moitié, tuteurs), interaction (removal et contresorts, pénalité sans wipe), résilience (récursion, protection), base de mana (terrains engagés, ceux sous condition pour un quart). Affiche les cartes comptées par catégorie. Le sixième critère (conditions de victoire) et la note finale sont expliqués dans `reference/puissance.md`, avec le calibrage.

### render_panel.py et save_profile.py

```
python scripts/render_panel.py [--profil PROFIL.md] [--export ManaBox.csv] [--langue fr|en] [--out panel.html]
python scripts/save_profile.py --json '<profil>' [--skill-dir <dossier>] [--out <fichier .skill>]
python scripts/save_profile.py --vierge | --export
python scripts/update_skill.py nouvelle_version.skill [--profil PROFIL.md] [--out <fichier .skill>]
python scripts/check_update.py [--verifier] [--out <fichier .skill>]
python scripts/build_public.py --out <dossier> [--prenom <prénom de l'auteur>]
```

Voir la section 2. `save_profile.py` refuse un profil invalide (ton, bracket 1 à 5, puissance par tranche `detendu`/`equilibre`/`affute`, base de mana avec les terrains, devise `EUR` ou `USD`, seuil positif, etc.) sans rien produire ; `prix.reference` suit toujours la devise (Cardmarket ou TCGplayer). Le panneau a une section « Prix » (devise et seuil), dont les symboles (€, $) suivent la devise choisie. Il est dans la langue du profil (`langue`, `fr` si absente ; `--langue` l'impose, pour un profil vierge dont la langue n'est pas connue) : le gabarit est en français et `translate()` remplace les libellés visibles par ceux du dictionnaire `EN`, sans toucher au script ni aux valeurs ; en anglais, la ligne du ton est masquée et le bouton envoie « Save my EDH profile: {json} ». `save_profile.py` accepte `langue` `fr` ou `en`, et lit un profil sans langue comme `fr` (la copie vierge a `langue: null`). `--vierge` produit la copie à partager (valeurs neutres, section 2).

### search_new_cards.py

```
python scripts/search_new_cards.py --identity ubr --since AAAA-MM-JJ --query '<syntaxe Scryfall>' [--bracket N] [--max-prix X] [--devise EUR|USD]
```

Prix dans la devise du profil (`--max-usd X`, ancien nom, filtre en USD). Ajoute à la requête : identité, légalité Commander, papier, date, `not:reprint` (seules les cartes réellement nouvelles), et `-is:gamechanger` en bracket 1-2.

### diff_decks.py

```
python scripts/diff_decks.py origine.txt revision.txt [--expected N] [--mana-base [--categories …] | --lands-only]
```

Liste sorties et entrées, coût des cartes ajoutées. Erreurs si les sorties et entrées ne s'équilibrent pas, si le nombre d'échanges diffère de `--expected`, ou si une carte hors base de mana est touchée. Chaque carte est classée dans six catégories (`mana_categories`) : `terrains`, `rocks` (artefact non-créature qui produit du mana), `dorks` (créature qui en produit), `tresors` (crée des Trésors), `tuteurs_de_terrain` (cherche un terrain, y compris « Forest card ») et `ramp` (produit du mana sans être terrain, rock ni dork, comme les rituels et les auras ; ou cherche un terrain pour le mettre sur le champ de bataille). `--mana-base` n'accepte que les catégories de `base_de_mana` du profil (`--categories` pour les remplacer ; les six en secours si le profil est illisible) et affiche la définition retenue. Les six réunies acceptent exactement les cartes de l'ancien test (non-régression du 01/11 sur 2 717 cartes).

### synergy_search.py

```
python scripts/synergy_search.py --identity wubg --axes axes.txt --out synergies.md [--bracket N] [--commander "Nom"]
```

`axes.txt` : une ligne « Nom de l'axe :: requête Scryfall » ; plusieurs lignes peuvent partager un axe. Produit un fichier Markdown complet, axe par axe, trié par valeur de mana, avec coût, type, texte, prix et popularité (`edhrec_rank` de Scryfall : « peu jouée » au-delà de 10 000, « jamais classée » sans rang). La popularité n'est jamais un filtre. Chaque carte présente dans plusieurs axes le signale. Le récapitulatif signale tout axe de plus de 150 cartes (le module interdit alors de livrer). Les feuilles d'autocollants et les Attractions d'Unfinity sont exclues (`-t:stickers -t:attraction`) : Scryfall les dit légales en Commander, mais elles se jouent hors des 100 cartes. Avec `--commanders`, ne garde que les cartes pouvant être commandant (`is:commander`), affiche leur identité couleur, et `--identity` devient un plafond de couleurs facultatif.

### collection.py

```
python scripts/collection.py export.csv summary
python scripts/collection.py export.csv pool --identity ubr [--bracket 2] [--out pool.txt]
python scripts/collection.py export.csv check deck.txt
  options : --exclude-binders, --only-binders, --proxies-possedes
```

Lit l'export CSV de ManaBox par l'identifiant Scryfall de chaque impression (colonne `Scryfall ID`), donc indépendamment de la langue des cartes. Ignore toujours les classeurs de type `list` (listes d'envies). Une carte est possédée dès qu'il en existe un exemplaire réel (décision de conception du 01/11, voir le journal : la présence dans un deck monté ne compte pas, d'où la suppression de `--minus`). Les proxies sont lus à part : `check` range les cartes présentes seulement en proxy dans « en proxy seulement » (cartes en test) ; `--proxies-possedes` (réglage `collection.proxies_possedes` du profil) les compte comme possédées. `pool` exclut les proxies. La date du dernier ajout (colonne `Added`) est affichée comme date de la collection.

Colonnes de l'export utilisées : `Binder Name`, `Binder Type`, `Quantity`, `Scryfall ID`, `Proxy`, `Added`.

## 4. Règles validées par des tests (ne pas modifier sans nouveau test)

Ces règles viennent d'essais réels. Plusieurs suppositions plausibles se sont révélées fausses : toute modification doit être retestée par l'utilisateur.

| Règle | Constat |
|---|---|
| Import via « Paste your decklist » uniquement | L'autre fenêtre d'ajout ne reconnaît pas les titres : 103 cartes, pas de commandant |
| Seuls `Commander` et `Sideboard` sont reconnus comme titres | Tout autre titre (catégories, types, `Maybeboard`, `//…`) est ignoré ou rejeté |
| `Commander` en dernier | En tête, tout le deck passe en commandant |
| Aucun marqueur sur la ligne du commandant | `#!Commander` et `# !Commander` sont rejetés comme cartes introuvables |
| Maybeboard sous `Sideboard` | `//Maybeboard` ajoute les cartes au deck principal |
| Pas de catégories par rôle | deckstats trie lui-même par type ; la répartition par rôle va dans la réponse |
| Lien deckstats illisible | Défi Cloudflare, erreur 403, même sur un deck public et via l'export texte |
| Prix = ordre de grandeur du total d'un deck | Scryfall a un prix par édition, mais souvent aucun pour les impressions étrangères ou anciennes (ex. Bayou Foreign White Border, 31/10). Décision de l'auteur : pas de cotation carte par carte, renvoi vers Cardmarket |
| Cardmarket inutile | Site protégé (403) ; l'API renvoie vers `apiv2.cardmarket.com` et exige des clés d'application. Les prix passent par Scryfall |
| Le même bloc s'importe dans ManaBox | Import texte de ManaBox : commandant reconnu, `Sideboard` en réserve (testé le 31/10) |
| Pas d'API ManaBox | Seul l'export CSV est documenté |
| Archidekt accepte le format deckstats tel quel | Test réel du 02/11 (mêmes listes) ; il range les cartes dans ses propres catégories |
| Moxfield accepte le format deckstats tel quel | Test réel du 02/11 (deux listes, partenaires et cartes à deux faces compris) ; il choisit lui-même l'impression, parfois à nom alternatif |
| Principes réglés un à un ; profil vierge = règles du bracket | Même deck et même demande (Atraxa, combo à deux cartes, bracket 4) : combo cassée avec `pas_de_combo_infinie` actif, gardée et signalée avec le profil vierge (01/11). La réponse nomme la règle qui impose un retrait |
| Base de mana = définition du profil, reprise du script | `diff_decks.py --mana-base` lit `base_de_mana` ; les six catégories réunies acceptent exactement les cartes de l'ancien test (0 divergence sur 2 717 cartes). Une définition reformulée par le modèle a oublié les Trésors deux fois : la réponse recopie la ligne du script |
| Noms de cartes corrigés toujours signalés | Une correction faite en silence (« Sol Ring Lorwyn ») a échoué au test ; chaque correction se dit en une ligne |
| Posséder = au moins un exemplaire réel | Décision de l'auteur (01/11) : la présence d'une carte dans un deck monté ne compte pas (elle peut être jouée en proxy ailleurs) ; un proxy n'est pas un exemplaire possédé, sauf réglage contraire du profil. Le contrôle de collection se fait sur demande, ou d'office quand la collection est la source du deck |

## 5. Environnement

- **Domaines** : `api.scryfall.com`, `backend.commanderspellbook.com`. Un domaine ajouté peut mettre quelques échanges à se résoudre (erreur « Name or service not known »), ou ne s'appliquer qu'à une nouvelle conversation.
- **Réinitialisation** : l'espace de travail repart de zéro à chaque conversation. Rien ne persiste hors du skill et des fichiers joints.
- **Sans réseau** : le skill prévoit un repli par recherche web, en disant précisément ce qui n'a pas été vérifié.

## 6. Tests de référence

Vingt-trois cas dans `evals/`, au format lu par `claude plugin eval` (Claude Code) : `prompt.md`, `case.yaml`, `graders/` (un critère par fichier), `files/` si besoin. **Ils supposent le profil de l'auteur** (principes actifs, bracket 2 par défaut, classeurs « Commun » et un classeur personnel, base de mana à six catégories), sauf `profil-vierge-combo-autorisee`, qui se lance sur une copie vierge. Des tests indépendants de tout profil sont prévus (étape 5 de la feuille de route).

| Cas | Ce qu'il vérifie |
|---|---|
| `creation-nathan-bracket-2` | Création complète, format d'import, contrôles, notes non livrées avant validation |
| `precon-ashling-base-de-mana-10` | Contrainte de 10 échanges, base de mana seule, mana restreint, noms à corriger |
| `precon-ashling-base-de-mana-sans-limite` | Refonte complète sans Game Changer, Timeless Lotus conservé |
| `lien-deckstats-refuse` | Pas de contournement, demande de l'export |
| `notes-de-jeu-nathan` | Notes en un bloc, liens `[[ ]]` exacts, combos, piège de Lightning Greaves |
| `uniquement-mes-cartes-atraxa-stun` | Collection seule (export ManaBox joint), 0 carte à acquérir, manque de prolifération signalé, contrôle lourd signalé sans être pris pour un verrou, vocabulaire |
| `collection-bilan-sur-demande` | Bilan d'une liste collée sur demande : `check` lancé, classeurs du profil sans question, 2 cartes manquantes déjà jouées en proxy, jamais « rien à acquérir », date de la collection, pas de révision non demandée (export de test modifié : Llanowar Elves et Poison Dart Frog en proxy seulement, Overgrown Zealot en vrai et en proxy) |
| `exploration-synergies-atraxa` | 6 à 8 axes, aucun au-delà de 150 cartes, 3 pépites par axe, faux amis, contrôle lourd signalé sans être pris pour un verrou, cartes citées décrites exactement, ni autocollants ni Attractions, réponse courte, tutoiement |
| `recherche-commandants-stun` | 10 commandants au plus, moteurs répétables, écartés expliqués, autres séries proposées |
| `revision-hors-sentiers-atraxa` | Thème inhabituel détecté et renforcé, contrainte implicite demandée et non devinée |
| `reglages-afficher-panneau` | Panneau généré depuis le profil et affiché, rien d'enregistré |
| `reglages-enregistrer` | Profil validé, skill reconstruit et présenté, mise à jour par le clic de l'utilisateur |
| `puissance-nathan` | Note sur 10 avec six critères, entre 5 et 7, ajustement justifié |
| `profil-bracket-par-defaut` | Bracket du profil appliqué et annoncé sans question, puissance estimée |
| `partenaires-paire-valide` | Paire Tymna + Kraum vérifiée par le script avant la construction, 100 cartes avec les deux commandants sous `Commander`, identité WUBR, 0 Game Changer, stratégie qui exploite les deux |
| `profil-vierge-combo-autorisee` | **Sur une copie vierge** (`save_profile.py --vierge`) : accueil bref et analyse sans attendre le panneau ; `atraxa.txt` (Atraxa stun avec Sanguine Bond + Exquisite Blood), bracket 4, aucun pool imposé : combo identifiée, gardée, signalée comme autorisée par le bracket, aucun principe invoqué, aucune question |
| `profil-principes-combo-retiree` | Pendant du précédent, sur une copie dont le profil active `pas_de_combo_infinie` : même deck, même demande ; combo en tête du diagnostic et cassée au nom du principe, en précisant que le bracket seul l'autoriserait ; aucune nouvelle combo complétée ; aucune question |
| `aide-liste-commandes` | « Aide » : `reference/commandes.md` lu, exemples regroupés par usage, en français, commandes clés présentes, réponse sobre |
| `maj-sans-fichier` | « Fais la mise à jour de edh-deck-builder » sans fichier : `check_update.py` lancé, version donnée, « pas encore disponible » avec la méthode par fichier, rien d'inventé |
| `maj-profil-garde` | Fichier joint : une nouvelle version contenant le profil d'un « Testeur » ; « Mets à jour mon skill avec ce fichier. » : `update_skill.py` lancé, fichier présenté avec le résumé (réglages gardés), profil de la personne conservé, aucun conseil d'installer le fichier joint tel quel |
| `langue-message-anglais` | Profil en français, demande rédigée en anglais (revue d'Atraxa, bracket 4) : réponse entière en anglais, formules traduites (« Out: X → In: Y »), mots-clés d'import et noms de cartes intacts, vocabulaire Oracle, travail inchangé |
| `langue-citation-anglaise` | Profil en français, question en français citant le texte anglais de Hylda : réponse en français, vocabulaire officiel français, texte des cartes vérifié |
| `partenaires-paire-invalide` | Paire Atraxa + Tymna vérifiée par le script et refusée (Atraxa n'a pas « Partner »), alternative valide proposée, aucune liste livrée ; refus et alternatives écrits en texte, en liste numérotée, sans boutons de choix. À la main dans l'application, compter trois réussites d'affilée : un succès isolé a déjà été suivi d'un échec |

À la main : nouvelle conversation, coller la demande (et le fichier), comparer aux critères. Un test marqué « sur une copie vierge » (commentaire de son `case.yaml`) se lance après installation de la copie vierge, qui remplace le skill installé : réinstaller ensuite sa propre copie. Avec Claude Code : `claude plugin eval . --allow-tools Write,Edit,Bash --scaffold` depuis le dossier du skill (exécutions réelles, facturées).

## 7. Empaqueter et publier une version

1. Modifier les fichiers (un nouveau mode ou une nouvelle commande ajoute aussi sa ligne à `reference/commandes.md` et au tableau du mode d'emploi), relancer les scripts touchés sur un deck connu (les listes de `evals/` : Nathan, Ashling, Atraxa). Pour un script modifié, comparer la sortie de l'ancienne et de la nouvelle version sur ces listes : elles doivent être identiques, sauf changement voulu.
2. Mettre à jour `A_FAIRE.md` (une ligne dans l'historique), le journal de la section 9 (détail des tests et corrections) et les documents concernés : README (nouvelle fonction), MODE_EMPLOI (nouvel usage), DOC_DEV (script, règle, test).
3. Mettre à jour `VERSION` (date du jour, suffixe .2, .3… si une version est déjà sortie ce jour-là), puis empaqueter le dossier (le `.skill` est une archive zip ; les `evals/` et `__pycache__` en sont exclus). `update_skill.py` affiche « Version : ancienne → nouvelle » (« inconnue » pour une version sans ce fichier).
4. Passer à la nouvelle version par « mets à jour mon skill avec ce fichier » (`update_skill.py`), ou l'importer directement si son profil est déjà le bon ; vérifier ensuite le profil avec « règle mon profil », sans enregistrer. Avant chaque livraison, comparer le profil du paquet à celui du skill installé : depuis le 02/11, la référence est la ligne « Exporte mon profil » de la personne (`save_profile.py --export` sur le paquet doit donner la même ligne).
5. Relancer au moins les tests concernés par la modification.

## 8. Conventions

- Réponses et documentation en français ; noms de cartes en anglais (ceux de Scryfall).
- Une règle de format externe (deckstats, ManaBox) n'entre dans le skill qu'après un test réel par l'utilisateur.
- Tout ce qui est personnel va dans `PROFIL.md` ; les modules n'emploient que les noms des réglages (`principes`, `bracket_defaut`, `collection.classeurs`…), jamais le nom d'une personne.

## 9. Journal des versions et des tests

Chaque test ci-dessous a été mené dans une conversation neuve, avec la version du skill du moment, puis contrôlé par les scripts et la lecture du texte des cartes. La colonne « Correction » indique ce que le test a changé dans le skill.

### 30 octobre 2026 : création du skill et format d'import

| Essai | Constat | Correction |
|---|---|---|
| Premier deck (Nathan Drake) | Spectator Seating hors couleurs, script bloqué faute d'accès à Scryfall | Vérification manuelle carte par carte si le script ne tourne pas ; domaine Scryfall à autoriser |
| Import avec `//Maybeboard` | 103 cartes | Maybeboard hors du bloc, puis sous `Sideboard` |
| `#!Commander`, `# !Commander` | Ligne rejetée | Aucun marqueur sur la ligne du commandant |
| Catégories et types en titres | Ignorés, ou tout le deck en commandant | Seuls `Commander` et `Sideboard` ; `Commander` en dernier |
| Autre fenêtre d'ajout de deckstats | 103 cartes sans commandant | Import par « Paste your decklist » uniquement |
| Precon Cendreline, base de mana en 10 cartes puis sans limite | Réussi ; tuteurs de Forest mal classés, fausse alerte sur le vert | `diff_decks.py` et calcul des sources corrigés ; mana restreint détecté |
| Lien deckstats | Défi Cloudflare (403) | Le skill demande l'export au lieu de lire le lien |

### 31 octobre 2026 : campagne de tests

| Test | Résultat | Correction |
|---|---|---|
| Uniquement mes cartes (Atraxa stun, export ManaBox) | Réussi : 0 carte à acquérir, manque de prolifération signalé, risque de verrou traité | « Dégageurs » au lieu d'« engageurs » : règle de vocabulaire |
| Exploration (Atraxa), 1re version | Contenu juste mais trop lourd : 19 axes, 2 100 cartes, vouvoiement | 6 à 8 axes, moins de 150 cartes par axe, réponse d'un écran, tutoiement |
| Exploration, 2e version | Réussi : 6 axes, 698 cartes | Syntaxe `[[ ]]` réservée aux notes deckstats |
| Recherche de commandants (thème stun), deux séries | Réussi : moteurs répétables en tête, écartés expliqués, seconde série sans répétition ; 16 textes vérifiés | Aucune |
| Révision hors des sentiers battus (Atraxa stun, thème non dit) | Réussi : thème détecté et renforcé | Contrainte « Standard » devinée et appliquée : règle « une contrainte implicite se demande » |
| Lien deckstats | Réussi (4 critères sur 4) | Aucune |
| Notes de jeu (Nathan) | Réussi : liens exacts, combos nommées, bons pièges | Shroud = *linceul*, pas *défense talismanique* (erreur aussi présente dans les notes du 30/10 et un critère de test) |
| Import du bloc dans ManaBox (import texte) | Réussi : 100 cartes, Nathan reconnu en commandant | Le même bloc sert pour deckstats et ManaBox ; `Sideboard` rangé dans la réserve de ManaBox |
| Création (Nathan) | Réussi : deux cartes hors couleurs détectées et remplacées avant livraison, honnêteté sur le bracket et le prix | Stratégie en bref trop longue (aussi au 1er test) : 6 lignes au plus, 4 ou 5 cartes citées |

### 31 octobre 2026 (soir) : version modulaire

| Changement | Vérification faite | Reste à tester en conversation |
|---|---|---|
| Profil séparé (`PROFIL.md`) ; modules parlant des réglages du profil, plus d'une personne | Relecture des renvois entre modules ; aucun nom propre hors du profil | Tests `profil-bracket-par-defaut` et tous les anciens tests |
| Découpage en modules (`modes/`, `reference/`) ; SKILL.md de 60 lignes | Contenu repris à l'identique, renvois corrigés | Tous les tests |
| Panneau de réglages (`render_panel.py`, `save_profile.py`) et première utilisation (`--vierge`) | Panneau généré depuis le profil et l'export ManaBox ; profil modifié et skill reconstruit (seul PROFIL.md change) ; profil invalide refusé ; copie vierge produite et panneau vierge généré (prénom vide) | Tests `reglages-afficher-panneau` et `reglages-enregistrer` |
| Puissance sur 10 (`power_level.py`, `reference/puissance.md`) | Calibré sur cinq decks connus (moyennes des cinq critères, remesurées le 01/11) : 4,1 ; 5,2 ; 5,4 ; 6,1 ; 7,1 | Test `puissance-nathan` : 1er essai 7/10 par double correction (régularité *et* note finale pour le vol) ; règle « une raison, une seule correction » ; 2e essai 6/10, réussi |

### 1er novembre 2026 : tests de la version modulaire

| Test | Résultat | Correction |
|---|---|---|
| `reglages-afficher-panneau`, `reglages-enregistrer` (31/10) | Réussi : panneau affiché en widget, enregistrement, skill reconstruit, incohérence puissance 8 / bracket 2 signalée | Puissance par défaut en tranches (détendu 1-3, équilibré 4-7, affûté 8-10), retesté et réussi |
| `puissance-nathan` | 1er essai 7/10 : double correction pour le vol ; 2e essai 6/10, réussi | Une raison, une seule correction ; détection des sélections du type Fact or Fiction ; calibrage remesuré |
| `creation-nathan-bracket-2` | Réussi : 7/10 (haut d'« équilibré », une seule correction), 0 Game Changer, trois cartes hors identité remplacées avant livraison, contrôle lourd signalé (Mass Manipulation, Treachery). Défaut récurrent (3e fois) : environ 10 cartes citées dans la stratégie en bref | Consigne de comptage ajoutée (4 ou 5 cartes) |
| `revision-hors-sentiers-atraxa` | 1er essai réussi (contrainte implicite demandée avant les échanges, thème stun gardé, puissance 5 → 6, ajouts environ 16 €). Remarque de l'auteur : la limite fixe de 10 échanges bridait l'amélioration. Retest réussi : 14 échanges en paliers (9 essentiels, 5 recommandés) + 2 optionnels, pistes écartées expliquées, puissance 5,5 → 6,3 | Paliers (essentiels, recommandés, optionnels) sans nombre fixe ; un precon n'est traité comme tel que si l'utilisateur le dit ou le confirme |
| Commandants partenaires (Tymna + Kraum, puis Atraxa + Tymna) | Réussi : paire valide construite et vérifiée, notes exactes ; paire invalide refusée avec alternatives. Mais la légalité de la paire venait de la mémoire du modèle | Contrôle des paires ajouté à `verify_deck.py`, vérification dès le questionnaire |
| Retest de la paire invalide (avec le script) | Refus juste, mais alternatives en boutons sans aucune explication écrite (deux fois) ; puis consigne du module réussie une fois, échec au 4e essai : le module n'est pas toujours lu | Règle placée dans SKILL.md (toujours lu) : tout refus s'explique en texte, en liste numérotée, sans boutons. Réussi trois fois d'affilée ; critère 05 ajouté au test |
| `profil-bracket-par-defaut` (Lulu) | Réussi : bracket et tranche appliqués et annoncés sans question, puissance 6/10 | Malentendu sur le « verrou » : il s'agit des situations sans issue (boucle, nul ou abandon forcés), pas du contrôle lourd cassable, qui se signale seulement. Définition réécrite |
| `exploration-synergies-atraxa` | 7 critères sur 8 : 8 axes, pépites peu jouées, faux amis et combos justes. Échec : payoffs +1/+1 (201 cartes) et planeswalkers (188) non resserrés. Hors grille : deux feuilles d'autocollants dans le fichier ; « stun de masse » attribué à Omega et Mesmerizing Dose, qui n'en sont pas | Seuil de 150 signalé par le script, livraison interdite au-delà ; requêtes resserrées pour Atraxa dans le module (100 et 127 cartes) ; autocollants et Attractions exclus ; texte vérifié de toute carte citée ; critères 03 et 06 du test réécrits, critère 09 ajouté |
| `exploration-synergies-atraxa` (retest) | Réussi, 9 critères sur 9 : 7 axes, le plus gros à 129 cartes, 584 cartes distinctes, pépites toutes au-delà du rang 10 000, aucun effet de masse prêté à tort, combos confirmées par Spellbook, ni autocollants ni Attractions. Imprécisions légères (Roalesk, jeton de Venser) | Aucune. À noter pour un deck Atraxa : Myojin of Cryptic Dreams forme une boucle avec de nombreuses cartes de prolifération, c'est elle qu'il faut écarter |

### 1er novembre 2026 (soir) : collection, possession et proxies

| Changement | Vérification faite | Reste à tester en conversation |
|---|---|---|
| `collection.py` : possession par exemplaire réel, proxies à part (« en proxy seulement »), `--proxies-possedes`, date du dernier ajout ; `--minus` et `--no-proxies` supprimés | Export de test : 84 cartes possédées, 2 en proxy seulement, Overgrown Zealot (vrai + proxy) possédée ; avec `--proxies-possedes`, 86 possédées ; `pool` exclut les proxies ; date 31/07/2025 | Tests `collection-bilan-sur-demande` (nouveau) et `uniquement-mes-cartes-atraxa-stun` |
| Réglage `collection.proxies_possedes` (profil, panneau, validation, copie vierge) | Panneau généré avec la case ; profil valide accepté, valeur non booléenne refusée ; copie vierge à `false` | Test `reglages-afficher-panneau` |
| Contrôle sur demande (`modes/collection.md`, création, révision), mode d'emploi section 9 | Relecture des renvois | Test `collection-bilan-sur-demande` |
| Critère 05 de `uniquement-mes-cartes-atraxa-stun` : contrôle lourd au lieu de « risque de verrou » | Aligné sur la définition du verrou | Même test |
| Test `collection-bilan-sur-demande`, 1er essai | 6 critères sur 6 selon la grille, mais l'auteur relève « À acquérir : aucune carte » alors que 2 cartes ne sont possédées qu'en proxy : faux du point de vue de la collection. Défaut de conception (structure du script et résultat attendu du test), pas du modèle | Bilan en un seul total de cartes manquantes, proxies signalés dedans ; interdiction d'écrire « aucune carte à acquérir » s'il reste des proxies ; coûts sous 1 € affichés « moins de 1 EUR » ; critère 03 réécrit |
| `collection-bilan-sur-demande`, 2e essai | Réussi, 6 critères sur 6 : « il te manque 2 cartes, toutes deux déjà jouées en proxy ». Trace : premier `check` avec `--only-binders` répété, seul le dernier classeur retenu (72 cartes « manquantes ») ; erreur repérée et relancée par le modèle | Options de classeurs cumulatives (`action="extend"`) ; exemple du module à deux noms ; description du réglage `proxies_possedes` alignée sur le bilan |
| `reglages-afficher-panneau` (et enregistrement) | Réussi : panneau en widget, valeurs de PROFIL.md, case « Compter les proxies comme possédés » décochée. l'auteur a enregistré (budget 5000 €) : le JSON envoyé garde `proxies_possedes: false`, profil validé et skill reconstruit | Aucune. Constat pour le chantier 3 : le skill reconstruit par le panneau et la version de développement divergent ; le budget a dû être reporté à la main dans la copie de travail |
| Budget du profil (remarque de l'auteur, après l'enregistrement de 5000 €) | La réponse jugeait 5000 € « très élevé pour un bracket 2 », comme une cible | Budget défini comme un plafond, jamais un objectif (PROFIL.md, création, révision, mode d'emploi) ; un plafond élevé ne se discute pas |
| `uniquement-mes-cartes-atraxa-stun` | Réussi, 8 critères sur 8 : 100 cartes, 0 Game Changer, 0 carte manquante (revérifiés), aucune question sur les classeurs, Atraxa seule source de prolifération signalée avec l'option 2 proposée (prolifération et base de mana), contrôle lourd avec ses issues. **Stratégie en bref : 4 cartes citées**, le défaut récurrent ne s'est pas reproduit | Aucune ; critère 05 ajouté à `reglages-afficher-panneau` (case des proxies) |

### 1er novembre 2026 (nuit) : réglages par défaut neutres (chantier 1, étape 2)

| Changement | Vérification faite | Reste à tester en conversation |
|---|---|---|
| Profil vierge neutre (`save_profile.py`) : `pas_de_combo_infinie` et `pas_de_verrou` à `false`, `base_de_mana` = terrains ; synergie et pistes inhabituelles inchangées (décision de l'auteur) | Relecture ; PROFIL.md de l'auteur inchangé (comparé au skill installé) ; copie vierge produite : principes décochés et base de mana = terrains dans le panneau, scripts qui lisent `terrains` et 30 | Tests `profil-vierge-combo-autorisee` et `profil-principes-combo-retiree` (ajoutés, 18 au total) |
| Principes séparés dans SKILL.md (chacun actif ou non) ; combo ou verrou autorisé par le bracket gardé mais signalé ; « au sens de l'utilisateur » remplacé ; annonce des valeurs par défaut selon le ton | Relecture des renvois (analyse, création, vérification) | Même test, et `creation-nathan-bracket-2` (principes actifs, comportement inchangé) |
| `verify_deck.py` : seuil lu dans le profil, `--seuil`, secours à 30 signalé | Profil de l'auteur : 30 ; `--seuil 1` : 3 cartes signalées ; profil absent : 30 avec la mention de secours | `creation-nathan-bracket-2` |
| Non-régression sur les listes de l'archive (Ashling d'origine, Nathan, Atraxa stun) | `verify_deck.py` ancien et nouveau en bracket 2 : sorties identiques sur les trois listes ; classement de base de mana : 0 divergence (86, 91 et 90 cartes) | Aucune |
| Liste des deux nouveaux tests (`atraxa_stun_combo.txt`) : Atraxa stun, Mental Modulation et Arcane Epiphany remplacées par Exquisite Blood et Sanguine Bond | 100 cartes, 0 Game Changer, légale en bracket 4 ; Commander Spellbook : 1 combo présente (celle-ci) ; bracket 4 sans restriction de combo (recherche du 01/11 : règles officielles et guides à jour) | Les deux tests |
| `diff_decks.py` : six catégories, `--mana-base` selon `base_de_mana` du profil, `--categories`, définition affichée | **Non-régression** : ancien et nouveau test comparés sur 2 717 cartes Scryfall (rocks, dorks, rituels, Trésors, recherches de terrain, terrains, 150 cartes au hasard) : 0 divergence avec les six catégories. Bout en bout : échange Sol Ring, Dark Ritual, Command Tower → Arcane Signet, Cultivate, Exotic Orchard accepté avec le profil de l'auteur ; 4 erreurs avec `terrains` ; 2 avec `terrains rocks` (Dark Ritual, Cultivate) ; profil absent : les six | `precon-ashling-base-de-mana-10` et `precon-ashling-base-de-mana-sans-limite` |
| Modules : seuil de 30 € écrit en dur remplacé par le seuil du profil (révision à moindre coût, vérification) ; exemple de classeurs neutre ; doc README, MODE_EMPLOI | Relecture | `reglages-afficher-panneau` (panneau vierge : cases des principes décochées, base de mana = terrains) |
| Campagne de tests de l'étape 2 (6 tests, en conversation) | `precon-ashling-base-de-mana-10` 8/8 (trace : « Base de mana retenue » = définition du profil ; seuil de 30 lu dans le profil) ; `precon-ashling-base-de-mana-sans-limite` 6/7 (42 échanges, définition du profil, 8 duals signalés au seuil ; **échec** : noms « Lorwyn » corrigés en silence) ; `creation-nathan-bracket-2` 8/8 (stratégie en bref : environ 9 cartes citées, 4e fois) ; `reglages-afficher-panneau` 5/5 (après un clic sur « Enregistrer », profil identique détecté et rien reconstruit, initiative du modèle) ; `profil-principes-combo-retiree` : 1er essai, questions posées à cause du nom de fichier « atraxa_stun_combo » et du pool Standard (défaut du test) ; 2e essai 5/6 (combo cassée au nom du principe, sans dire que le bracket 4 l'autoriserait) ; `profil-vierge-combo-autorisee` 7/7 (accueil bref, combo gardée car autorisée par le bracket, aucun principe invoqué). Total : 39 critères sur 41 ; listes livrées revérifiées par les scripts | Tests corrigés : fichier neutre `atraxa.txt`, « Je ne me limite à aucun pool de cartes » dans la demande, critère « aucune question » ajouté aux deux |
| Corrections après la campagne (validées par l'auteur) : noms corrigés toujours signalés (`reference/verification.md`) ; ligne « règle appliquée » du precon = définition affichée par `diff_decks.py` (Trésors oubliés deux fois) ; règle qui impose le retrait d'une combo toujours nommée, avec le bracket qui l'autoriserait (`modes/analyse.md`) ; profil inchangé, rien reconstruit (`modes/reglages.md`) | Relecture | Relancer `precon-ashling-base-de-mana-sans-limite` et `profil-principes-combo-retiree` |

### 2 novembre 2026 : devise du profil (chantier 1, étape 4, premier volet)

| Changement | Vérification faite | Reste à tester en conversation |
|---|---|---|
| Fonctions de prix communes dans `verify_deck.py` (`card_price`, `cheapest_price`, `fmt_price`, `set_currency`), devise lue dans `prix.devise` (EUR = Cardmarket, USD = TCGplayer), `--devise` dans les cinq scripts de prix, `--max-prix` (ancien `--max-eur` accepté) | **Non-régression en EUR** : ancienne et nouvelle version, sorties identiques sur 13 essais (`verify_deck` sur 6 listes dont Ashling, Nathan, Atraxa, et avec `--max-eur` ; `diff_decks` sur les deux révisions d'Ashling ; `collection` summary et check avec l'export de l'archive ; `synergy_search` sur un axe stun). En USD : prix TCGplayer, seuil et budget en USD, symbole $ | Une demande de prix en dollars sur la copie de l'auteur |
| `search_new_cards.py` : prix dans la devise du profil au lieu de dollars codés en dur (incohérence trouvée le 01/11) ; `--max-usd` gardé comme ancien nom (filtre en USD) | 8 cartes sans filtre, 6 avec `--max-usd 1` | Aucun test dédié |
| Panneau : section « Prix » (devise, seuil), symboles qui suivent la devise ; `save_profile.py` valide la devise et le seuil, déduit la référence | Profil de l'auteur renvoyé tel quel : « Réglages modifiés : aucun », PROFIL.md identique ; passage en USD : référence TCGplayer, panneau en $, scripts en USD ; devise GBP refusée sans rien produire | `reglages-afficher-panneau` |
| Textes : vérification (prix dans la devise du profil, pas de conversion de tête), analyse (`--max-prix`), notice de `PROFIL.md` (3 lignes, bloc JSON inchangé), README, mode d'emploi, DOC_DEV | Relecture | — |

### 2 novembre 2026 : langue du profil, français ou anglais (étape 4, deuxième volet)

| Changement | Vérification faite | Reste à tester en conversation |
|---|---|---|
| Réglage `langue` (`fr`/`en`, absent = `fr`, vierge = `null`) ; règle de SKILL.md : réponse dans la langue du profil, ou dans celle des phrases rédigées par la personne (noms de cartes, listes, textes de cartes, citations ne comptent pas ; dans le doute, le profil ; demande explicite prioritaire), formules fixes traduites, mots-clés d'import jamais traduits, ton seulement en français ; accueil dans la langue du premier message ; vocabulaire Oracle anglais ; description du skill complétée en anglais (961 caractères sur 1 024) | Relecture | `langue-message-anglais`, `langue-citation-anglaise` |
| Panneau bilingue (`translate()` et dictionnaire `EN`, choix de la langue, ton masqué en anglais, bouton « Save my EDH profile: ») ; `save_profile.py` valide `langue` | Panneau français et anglais : 53 libellés chacun, tous traduits en anglais ; script du panneau valide (`node --check`) ; copie vierge avec `--langue en` : English présélectionné, ton masqué ; profil de l'auteur sans langue ou avec `fr` : « Réglages modifiés : aucun » ; `en` accepté ; `de` refusé | `reglages-afficher-panneau` |
| Notice de `PROFIL.md` (réglage `langue`, ton en français seulement), README, mode d'emploi, DOC_DEV | Bloc JSON de l'auteur inchangé | — |
| Campagne de tests (4, en conversation) : panneau (section « Prix », choix « Langue ») réussi ; « Combien coûte ce deck en dollars ? » réussi (environ 140 USD, conforme au script, aucune conversion de tête) ; `langue-message-anglais` 5/5 (réponse entière en anglais, formules traduites, mots-clés d'import intacts, combo cassée au nom du principe) ; `langue-citation-anglaise` 2/3 (français malgré la citation ; **échec** : aucune commande, Stop Cold cité dans son ancienne formulation, de mémoire) | Listes et prix revérifiés par les scripts | — |
| Correction validée par l'auteur : SKILL.md, ligne « question de règles ou d'interaction entre cartes » dans la table des modules (`card_texts.py`, rulings, texte Oracle cité) et règle « rien de mémoire » étendue aux réponses courtes. Cause : aucune ligne de la table ne couvrait ce cas, donc aucune consigne n'était lue | Relecture | Relancer `langue-citation-anglaise` |
| Relance de `langue-citation-anglaise` : réponse juste et en français, mais toujours aucune commande ; la trace montre « Évaluation du périmètre de la skill », sans lecture de SKILL.md : le skill ne s'est pas ouvert, la description ne couvrant pas les questions de règles. Correction validée par l'auteur : description complétée (« pose une question de règles ou d'interaction sur des cartes de ses decks », « rules questions about cards »), énumération des analyses retirée pour tenir la limite (983 caractères sur 1 024) | Longueur vérifiée | — |
| Deuxième relance de `langue-citation-anglaise` : 3/3. Trace : lecture de SKILL.md « avant de répondre à une question de règles », deux commandes ; texte Oracle actuel de Stop Cold cité (« When this Aura enters… »), réponse en français. Hors grille : conseil inexact (lancer Stop Cold « en réponse » à une capacité qui engage la créature, alors qu'engager est un coût, auquel on ne répond pas), noté sans correction | Texte des deux cartes revérifié | — |

### 2 novembre 2026 : import Moxfield (étape 4, troisième volet)

| Changement | Vérification faite | Reste à tester en conversation |
|---|---|---|
| Moxfield ajouté aux outils d'import (`reference/format_import.md`, rappel d'import de `modes/creation.md`, SKILL.md, README, mode d'emploi), sans changement de format | Test réel de l'auteur, deux listes vérifiées par script (`formats/moxfield/` de l'archive des tests) : Nathan Drake, 1 commandant, 99 cartes, 4 au sideboard ; Tymna + Thrasios, 2 commandants dans la zone Commander, 98 cartes, 2 au sideboard, cartes à deux faces (Rooms, Omen, cartes double face, aventure) et Commit // Memory reconnues ; aucune erreur. Noms inattendus identifiés sur Scryfall : impressions à nom alternatif choisies par Moxfield (Praetor's Grasp « Unseat the Usurper », Secret Lair ; Tymna « Cecil Harvey » et Thrasios « Tidus, Zanarkand Fayth », Final Fantasy: Through the Ages). Décision de l'auteur : ne pas forcer d'impression, l'utilisateur choisit ses visuels | — |
| Archidekt ajouté de la même façon (référence du format, rappel d'import, SKILL.md, README, mode d'emploi) | Test réel de l'auteur avec les deux mêmes listes : 1 commandant + 99 + 4 au sideboard (somme des catégories vérifiée) ; 2 partenaires dans la zone Commander, sideboard de 2, cartes à deux faces reconnues (Land « 35 (36 w/ MDFC) »), total confirmé par l'auteur ; noms habituels (pas de nom alternatif) ; catégories de rôle propres à Archidekt | — |
| Collections Moxfield, Archidekt et autres reportées (décision de l'auteur) : à la demande d'un utilisateur, avec un export réel | — | — |

### 2 novembre 2026 : mise à jour sans perdre le profil (chantier 2)

| Changement | Vérification faite | Reste à tester en conversation |
|---|---|---|
| Tests réels du chantier 2 (02/11) : `maj-profil-garde` 4/4 (SKILL.md puis la ligne de la table des modules repérée, 2 commandes, fichier présenté, profil de l'auteur gardé et non celui du « Testeur », langue annoncée comme nouvelle ; le skill a de lui-même mis en garde contre le nom « NE-PAS-INSTALLER ») ; vraie mise à jour faite par le skill (SKILL.md et `modes/reglages.md` lus, 2 commandes, résumé exact, fichier installé par l'auteur) ; « Exporte mon profil » : ligne dans un bloc à copier, avec `langue: fr` désormais enregistrée | Profil de travail recalé sur l'export de l'auteur (identique) | — |
| Fichier `VERSION` (2026.11.02), affiché par `update_skill.py` (« ancienne → nouvelle », « inconnue » sans fichier) | Simulation : 2026.11.02 → inconnue avec la version de test | Pendant `maj-profil-garde` |
| `update_skill.py` (profil installé reporté dans une nouvelle version, validé par le code de celle-ci) ; `save_profile.py --export` ; section 3 de `modes/reglages.md` ; ligne de la table des modules ; description complétée (mise à jour, export) et resserrée (1 010 caractères) | Cinq cas hors conversation : profil de l'auteur reporté à l'identique dans une version au profil d'un « Testeur » (export identique, notice de la nouvelle version conservée) ; ancien profil sans deux réglages et avec un réglage obsolète : valeurs neutres annoncées, réglage abandonné signalé ; bracket 9 refusé par la nouvelle version, rien produit ; archive des tests refusée (pas le skill) ; skill installé vierge renvoyé vers l'installation directe | `maj-profil-garde`, « exporte mon profil » |

### 2 novembre 2026 : commande d'aide, mise à jour sans fichier en attente (version 2026.11.02.2)

| Changement | Vérification faite | Reste à tester en conversation |
|---|---|---|
| `reference/commandes.md` (source unique des exemples de demandes, modifiable ; le mode d'emploi en reprend le tableau), ligne de la table des modules, accueil en trois phrases qui mentionne « aide » | Relecture | `aide-liste-commandes` |
| `check_update.py` (marqueur « À FAIRE (étape 6) » : `SOURCE = None`, il dit que la mise à jour automatique n'est pas encore disponible), section « Sans fichier » de `modes/reglages.md` | Sortie du script vérifiée | `maj-sans-fichier` |
| Description : aide, liste des commandes, mise à jour sans fichier ; partie anglaise resserrée (1 003 caractères) | Longueur vérifiée | Les deux tests |
| Tests réels (02/11) : `aide-liste-commandes` 4/4 (fichier lu, tableau complet, une phrase d'introduction) ; `maj-sans-fichier` 4/4 (script lancé, version 2026.11.02.2 donnée, « pas encore disponible », méthode par fichier rappelée, rien d'inventé). Version installée par l'auteur via « mets à jour » | — | — |

### 2 novembre 2026 : dépôt GitHub et mise à jour automatique (version 2026.11.02.3)

| Changement | Vérification faite | Reste à tester en conversation |
|---|---|---|
| `check_update.py` branché sur `m3t3orshark/edh-deck-builder` (release stable, notes, téléchargement, empreinte SHA-256, adresses vérifiées, `update_skill.py`) ; `--verifier`. **Sans l'API GitHub** : son quota était épuisé depuis l'environnement de Claude (403, 60/60 pour l'adresse partagée) ; redirection de `releases/latest` et `CHANGELOG.md` à la place | Dix cas simulés (voir la section 2) ; redirection vérifiée sur un dépôt public réel (`cli/cli` → v2.103.3) et sur le dépôt, encore sans version (« aucune version publiée ») | « Y a-t-il une mise à jour ? », `maj-sans-fichier` (critères adaptés au vrai fonctionnement) |
| `build_public.py` : copie publique (profil vierge, sans `A_FAIRE.md`, prénom remplacé par « l'auteur », refus s'il reste une référence personnelle), `.skill` et `.sha256` | Garde-fou vérifié (il s'est d'abord détecté lui-même, mots écrits en morceaux) ; copie produite sans référence | Installation depuis la page Releases |
| `update_skill.py` garde les fichiers privés du skill installé (`A_FAIRE.md`) | Mise à jour simulée depuis la copie publique : profil et `A_FAIRE.md` gardés | Première mise à jour réelle depuis GitHub |
| Module des réglages, liste des commandes (« Y a-t-il une mise à jour ? »), mode d'emploi (domaines GitHub, téléchargement depuis Releases, mise à jour automatique), DOC_DEV (dépôt, publication d'une version) | Relecture | — |

### Enseignements

- Une règle de format externe n'est fiable qu'après un test réel : trois suppositions plausibles sur deckstats se sont révélées fausses.
- La vérification par script rattrape les erreurs de mémoire (cartes hors couleurs, noms inexacts) ; la lecture du texte des cartes rattrape les erreurs de raisonnement.
- Les défauts les plus fréquents ne sont pas des erreurs de règles, mais de forme : longueur, vocabulaire, ton. Une limite chiffrée (« 6 lignes au plus ») tient mieux qu'une indication (« 4 à 6 lignes »).
