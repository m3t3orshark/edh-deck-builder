# Format de la liste (import deckstats, ManaBox, Moxfield et Archidekt)

La liste se colle dans l'import **« Paste your decklist »** de deckstats (format EDH / Commander). Ce format a été testé et validé par l'utilisateur : commandant reconnu automatiquement (badge CMD), 100 cartes dans le deck, sideboard séparé, tri automatique par type. **C'est le seul chemin d'import qui fonctionne avec ce format** : l'autre fenêtre d'ajout de deck de deckstats refuse les titres `Commander` et `Sideboard` et donne 103 cartes sans commandant. Le rappel d'import (rappel d'import de la réponse) le précise toujours.

```
1 Sol Ring
1 Arcane Signet
1 Counterspell
...
1 Command Tower
5 Island
5 Swamp

Sideboard
1 Maze of Ith
1 Mind Stone

Commander
1 Nathan Drake, Treasure Hunter
```

Règles, toutes vérifiées sur deckstats par l'utilisateur. Ne les modifie pas sur la foi d'une source externe sans nouveau test de sa part :

- **Cet import ne reconnaît que deux titres : `Commander` et `Sideboard`**, écrits seuls sur leur ligne, sans `//`. Tout autre titre (catégories par rôle, types de cartes, `Maybeboard`, ou n'importe quel titre précédé de `//`) est ignoré ou rejeté comme carte introuvable, et les cartes qui suivent restent dans la dernière section reconnue. N'en ajoute donc aucun autre.
- **Les 99 cartes du deck viennent en premier, sans titre.** Ordre conseillé pour la relecture : sorts par rôle (ramp, pioche, removal, wipes, protection, thème, finishers), puis terrains non basiques, puis terrains de base. Deckstats trie de toute façon par type et par valeur de mana ; la répartition par rôle se donne dans la réponse (voir la réponse de proposition).
- **Le maybeboard va sous `Sideboard`**, puisque l'import n'a pas de titre maybeboard : l'utilisateur déplace ces cartes vers le maybeboard après l'import. S'il n'y a pas de maybeboard, omets la section.
- **`Commander` vient toujours en dernier**, avec le commandant seul en dessous (et son partenaire ou *background* s'il y en a un). Placé en tête, ce titre fait passer tout le deck en commandant.
- **Aucun marqueur sur la ligne du commandant** : `#!Commander` et `# !Commander` ont été testés, la ligne est rejetée comme carte introuvable.
- Le total hors sideboard, commandant compris, fait exactement 100.

**Le maybeboard** (facultatif, hors des 100 cartes) se propose seulement dans deux cas :
- une carte coûteuse du deck mérite une alternative moins chère ;
- un rôle a beaucoup de bonnes options et le choix tient à un goût ou à un méta.

Sélectionne alors uniquement les meilleures, 8 cartes au maximum. Un maybeboard trop long ne l'aide pas à choisir, il le renvoie au travail de tri qu'il voulait éviter.

**Moxfield** (testé le 02/11 avec deux listes : un commandant et un sideboard ; deux partenaires, cartes à deux faces de tous types, carte scindée, terrains de base en plusieurs exemplaires) : le **même bloc** s'importe tel quel par l'import de texte d'un deck Commander. Le ou les commandants vont dans la zone Commander, les 99 (ou 98) cartes dans le deck, le `Sideboard` dans le sideboard ; aucune erreur. Moxfield choisit lui-même l'impression de chaque carte quand la liste n'en précise pas : il peut retenir une impression à **nom alternatif** (par exemple Tymna the Weaver affichée « Cecil Harvey », impression Final Fantasy). C'est la même carte ; l'utilisateur change l'impression dans Moxfield s'il préfère un autre visuel. Ne précise pas d'édition pour l'éviter.

**Archidekt** (testé le 02/11 avec les deux mêmes listes) : le **même bloc** s'importe tel quel. Commandant ou partenaires dans la zone Commander, 99 (ou 98) cartes dans le deck, `Sideboard` dans sa catégorie, cartes à deux faces reconnues ; aucune erreur, noms habituels des cartes. Archidekt range lui-même les cartes dans ses propres catégories de rôle (Draw, Removal…), que l'utilisateur peut réorganiser : ce ne sont pas celles du skill.

**Les lignes de carte** : quantité, espace, nom anglais exact (celui de Scryfall). Les cartes doubles s'écrivent avec les deux faces : `1 Brazen Borrower // Petty Theft`. Par défaut, n'indique pas l'édition. Deckstats accepte aussi `1 Sol Ring (SLD) 2683` (code d'édition, puis numéro de collection), mais ne l'utilise que si l'utilisateur le demande, et récupère alors le code et le numéro réels sur Scryfall : une impression inventée ferait échouer l'import de la carte.
