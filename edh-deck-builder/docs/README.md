# edh-deck-builder

*Documentation validée le 31 octobre 2026, revue le 1er novembre 2026 (réglages par défaut neutres), mise à jour avec chaque version du skill.*

Un skill pour Claude qui construit, analyse et améliore des decks Magic: The Gathering au format **EDH / Commander**, pour des joueurs en papier qui veulent des decks solides et cohérents sans y passer des heures, directement importables dans deckstats.net, ManaBox, Moxfield ou Archidekt.

## L'intention

Monter un deck Commander demande des heures : trouver 99 cartes qui servent un commandant, équilibrer la ramp, la pioche et l'interaction, vérifier la ban list et les règles du bracket, puis tout saisir dans un outil. Ce skill fait ce travail en posant peu de questions, et livre :

- une **liste de 100 cartes** prête à coller dans deckstats, ManaBox, Moxfield ou Archidekt ;
- une **explication courte** de la stratégie, pour décider en connaissance de cause ;
- une fois la liste validée, des **notes de jeu** à coller dans la fenêtre Deck Notes de deckstats.

Il sait aussi **analyser un deck existant** : l'améliorer, changer son bracket, réduire son coût, améliorer un precon selon une règle (« 10 cartes », « base de mana seule »…) ou y intégrer les nouveautés des dernières éditions.

## Les principes

Chaque utilisateur a son **profil** : ses préférences, réglées une fois dans un panneau à la première utilisation. Sans réglage, le skill part de valeurs neutres. Les principes de jeu :

- **Les règles officielles du bracket, par défaut** : combos infinies et verrous ne sont interdits que là où le bracket les interdit. Le profil peut les bannir quel que soit le bracket, pour des parties qui se jouent jusqu'au bout ; quand une combo sort pour cette raison, le skill dit que le bracket seul l'aurait permise. Dans tous les cas, une combo, un verrou ou un contrôle lourd présents dans le deck sont signalés.
- **La synergie avant la puissance brute** (activée par défaut, désactivable) : un thème principal, au plus un axe secondaire.
- **Le bracket est respecté** : Game Changers comptés, règles du bracket vérifiées.
- **Cartes papier uniquement**, **ban list à jour**, **identité couleur stricte**, **exactement 100 cartes**.

Et un principe de méthode : **rien n'est affirmé de mémoire quand on peut le vérifier**. La légalité, les Game Changers, le texte des cartes, les combos, la base de mana et les prix passent par des scripts qui interrogent Scryfall et Commander Spellbook. Les règles de format deckstats ont toutes été testées à l'import.

## Ce qu'il faut pour l'utiliser

- Claude avec les skills, **l'exécution de code** activée et **l'accès réseau** à `api.scryfall.com` et `backend.commanderspellbook.com` (voir le mode d'emploi, section 1).
- Pour la collection : l'application **ManaBox** et son export CSV. Pour les listes : un compte **deckstats.net**, **Moxfield** ou **Archidekt**, ou l'application ManaBox (facultatif, la liste reste lisible telle quelle).

## Ce que le skill sait faire

| Besoin | Ce que fait le skill |
|---|---|
| Créer un deck | Questionnaire court, analyse du commandant, construction, vérification, liste importable |
| Analyser un deck | Diagnostic (rôles, base de mana, combos, bracket, puissance, coût), échanges classés en paliers |
| Améliorer un precon | Selon ta règle : nombre d'échanges, base de mana seule, budget |
| Réduire le coût | Remplaçantes dans le même rôle, économie chiffrée |
| Nouveautés | Recherche des cartes récentes qui servent les synergies du deck |
| Explorer les synergies | Toutes les cartes qui servent un commandant, par axe, sans filtre de popularité, avec les pépites peu jouées |
| Trouver un commandant | À partir d'un thème ou d'une mécanique, 10 commandants expliqués (et les écartés, avec la raison), d'autres séries sur demande |
| Niveau de puissance | Une note sur 10 en plus du bracket, fondée sur six critères nommés |
| Aide | « Aide EDH » affiche la liste des demandes possibles, avec un exemple pour chacune |
| Réglages | Un panneau visuel pour tes préférences, enregistré d'un clic ; mise à jour vers une nouvelle version sans perdre ton profil ; export du profil en une ligne |
| Notes de jeu | Plan de jeu, main de départ, synergies, pièges de règles, combos à éviter |
| Collection ManaBox | Uniquement mes cartes, en priorité mes cartes, ou meilleur deck puis bilan des achats ; sur demande, comparaison de n'importe quelle liste avec ta collection (possédées, en proxy seulement, à acquérir) |

## Ce qu'il ne fait pas

- Il ne lit pas un lien deckstats (le site bloque les lecteurs automatiques) : il faut coller l'export.
- Il ne se connecte pas à ManaBox (pas d'API publique) : il faut joindre l'export CSV.
- Il ne cherche pas dans quel deck se trouvent tes cartes : une carte possédée une fois compte pour tous tes decks, l'autre exemplaire pouvant être un proxy.
- Il parle **français** ou **anglais**, au choix dans le profil (et il répond dans la langue de tes phrases si tu changes de langue) ; les noms de cartes restent en anglais. La documentation n'existe pour l'instant qu'en français. Les prix sont en **euros** (Cardmarket) ou en **dollars** (TCGplayer), au choix dans le profil : ce sont les deux devises que fournit Scryfall, sans conversion vers d'autres. Les listes s'importent dans deckstats, ManaBox, Moxfield et Archidekt ; d'autres outils viendront quand leur import aura été testé. Pour la collection, seul l'export ManaBox est lu.
- Il ne remplace pas ton jugement : il propose, tu valides.

## Pour aller plus loin

- **[Mode d'emploi](MODE_EMPLOI.md)** : installer le skill et s'en servir au quotidien.
- **[Documentation développeur](DOC_DEV.md)** : architecture, scripts, règles validées et tests.
- **`A_FAIRE.md`** (à la racine du skill) : les chantiers en cours.
