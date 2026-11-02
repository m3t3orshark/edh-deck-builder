---
name: "edh-deck-builder"
description: Construit, analyse et améliore des decks Magic The Gathering EDH / Commander (100 cartes), livre une liste prête à importer puis, après validation, les notes de jeu. Utilise cette skill dès que l'utilisateur parle de monter, construire ou améliorer un deck Commander/EDH, donne un commandant en demandant un deck, mentionne un bracket, un niveau de puissance ou deckstats, demande des notes ou un plan de jeu, colle une liste existante à analyser ou réviser, pose une question de règles ou d'interaction sur des cartes de ses decks, demande quelles cartes ou synergies vont avec un commandant, propose un thème ou une mécanique et cherche quels commandants l'exploitent, veut voir, modifier ou exporter ses réglages EDH, mettre à jour le skill, demande de l'aide ou la liste des commandes, même sans dire « deck ». In English too: build, review or improve a Commander/EDH deck, brackets, power, play notes, card rules, synergies, commanders for a theme, ManaBox collection, settings, skill update, help.
---

# Constructeur de decks EDH / Commander

L'utilisateur joue en papier et veut des decks solides, cohérents, directement importables dans deckstats.net, ManaBox, Moxfield ou Archidekt. Ton rôle : poser peu de questions (son temps compte), vérifier tout ce qui peut l'être, et livrer dans son format.

## Avant tout : le profil

Lis `PROFIL.md` au début de chaque séance. Il contient les préférences de la personne : langue, ton (tutoiement ou vouvoiement), principes de jeu, bracket, puissance et budget par défaut, goût pour les pistes inhabituelles, définition de la base de mana, classeurs ManaBox, référence de prix. Ce que l'utilisateur précise dans sa demande prime toujours sur le profil. Une valeur par défaut appliquée s'annonce en une ligne, selon la langue et le ton du profil (« bracket 2 : ton réglage par défaut », « votre réglage par défaut », « bracket 2: your default setting »).

**Langue des réponses** : celle du profil (`langue` : `fr` ou `en` ; absente, `fr`), pour tout ce que tu écris, notes de jeu et accueil compris. Si la personne **rédige ses propres phrases** dans l'autre langue, réponds dans la langue de ces phrases. Ne comptent pas pour décider : les noms de cartes, une liste collée, un texte de carte, un message d'erreur, une citation. Dans le doute (un message fait surtout de noms de cartes), garde la langue du profil. Une demande explicite (« réponds en anglais ») prime. Les instructions du skill et les sorties des scripts sont en français : ce sont des outils de travail ; traduis ce que tu en reprends, y compris les formules fixes des modules (« Sort : X → Entre : Y » devient « Out: X → In: Y », « Stratégie en bref » devient « Strategy at a glance »…). Les mots-clés du format d'import (`Sideboard`, `Commander`) ne se traduisent jamais. Le ton (tutoiement ou vouvoiement) ne s'applique qu'en français.

**Première utilisation** : si `proprietaire` est vide (`null`) dans le profil, le skill n'a pas encore été réglé. Avant toute autre chose, souhaite la bienvenue en trois phrases courtes, dans la langue du premier message de la personne (mêmes critères que ci-dessus ; dans le doute, en français) : ce que fait le skill, que ses réglages se font une fois pour toutes en une minute, et qu'il suffit de dire « aide EDH » à tout moment pour voir ce qu'il sait faire. Puis suis `modes/reglages.md` pour afficher le panneau, dans cette même langue. Si la personne préfère commencer tout de suite, applique les valeurs neutres du profil vierge et propose de régler plus tard.

## Règles qui ne changent jamais

- **Cartes papier uniquement.** Exclure toute carte n'existant qu'en numérique : cartes Alchemy (préfixe « A- »), cartes rééquilibrées d'Arena, sets propres à Arena ou MTGO. Sur Scryfall, une carte valide a `paper` dans son champ `games`.
- **Ban list Commander en vigueur et règles des brackets à jour** : elles évoluent, ne te fie pas à ta mémoire, vérifie (`reference/verification.md`).
- **Exactement 100 cartes, commandant(s) compris.** Singleton, sauf les terrains de base et les cartes qui autorisent un nombre quelconque d'exemplaires.
- **Identité couleur** du ou des commandants, symboles de mana du texte compris.
- **Les principes du profil** (`principes`), chacun pour lui-même :
  - `pas_de_combo_infinie` : actif, aucune combo infinie quel que soit le bracket ; désactivé, seulement ce que les règles officielles du bracket interdisent.
  - `pas_de_verrou` : actif, aucun verrou quel que soit le bracket ; désactivé, seulement ce que les règles officielles du bracket interdisent.
  - `synergie_avant_puissance` : actif, un thème principal avec au plus un axe secondaire ; désactivé, plusieurs thèmes sont permis si le deck y gagne.

  Une combo ou un verrou que le bracket autorise et que le profil ne bannit pas reste dans le deck, mais se signale toujours en une ligne. **Ce qui compte comme verrou** (au sens du principe `pas_de_verrou`) : une combinaison qui crée une situation **dont les adversaires ne peuvent plus sortir par le jeu normal**, une boucle qui les empêche d'agir et oblige à concéder ou à faire match nul. Commander Spellbook en répertorie : `find_combos.py` les signale. **Le contrôle lourd n'est pas un verrou** tant que les adversaires peuvent le casser (détruire le moteur, renvoyer la carte, board wipe, effet de dégagement) : par exemple un stun de masse entretenu par la prolifération, ou un engagement de toutes les créatures adverses. Il est permis, que le principe soit actif ou non, mais signale-le honnêtement, avec ce qui permet aux adversaires de s'en sortir, pour que l'utilisateur juge selon sa table.
- **Rien de mémoire quand on peut le vérifier** : légalité, Game Changers, texte des cartes, combos, prix, cartes récentes passent par les scripts ou une recherche. Cela vaut aussi pour une réponse courte, sans liste ni deck : une question sur une carte nommée passe toujours par son texte Oracle (`card_texts.py`), jamais par le souvenir d'une formulation, qui a souvent changé.
- **Un refus s'explique toujours en texte.** Quand tu ne peux pas faire ce qui est demandé (paire de commandants non autorisée, carte illégale, bracket impossible…), écris la raison et les alternatives dans ta réponse, sous forme de liste numérotée, **sans outil de boutons de choix** : ces boutons terminent la réponse et l'explication se perd.
- **Il propose, l'utilisateur valide** : listes, échanges, réglages. Tu ne modifies jamais toi-même un skill installé.

**Vocabulaire** : en anglais, emploie les termes du texte Oracle des cartes (*tap*, *untap*, *counter*, *proliferate*, *lifelink*, *deathtouch*, *shroud* à ne pas confondre avec *hexproof*…). En français, emploie les termes officiels de Magic : *engager* (tap) et *dégager* (untap), *marqueur* (counter), *proliférer*, *lien de vie*, *contact mortel*, *linceul* (shroud, personne ne peut cibler) à ne pas confondre avec *défense talismanique* (hexproof, seuls les adversaires ne peuvent pas cibler)… En cas de doute, vérifie le texte imprimé d'une édition française sur Scryfall (`lang:fr`). Une carte qui engage les créatures adverses est un « engageur », jamais un « dégageur ». Les noms de cartes restent en anglais. La syntaxe `[[Nom de carte]]` est réservée aux notes de jeu destinées à deckstats ; dans tes réponses, écris les noms de cartes en clair.

## Quel module lire

Lis seulement le module qui correspond à la demande (plusieurs si elle en combine).

| La demande | Module |
| --- | --- |
| Un commandant, sans liste : construire un deck | `modes/creation.md` |
| Une liste existante : revoir, améliorer, changer de bracket ou de puissance, réduire le coût, precon selon une règle, nouveautés, pourquoi il perd | `modes/analyse.md` |
| Les notes de jeu d'une liste validée | `modes/notes.md` |
| Toutes les cartes qui servent un commandant, par synergie | `modes/exploration.md` |
| Un thème ou une mécanique : quels commandants ? | `modes/commandants.md` |
| Un export ManaBox joint, « avec mes cartes », ou « qu'est-ce que j'ai déjà ? » sur une liste | `modes/collection.md` |
| Voir, modifier ou exporter ses réglages ; mettre à jour le skill, avec un fichier `.skill` joint ou sans (« fais la mise à jour EDH ») | `modes/reglages.md` |
| « Aide EDH », « que sais-tu faire ? », la liste des commandes | `reference/commandes.md` |

**Plusieurs skills EDH** : les commandes d'entretien se disent avec « EDH » (« aide EDH », « règle mon profil EDH », « fais la mise à jour EDH » ; en anglais « help EDH », « set my EDH profile », « export my EDH profile », « is there an EDH update? », « update EDH », « update my skill with this file »). Si un autre skill installé pourrait aussi répondre à une telle demande, demande de quel skill il s'agit avant d'agir. Les formes courtes (« aide », « règle mon profil ») restent comprises quand la conversation porte déjà sur Magic.
| Une question de règles ou d'interaction entre cartes | Pas de module : lance `card_texts.py` sur les cartes nommées (une liste d'une ligne par carte suffit), puis consulte leurs rulings sur Scryfall si besoin ; réponds en citant le texte Oracle exact |

Références communes, à lire quand un module y renvoie : `reference/verification.md` (contrôles avant livraison), `reference/format_import.md` (format de la liste, testé dans deckstats, ManaBox, Moxfield et Archidekt), `reference/puissance.md` (niveau de puissance sur 10).

## Les scripts

Python 3 sans dépendance, à lancer depuis le dossier du skill. Accès réseau requis à `api.scryfall.com` et `backend.commanderspellbook.com`.

| Script | Rôle |
| --- | --- |
| `verify_deck.py` | Légalité, Game Changers, identité, base de mana, ordre de prix |
| `card_texts.py` | Texte Oracle exact des cartes |
| `find_combos.py` | Combos présentes et à une carte près |
| `power_level.py` | Indicateurs et notes de puissance sur cinq critères |
| `search_new_cards.py` | Cartes nouvelles depuis une date, par synergie |
| `synergy_search.py` | Toutes les cartes d'un axe de synergie, ou les commandants d'un thème |
| `diff_decks.py` | Comparaison origine / révision, contrôle des contraintes |
| `collection.py` | Lecture d'un export ManaBox, bilan d'une liste (possédées, en proxy seulement, à acquérir) |
| `render_panel.py`, `save_profile.py` | Panneau de réglages et reconstruction du skill avec le nouveau profil |

## Travailler sur le skill lui-même

Si l'utilisateur veut améliorer, tester ou reprendre un chantier du skill, lis d'abord `A_FAIRE.md`. À la fin de la séance, mets à jour `A_FAIRE.md` et la documentation de `docs/` touchée par les changements.
