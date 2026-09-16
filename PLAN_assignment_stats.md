# Bloc 3, travail en autonomie : la fiche d'analyse

**Construit** le 16 septembre 2026 : `stats_crypto/assignment/fiche_analyse.ipynb`, généré par `build/build_a3.py`, solutions dans `build/sol_a3.json`. Un seul exercice pour les deux séances, en deux volets.

Données : `crypto.csv`, déjà connu. Aucun nouveau fichier.

---

## 1. Ce que c'est, et ce que ce n'est pas

**Ce n'est pas un travail noté.** Pas de barème, pas de points, pas de rendu. C'est du travail en autonomie : l'étudiant vérifie seul qu'il sait faire ce que les séances 5 et 6 ont montré, et repart avec un document présentable.

Conséquence sur l'écriture : **tout doit pouvoir se faire sans l'enseignant à côté.** Chaque étape dit ce qu'on cherche, pourquoi, et où c'était dans le cours. Elle ne donne jamais la ligne à écrire. Les cellules `verifier` remplacent la correction : un `A REVOIR` porte un indice, pas une sanction.

> **Fait le 16 septembre 2026** : les deux travaux précédents (`simulateur_pret`, `investissement_programme`) sont convertis dans le même esprit — plus de barème, plus de points par partie, plus de rendu ni de nom à inscrire. Le README suit.

## 2. L'idée

**Nous codons la présentation, ils codent le contenu.**

Une fonction `afficher_fiche(...)` est fournie. Elle dessine une fiche en deux volets.

**Premier volet — le risque** (séance 5), en quatre étages :

1. un **bandeau** avec le nom de la monnaie et la période couverte ;
2. le **cours au fil du temps**, en grand ;
3. les **cinq indicateurs** en tuiles : rendement moyen, rendement médian, volatilité, VaR 95 %, part de jours de hausse ;
4. en bas, la **distribution des rendements** avec la VaR et le pire jour marqués, et le **classement de volatilité** des sept monnaies, celle de l'étudiant en rouge.

**Tout argument omis affiche « à compléter »** — les tuiles comme les panneaux graphiques, qui prennent un cadre gris au lieu d'axes vides.

**Le ressort.** La fonction est appelée dès le début, avec le seul nom de la monnaie. La fiche apparaît **entièrement vide**, et le notebook dit : voilà ce que vous allez remplir. Chaque étape en remplit une partie. Le résultat est visible dès la première minute, et il se construit sous leurs yeux.

La fonction vit dans `prototypes/fiche_risque.py` ; `build_a3.py` la lit et l'inline dans le notebook, pour qu'il n'y ait qu'une source.

## 3. Le déroulé

**Décor.** Setup, la fonction fournie — « longue, et vous n'avez pas à la lire ». Choix de `MONNAIE`, chargement, premier appel : la fiche entièrement vide, deux volets gris.

### Premier volet — le risque

**Étape 1, la table et la colonne `r`.** Les deux pièges de la séance 5 rappelés. Puis `periode` et `prix` passés : la courbe du cours apparaît.

**Étape 2, les quatre indicateurs.** Moyenne, médiane, volatilité, VaR — en un tableau qui dit pour chacun ce qu'il mesure. Un `verifier` attrape `quantile(0.95)` au lieu de `0.05`. La consigne demande de traduire la VaR en euros.

**Étape 3, la forme des journées et le pire jour.** C'est ici qu'on enseigne `idxmin` et `.loc`, en trois cellules. La paire `min`/`idxmin` est énoncée. `part_hausse` a un `verifier` qui attrape l'oubli du `* 100`.

**Étape 4, le classement des sept.** Le premier volet est complet.

### Second volet — l'idée de stratégie

Amené par la citation du forum : *« le cours rebondit après une grosse baisse, il suffit d'acheter le lendemain »*. L'étudiant a noté son intuition en tête de notebook.

**Étape 5, `r_hier` et les deux paquets.** `shift` appliqué au rendement, par monnaie. Deux paquets complémentaires, vérifiés comme tels. Les moyennes tombent : le lendemain rapporte plusieurs fois une journée ordinaire. Le verdict reste « EN ATTENTE ».

**Étape 6, l'épaisseur.** Bootstrap de **l'écart entre les deux paquets**, pas de la seule moyenne du premier — sinon l'intervalle et le test t répondent à deux questions différentes et se contredisent. Deux tirages par tour, une différence rangée.

**Étape 7, le test t.** Le verdict tombe.

**Étape 8, la grille.** 28 tests fournis, 7 passent là où le hasard en prédit 1,4.

**Étape 9, la seule preuve.** ADA passe aux quatre seuils. On coupe son histoire en deux : p = 0,003 sur la première moitié, **p = 0,047 sur la seconde, jamais consultée**. L'effet tient. Le bitcoin, lui, donne 0,221 puis 0,834. C'est la charnière vers le bloc ML.

**Pour finir.** `fiche_de(code)` fournie — leurs lignes rassemblées — puis le champ de saisie `ipywidgets`.

## 4. Deux choix à connaître

**Le bootstrap porte sur l'écart.** Première version : bootstrap de la seule moyenne du paquet « après baisse ». Sur SOL, l'intervalle excluait zéro (verdict « effet détecté ») alors que p = 0,20. Les deux répondaient à des questions différentes — « le gain diffère-t-il de zéro » contre « diffère-t-il des autres jours ». Corrigé : le bootstrap porte sur la différence, et les deux méthodes s'accordent sur six monnaies sur sept.

**La septième est `DOGE`**, où l'intervalle exclut zéro mais p = 0,099. Ce n'est pas un bug : le test t suppose que les moyennes se comportent normalement, et le +354 % de janvier 2021 casse cette supposition. Le notebook le dit explicitement, en encadré — c'est l'intervalle qu'il faut croire, et la divergence est elle-même un signal. C'est une bonne leçon, pas un défaut.

## 5. Valeurs de référence

Recalculées et vérifiées sur `crypto.csv` le 16 septembre 2026.

| monnaie | jours | moyenne | médiane | volatilité | VaR 95 % | % hausse | pire jour | date |
|---|---|---|---|---|---|---|---|---|
| BTC | 3 164 | +0,11 | +0,06 | 3,33 | −5,02 | 51,0 | −37,17 | 2020-03-12 |
| ETH | 3 164 | +0,13 | +0,06 | 4,37 | −6,59 | 50,9 | −42,35 | 2020-03-12 |
| SOL | 2 334 | +0,39 | **−0,04** | 6,19 | −8,29 | 49,6 | −42,28 | 2022-11-09 |
| DOGE | 3 164 | +0,32 | +0,00 | 8,93 | −7,63 | **39,9** | −40,25 | 2021-01-30 |
| XRP | 3 164 | +0,12 | −0,10 | 5,38 | −6,85 | 48,6 | −42,33 | 2020-12-23 |
| BNB | 3 164 | +0,25 | +0,10 | 4,78 | −6,20 | 52,0 | −41,90 | 2020-03-12 |
| ADA | 3 164 | +0,10 | −0,11 | 5,39 | −7,81 | 48,5 | −39,39 | 2020-03-12 |

**Le rebond, seuil −5 %** — intervalle de l'écart et p-value :

| monnaie | occasions | écart mesuré | intervalle | p | verdict |
|---|---|---|---|---|---|
| BTC | 166 | +0,44 | [−0,26 ; +1,24] | 0,242 | on ne peut pas conclure |
| SOL | 298 | +0,63 | [−0,33 ; +1,57] | 0,203 | on ne peut pas conclure |
| DOGE | 339 | +1,87 | [+0,20 ; +4,35] | 0,099 | *les deux méthodes divergent* |
| ADA | 365 | **+1,24** | **[+0,56 ; +1,86]** | **0,000** | effet détecté |

**Hors échantillon, ADA** — première moitié p = 0,003, seconde moitié p = 0,047. **BTC** — 0,221 puis 0,834.

Toutes les cellules `verifier` sont **relationnelles** : elles recalculent l'attendu sur la monnaie choisie. Le notebook fonctionne pour les sept.

## 6. Vérifications passées

Exécuté de bout en bout avec `sol_a3.json` : 33 cellules de code, **26 `verifier` sur 26 au vert**, aucune erreur. Build idempotent, aucune sortie enregistrée, aucune cellule affichant un type numpy.

Le champ de saisie se construit sans erreur hors Colab, mais **son rendu dans Colab n'a pas été testé**. D'où la note de repli et sa position en dernier.

## 7. Ce qui reste ouvert

**Le temps.** Huit cellules à écrire, dont deux longues (les quatre indicateurs, les deux paquets) et une lente (le bootstrap). J'estime **60 à 75 minutes**, donc au-dessus des 30-45 min visées au départ — mais c'est le prix de la fusion des deux séances. Si c'est trop, l'étape 4 (le classement) et l'étape 3 (la part de hausse) sont les plus faciles à fournir.

**L'attribution de la monnaie.** Libre, `SOL` par défaut. Noter que le verdict du second volet **dépend de la monnaie choisie** : quatre donnent « on ne peut pas conclure », ADA donne « effet détecté », DOGE fait diverger les deux méthodes. C'est une richesse, mais ça veut dire que tous les étudiants n'auront pas la même conclusion — à annoncer en classe.

**La couleur de la tuile « rendement médian »**, rouge quand la valeur est négative. Gardée : sur une fiche de risque, c'est bien une alerte.

**`//` dans l'étape 9.** La division entière a été écartée du programme Python ; je l'emploie en l'expliquant en une incise. Dites-moi si vous préférez que la ligne de découpage soit fournie.
