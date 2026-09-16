# Bloc 3, travail en autonomie : la fiche de risque

**Construit** le 16 septembre 2026 : `stats_crypto/assignment/fiche_de_risque.ipynb`, généré par `build/build_a3.py`, solutions dans `build/sol_a3.json`.

Données : `crypto.csv`, déjà connu. Aucun nouveau fichier.

---

## 1. Ce que c'est, et ce que ce n'est pas

**Ce n'est pas un travail noté.** Pas de barème, pas de points, pas de rendu. C'est du travail en autonomie : l'étudiant vérifie seul qu'il sait faire ce que les séances 5 et 6 ont montré, et repart avec un document présentable.

Conséquence sur l'écriture : **tout doit pouvoir se faire sans l'enseignant à côté.** Chaque étape dit ce qu'on cherche, pourquoi, et où c'était dans le cours. Elle ne donne jamais la ligne à écrire. Les cellules `verifier` remplacent la correction : un `A REVOIR` porte un indice, pas une sanction.

> Les deux travaux précédents (`simulateur_pret`, `investissement_programme`) sont encore écrits comme des devoirs notés, avec barème. À reprendre dans le même esprit.

## 2. L'idée

**Nous codons la présentation, ils codent le contenu.**

Une fonction `afficher_fiche(...)` est fournie. Elle dessine une fiche de risque en quatre étages :

1. un **bandeau** avec le nom de la monnaie et la période couverte ;
2. le **cours au fil du temps**, en grand ;
3. les **cinq indicateurs** en tuiles : rendement moyen, rendement médian, volatilité, VaR 95 %, part de jours de hausse ;
4. en bas, la **distribution des rendements** avec la VaR et le pire jour marqués, et le **classement de volatilité** des sept monnaies, celle de l'étudiant en rouge.

**Tout argument omis affiche « à compléter »** — les tuiles comme les panneaux graphiques, qui prennent un cadre gris au lieu d'axes vides.

**Le ressort.** La fonction est appelée dès le début, avec le seul nom de la monnaie. La fiche apparaît **entièrement vide**, et le notebook dit : voilà ce que vous allez remplir. Chaque étape en remplit une partie. Le résultat est visible dès la première minute, et il se construit sous leurs yeux.

La fonction vit dans `prototypes/fiche_risque.py` ; `build_a3.py` la lit et l'inline dans le notebook, pour qu'il n'y ait qu'une source.

## 3. Le déroulé

**Décor.** Setup, la fonction fournie — « longue, et vous n'avez pas à la lire ». Choix de `MONNAIE`, chargement, premier appel : la fiche vide.

**Étape 1 — la table et la colonne de rendement.** Les deux pièges de la séance 5 rappelés : le `groupby` obligatoire, et le `dropna`. On accepte les deux ordres possibles (filtrer puis calculer, ou l'inverse) en le disant. Puis `periode` et `prix` sont passés : **la courbe du cours apparaît.**

**Étape 2 — rendement moyen et médian.** Et la remarque qui compte : une moyenne positive avec une médiane négative n'est pas une erreur, c'est une information.

**Étape 3 — volatilité et VaR.** Avec un `verifier` qui attrape l'erreur classique, `quantile(0.95)` au lieu de `quantile(0.05)`. Et la consigne de **traduire la VaR en euros** sur 10 000 € — c'est la phrase qu'un comité attend, pas le pourcentage.

**Étape 4 — part de jours de hausse.** En pourcentage, avec un `verifier` qui attrape l'oubli du `* 100`. Puis **les cinq tuiles se remplissent**, et le notebook fait remarquer ce que la fonction a annualisé toute seule.

**Étape 5 — le pire jour et sa date.** C'est ici qu'on enseigne `idxmin` et `.loc`, les deux seules nouveautés du notebook, en trois cellules : `min` donne la valeur, `idxmin` donne la ligne, `.loc[ligne, colonne]` va lire la case. La paire `min`/`idxmin` et `max`/`idxmax` est énoncée.

**Étape 6 — le classement des sept.** Sur `crypto`, pas sur `t` — et le piège est signalé : `crypto` n'a pas encore de colonne `r`.

**La fiche complète.**

**Étape 7 — lire sa fiche.** Trois questions en texte : recommandez-vous la ligne et à quelle taille ; quel est le chiffre le moins fiable et pourquoi (le rendement moyen — la séance 6 a mesuré son épaisseur) ; qu'est-ce qui, dans cette fiche, a une chance de valoir pour demain (la volatilité persiste, le rendement moyen ne prédit rien — c'est la charnière vers le bloc ML).

**Pour finir — la petite application.** `fiche_de(code)` est fournie : ce sont leurs lignes, rassemblées. Ils la lisent et doivent tout reconnaître. Puis un champ de saisie `ipywidgets` avec bouton, qui appelle `fiche_de`. Une note dit que si le champ n'apparaît pas, `fiche_de("BTC")` marche de toute façon.

> `def` n'est pas au programme du bloc 1 : c'est pourquoi `fiche_de` est **fournie** et non demandée. Le bénéfice reste entier — ils voient leur propre travail généralisé.

## 4. Valeurs de référence

Recalculées et vérifiées sur `crypto.csv` le 16 septembre 2026. **Quatre VaR et une médiane de la version précédente de ce document étaient fausses** ; voici les bonnes.

| monnaie | jours | moyenne | médiane | volatilité | VaR 95 % | % hausse | pire jour | date |
|---|---|---|---|---|---|---|---|---|
| BTC | 3 164 | +0,11 | +0,06 | 3,33 | −5,02 | 51,0 | −37,17 | 2020-03-12 |
| ETH | 3 164 | +0,13 | +0,06 | 4,37 | −6,59 | 50,9 | −42,35 | 2020-03-12 |
| SOL | 2 334 | +0,39 | **−0,04** | 6,19 | −8,29 | 49,6 | −42,28 | 2022-11-09 |
| DOGE | 3 164 | +0,32 | +0,00 | 8,93 | −7,63 | **39,9** | −40,25 | 2021-01-30 |
| XRP | 3 164 | +0,12 | −0,10 | 5,38 | −6,85 | 48,6 | −42,33 | 2020-12-23 |
| BNB | 3 164 | +0,25 | +0,10 | 4,78 | −6,20 | 52,0 | −41,90 | 2020-03-12 |
| ADA | 3 164 | +0,10 | −0,11 | 5,39 | −7,81 | 48,5 | −39,39 | 2020-03-12 |

> **SOL est la monnaie par défaut du notebook.** Rendement moyen le plus élevé des sept (+0,39 %/jour, soit +314 % par an) et pourtant **médiane négative** : elle baisse plus d'un jour sur deux. L'écart entre moyenne et médiane, simple notion en séance 5, devient ici le cœur de l'avis à rendre. XRP et ADA donnent le même effet, DOGE en plus brutal.

Toutes les cellules `verifier` sont **relationnelles** : elles recalculent la valeur attendue sur la monnaie choisie plutôt que de comparer à une constante. Le notebook fonctionne donc pour les sept.

## 5. Vérifications passées

Exécuté de bout en bout avec `sol_a3.json` : 24 cellules de code, **15 `verifier` sur 15 au vert**, aucune erreur. Build idempotent, aucune sortie enregistrée, aucune cellule affichant un type numpy.

Le champ de saisie se construit sans erreur hors Colab, mais **son rendu dans Colab n'a pas été testé** — ça demande un vrai notebook. C'est la raison de la note de repli, et la raison pour laquelle il est en dernière position.

## 6. Ce qui reste ouvert

**L'attribution de la monnaie.** Le notebook laisse choisir, avec `SOL` par défaut. Si vous préférez attribuer, il suffit de changer une ligne et la consigne autour.

**La couleur de la tuile « rendement médian »**, rouge quand la valeur est négative — le cas de SOL, XRP et ADA. Je l'ai gardée : sur une fiche de risque, un rendement médian négatif *est* une alerte, et le contraste avec le rendement moyen vert est exactement ce qu'on veut faire voir. À dire si vous voulez du neutre.

**Le temps.** Sept étapes, six cellules à écrire, aucune longue. À vue de nez 45 min à 1h. À confirmer sur un vrai étudiant.
