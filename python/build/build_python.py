"""Construit le notebook unique du bloc 1 (2h de classe).

    python3 python/build/build_python.py
"""
import json, os, textwrap

OUT = "python/cours/python_cours.ipynb"
LOGO = '<img src="https://cdn.jsdelivr.net/gh/aureliensalas/python_finance@main/ressources/img/logo_macmia.png" alt="Banque des Territoires · France 2030 · MACMIA" width="520">'
BADGE = "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aureliensalas/python_finance/blob/main/python/cours/python_cours.ipynb)"

cells = []

def md(s):
    s = textwrap.dedent(s).strip("\n")
    cells.append({"cell_type": "markdown", "metadata": {}, "source": s.splitlines(keepends=True)})

def code(s):
    s = textwrap.dedent(s).strip("\n")
    cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
                  "source": s.splitlines(keepends=True)})

def predire(*exprs):
    """Une cellule par expression, nue. On annonce la valeur à voix haute, puis on exécute."""
    for e in exprs:
        code(e)

md(f"""
{LOGO}

{BADGE}

# Python pour la finance

**Cours** · 2h · Python pur, sans fichier de données

> ⚠️ **Avant de taper quoi que ce soit :** *Fichier → Enregistrer une copie dans Drive*. Sinon votre travail sera perdu en fermant l'onglet.
>
> 📱 Sur tablette, faites d'abord les réglages de [Bien démarrer](https://github.com/aureliensalas/python_finance/blob/main/ressources/setup_tablette.md).
""")

md("""
## Objectifs

À la fin de cette séance, vous saurez :

- taper une expression et lire la valeur que Python en tire
- reconnaître les quatre types de valeurs du cours et passer de l'un à l'autre
- créer une variable, la modifier, et dire ce qu'elle contient
- appeler une fonction, avec ses arguments, et charger un module
- appliquer une méthode à une chaîne de caractères, et en découper un morceau
- lire et écrire une condition qui donne `True` ou `False`
- faire dépendre l'exécution d'une condition avec `if`, `elif`, `else`
- ranger plusieurs valeurs dans une liste et y accéder
- répéter un calcul sur chaque élément d'une liste avec `for`
- transformer une liste de résultats en Series pandas et la tracer
- lire la dernière ligne d'un message d'erreur

## Huit mots

Ces huit mots reviennent tout le semestre. Ils ont toujours le même sens.

| Mot | Sens |
|---|---|
| **expression** | un bout de code qui représente quelque chose |
| **valeur** | ce que Python obtient en évaluant une expression |
| **type** | la famille d'une valeur : entier, décimal, booléen, texte |
| **variable** | une boîte avec un nom, qui contient une valeur |
| **affectation** | l'instruction qui met une valeur dans une boîte : `x = 5` |
| **appel** | demander à une fonction de travailler : `round(2.7)` |
| **argument** | ce qu'on donne à la fonction, entre les parenthèses |
| **méthode** | une fonction attachée à une valeur : `s.upper()` |

## Comment on travaille

| Type de cellule | Ce que vous faites |
|---|---|
| **Démonstration** | vous exécutez et vous lisez |
| **Prédire** | vous **annoncez à voix haute** la valeur attendue, puis vous exécutez |
| **Écrire** | vous remplissez la cellule vide ; la cellule `verifier` d'après vous dit si c'est bon |
| **Corriger** | la cellule est fausse : exécutez, lisez **la dernière ligne**, réparez |

Le parcours va des valeurs aux boucles, en quatorze sections. Une **pause** est prévue à la moitié, après la section 8.
""")


md("""
## 0. Colab

Ce document est un **notebook**. Il alterne deux sortes de cellules :

- des **cellules de texte**, comme celle-ci ;
- des **cellules de code**, comme celle du dessous.

Pour exécuter une cellule : cliquer dedans, puis **`Maj + Entrée`**.
Pour en ajouter une : **`+ Code`** ou **`+ Texte`**, en haut à gauche.
""")

code('print("Bonjour")')

md("""
Le `[1]` apparu à gauche dit que c'est la première cellule exécutée.

### La cellule de setup

La cellule ci-dessous est en tête de tous les notebooks du cours. Exécutez-la **en premier**, sans chercher à la comprendre : elle charge des outils et définit `verifier`, qui vous dira si vos réponses sont bonnes.
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


md("""
## 1. Expressions et valeurs

Une **expression** représente quelque chose.
Python l'**évalue** et la transforme en **valeur**, comme une calculatrice.

Colab affiche la valeur de la dernière ligne de la cellule.
""")

code("2.2")

code("(3 * 7 + 1) / 10")

md("""
Deux expressions différentes, la même valeur.

| Opération | Signe |
|---|---|
| addition, soustraction | `+` `-` |
| multiplication, division | `*` `/` |
| puissance | `**` |
| priorité | `( )` |

Priorités comme en maths : puissance, puis `*` `/`, puis `+` `-`.
""")


md("""
## 2. Types

Deux cellules, le même signe `+`.
""")

code("3 + 4")

code('"Hello" + "World"')

md("""
Une addition d'un côté, une mise bout à bout de l'autre.

Python a fait deux choses différentes parce que les valeurs **n'ont pas le même type**.
C'est l'idée de base de la programmation : **chaque valeur a un type, et le type décide de ce que les opérations font.**

> **Un type = un ensemble de valeurs + des opérations sur ces valeurs.**

`type(...)` donne le type d'une valeur.
""")

code("type(3)")

code('type("Hello")')

md("""
**Les quatre types du cours.**

| Type | Valeurs | Opérations | À retenir |
|---|---|---|---|
| `int` | entiers, sans point : `3`, `-12` | `+` `-` `*` `/` `**` | la division `/` donne toujours un `float` |
| `float` | avec un point : `2.0`, `0.035` | `+` `-` `*` `/` `**` | `2` et `2.0` : même valeur, pas même type |
| `bool` | `True`, `False`, majuscule obligatoire | `and` `or` `not` | produit par les comparaisons ; section 9 |
| `str` | du texte : `"Hello"`, `'EUR'` | `+`, qui met bout à bout | entre deux `str` seulement |
""")

code("type(7 / 7)")

code("2 == 2.0")

code("type(2.0)")

code("3 > 2")

code("type(3 > 2)")

code('"Hello" + " " + "World"')

md("""
### Prédire

Quel **type** ? Annoncez-le, puis exécutez.
""")

predire("type(7 / 7)", 'type("7")', 'type("sept" + "huit")')


md("""
## 3. Conversions

On change le type d'une valeur avec un appel de la forme **`type(expression)`**.
""")

code("float(2)")

code("int(2.6)")

code("str(2)")

code('float("2.5")')

md("""
Les types s'emboîtent, du plus étroit au plus large :

```
bool  ⊂  int  ⊂  float
```

**Vers le plus large**, Python convertit tout seul : on ne perd rien.
""")

code("1 / 2.0")

md("""
L'entier `1` est devenu un décimal sans qu'on le demande.

**Vers le plus étroit**, Python ne le fait jamais seul : on perd de l'information.
`int(2.6)` donne `2`, et il faut l'écrire.
""")


md("""
## 4. Expression et statement

| | Une **expression** | Un **statement** |
|---|---|---|
| c'est | quelque chose qui **représente** une valeur | quelque chose qui **fait** une action |
| Python | l'**évalue** | l'**exécute** |
| au bout | une valeur | pas forcément de valeur |
| exemple | `2.3`, `3 + 5 / 4` | `print("Hello")` |

Dans Colab, la dernière **expression** d'une cellule s'affiche. Un **statement** n'affiche rien par lui-même.
""")

code('print("Hello")')


md("""
## 5. Variables et affectation

Une **variable**, c'est une boîte. Elle a un **nom**, et une **valeur** dedans.

| Nom de la boîte | Valeur dedans | Type de cette valeur |
|---|---|---|
| `x` | `5` | `int` |
| `capital` | `1000.1` | `float` |

On crée la boîte par une **affectation**. C'est un statement : rien ne s'affiche.
""")

code("x = 5")

md("Une variable s'utilise dans une expression. Python va **lire la valeur dans la boîte**.")

code("x + 1")

md("""
Une variable peut **changer de valeur**.

Python évalue **d'abord** la partie droite, **puis** range le résultat dans la boîte de gauche.
""")

code("""
x = x + 1
x
""")

md("""
Une variable peut même **changer de type**.
Beaucoup de langages l'interdisent. Python le permet, donc on vérifie ses types.
""")

code("""
x = "cinq"
type(x)
""")

md("Une affectation peut contenir **n'importe quelle expression**.")

code("""
capital = 1000 * (1 + 0.03) ** 5
capital
""")

md("""
Une variable **n'existe pas avant son affectation**.

Exécutez la cellule ci-dessous et lisez **la dernière ligne** du message.
""")

code("print(capitale)")

md("""
```
NameError: name 'capitale' is not defined
```

Python dit : ce nom n'existe pas. La variable s'appelle `capital`.
Tout ce qui précède la dernière ligne est le chemin parcouru par Python. Il ne vous concerne pas.

**Noms de variables** : minuscules, `_` entre les mots, pas d'espace, pas d'accent, pas de chiffre en premier.

### Sur papier

Prenez une feuille. Dessinez la boîte `x` avec `5` dedans.

1. On exécute `x = x + 2`. Dessinez la boîte après.
2. On exécute `x = 3.0 * x + 1.0`. Dessinez la boîte, et écrivez son type.
3. On exécute `x = str(x)`. Dessinez la boîte, et écrivez son type.

Ensuite seulement, exécutez la cellule pour vérifier.
""")

code("""
x = 5
x = x + 2
x = 3.0 * x + 1.0
x = str(x)
x
""")

code("type(x)")


md("""
## 6. L'ordre d'exécution

Exécutez la cellule de départ, puis la **cellule A**, puis la **cellule B**, puis **remontez** ré-exécuter la cellule A.
""")

code("""
revenu = 12500
cout = 5000
""")

code("""
# Cellule A
benefice = revenu - cout
benefice
""")

code("""
# Cellule B
cout = 9000
""")

md("""
Au second passage, A n'affiche plus `7500` mais `3500`. Vous n'avez pas touché à A.

> Le notebook retient ce qui a été exécuté, **dans l'ordre où ça l'a été**, pas dans l'ordre d'affichage.

**Le réflexe en cas de doute :** *Exécution → Redémarrer et tout exécuter*. Tout est recalculé de haut en bas.
""")


md("""
## 7. Appels de fonctions et modules

Un **appel de fonction** ressemble à une fonction mathématique :

```
nom(argument, argument)
```

- les **arguments** sont des **expressions**, pas seulement des valeurs ;
- ils sont séparés par des **virgules**.
""")

code("round(2 * 3.14159, 2)")

md("""
Un appel est une **expression** : il produit une valeur.

Donc il se range dans une variable, et il se met dans un autre appel.
""")

code("""
resultat = round(max(1.234, 2.345), 1)
resultat
""")

md("""
On en a déjà utilisé : `type`, `int`, `float`, `str`. Les autres du cours :

| Appel | Valeur |
|---|---|
| `round(x, n)` | `x` arrondi à `n` décimales |
| `abs(x)` | la valeur absolue |
| `max(a, b, c)`, `min(a, b, c)` | le plus grand, le plus petit |
| `len(s)` | la longueur |
""")

code("round(2.5678, 2)")

code("abs(-250)")

code("max(3, 8, 5)")

code("min(3, 8, 5)")

code('len("finance")')

md("""
### `print` est à part

`print` **affiche** et ne renvoie rien d'utile. Il prend plusieurs arguments, séparés par des virgules, et les affiche séparés par des espaces.
""")

code("""
capital = 1000
print("Capital :", capital, "euros")
""")

md("""
### Modules

Certaines fonctions sont rangées dans des **modules**, qu'on charge avec `import`.
La forme devient **`alias.fonction(arguments)`**.
""")

code("""
import numpy as np

np.sqrt(2)
""")

code("np.log(1.05)")

md("""
À la séance pandas, `pd.read_csv(...)` aura exactement cette forme.

### Prédire
""")

predire("round(2.5678, 1)", "round(1000 / 3)", "type(round(2.7))")

md("""
### Écrire

**1.** Un capital de 1 000 € placé à 3 % pendant 5 ans. Calculez sa valeur finale, arrondie à 2 décimales, **en un seul appel imbriqué**. Rangez-la dans `valeur_finale`.
""")

code("")

code("""
verifier("valeur finale", abs(valeur_finale - 1159.27) < 0.01, "revoyez la section 7 : round(expression, 2)")
""")

md("""
**2.** La mensualité d'un prêt de 200 000 € à 3 % sur 20 ans.

Formule : `capital * t / (1 - (1 + t) ** -n)`, avec `t` le taux mensuel (le taux annuel divisé par 12) et `n` le nombre de mois.

Rangez-la, arrondie à 2 décimales, dans `mensualite`.
""")

code("")

code("""
verifier("mensualite", abs(mensualite - 1109.20) < 0.01, "t = 0.03 / 12 et n = 240")
""")

md("""
**3.** La valeur absolue de `-3.14159`, arrondie à 2 décimales, **en un seul appel imbriqué**. Rangez-la dans `valeur`.
""")

code("")

code("""
verifier("valeur absolue arrondie", valeur == 3.14, "round(abs(...), 2) : un appel dans l'autre")
""")

md("""
### Corriger

Chaque cellule est fausse. Exécutez, lisez la dernière ligne, réparez.
""")

code("round(3.14159, 2")

code("Round(2.5)")


md("""
## 8. Chaînes de caractères

Les chaînes ont des fonctions à elles. C'est ce qu'on va voir.

### Ce qu'on peut faire sur une chaîne

| Écriture | Sens |
|---|---|
| `s + t` | mettre bout à bout |
| `len(s)` | le nombre de caractères |
| `"EUR" in s` | `True` si `s` contient `"EUR"` |
| `s == t` | `True` si les deux textes sont identiques |
""")

code('s = "2.5 EUR"')

code('''s + " aujourd'hui"''')

code("len(s)")

code('"EUR" in s')

code('s == "2.5 EUR"')

md("""
`+` ne marche qu'entre deux `str`. Pour coller un nombre à du texte, on le convertit d'abord : c'est l'usage de `str()`.
""")

code('"Prix : " + str(12.5)')

md("""
### Méthodes

Il y a une deuxième façon d'appeler une fonction :

```
valeur.methode(arguments)
```

La fonction est **attachée à la valeur** qui est devant le point. On l'appelle une **méthode**.
Ça marche comme un appel : c'est une expression, elle produit une valeur.

> Tout le cours pandas est fait de méthodes.

| Méthode | Effet |
|---|---|
| `s.upper()`, `s.lower()` | en majuscules, en minuscules |
| `s.strip()` | enlève les espaces au début et à la fin |
| `s.replace(ancien, nouveau)` | remplace un morceau par un autre |

Ces trois-là sont l'outillage de base pour **nettoyer une base de données** : harmoniser la casse, retirer les espaces parasites, corriger un séparateur. On s'en servira sur des colonnes entières au bloc pandas.
""")

code("s.upper()")

code("s.lower()")

code('"  AIR  ".strip()')

code('"12-03-2024".replace("-", "/")')

md("Les appels s'enchaînent, de gauche à droite.")

code('"1 250,50".replace(" ", "").replace(",", ".")')

md("""
### Positions

Les caractères d'une chaîne sont **numérotés**. Deux numérotations coexistent : depuis le début à partir de `0`, et **depuis la fin** à partir de `-1`.

Pour `s = "2.5 EUR"` :

| caractère | `2` | `.` | `5` | *espace* | `E` | `U` | `R` |
|---|---|---|---|---|---|---|---|
| **depuis le début** | `0` | `1` | `2` | `3` | `4` | `5` | `6` |
| **depuis la fin** | `-7` | `-6` | `-5` | `-4` | `-3` | `-2` | `-1` |

L'espace est un caractère comme un autre : il occupe la position `3`.

Ce numéro s'appelle un **index**. Les listes et les tableaux en auront un aussi.

| Écriture | Ce que ça prend | Valeur |
|---|---|---|
| `s[0]` | le caractère en position 0 | `"2"` |
| `s[0:3]` | de 0 inclus à 3 **exclu** | `"2.5"` |
| `s[4:]` | de 4 jusqu'au bout | `"EUR"` |
| `s[-1]` | le dernier | `"R"` |
| `s[-3:]` | les trois derniers | `"EUR"` |
| `s[:-4]` | tout sauf les quatre derniers | `"2.5"` |

Les index négatifs sont **la** façon d'attraper ce qui est à la fin d'un texte dont on ne connaît pas la longueur. Vous en aurez besoin dans le devoir.
""")

code("s[0]")

code("s[0:3]")

code("s[4:]")

code("s[-1]")

code("s[-3:]")

code("s[:-4]")

md("### Prédire")

predire('"abc".upper()', '"finance"[2:5]', '"finance"[-3:]', '"Prix : " + 12.5')

md("""
### Écrire

**1.** Transformez `"2 500,75 €"` en nombre. Rangez-le dans `prix`.
""")

code("")

code("""
verifier("prix en nombre", prix == 2500.75, "trois replace, puis float")
""")

md("""
**2.** Extrayez l'année de `"2024-03-12"`, en texte. Rangez-la dans `annee`.
""")

code("")

code("""
verifier("annee", annee == "2024", "un slicing depuis le début")
""")

md("""
---

## Pause

Vous avez fait la moitié du chemin. Jusqu'ici, **toutes** les lignes s'exécutent, une fois, de haut en bas.

La seconde moitié ajoute deux choses, et seulement deux : des lignes qui **ne s'exécutent pas toujours** (`if`), et des lignes qui s'exécutent **plusieurs fois** (`for`).

---
""")


md("""
## 9. Booléens

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

code("3 > 2")

code("3 == 3.0")

code('"EUR" in "2.5 EUR"')

md("Un booléen se range dans une variable comme n'importe quelle valeur, et s'utilise ensuite.")

code("""
rendement = 0.05
positif = rendement > 0
positif
""")

code("positif and rendement < 0.1")

md("""
`True` vaut aussi `1`, et `False` vaut `0`.

C'est ce qui permettra, à la séance pandas, de **compter** les lignes qui remplissent une condition.
""")

code("int(True)")

code("True + True")

code("True == 1")

md("""
### Prédire

Neuf cellules. Pour chacune, annoncez la valeur, puis exécutez.

**Comparaisons**
""")

predire('3 == "3"', '"EUR" == "eur"')

md("**Opérateurs**")

predire("True or False", "not (3 > 2)", "True and not False")

md("**Avec une variable**")

code("rendement = 0.05")

predire("rendement > 0 and rendement < 0.1", "not rendement > 0")

md("**Arithmétique et chaînes**")

predire("True + True + False", '"eur" in "2.5 EUR"')

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


md("""
## 10. `if`, `elif`, `else`

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


md("""
## 11. Listes

Une **liste** est une suite de valeurs entre crochets, séparées par des virgules.
""")

code('flux = [500, 700, 400, 200]')

md("""
On y accède **comme aux caractères d'une chaîne** (section 8) : même numérotation, même syntaxe, même `len`.

Pour `flux = [500, 700, 400, 200]` :

| élément | `500` | `700` | `400` | `200` |
|---|---|---|---|---|
| **depuis le début** | `0` | `1` | `2` | `3` |
| **depuis la fin** | `-4` | `-3` | `-2` | `-1` |
""")

code("flux[1]")

code("flux[1:3]")

code("len(flux)")

md("Les **index négatifs** aussi, comme sur les chaînes : `-1` est le dernier élément.")

code("flux[-1]")

code("flux[-2:]")

md("""
Une chaîne et une liste sont deux sortes de **conteneurs** : quelque chose qui contient des valeurs numérotées.

Une différence, qui servira au bloc pandas : **une liste est modifiable, une chaîne ne l'est pas.** `flux[1] = 800` marche ; `s[1] = "x"` donne une `TypeError`.
""")

code("""
flux[1] = 800
flux
""")

md("""
### Ajouter à la fin : `append`

Une méthode de la liste. Elle **modifie** la liste, et ne renvoie rien.
""")

code("""
flux.append(300)
flux
""")

md("### Fonctions utiles")

code("sum(flux)")

code("max(flux)")

code("400 in flux")

md("### La position d'une valeur : `index`")

code("flux.index(400)")

md("### Prédire")

predire("[1, 2, 3] + [4]", "[10, 20, 30][-1]", "[1, 2, 3] * 2")

md("""
Gardez le résultat de la dernière en tête : on la reverra à la section 13.

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


md("""
## 12. Répéter : `for`

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

| Morceau | Ici | Rôle |
|---|---|---|
| la **variable de boucle** | `x` | prend chaque valeur à tour de rôle |
| l'**itérable** | `flux` | ce sur quoi on passe |
| le **corps** | `print(x)` | exécuté une fois par valeur |

Le `:` en fin de ligne et le **décalage de 4 espaces** du corps font partie de la syntaxe, comme pour le `if`.

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
### Garder les résultats : un accumulateur qui est une liste

Un accumulateur n'est pas forcément un nombre. Si on veut **un résultat par élément**, on part d'une liste vide et on `append` à chaque tour.
""")

code("""
plus_un = []
for x in flux:
    plus_un.append(x + 1)
plus_un
""")

md("""
> **Le motif qui reviendra tout le cours : une liste vide avant, `append` dedans, le résultat après.**

### Passer sur les positions : `range`

`range(n)` fabrique l'itérable des positions `0, 1, ..., n-1`. C'est son seul rôle.
""")

code("list(range(4))")

md("""
Premier usage : **lire deux listes en parallèle**, à la même position. La variable de boucle est alors un **numéro**, pas une valeur.
""")

code("""
depenses = [120, 90, 200]
recettes = [500, 700, 400]

for i in range(len(depenses)):
    print(i, recettes[i] - depenses[i])
""")

md("""
Second usage : **répéter `n` fois**, sans liste du tout.
""")

code("""
capital = 1000
for annee in range(10):
    capital = capital * 1.03
capital
""")

md("""
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

Formule de la section 7 : `capital * t / (1 - (1 + t) ** -n)`, avec `t` le taux mensuel et `n = 240`.
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


md("""
## 13. Passerelle vers pandas : la Series

Une **Series**, c'est une liste qui a **une étiquette par valeur** et qui **sait faire des maths sur elle-même**.
""")

code("""
serie = pd.Series(mensualites, index=taux)
serie
""")

md("Même signe `*`, deux types, deux opérations. C'est la définition d'un type, vue à la section 2.")

code("[1, 2, 3] * 2")

code("pd.Series([1, 2, 3]) * 2")

md("Les méthodes d'une Series : les mêmes noms que les fonctions sur les listes.")

code("serie.mean()")

code("serie.max()")

md("Et un graphique, en une ligne.")

code("serie.plot()")

md("""
## 14. Ce que vous savez faire

**Les valeurs et les variables**

| Vous voulez... | Vous écrivez |
|---|---|
| afficher | `print("Capital :", capital)` |
| connaître un type | `type(x)` |
| convertir | `int("3")`, `float("2.5")`, `str(12)` |
| créer ou modifier une variable | `x = 5`, `x = x + 1` |
| appeler une fonction | `round(x, 2)`, `max(a, b)`, `len(s)` |
| charger un module | `import numpy as np`, puis `np.sqrt(2)` |

**Le texte**

| Vous voulez... | Vous écrivez |
|---|---|
| une méthode sur une chaîne | `s.upper()`, `s.strip()`, `s.replace(",", ".")` |
| un morceau de chaîne | `s[0:3]`, `s[4:]` |
| la fin d'une chaîne | `s[-1]`, `s[-4:]`, `s[:-1]` |

**Décider**

| Vous voulez... | Vous écrivez |
|---|---|
| comparer | `a > b`, `a == b`, `a != b` |
| combiner des conditions | `a > 0 and a < 1`, `not a` |
| exécuter selon une condition | `if a > b:` |
| deux issues, plus de deux | `if ... :` `else:` · `if ... :` `elif ... :` `else:` |
| afficher avec des valeurs | `f"Taux : {taux:.1%}"`, `f"{x:.2f}"` |

**Répéter**

| Vous voulez... | Vous écrivez |
|---|---|
| une liste | `flux = [500, 700, 400]` |
| un élément, une tranche | `flux[0]`, `flux[1:3]`, `flux[-1]` |
| ajouter à la fin | `flux.append(300)` |
| passer sur chaque élément | `for x in flux:` |
| passer sur les positions | `for i in range(len(flux)):` |
| répéter n fois | `for i in range(n):` |
| accumuler | `total = 0` avant, `total = total + x` dedans |
| garder les résultats | `resultats = []` avant, `resultats.append(...)` dedans |
| une Series, la tracer | `pd.Series(resultats, index=taux)`, `serie.plot()` |

## Cinq réflexes

1. **`=` affecte, `==` compare.**
2. **Seule la dernière ligne d'une erreur compte.**
3. **En cas de doute, Redémarrer et tout exécuter.** Le notebook retient l'ordre d'exécution, pas l'ordre d'affichage.
4. **Un résultat bizarre : `type()`.** Le type décide de ce que les opérations font.
5. **Une variable de boucle est une boîte à part.** Pour garder un résultat, il faut un accumulateur.
""")

md("""
## Avant le travail noté

À faire chez vous, avant d'ouvrir le sujet. Cinq cellules à prédire, deux à écrire.
""")

predire("int(7.9) + 1", 'str(3) + str(4)', "round(10 / 4, 1)", '"finance"[0] + "finance"[4:]', '"2026-09-16"[-2:]')

md("""
**1.** Un placement de 5 000 € à 2 % pendant 3 ans. Sa valeur finale, arrondie à 2 décimales, dans `placement`.

**2.** Le texte `"3,5 %"` en nombre décimal `3.5`, dans `taux`.
""")

code("")

code("""
verifier("placement", abs(placement - 5306.04) < 0.01, "5000 * (1 + 0.02) ** 3")
verifier("taux", taux == 3.5, "replace, puis float")
""")

md("""
## La suite

Le **travail noté** : un simulateur de prêt, construit sur le taux directeur de la Banque centrale européenne du jour. Tout ce qu'il demande est dans ce notebook.

Le **bonus** ci-dessous est facultatif et ne sert pas au devoir.
""")


md("""
---

## Bonus facultatif — un convertisseur de devises

> **Facultatif. Non noté. Rien dans la suite du cours n'en dépend** — ni le travail noté, ni le bloc pandas.\n>\n> À faire chez vous si le cœur vous en dit. On n'y touche pas en classe.

On assemble tout ce qui précède : une cellule de paramètres en haut, une phrase en bas, et on peut changer les paramètres. Les taux viennent d'un service web gratuit.

### Une méthode de plus : `find`

Jusqu'ici, pour découper une chaîne, on comptait les positions à la main. Quand on ne les connaît pas, on cherche un **point de repère** dans le texte.

`s.find(morceau)` renvoie la **position** où commence le morceau, ou `-1` s'il n'y est pas.
""")

code('"2.5 EUR".find("EUR")')

code('"2.5 EUR".find("$")')

md("""
Combinée à un slicing, elle permet d'extraire ce qui suit un repère :

```python
t = '{"EUR":2.1567}'
debut = t.find('"EUR":') + len('"EUR":')   # juste après le repère
t[debut:]                                   # '2.1567}'
```

### Étape 1 : les paramètres
""")

code("""
devise_depart = "USD"
devise_arrivee = "EUR"
montant = 2.5
""")

md("""
### Étape 2 : l'adresse

Le service attend une adresse de cette forme :

```
https://api.frankfurter.dev/v1/latest?amount=2.5&from=USD&to=EUR
```

On la construit par concaténation, avec les trois paramètres. `str(montant)` est obligatoire.
""")

code("""
url = "https://api.frankfurter.dev/v1/latest?amount=" + str(montant) + "&from=" + devise_depart + "&to=" + devise_arrivee
url
""")

md("""
### Étape 3 : la réponse

Deux lignes fournies. Elles vont chercher la page et rangent son texte dans `reponse`.
""")

code("""
import requests

reponse = requests.get(url).text
print(reponse)
""")

md("""
Si le réseau ne répond pas, exécutez cette cellule de secours à la place :
""")

code("""
# reponse = '{"amount":2.5,"base":"USD","date":"2026-09-11","rates":{"EUR":2.1567}}'
""")

md("""
### Étape 4 : le nombre

Dans `reponse`, le nombre qui nous intéresse commence juste après le texte `"EUR":` et se termine juste avant `}`.

Avec `find`, `len`, un slicing et `float`, rangez ce nombre dans `resultat`. Deux repères : `'"EUR":'` pour le début, `"}"` pour la fin.
""")

code("")

code("""
verifier("resultat", type(resultat) == float and resultat > 0, "find pour le début, find pour la fin, slicing, float")
""")

md("""
### Étape 5 : la phrase

Par concaténation, construisez la phrase suivante dans `phrase`, puis affichez-la :

```
Vous pouvez échanger 2.5 USD contre 2.16 EUR.
```

`str()` pour les nombres, `round(resultat, 2)` pour l'arrondi. Le point final compte.
""")

code("")

code("""
verifier("phrase", phrase.startswith("Vous pouvez échanger 2.5 USD contre") and phrase.endswith("EUR."), "concaténation, str(), round(resultat, 2)")
""")

md("""
### Étape 6 : la machine

Remontez à l'étape 1. Mettez `"GBP"` comme devise d'arrivée. *Exécution → Redémarrer et tout exécuter*.

Ça plante à l'étape 4 : le texte cherché est toujours `"EUR":`.
Remplacez `'"EUR":'` par `'"' + devise_arrivee + '":'`, et relancez tout. Essayez `"JPY"`, `"CHF"`, `1000`.
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
