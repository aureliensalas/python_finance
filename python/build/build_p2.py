import json, os, textwrap

OUT = "python/cours/seance2_cours.ipynb"
LOGO = '<img src="https://cdn.jsdelivr.net/gh/aureliensalas/python_finance@main/ressources/img/logo_macmia.png" alt="Banque des Territoires · France 2030 · MACMIA" width="520">'
BADGE = "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aureliensalas/python_finance/blob/main/python/cours/seance2_cours.ipynb)"

cells = []

def md(s):
    s = textwrap.dedent(s).strip("\n")
    cells.append({"cell_type": "markdown", "metadata": {}, "source": s.splitlines(keepends=True)})

def code(s):
    s = textwrap.dedent(s).strip("\n")
    cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
                  "source": s.splitlines(keepends=True)})

def predire(*exprs):
    for e in exprs:
        code(f"# Prédiction :\n{e}")

# ---------------------------------------------------------------- en-tête
md(f"""
{LOGO}

{BADGE}

# Séance 2 : Python décide et répète

**Cours** · 2h · Python pur, sans fichier de données

> ⚠️ **Avant de taper quoi que ce soit :** *Fichier → Enregistrer une copie dans Drive*. Sinon votre travail sera perdu en fermant l'onglet.
>
> 📱 Sur tablette, faites d'abord les réglages de [Bien démarrer](https://github.com/aureliensalas/python_finance/blob/main/ressources/setup_tablette.md).
""")

md("""
## Objectifs

À la fin de cette séance, vous saurez :

- lire et écrire une condition qui donne `True` ou `False`
- faire dépendre l'exécution d'une condition avec `if`, `elif`, `else`
- ranger plusieurs valeurs dans une liste et y accéder
- répéter un calcul sur chaque élément d'une liste avec `for`
- transformer une liste de résultats en Series pandas et la tracer

## Rappel des huit mots

**expression** · **valeur** · **type** · **variable** · **affectation** · **appel** · **argument** · **méthode**

Exécutez d'abord la cellule de setup.
""")

code("""
import numpy as np
import pandas as pd


def verifier(nom, condition, indice=""):
    if condition:
        print("OK       -", nom)
    else:
        print("A REVOIR -", nom, ":", indice)
""")

# ---------------------------------------------------------------- 0. Échauffement
md("""
## 0. Échauffement

Trois cellules sur la séance 1.

**1.** Le texte `"1 250,50 €"` en nombre, dans `montant`.
""")

code("")

code("""
verifier("montant", montant == 1250.5, "replace pour l'espace, la virgule, le symbole ; puis float")
""")

md("**2.** La valeur absolue de `-3.14159`, arrondie à 2 décimales, en un seul appel imbriqué, dans `valeur`.")

code("")

code("""
verifier("valeur", valeur == 3.14, "round(abs(...), 2)")
""")

md("**3.** Cette cellule est fausse. Exécutez, lisez la dernière ligne, réparez.")

code("""
capital = 1000
print("Capital :", capital
""")

# ---------------------------------------------------------------- 1. Booléens
md("""
## 1. Booléens

- **Valeurs** : `True` et `False`
- **Opérations** : `and`, `or`, `not`

| `a` | `b` | `a and b` | `a or b` | `not a` |
|---|---|---|---|---|
| `True` | `True` | `True` | `True` | `False` |
| `True` | `False` | `False` | `True` | `False` |
| `False` | `True` | `False` | `True` | `True` |
| `False` | `False` | `False` | `False` | `True` |

**Ce qui produit un booléen** : les comparaisons, et `in`.

| `<` `<=` | `>` `>=` | `==` | `!=` | `in` |
|---|---|---|---|---|
| plus petit | plus grand | égal | différent | contenu dans |

> `=` **affecte** une valeur. `==` **compare** deux valeurs.
""")

code('3 > 2, 3 == 3.0, "EUR" in "2.5 EUR"')

md("Un booléen se range dans une variable comme n'importe quelle valeur, et s'utilise ensuite.")

code("""
rendement = 0.05
positif = rendement > 0
positif, positif and rendement < 0.1
""")

md("""
`True` vaut aussi `1`, et `False` vaut `0`.

C'est ce qui permettra, à la séance pandas, de **compter** les lignes qui remplissent une condition.
""")

code("int(True), True + True, True == 1")

md("""
### Prédire

Vingt cellules, cinq paquets. Pour chacune, écrivez la valeur attendue, puis exécutez.

**Comparaisons**
""")

predire("3 > 2", "3 == 3.0", '3 == "3"', '"EUR" == "eur"', "2.5 >= 2.5")

md("**Opérateurs**")

predire("True and False", "True or False", "not (3 > 2)", "(3 > 2) or (2 > 3)", "True and not False")

md("**Avec une variable**")

code("rendement = 0.05")

predire("rendement > 0 and rendement < 0.1", "rendement > 0.1 or rendement < -0.1", "not rendement > 0")

md("**Arithmétique**")

predire("True + True + False", "(3 > 2) + (2 > 1)", "int(False), float(True)")

md("**Chaînes**")

predire('"EUR" in "2.5 EUR"', '"eur" in "2.5 EUR"', '"2.5 EUR".find("$") == -1')

md("""
### Écrire

Avec `revenu = 42000` et `age = 40` : un client est éligible si son revenu dépasse 30 000 **et** s'il a moins de 65 ans. Rangez le booléen dans `eligible`.
""")

code("""
revenu = 42000
age = 40
""")

code("")

code("""
verifier("eligible", eligible == True, "deux comparaisons reliées par and")
""")

md("### Corriger")

code("True and false")

# ---------------------------------------------------------------- 2. if
md("""
## 2. `if`, `elif`, `else`

Jusqu'ici, **toutes** les lignes s'exécutent. Avec `if`, **certaines ne s'exécutent pas**.

| La **structure** du programme | Le **flux** du programme |
|---|---|
| ce qui est écrit | ce qui s'exécute |

On l'a déjà vu sous une autre forme : les cellules s'exécutent dans l'ordre où on les exécute, pas dans l'ordre où elles sont écrites.

### La forme

```
if expression:
    statement
    statement
```

Si l'expression vaut `True`, Python exécute les statements **décalés** en dessous. Sinon, il les saute.

Le `:` et le décalage de 4 espaces font partie de la syntaxe.

### Trois formes

**`if` seul : une action optionnelle.** Il peut ne rien se passer.
""")

code("""
van = -1500

if van < 0:
    print("Le projet détruit de la valeur.")
print("Analyse terminée.")
""")

md("**`if / else` : deux issues.** Exactement une des deux s'exécute. Rien n'est optionnel.")

code("""
if van > 0:
    print("On investit.")
else:
    print("On n'investit pas.")
""")

md("**`if / elif / else` : une condition de plus.** C'est un `if / else` étendu.")

code("""
rendement = 0.12

if rendement > 0.10:
    verdict = "excellent"
elif rendement > 0:
    verdict = "positif"
else:
    verdict = "perte"
verdict
""")

md("""
### Le piège de l'ordre

Python lit les conditions de haut en bas et **s'arrête à la première qui est vraie**.
""")

code("""
if rendement > 0:
    verdict = "positif"
elif rendement > 0.10:
    verdict = "excellent"
else:
    verdict = "perte"
verdict
""")

md("""
Avec `0.12`, la branche `"excellent"` est **inatteignable** : `rendement > 0` est vraie avant.

Si plusieurs conditions doivent pouvoir être vraies **en même temps**, on écrit plusieurs `if` séparés.
""")

code("""
if rendement > 0.10:
    print("Rendement excellent.")
if rendement > 0.08:
    print("Au-dessus de l'objectif.")
""")

md("""
### Afficher un verdict : les f-strings

Un `f` devant les guillemets autorise des `{...}` dans le texte. Python y met la valeur.
Deux formats à connaître : `:.2f` pour deux décimales, `:.1%` pour un pourcentage.
""")

code("""
print(f"Rendement de {rendement:.1%} : {verdict}.")
print(f"Mensualité : {1109.2:.2f} euros.")
""")

md("""
### Écrire

**1.** Le maximum de deux nombres, **sans** `max`. Avec `a = 12` et `b = 7`, comparez-les et rangez le plus grand dans `plus_grand`.
""")

code("""
a = 12
b = 7
""")

code("")

code("""
verifier("plus grand de deux", plus_grand == 12, "if a > b, sinon...")
""")

md("**2.** Le maximum de trois nombres, sans `max`. `a = 12`, `b = 7`, `c = 15`. Rangez-le dans `plus_grand_3`.")

code("""
a = 12
b = 7
c = 15
""")

code("")

code("""
verifier("plus grand de trois", plus_grand_3 == 15, "if, elif, else : trois branches")
""")

md("**3.** Le signe d'un rendement : `\"hausse\"`, `\"baisse\"` ou `\"stable\"`, dans `signe`, pour `rendement = -0.02`.")

code("rendement = -0.02")

code("")

code("""
verifier("signe", signe == "baisse", "trois cas : > 0, < 0, sinon")
""")

md("### Corriger")

code("""
taux = 0.03
if taux = 0.03:
    print("trois pour cent")
""")

code("""
if taux > 0.02
    print("plus de deux pour cent")
""")

code("""
if taux > 0.02:
print("plus de deux pour cent")
""")

# ---------------------------------------------------------------- 3. Listes
md("""
## 3. Listes

Une **liste** est une suite de valeurs entre crochets, séparées par des virgules.
""")

code('flux = [500, 700, 400, 200]')

md("""
On y accède **comme aux caractères d'une chaîne** : même numérotation à partir de 0, même syntaxe, même `len`.

```
 flux  =  [500, 700, 400, 200]
            0    1    2    3
```
""")

code("flux[1], flux[1:3], len(flux)")

code("""
s = "abcd"
s[1], s[1:3], len(s)
""")

md("""
Une chaîne et une liste sont deux sortes de **conteneurs** : quelque chose qui contient des valeurs numérotées.

Deux différences : ce qu'on peut mettre dedans, et ceci.

### Une liste est modifiable. Une chaîne ne l'est pas.
""")

code("""
flux[1] = 800
flux
""")

code('s[1] = "x"')

md("""
```
TypeError: 'str' object does not support item assignment
```

### Ajouter à la fin : `append`

Une méthode de la liste. Elle **modifie** la liste, et ne renvoie rien.
""")

code("""
flux.append(300)
flux
""")

md("### Fonctions utiles")

code("sum(flux), max(flux), min(flux), 400 in flux")

md("### La position d'une valeur : `index`")

code("flux.index(400)")

md("### Prédire")

predire("[1, 2, 3] + [4]", "[10, 20, 30][2]", "len([])", "[1, 2, 3] * 2")

md("""
Gardez le résultat de la dernière en tête : on la reverra à la section 5.

### Écrire

Quatre flux de trésorerie `[1200, 800, 1500, 900]` dans `flux`.
Remplacez le troisième par `1600`. Ajoutez `700` à la fin.
Rangez la somme dans `total` et la position du plus grand dans `position_max`.
""")

code("")

code("""
verifier("total", total == 5200, "sum après les modifications")
verifier("position du max", position_max == 2, "flux.index(max(flux))")
""")

# ---------------------------------------------------------------- 4. for
md("""
## 4. Répéter : `for`

On veut calculer la somme d'une liste **nous-mêmes**, sans `sum`.

Problème : une liste peut avoir **n'importe quelle taille**. On ne peut pas écrire `flux[0] + flux[1] + ...` sans savoir où s'arrêter.

Il faut une instruction qui passe sur **chaque élément**, quelle que soit la taille.

### La boucle la plus simple du monde
""")

code("""
flux = [500, 700, 400, 200]

for x in flux:
    print(x)
""")

md("""
Trois morceaux, toujours les mêmes :

```
for  x  in  flux :
     │      │
     │      └── l'itérable : ce sur quoi on passe
     └── la variable de boucle : prend chaque valeur à tour de rôle

    print(x)      ← le corps : exécuté une fois par valeur
```

L'itérable doit être quelque chose sur quoi on **peut** passer. Une liste, oui. Une chaîne, oui. Un nombre, non :
""")

code("""
for x in 5:
    print(x)
""")

md("""
```
TypeError: 'int' object is not iterable
```

### La somme : premier essai

On prend une variable `total` et on y met chaque élément.
""")

code("""
total = 0
for x in flux:
    total = x
total
""")

md("""
`200`. Pas la somme : le **dernier** élément.

### Réflexion : les boîtes

À chaque tour, `total = x` **remplace** ce qu'il y a dans la boîte `total` par la valeur de `x`.

| tour | `x` | `total` après `total = x` |
|---|---|---|
| 1 | 500 | 500 |
| 2 | 700 | 700 |
| 3 | 400 | 400 |
| 4 | 200 | 200 |

Ce qu'on veut, c'est que la boîte **reçoive** chaque valeur **en plus** de ce qu'elle contient déjà : `total = total + x`.

| tour | `x` | `total` après `total = total + x` |
|---|---|---|
| 1 | 500 | 500 |
| 2 | 700 | 1200 |
| 3 | 400 | 1600 |
| 4 | 200 | 1800 |

Une variable qui part de zéro et reçoit chaque élément s'appelle un **accumulateur**.
""")

code("""
total = 0
for x in flux:
    total = total + x
total
""")

md("`sum(flux)` fait exactement ça.")

code("sum(flux)")

md("""
### Modifier chaque élément : deuxième piège

On veut ajouter 1 à chaque élément de `flux`.
""")

code("""
for x in flux:
    x = x + 1
flux
""")

md("""
La liste n'a pas changé.

**Les boîtes, encore.** `x` est une boîte à part. À chaque tour, Python y **copie** la valeur de l'élément. `x = x + 1` change la boîte `x`, pas la liste.

Deux solutions.

**Solution 1 : un accumulateur qui est une liste.** On construit une copie modifiée, avec `append`.
""")

code("""
plus_un = []
for x in flux:
    plus_un.append(x + 1)
plus_un
""")

md("""
**Solution 2 : passer sur les positions, pas sur les valeurs.**

`range(n)` fabrique l'itérable des positions `0, 1, ..., n-1`. C'est son seul rôle.
""")

code("list(range(4))")

code("""
for i in range(len(flux)):
    flux[i] = flux[i] + 1
flux
""")

md("""
Cette fois on écrit dans la liste elle-même, case par case.

### Répéter `n` fois

`range(n)` sert aussi à répéter, sans liste du tout.
""")

code("""
capital = 1000
for annee in range(10):
    capital = capital * 1.03
capital
""")

md("""
> Une boucle sert à faire quelque chose **de façon répétée**.
>
> Le motif qui reviendra tout le cours : **une liste vide avant, `append` dedans, le résultat après.**

### Écrire

**1.** La moyenne de `flux`, sans `sum` ni `len` dans le corps de la boucle : un accumulateur pour le total, un compteur pour le nombre d'éléments, la division après la boucle. Rangez-la dans `moyenne`.
""")

code("flux = [500, 700, 400, 200]")

code("")

code("""
verifier("moyenne", moyenne == 450, "deux accumulateurs, une division après la boucle")
""")

md("""
**2.** Un capital de 1 000 € à 3 %, année par année pendant 10 ans. Rangez la valeur de **chaque fin d'année** dans une liste `historique`.
""")

code("")

code("""
verifier("dix valeurs", len(historique) == 10, "un append par tour de boucle")
verifier("derniere valeur", abs(historique[9] - 1343.92) < 0.01, "capital = capital * 1.03 à chaque tour, puis append")
""")

md("""
**3.** La mensualité pour chaque taux de `taux = [0.02, 0.03, 0.04, 0.05]`, pour 200 000 € sur 20 ans, dans une liste `mensualites`.

Formule de la séance 1 : `capital * t / (1 - (1 + t) ** -n)`, avec `t` le taux mensuel et `n = 240`.
""")

code("taux = [0.02, 0.03, 0.04, 0.05]")

code("")

code("""
verifier("quatre mensualites", len(mensualites) == 4, "une par taux")
verifier("premiere", abs(mensualites[0] - 1011.77) < 0.01, "t = 0.02 / 12")
verifier("derniere", abs(mensualites[3] - 1319.91) < 0.01, "t = 0.05 / 12")
""")

md("### Corriger")

code("""
for x in flux
    print(x)
""")

md("La cellule suivante ne produit pas d'erreur. Elle n'affiche rien. Pourquoi ?")

code("""
resultats = []
for x in flux:
    resultats.append(x * 2)
    resultats
""")

# ---------------------------------------------------------------- 5. Series
md("""
## 5. Passerelle vers pandas : la Series

Une **Series**, c'est une liste qui a **une étiquette par valeur** et qui **sait faire des maths sur elle-même**.
""")

code("""
serie = pd.Series(mensualites, index=taux)
serie
""")

md("Même signe `*`, deux types, deux opérations. C'est la définition d'un type, vue à la séance 1.")

code("[1, 2, 3] * 2")

code("pd.Series([1, 2, 3]) * 2")

md("Les méthodes d'une Series : les mêmes noms que les fonctions sur les listes.")

code("serie.mean(), serie.max()")

md("Et un graphique, en une ligne.")

code("serie.plot()")

# ---------------------------------------------------------------- 6. Synthèse
md("""
## 6. Ce que vous savez faire

| Vous voulez... | Vous écrivez |
|---|---|
| comparer | `a > b`, `a == b`, `a != b` |
| combiner des conditions | `a > 0 and a < 1`, `not a` |
| exécuter selon une condition | `if a > b:` |
| deux issues | `if ... :` `else:` |
| plus de deux | `if ... :` `elif ... :` `else:` |
| afficher avec des valeurs | `f"Taux : {taux:.1%}"` |
| une liste | `flux = [500, 700, 400]` |
| un élément, une tranche | `flux[0]`, `flux[1:3]` |
| ajouter à la fin | `flux.append(300)` |
| passer sur chaque élément | `for x in flux:` |
| passer sur les positions | `for i in range(len(flux)):` |
| répéter n fois | `for i in range(n):` |
| accumuler | `total = 0` avant, `total = total + x` dedans |
| garder les résultats | `resultats = []` avant, `resultats.append(...)` dedans |
| une Series | `pd.Series(resultats, index=taux)` |
| la tracer | `serie.plot()` |

## Trois réflexes

1. **`=` affecte, `==` compare.**
2. **Le `:` et le décalage** sont la syntaxe du `if` et du `for`.
3. **Une variable de boucle est une boîte à part.** Pour garder un résultat, il faut un accumulateur.

## La suite

L'assignment noté : un simulateur de prêt, à partir du taux directeur de la Banque centrale européenne du jour. Tout ce qu'il demande est dans ces deux séances.
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
