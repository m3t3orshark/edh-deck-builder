# Les notes de jeu (après validation)

Quand l'utilisateur valide la liste (il dit qu'elle lui convient, ou qu'il l'a importée et n'a plus de changement à faire), livre les notes du deck, prêtes à coller dans la fenêtre **Deck Notes** de deckstats. Si la liste change entre-temps, les notes portent sur la version finale. Ne les livre pas avant la validation : elles seraient à refaire au moindre changement.

**Le format** : un seul bloc de code, en Markdown, que l'utilisateur copie tel quel. La fenêtre accepte le Markdown et les liens de carte `[[Nom de la carte]]` (nom anglais exact) : mets chaque carte citée sous cette forme, elle devient survolable dans deckstats. Titres en `##` ou en gras, listes à puces courtes. Vise 300 à 500 mots : ce sont des notes à relire avant une partie, pas un primer.

**Le contenu**, dans cet ordre (omets une rubrique qui n'a rien d'utile à dire) :

1. **Plan de jeu** : la stratégie en 3 ou 4 phrases, comment le deck gagne.
2. **Main de départ** : ce qu'on garde, ce qu'on mulligan, les cartes idéales au tour 1-3.
3. **Déroulé d'une partie** : début, milieu et fin de partie, avec les priorités de chaque phase (quand poser le commandant, quand garder l'interaction, quand basculer vers les finishers).
4. **Synergies clés** : les 4 à 6 interactions qui font gagner, une ligne chacune.
5. **Points de règles et pièges** : les interactions faciles à rater ou à mal jouer (ordre des déclencheurs, cible bloquée par un linceul ou une défense talismanique, timing d'activation…).
6. **Combos à ne pas compléter** : reprends la liste des combos à une carte près donnée par `find_combos.py` et nomme les cartes à ne pas ajouter, regroupées par carte du deck concernée, pour respecter le principe `pas_de_combo_infinie` du profil (ou par simple prudence s'il est désactivé).
7. **Pistes d'évolution** : les cartes du maybeboard et ce qu'elles remplaceraient, en une ligne chacune.

Vérifie que chaque nom de carte entre `[[ ]]` est exactement celui de la liste : un nom mal écrit casse le lien.
