import json, os, textwrap

OUT = "python/assignment/simulateur_pret.ipynb"
LOGO = '<img src="https://cdn.jsdelivr.net/gh/aureliensalas/python_finance@main/ressources/img/logo_macmia.png" alt="Banque des Territoires · France 2030 · MACMIA" width="520">'
BADGE = "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aureliensalas/python_finance/blob/main/python/assignment/simulateur_pret.ipynb)"

cells = []

def md(s):
    s = textwrap.dedent(s).strip("\n")
    cells.append({"cell_type": "markdown", "metadata": {}, "source": s.splitlines(keepends=True)})

def code(s):
    s = textwrap.dedent(s).strip("\n")
    cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
                  "source": s.splitlines(keepends=True)})

# ---------------------------------------------------------------- en-tête
md(f"""
{LOGO}

{BADGE}

# Assignment 1 : le simulateur de prêt

**Travail noté** · lancé en séance, terminé à la maison

> ⚠️ **Avant de taper quoi que ce soit :** *Fichier → Enregistrer une copie dans Drive*. Sinon votre travail sera perdu en fermant l'onglet.

| | |
|---|---|
| **Rendu** | ce notebook, toutes les cellules exécutées, [date à fixer] |
| **Travail** | [seul ou en binôme, à fixer] |
| **Ressources** | les notebooks des séances 1 et 2, rien d'autre n'est nécessaire |
| **Barème** | 20 points, détaillé partie par partie |

Écrivez votre nom ici : **[nom]**
""")

md("""
## Ce que vous allez construire

Un client demande un prêt immobilier. Vous allez écrire, de bout en bout, ce qu'une banque fait pour lui répondre :

1. lire sa demande, et aller chercher le taux du jour à la Banque centrale européenne ;
2. calculer sa mensualité ;
3. décider si le prêt est accordé ;
4. construire le tableau d'amortissement, mois par mois, sur toute la durée ;
5. en tirer la courbe du capital restant dû et le coût total du crédit ;
6. comparer plusieurs durées pour trouver celle qui convient.

```
 formulaire  →  paramètres  →  mensualité  →  verdict  →  tableau  →  résultats  →  scénarios
  partie 1                     partie 2       partie 3    partie 4    partie 5      partie 6
```

Chaque partie utilise le résultat de la précédente. Les cellules s'exécutent dans l'ordre, de haut en bas.

Tout ce qui est demandé a été vu en séance 1 ou 2. Quand une partie renvoie à une section du cours, c'est là qu'est la réponse.

## Comment travailler

- Une idée par cellule. Une cellule qui fait trois choses est difficile à corriger.
- Après chaque exercice, une cellule `verifier` vous dit si le résultat est bon. Un `A REVOIR` n'enlève pas de points : il vous dit où regarder.
- Avant de rendre : *Exécution → Redémarrer et tout exécuter*. Tout doit passer sans erreur, de haut en bas.

| Partie | Points |
|---|---|
| 1. Les paramètres | 3 |
| 2. La mensualité | 3 |
| 3. Le verdict | 3 |
| 4. Le tableau d'amortissement | 6 |
| 5. Les résultats | 3 |
| 6. Les scénarios | 2 |

Exécutez d'abord la cellule de setup.
""")

code("""
import numpy as np
import pandas as pd
import requests


def verifier(nom, condition, indice=""):
    if condition:
        print("OK       -", nom)
    else:
        print("A REVOIR -", nom, ":", indice)
""")

# ---------------------------------------------------------------- Partie 1
md("""
## Partie 1 : les paramètres (3 points)

La demande du client arrive d'un formulaire en ligne. Les champs sont remplis par un humain, donc ce sont des **textes**, avec des espaces et des unités.
""")

code("""
capital_txt = "200 000 €"
duree_txt = "20 ans"
revenu_txt = "3 200 €"
""")

md("""
### 1a. Du texte aux nombres (1 point)

Convertissez ces trois textes en nombres :

| Variable à créer | Type | Valeur attendue |
|---|---|---|
| `capital` | `float` | `200000.0` |
| `duree_annees` | `int` | `20` |
| `revenu_mensuel` | `float` | `3200.0` |

**Indication.** Essayez d'abord `float(capital_txt)` dans une cellule. Vous obtiendrez une erreur : `float` ne sait pas quoi faire des espaces ni du symbole `€`. Il faut d'abord les retirer, et c'est le rôle de la méthode `replace` (séance 1, section 8).

Exemple sur un autre texte :

```python
"12 500 €".replace(" ", "")        # donne "12500€"
"12 500 €".replace(" ", "").replace("€", "")   # donne "12500"
```

Puis `float(...)` sur le résultat. Pour la durée, retirez `" ans"` et utilisez `int`.
""")

code("")

code("""
verifier("capital", capital == 200000.0, "replace pour l'espace et le symbole, puis float")
verifier("duree en annees", duree_annees == 20 and type(duree_annees) == int, "replace pour ' ans', puis int")
verifier("revenu mensuel", revenu_mensuel == 3200.0, "même méthode que pour le capital")
""")

md("""
### 1b. Le taux du jour (1 point)

Une banque ne fixe pas son taux au hasard. Elle se finance auprès de la **Banque centrale européenne** à un taux appelé **taux directeur**, et elle prête à ses clients un peu plus cher. Le taux directeur est public : la BCE le publie sur un service web.

Les deux cellules suivantes vont le chercher. Elles sont fournies, exécutez-les.
""")

code("""
url_bce = "https://data-api.ecb.europa.eu/service/data/FM/B.U2.EUR.4F.KR.MRR_FR.LEV?lastNObservations=1&format=csvdata&detail=dataonly"
""")

code("""
reponse = requests.get(url_bce).text
print(reponse)
""")

md("""
**Observez la réponse.** C'est un texte de deux lignes. La première est un en-tête : les noms des colonnes. La seconde contient les valeurs, et **se termine** par ce qui nous intéresse :

```
...,MRR_FR,LEV,2026-09-16,2.65
```

Le taux est le tout dernier élément, précédé de la date. Le début de la ligne est long et illisible ; la fin, elle, a toujours la même forme : une **date de 10 caractères**, une virgule, puis le **taux**, qui s'écrit toujours `X.XX` — quatre caractères.

**Le raisonnement.** On ne connaît pas la longueur du texte, donc on ne peut pas compter depuis le début. Mais on sait compter **depuis la fin** : ce sont les index négatifs de la séance 1, section 8.

Un obstacle d'abord : le texte se termine par un **retour à la ligne** invisible. Tant qu'il est là, le dernier caractère n'est pas `5` mais ce retour à la ligne. On le retire avec `strip()`, qui enlève les espaces et les retours à la ligne au début et à la fin.

```python
ligne = reponse.strip()
```

Ensuite, sur `ligne` :

- `ligne[-4:]` : les **quatre derniers** caractères, c'est-à-dire le taux, en texte ;
- `float(...)` pour en faire un nombre.

Exemple du même raisonnement sur un texte court :

```python
t = "FM,B,code,2026-09-16,2.65\\n"
ligne = t.strip()
ligne[-4:]                          # donne "2.65"
float(ligne[-4:])                   # donne 2.65
ligne[-15:-5]                       # donne "2026-09-16", la date
```

Rangez le taux dans `taux_bce`.
""")

code("")

code("""
verifier("taux BCE", type(taux_bce) == float and 0 < taux_bce < 10, "strip() pour le retour à la ligne, puis les 4 derniers caractères, puis float")
""")

md("""
Si le service ne répond pas, utilisez la cellule de secours ci-dessous : retirez le `#` et exécutez-la à la place de la précédente.
""")

code("""
# taux_bce = 2.65
""")

md("""
### 1c. Le taux du prêt (1 point)

La banque prête plus cher qu'elle n'emprunte : elle ajoute une **marge de 1,2 point** au taux directeur. Si la BCE est à 2,65 %, la banque prête à 3,85 %.

Créez trois variables :

- `taux_annuel` : le taux directeur plus la marge ;
- `taux_mensuel` : le taux annuel divisé par 100 (pour passer du pourcentage au nombre), puis divisé par 12 (pour passer de l'année au mois) ;
- `nb_mois` : le nombre de mois du prêt. Combien de mois dans 20 ans ? Calculez-le à partir de `duree_annees`, pas à la main.
""")

code("")

code("""
verifier("taux annuel", abs(taux_annuel - (taux_bce + 1.2)) < 1e-9, "le taux BCE plus 1.2")
verifier("taux mensuel", abs(taux_mensuel - taux_annuel / 100 / 12) < 1e-12, "divisé par 100, puis par 12")
verifier("nombre de mois", nb_mois == 240, "12 mois par année")
""")

md("""
### Point d'étape

Vous disposez maintenant de cinq nombres :

| Variable | Rôle |
|---|---|
| `capital` | ce que le client emprunte |
| `nb_mois` | le nombre de mensualités |
| `taux_mensuel` | ce que coûte chaque mois le capital encore dû |
| `revenu_mensuel` | ce que le client peut payer |
| `taux_annuel` | le taux affiché sur l'offre |

C'est tout ce dont une banque a besoin pour construire une offre. Le reste du travail n'utilise que ces cinq variables.
""")

# ---------------------------------------------------------------- Partie 2
md("""
## Partie 2 : la mensualité (3 points)

Un prêt se rembourse par des versements **égaux** tous les mois. Chaque versement sert à deux choses : payer les **intérêts** sur ce qui reste dû, et rembourser un **morceau du capital**. Au début, ce qui reste dû est élevé, donc les intérêts sont élevés et le morceau de capital est petit. À la fin, c'est l'inverse.

La mensualité est le montant constant qui fait qu'après `nb_mois` versements, le capital est exactement remboursé. Sa formule, avec `t` le taux mensuel et `n` le nombre de mois :

```python
mensualite = capital * t / (1 - (1 + t) ** -n)
```

Calculez `mensualite` avec vos variables, puis affichez-la avec une f-string (séance 2, section 2) sous cette forme, arrondie à 2 décimales :

```
Pour 200000 € sur 20 ans à 3.85 %, la mensualité est de 1196.21 €.
```

Les nombres affichés dépendent du taux du jour.
""")

code("")

code("""
verifier("mensualite", abs(mensualite - capital * taux_mensuel / (1 - (1 + taux_mensuel) ** -nb_mois)) < 0.01, "la formule, avec t = taux_mensuel et n = nb_mois")
""")

md("""
### Point d'étape

La mensualité est le premier chiffre de l'offre. C'est aussi celui que le client regarde en premier, et celui sur lequel la banque va décider.
""")

# ---------------------------------------------------------------- Partie 3
md("""
## Partie 3 : le verdict (3 points)

Une banque n'accorde pas un prêt dont la mensualité écraserait le budget du client. Elle calcule le **taux d'effort** : la part du revenu mensuel qui part dans la mensualité.

### 3a. Le taux d'effort et la décision (2 points)

Calculez `taux_effort`, la mensualité divisée par le revenu mensuel.

Puis écrivez un `if / elif / else` (séance 2, section 2) qui range dans `verdict` :

| Condition | `verdict` |
|---|---|
| taux d'effort au-dessus de 35 % | `"refus"` |
| sinon, au-dessus de 30 % | `"accord sous réserve"` |
| sinon | `"accord"` |

Puis affichez, en une f-string, le taux d'effort en pourcentage à une décimale et le verdict :

```
Taux d'effort : 37.4%, verdict : refus.
```
""")

code("")

code("""
verifier("taux d'effort", abs(taux_effort - mensualite / revenu_mensuel) < 1e-9, "mensualite / revenu_mensuel")
verifier("verdict coherent", (taux_effort > 0.35 and verdict == "refus") or (0.30 < taux_effort <= 0.35 and verdict == "accord sous réserve") or (taux_effort <= 0.30 and verdict == "accord"), "trois branches, dans l'ordre : > 0.35, puis > 0.30, puis else")
""")

md("""
### 3b. Deux avertissements (1 point)

Indépendamment du verdict, la banque signale deux choses, qui peuvent être vraies **toutes les deux** :

- si la durée dépasse 25 ans, afficher `"Attention : durée supérieure à 25 ans."` ;
- si la mensualité dépasse 1 000 €, afficher `"Attention : mensualité supérieure à 1 000 €."`.

Deux `if` séparés, pas de `elif` : les deux messages doivent pouvoir s'afficher ensemble (séance 2, section 2, « plusieurs `if` séparés »).
""")

code("")

md("""
### Point d'étape

Avec les données du formulaire et le taux du jour, le prêt est **refusé** : la mensualité représente plus de 35 % du revenu. C'est un résultat, pas une erreur. Ne modifiez pas les paramètres : la partie 6 cherchera une durée qui rend le prêt acceptable.

Jusqu'ici, tout tient en quelques nombres. La suite construit le détail, mois par mois.
""")

# ---------------------------------------------------------------- Partie 4
md("""
## Partie 4 : le tableau d'amortissement (6 points)

Le tableau d'amortissement décrit chaque mois du prêt : combien d'intérêts, combien de capital remboursé, combien il reste à rembourser après le versement.

La mécanique d'un mois :

1. les **intérêts** du mois se calculent sur ce qui reste dû : `capital_restant * taux_mensuel` ;
2. le **capital remboursé** ce mois-ci est ce qui reste de la mensualité une fois les intérêts payés : `mensualite - interets` ;
3. le **capital restant** diminue d'autant : `capital_restant - rembourse`.

### 4a. Les deux premiers mois, à la main (1 point)

Avant d'écrire du code, faites le calcul pour les deux premiers mois et écrivez les résultats dans le tableau ci-dessous, en double-cliquant sur cette cellule. Utilisez une cellule de code comme calculatrice si vous voulez.

| Mois | Capital restant avant | Intérêts | Capital remboursé | Capital restant après |
|---|---|---|---|---|
| 1 | 200 000,00 | | | |
| 2 | | | | |

Vérifiez que le capital restant après le mois 1 est le capital restant avant le mois 2.
""")

md("""
### 4b. La boucle (4 points)

Le calcul du 4a se répète `nb_mois` fois. C'est le travail d'une boucle `for` (séance 2, section 4).

Trois listes vides recevront les résultats, une par colonne du tableau, et une variable suivra le capital restant :
""")

code("""
interets_liste = []
capital_liste = []
restant_liste = []

capital_restant = capital
""")

md("""
La boucle passe sur chaque mois. `range(nb_mois)` fabrique la suite `0, 1, ..., 239` : le corps de la boucle s'exécute une fois par mois.

À chaque tour, le corps doit :

1. calculer les intérêts du mois ;
2. calculer le capital remboursé ce mois-ci ;
3. mettre à jour `capital_restant` ;
4. ajouter les trois valeurs du mois à la fin des trois listes, avec `append`.

Complétez le corps de la boucle dans la cellule ci-dessous.
""")

code("""
for mois in range(nb_mois):
    # 1. les intérêts du mois

    # 2. le capital remboursé ce mois-ci

    # 3. le nouveau capital restant

    # 4. ajouter les trois valeurs aux trois listes

""")

code("""
verifier("une valeur par mois", len(interets_liste) == nb_mois and len(capital_liste) == nb_mois and len(restant_liste) == nb_mois, "trois append par tour de boucle")
verifier("interets du mois 1", abs(interets_liste[0] - capital * taux_mensuel) < 0.01, "capital_restant * taux_mensuel, avant toute mise à jour")
verifier("pret solde", abs(restant_liste[-1]) < 0.01, "au dernier mois, le capital restant doit être 0 : vérifiez la mise à jour de capital_restant")
verifier("bilan", abs(mensualite * nb_mois - (capital + sum(interets_liste))) < 1, "ce qui a été payé = le capital + tous les intérêts")
""")

md("""
### 4c. Le tableau (1 point)

La cellule suivante assemble vos trois listes en un **tableau à trois colonnes**. Chaque colonne est une de vos listes. C'est un objet pandas, que vous apprendrez à manipuler à la prochaine séance. Exécutez-la.
""")

code("""
tableau = pd.DataFrame({"interets": interets_liste, "capital": capital_liste, "restant": restant_liste})
tableau.round(2).head(12)
""")

md("""
Regardez la colonne `interets` et la colonne `capital` sur ces douze premiers mois. Écrivez ici, en une phrase, ce que vous observez :

**Observation :** [à compléter]

### Point d'étape

Le tableau d'amortissement est l'offre complète : pour chacun des 240 mois, la banque sait ce qu'elle encaisse en intérêts et ce que le client a encore à rembourser. Les trois listes contiennent toute cette information. La partie 5 en extrait ce qui compte.
""")

# ---------------------------------------------------------------- Partie 5
md("""
## Partie 5 : les résultats (3 points)

### 5a. La courbe du capital restant dû (1 point)

Tracez l'évolution du capital restant dû sur toute la durée du prêt.

Rappel : une liste devient une Series avec `pd.Series(liste)`, et une Series se trace avec `.plot()` (séance 2, section 5).
""")

code("")

md("""
### 5b. Le coût total du crédit (1 point)

Le coût du crédit, c'est tout ce que le client paie **en plus** du capital : la somme de tous les intérêts.

Calculez-le dans `cout_credit` et affichez-le avec une f-string, arrondi à 2 décimales :

```
Coût total du crédit : 87090.68 €
```

Rappel : `sum` calcule la somme d'une liste.
""")

code("")

code("""
verifier("cout du credit", abs(cout_credit - sum(interets_liste)) < 0.01, "sum sur la liste des intérêts")
""")

md("""
### 5c. Le mois de bascule (1 point)

Au début du prêt, chaque mensualité sert surtout à payer des intérêts. Il arrive un mois où, pour la première fois, la part de capital remboursé dépasse la part d'intérêts. C'est le **mois de bascule**.

Trouvez-le et rangez son numéro (en comptant à partir de 1) dans `bascule`.

**Le raisonnement.** Il faut comparer, pour chaque mois, `capital_liste[i]` et `interets_liste[i]`. Une boucle sur les positions, `for i in range(nb_mois)`, permet de lire les deux listes à la même position. Un `if` détecte le mois où le capital dépasse les intérêts.

La difficulté : on veut le **premier** mois, et la boucle continue après. La solution : une variable `bascule` qui vaut `0` avant la boucle, et une condition qui ne s'active que si `bascule` vaut encore `0`. Une fois `bascule` rempli, la condition ne s'active plus.

Le numéro du mois est `i + 1`, parce que les positions commencent à 0.
""")

code("")

code("""
verifier("mois de bascule", bascule > 1 and capital_liste[bascule - 1] > interets_liste[bascule - 1] and capital_liste[bascule - 2] <= interets_liste[bascule - 2], "le premier mois où capital_liste[i] > interets_liste[i], numéroté i + 1")
""")

md("""
### Point d'étape

Une courbe, un coût, un mois de bascule : trois façons de résumer 240 lignes. C'est ce qu'on met dans une note d'une page, et c'est ce qu'un client comprend.

Il reste la question ouverte de la partie 3 : le prêt est refusé. Que faudrait-il changer ?
""")

# ---------------------------------------------------------------- Partie 6
md("""
## Partie 6 : les scénarios (2 points)

Le client ne peut pas changer son revenu. Il peut changer la **durée**. Une durée plus longue baisse la mensualité, donc le taux d'effort.

Pour chaque durée de la liste ci-dessous, calculez la mensualité avec la formule de la partie 2, et rangez les quatre résultats dans une liste `mensualites`. Le nombre de mois change à chaque tour ; le taux mensuel ne change pas.
""")

code("""
durees = [10, 15, 20, 25]
""")

code("")

code("""
verifier("quatre mensualites", len(mensualites) == 4, "un append par durée")
verifier("mensualite a 20 ans", abs(mensualites[2] - mensualite) < 0.01, "à 20 ans, on doit retrouver la mensualité de la partie 2")
verifier("decroissante", mensualites[0] > mensualites[1] > mensualites[2] > mensualites[3], "plus la durée est longue, plus la mensualité est basse")
""")

md("""
Tracez ces quatre mensualités en barres : `pd.Series(mensualites, index=durees).plot(kind="bar")`.
""")

code("")

md("""
Pour chaque durée, le taux d'effort est la mensualité divisée par le revenu. Quelle est la durée la plus courte qui fait passer le taux d'effort **sous 35 %** ? Quel est alors le verdict ?

**Réponse :** [à compléter, avec le taux d'effort correspondant]
""")

# ---------------------------------------------------------------- Fin
md("""
## Ce que vous avez construit

À partir de trois champs de formulaire et d'un taux lu en direct chez la BCE, vous avez produit une offre de prêt complète : la mensualité, la décision, le tableau d'amortissement sur 240 mois, la courbe du capital restant dû, le coût du crédit, le mois de bascule, et la comparaison des durées. Chaque étape a utilisé un outil des séances 1 et 2, et rien d'autre.

## Avant de rendre

1. *Exécution → Redémarrer et tout exécuter*.
2. Toutes les cellules `verifier` affichent `OK`.
3. Les deux réponses en texte sont remplies : l'observation de la partie 4c et la réponse de la partie 6.
4. Votre nom est en haut du notebook.
""")

nb = {
    "cells": cells,
    "metadata": {
        "colab": {"provenance": [], "toc_visible": True},
        "kernelspec": {"display_name": "Python 3", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 0,
}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(nb, open(OUT, "w"), ensure_ascii=False, indent=1)
print("écrit", OUT, len(cells), "cellules")
