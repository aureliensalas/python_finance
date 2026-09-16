# Travail noté du bloc 3 : la fiche de risque

Première version, à corriger. Même format que les deux autres travaux notés : mise en situation, parties numérotées, `verifier` relationnels, points d'étape, barème sur 20.

Données : `crypto.csv`, déjà connu. Aucun nouveau fichier.

---

## 1. L'idée

**Nous codons la présentation, ils codent le contenu.**

Le notebook fournit une fonction `afficher_fiche(...)` qui dessine une **fiche de risque** professionnelle : un bandeau avec le nom de la monnaie et la période, cinq tuiles d'indicateurs, la distribution des rendements avec la VaR et le pire jour marqués dessus, et un classement de volatilité où leur monnaie est mise en évidence.

Cette fonction est fournie, jamais à écrire, jamais à modifier. Elle prend **des arguments nommés**, un par indicateur. L'étudiant calcule les indicateurs ; la fiche les affiche.

**Le ressort pédagogique.** La fonction s'appelle dès la partie 1, alors qu'aucun indicateur n'est calculé. La fiche apparaît **vide** : bandeau correct, et cinq tuiles grises marquées « à compléter ». À chaque partie, l'étudiant rappelle la même cellule et **une tuile de plus s'allume**. À la fin, la fiche est complète et elle est belle.

C'est le contraire d'un devoir où l'on écrit vingt cellules avant de voir quoi que ce soit. Ici le résultat est visible dès la première minute, incomplet, et chaque calcul le remplit un peu. La motivation est dans la boucle de retour, pas dans la note.

> **Un prototype existe et tourne** sur `crypto.csv`. Il produit exactement la fiche décrite ci-dessus. Il reste à polir (voir section 6).

---

## 2. La mise en situation

> Vous êtes analyste risque dans une société de gestion. Le comité d'investissement envisage d'ouvrir une ligne sur une cryptomonnaie. Avant toute décision, il demande une **fiche de risque** : une page, cinq chiffres, deux graphiques, et un avis écrit.
>
> C'est le document standard que produit un desk risque avant d'autoriser une exposition. Vous allez le construire, puis conclure.

La monnaie est **attribuée**, pas choisie : une variable en tête de notebook. Deux avantages — la correction est automatisable, et les étudiants ne convergent pas tous sur BTC. On peut la tirer du nom de l'étudiant, ou la fixer par groupe.

---

## 3. Les parties

**Partie 0, fournie.** Setup, chargement, `afficher_fiche`, et la variable `MONNAIE`.

**Partie 1 — la table et la colonne (3 points).**
Construire `t`, la table de la monnaie attribuée, avec la colonne de rendement. C'est le geste de la séance 5, `groupby` compris, et le `verifier` vérifie que le maximum n'est pas aberrant — le piège des 933 041 % est rappelé en une ligne.
Puis premier appel d'`afficher_fiche` : **la fiche vide**. Point d'étape : « voilà ce que vous allez remplir ».

**Partie 2 — les trois indicateurs de tendance (4 points).**
`rendement_moyen`, `rendement_median`, et leur interprétation croisée. La consigne demande une phrase : lequel des deux décrit une journée ordinaire, lequel décrit le portefeuille sur la durée, et ce que leur écart raconte sur cette monnaie.
Deuxième appel : deux tuiles s'allument.

**Partie 3 — les deux indicateurs de risque (4 points).**
`volatilite` (l'écart-type) et `var_95` (le quantile 5 %). La consigne fait dire à l'étudiant ce que la VaR signifie **en euros**, sur une position de 10 000 €, et à quelle fréquence.
Troisième appel : quatre tuiles.

**Partie 4 — la part de jours de hausse et les extrêmes (3 points).**
`part_hausse`, `pire_jour`, et `date_pire` — cette dernière demande un `idxmin`, présenté comme nouveauté sur place, ou un `sort_values().head(1)` avec ce qu'ils savent déjà. *(À trancher : voir section 6.)*
Quatrième appel : la fiche est complète.

**Partie 5 — situer la monnaie (3 points).**
Le `groupby` sur les sept monnaies pour produire `classement`, la Series de volatilités triée, qui alimente le graphique de droite. L'étudiant écrit où se situe sa monnaie et ce que ça implique.

**Partie 6 — l'avis du comité (3 points).**
Trois questions en texte, et c'est la partie qui vaut le plus cher au regard de l'effort :
1. Sur la base de ces chiffres, recommandez-vous d'ouvrir la ligne ? À quelle taille ?
2. Quel est le chiffre **le moins fiable** de votre fiche, et pourquoi ? *(Réponse attendue : le rendement moyen — la séance 6 a montré que son intervalle va de +1 % à +126 % par an sur BTC.)*
3. Votre fiche décrit le passé. Qu'est-ce qui, dedans, a une chance de valoir pour demain — et qu'est-ce qui n'en a aucune ? *(La volatilité persiste, le rendement moyen ne prédit rien. C'est la charnière vers le bloc ML.)*

**Bonus, hors barème.** La même fiche pour une seconde monnaie, et deux lignes de comparaison. Un seul appel de plus, puisque tout est déjà écrit — et ça fait sentir ce qu'est une fonction réutilisable.

| Partie | Points |
|---|---|
| 1. La table et la colonne | 3 |
| 2. Tendance | 4 |
| 3. Risque | 4 |
| 4. Fréquence et extrêmes | 3 |
| 5. Situer la monnaie | 3 |
| 6. L'avis du comité | 3 |

---

## 4. La fonction fournie

Signature, à arguments nommés pour que l'appel se lise comme un formulaire :

```python
afficher_fiche(
    nom=MONNAIE,
    periode=...,              # texte, fourni en partie 1
    rendement_moyen=...,      # % par jour
    rendement_median=...,     # % par jour
    volatilite=...,           # écart-type, % par jour
    var_95=...,               # quantile 5 %, % par jour
    part_hausse=...,          # en %, entre 0 et 100
    pire_jour=...,            # % par jour
    date_pire=...,            # date du pire jour
    rendements=...,           # la colonne, pour l'histogramme
    classement=...,           # Series des volatilités, pour les barres
)
```

**Tout argument omis vaut `None`**, et la tuile correspondante affiche « à compléter » en gris. C'est ce qui permet d'appeler la fonction dès la partie 1.

Elle **annualise toute seule** ce qui doit l'être : le rendement moyen en rendement annuel, la volatilité quotidienne en volatilité annualisée (`× √365`). L'étudiant ne fournit que du quotidien. *(À trancher : voir section 6.)*

Elle ne valide rien et ne corrige rien : une valeur fausse s'affiche telle quelle. La vérification reste le travail des cellules `verifier`, qui restent le seul juge.

---

## 5. Valeurs de référence

Calculées sur `crypto.csv`, rendements en %.

| monnaie | moyenne | médiane | volatilité | VaR 95 % | % hausse | pire jour |
|---|---|---|---|---|---|---|
| BTC | +0,11 | +0,06 | 3,33 | −5,02 | 51,0 | −37,17 |
| ETH | +0,13 | +0,06 | 4,37 | −6,59 | 50,9 | −42,35 |
| SOL | +0,39 | **−0,04** | 6,19 | −8,29 | 49,6 | −42,28 |
| DOGE | +0,32 | −0,17 | 8,93 | −9,84 | **39,9** | −40,25 |
| XRP | +0,12 | −0,08 | 5,38 | −6,79 | 48,6 | −42,33 |
| BNB | +0,25 | +0,08 | 4,78 | −5,83 | 52,0 | −41,90 |
| ADA | +0,10 | −0,10 | 5,39 | −7,46 | 48,4 | −39,39 |

> **SOL est le meilleur cas d'attribution.** Rendement moyen le plus élevé des sept (+0,39 %/jour, soit +314 % par an), et pourtant une **médiane négative** : elle baisse plus d'un jour sur deux. L'écart entre moyenne et médiane, qui n'était qu'une notion en séance 5, devient ici le cœur de l'avis à rendre. DOGE produit le même effet en plus brutal.

Les VaR et médianes de ce tableau restent à revérifier au moment de la construction : seules celles de BTC et ETH ont été contrôlées deux fois.

---

## 6. Ce qu'il reste à trancher

**La date du pire jour.** `idxmin` n'est pas au programme. Trois options : l'introduire dans le devoir en trois lignes ; la faire obtenir par `sort_values("r").head(1)["date"]`, qui n'utilise que du connu mais donne une Series à une ligne ; ou retirer la date de la fiche. Je penche pour la deuxième.

**L'annualisation.** Si la fonction annualise seule, l'étudiant ne voit pas passer `√365` — et c'est une des formules les plus utiles de la finance. Si c'est lui qui la calcule, ça fait deux arguments de plus et un risque d'erreur qui casse la fiche. Je penche pour lui faire calculer **le rendement annuel** (simple, `(1+r)^365 − 1`) et laisser la fonction faire la **volatilité annualisée**, avec une note qui explique la racine.

**L'attribution de la monnaie.** Tirée du nom, fixée par groupe, ou libre ? Ça change la correction.

**Le polissage du prototype.** Trois défauts visibles sur la figure envoyée : l'étiquette « VaR 95 % » chevauche les barres de l'histogramme, l'espace entre le bandeau et les tuiles est trop grand, et la tuile « médiane » colore en rouge une valeur négative alors que ce n'est pas une alerte mais l'information centrale. À corriger à la construction.

**Le temps.** Six parties, une quinzaine de cellules à écrire. À vue de nez 1h à 1h15, donc comparable à l'assignment pandas. À confirmer.
