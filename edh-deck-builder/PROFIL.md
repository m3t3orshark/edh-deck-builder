# Profil de l'utilisateur

Ce fichier contient les préférences personnelles de la personne qui utilise ce skill. C'est le **seul fichier qui change d'une personne à l'autre** : pour une autre personne, on garde tout le skill et on remplace ce fichier. Il se modifie avec le panneau de réglages (« règle mon profil », voir `modes/reglages.md`), ou à la main dans le bloc ci-dessous.

Lis-le au début de chaque séance. Ce que l'utilisateur précise dans sa demande prime toujours sur le profil.

```json
{
  "proprietaire": null,
  "langue": null,
  "ton": "tutoiement",
  "principes": {
    "pas_de_combo_infinie": false,
    "pas_de_verrou": false,
    "synergie_avant_puissance": true
  },
  "bracket_defaut": null,
  "puissance_defaut": null,
  "budget_defaut": null,
  "pistes_inhabituelles": "proposer",
  "base_de_mana": [
    "terrains"
  ],
  "collection": {
    "classeurs": [],
    "classeurs_partages": [],
    "ignorer_listes": true,
    "proxies_possedes": false
  },
  "prix": {
    "devise": "EUR",
    "reference": "prix de tendance Cardmarket",
    "seuil_mise_en_evidence": 30
  }
}
```

## Signification des réglages

- **proprietaire** : prénom de la personne. Le classeur à son nom contient ses cartes exclusives. `null` : profil vierge, le skill propose les réglages à la première utilisation.
- **langue** : `fr` ou `en`, langue des réponses, des notes de jeu et du panneau ; absente, `fr`. La personne qui rédige ses propres phrases dans l'autre langue reçoit sa réponse dans cette langue (les noms de cartes et les citations ne comptent pas).
- **ton** : `tutoiement` ou `vouvoiement`, dans tous les modes (en français seulement ; sans effet en anglais).
- **principes** :
  - `pas_de_combo_infinie` : aucune boucle infinie (mana, jetons, dégâts, pioche, tours), quel que soit le bracket. Si une carte forte seule ouvre une combo avec une autre carte du deck, retire l'une des deux. Désactivé : suivre seulement les règles officielles du bracket.
  - `pas_de_verrou` : aucun verrou qui empêche les adversaires de jouer (une situation dont ils ne peuvent plus sortir par le jeu normal, qui oblige à concéder ou à faire match nul ; voir la définition dans SKILL.md). Le contrôle lourd que les adversaires peuvent casser n'en est pas un, mais se signale, quel que soit le bracket. Désactivé : suivre seulement les règles officielles du bracket.
  - `synergie_avant_puissance` : un thème principal, au plus un axe secondaire ; une carte qui ne sert ni le thème ni les fondamentaux n'a rien à faire là.
- **bracket_defaut**, **puissance_defaut** : appliqués quand la demande ne les précise pas, sans poser la question, en l'annonçant en une ligne (« bracket 2 : ton réglage par défaut »). `null` pour le bracket : le demander ; La puissance par défaut est une **tranche** : `detendu` (1-3), `equilibre` (4-7) ou `affute` (8-10) ; `null` : pas de cible, la puissance est seulement estimée et indiquée. Échelle : `reference/puissance.md`.
- **budget_defaut** : dans la devise du profil (`prix.devise`), total du deck ; `null` = pas de budget. C'est un **plafond, jamais un objectif** : le deck coûte ce que demandent son thème et la puissance visée, dans cette limite ; n'ajoute jamais une carte chère pour se rapprocher du montant. Un plafond élevé ne se discute pas : il revient à laisser le prix guider très peu les choix.
- **pistes_inhabituelles** : `ne_pas_proposer`, `proposer` (au moins une piste inhabituelle parmi les stratégies, jamais imposée) ou `mettre_en_avant`.
- **base_de_mana** : ce que comprend « la base de mana » quand l'utilisateur demande de ne toucher qu'à elle (`--mana-base` du script de comparaison). Le script lit lui-même cette définition et l'affiche (« Base de mana retenue : … »).
- **collection** : classeurs ManaBox comptés par défaut ; les classeurs partagés peuvent être utilisés par d'autres personnes ; `ignorer_listes` exclut les listes ManaBox (listes d'envies) ; `proxies_possedes` : `false` (un proxy n'est pas un exemplaire possédé ; une carte présente seulement en proxy compte parmi les cartes manquantes, signalée comme carte en test) ou `true` (les proxies comptent comme possédés, selon l'usage de son groupe de jeu).
- **prix** : devise (`EUR`, prix de tendance Cardmarket, ou `USD`, prix de marché TCGplayer : les deux que fournit Scryfall ; la référence suit la devise), et seuil au-delà duquel une carte est signalée (informatif). Les scripts de prix lisent la devise eux-mêmes.
