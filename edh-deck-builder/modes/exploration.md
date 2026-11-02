# Mode exploration des synergies

L'utilisateur donne un commandant et veut **toutes** les cartes qui servent ses mécaniques, classées par axe de synergie. Contrairement à EDHREC, qui reflète les decks les plus joués, la sélection ne dépend pas de la popularité : une carte rarement jouée peut avoir toute sa place dans la mécanique du deck, et ce sont souvent ces cartes que l'utilisateur cherche.

1. **Les réglages** : identité couleur (celle du commandant), et bracket seulement s'il le précise (en bracket 1-2, les Game Changers sont exclus ; sinon ils sont listés et marqués). Pas d'autre question.
2. **Lis le texte du commandant** avec `card_texts.py`, puis choisis **6 à 8 axes de synergie au plus** dans un premier temps : les plus directement liés au texte du commandant, plus un ou deux axes inhabituels (selon `pistes_inhabituelles` du profil, voir `modes/creation.md`, étape 2), en priorité ceux que l'utilisateur a nommés. Pour Atraxa, Praetors' Voice : prolifération, multiplicateurs de marqueurs, +1/+1, planeswalkers, poison, et les marqueurs stun s'il les demande. Les autres axes possibles (charge, rad, sagas, énergie…) se citent en une ligne à la fin, à explorer sur demande. **Évite les axes fourre-tout** : un axe qui ramène des centaines de cartes (« tout ce qui pose un marqueur +1/+1 ») ne sert à rien ; resserre la requête sur ce qui interagit vraiment avec le commandant (par exemple les cartes qui *profitent* des marqueurs, ou qui en posent beaucoup à bas coût), et vise moins de 150 cartes par axe. **Le script signale tout axe de plus de 150 cartes : ne livre pas tant qu'il en reste un**, resserre sa requête et relance.

   Exemple pour Atraxa, Praetors' Voice (requêtes mesurées le 01/11 en WUBG, bracket 2) : les deux axes larges se resserrent ainsi.
   ```
   Payoffs +1/+1 :: o:/creatures? you control with (a |one or more )?\+1\/\+1 counters?/
   Payoffs +1/+1 :: o:/for each \+1\/\+1 counter on/
   Planeswalkers :: o:/planeswalkers? you control/ -o:/you or (a|one or more|another) planeswalkers? you control/ -o:/you or planeswalkers you control/ -t:planeswalker
   Planeswalkers :: o:"loyalty counter" -t:planeswalker
   Planeswalkers :: t:planeswalker o:/(other|each) planeswalkers?/
   Planeswalkers :: t:planeswalker cmc<=3
   ```
   Résultat : 100 cartes de payoffs (au lieu de 201) et 127 pour les planeswalkers (au lieu de 188). Le principe se transpose à d'autres commandants : une carte qui *arrive* avec des marqueurs n'est pas un payoff, il faut celles qui *comptent* les marqueurs de tes créatures ; un axe de cartes d'un type (tous les planeswalkers) se remplace par ce qui les soutient, plus les moins chers ; les effets « toi ou un planeswalker que tu contrôles » (défense contre les attaques) sont du bruit.
3. **Traduis chaque axe en une ou plusieurs requêtes Scryfall** précises, dans un fichier d'axes (une ligne « Nom de l'axe :: requête »). Plusieurs requêtes peuvent porter le même axe. Vise l'exhaustivité : mieux vaut deux requêtes qui couvrent les formulations différentes d'une même mécanique qu'une seule trop étroite.
4. **Lance le script** :
   `python scripts/synergy_search.py --identity <couleurs> --axes axes.txt --out synergies.md [--bracket N] --commander "<nom>"`
   Il produit la liste complète, axe par axe, triée par valeur de mana, avec pour chaque carte son coût, son type, son texte, son prix et sa popularité (rang EDHREC fourni par Scryfall) : « peu jouée » au-delà du rang 10 000, « jamais classée » si elle n'a pas de rang. La popularité est affichée, jamais utilisée pour filtrer.
5. **Livre la liste complète dans un fichier**, jamais tronquée, et garde la réponse **courte, l'équivalent d'un écran environ** : le fichier est là pour le détail. Dans la réponse :
   - les axes trouvés, avec le nombre de cartes de chacun ;
   - pour chaque axe, **3 pépites peu jouées** au plus, chacune justifiée en une ligne par son texte ;
   - les **faux amis** principaux, en une liste courte, que la recherche de texte ramène et qu'il faut écarter ou manier avec prudence (par exemple, une créature qui arrive avec des marqueurs stun *sur elle-même* sert peu un deck qui en pose sur les adversaires) ;
   - les **risques au regard des principes du profil** : une combinaison de cartes qui ouvrirait une combo infinie ou un verrou au sens de SKILL.md (vérifie au besoin avec `find_combos.py` sur un petit fichier des cartes concernées) ; le contrôle lourd que les adversaires peuvent casser n'est pas un verrou : signale-le avec ce qui permet d'en sortir.

   **Toute carte citée dans la réponse** (pépite, faux ami, exemple d'un risque) **a son texte vérifié** (`card_texts.py` : le texte du fichier produit est tronqué) et est décrite exactement : une carte qui ne vise qu'une créature par adversaire n'est pas un effet de masse, une aura sur une créature n'est pas un stun, un bonus soumis à une condition (une capacité à activer d'abord) se dit avec sa condition.
6. **Propose la suite** en une phrase : approfondir un axe ou en explorer d'autres, construire un deck à partir d'un ou deux de ces axes (`modes/creation.md`, le thème étant alors choisi), ou croiser la liste avec sa collection ManaBox (`collection.py pool` sur la même identité).
