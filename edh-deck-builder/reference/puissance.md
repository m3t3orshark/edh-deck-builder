# Niveau de puissance sur 10

Le **bracket** dit ce que le deck a le droit de contenir (règles vérifiables). La **puissance** dit sa force à l'intérieur de sa catégorie. On les donne ensemble : « bracket 2, puissance 6/10 ». L'ancienne échelle sur 10 de la communauté a été abandonnée parce qu'elle était subjective ; ici, la note repose sur des critères nommés et contestables.

## Méthode

1. Lance `python scripts/power_level.py <fichier>`. Il note cinq critères mesurables sur 10, à partir du texte des cartes, et affiche les cartes comptées dans chaque catégorie.
2. Évalue toi-même le sixième critère, les **conditions de victoire** : en combien de tours réalistes et avec quelle fiabilité le deck gagne (menaces, finishers, pression), sur 10.
3. **Note finale** = moyenne des six critères, arrondie à l'entier. Deux corrections sont possibles quand les heuristiques ratent quelque chose d'évident, par exemple un commandant qui produit lui-même l'avantage de cartes (Nathan Drake lance les cartes des adversaires, ce que le critère de régularité ne compte pas) : **corriger le critère concerné**, ou **ajuster la note finale d'un point au plus**. **Une même raison ne justifie qu'une seule correction, jamais les deux** : si tu as relevé la régularité pour l'avantage de cartes du vol, tu ne rajoutes pas un point à la note finale pour la même raison. Justifie chaque correction en une phrase.
4. Présente la note ainsi : « Puissance estimée : 6/10, équilibré (vitesse 6, régularité 3, interaction 8, résilience 4, base de mana 8, victoire 6) », puis une ligne sur ce qui la tire vers le haut et vers le bas.

**Deux commandants** : ce sont deux cartes toujours accessibles. Si le second commandant apporte un moteur (pioche, ramp), tiens-en compte dans le critère concerné, avec la règle habituelle d'une seule correction.

## Les six critères

| Critère | Ce qui compte | Mesure |
| --- | --- | --- |
| Vitesse | Valeur de mana moyenne, ramp, mana rapide (coût 1 ou moins) | Script |
| Régularité | Moteurs de pioche et pioches multiples ; pioches simples et sélections du type Fact or Fiction pour moitié ; tuteurs | Script |
| Interaction | Removal ciblé et contresorts ; pénalité sans board wipe | Script |
| Résilience | Récursion depuis le cimetière, protection | Script |
| Base de mana | Terrains qui arrivent engagés (ceux qui le font sous condition comptent pour un quart) | Script |
| Conditions de victoire | Rapidité et fiabilité pour conclure | Jugement |

Les détections sont des heuristiques sur le texte Oracle : elles se trompent parfois (une carte qui pioche une fois de temps en temps, un removal qui ne vise que ses propres créatures). Le détail des cartes comptées permet de corriger. Si une catégorie est manifestement fausse, dis-le et corrige la note de ce critère.

## Les tranches

Une cible de puissance (demande ou `puissance_defaut` du profil) s'exprime en **tranche**, pas en note précise : viser « 6 plutôt que 5 » serait une précision illusoire. La note estimée reste à l'unité, pour mesurer ce qu'une révision apporte.

| Tranche | Notes | Correspond surtout à |
| --- | --- | --- |
| Détendu | 1-3 | Bracket 1, decks à thème |
| Équilibré | 4-7 | Bracket 2, du precon au deck bien amélioré |
| Affûté | 8-10 | Brackets 3 et 4, decks optimisés |

Présente toujours la note avec sa tranche : « puissance estimée 6/10 (équilibré) ». Une tranche visée incompatible avec le bracket (affûté en bracket 2) se signale : le bracket prime, et propose soit d'abaisser la tranche, soit de monter le bracket.

## Repères par bracket (indicatifs)

| Puissance | Description | Brackets habituels |
| --- | --- | --- |
| 1-2 | Deck à thème, très lent, peu d'interaction | 1 |
| 3-4 | Niveau d'un precon non modifié | 1-2 |
| 5-6 | Precon bien amélioré, deck cohérent et régulier | 2-3 |
| 7-8 | Deck optimisé, rapide, interaction efficace | 3-4 |
| 9-10 | Proche du compétitif | 4-5 |

Calibrage (01/11/2026), moyenne des cinq critères mesurés : precon d'Ashling non modifié 4,1 ; même precon avec base de mana refaite 5,2 ; Atraxa stun construite avec une collection 5,4 ; Nathan Drake, liste du 30/10 (celle des tests de référence, `nathan_drake_deckstats.txt`) 6,1 ; Nathan Drake, autre liste construite le 31/10 (avec les dual lands, environ 1 000 €) 7,1. Le script ne voit que la pioche écrite noir sur blanc : toute autre source d'avantage de cartes (vol des cartes adverses, exil puis jeu du dessus de sa bibliothèque, moteur propre au commandant, jetons qui se transforment en cartes, recyclage…) se juge à part, avec une seule correction, quel que soit le deck. Ne confonds pas ces deux listes de Nathan.

## Usages

- **En création** : si une tranche de puissance est visée (demande ou `puissance_defaut` du profil), construis pour y entrer, puis annonce l'écart éventuel dans la ligne de contrôle. Une puissance visée au-delà de ce que permet le bracket se signale : le bracket prime.
- **En analyse** : note **avant et après** les échanges (« puissance 4 → 6 »). Pour monter ou descendre en puissance sans changer de bracket, cible les critères les plus faibles ou les plus forts.
