import json, os, textwrap

OUT = "python/cours/seance1_cours.ipynb"
LOGO = '<img src="https://cdn.jsdelivr.net/gh/aureliensalas/python_finance@main/ressources/img/logo_macmia.png" alt="Banque des Territoires · France 2030 · MACMIA" width="520">'
BADGE = "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aureliensalas/python_finance/blob/main/python/cours/seance1_cours.ipynb)"

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

# ---------------------------------------------------------------- en-tête
md(f"""
{LOGO}

{BADGE}

# Séance 1 : Python calcule

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
- lire la dernière ligne d'un message d'erreur

> **Les cellules « Prédire ».** Avant de les exécuter, on annonce **à voix haute** la valeur attendue. Rien à écrire : on dit, on exécute, on compare.

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
""")

# ---------------------------------------------------------------- 0. Colab
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

# ---------------------------------------------------------------- 1. Expressions
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

# ---------------------------------------------------------------- 2. Types
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
| `bool` | `True`, `False`, majuscule obligatoire | `and` `or` `not` | produit par les comparaisons ; séance 2 |
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

# ---------------------------------------------------------------- 3. Conversions
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

# ---------------------------------------------------------------- 4. Expression et statement
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

# ---------------------------------------------------------------- 5. Variables
md("""
## 5. Variables et affectation

Une **variable**, c'est une boîte. Elle a un **nom**, et une **valeur** dedans.

<table style="border-collapse:separate;border-spacing:40px 0">
<tr>
<td align="center"><b><code>x</code></b><br>
<div style="border:3px solid #2878B5;border-radius:8px;padding:14px 30px;font-size:22px;background:#EAF2FA">5</div>
<small>int</small></td>
<td align="center"><b><code>capital</code></b><br>
<div style="border:3px solid #2878B5;border-radius:8px;padding:14px 30px;font-size:22px;background:#EAF2FA">1000.1</div>
<small>float</small></td>
</tr>
</table>

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

# ---------------------------------------------------------------- 6. Ordre d'exécution
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

# ---------------------------------------------------------------- 7. Fonctions et modules
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
### Corriger

Chaque cellule est fausse. Exécutez, lisez la dernière ligne, réparez.
""")

code("round(3.14159, 2")

code("Round(2.5)")

# ---------------------------------------------------------------- 8. Chaînes
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

Les caractères sont **numérotés à partir de 0**.

```
 s  =  "2.5 EUR"
        0123456
```

| Écriture | Valeur |
|---|---|
| `s[0]` | le caractère en position 0 |
| `s[0:3]` | de la position 0 incluse à 3 **exclue** |
| `s[4:]` | de la position 4 jusqu'au bout |

Ce numéro s'appelle un **index**. Les listes et les tableaux en auront un aussi.

### Compter depuis la fin : les index négatifs

On peut aussi numéroter **en partant de la fin**. `-1` est le dernier caractère, `-2` l'avant-dernier.

```
 s  =  "2.5 EUR"

         2   .   5   ␣   E   U   R
         0   1   2   3   4   5   6     depuis le début
        -7  -6  -5  -4  -3  -2  -1     depuis la fin
```

(`␣` est l'espace : c'est un caractère comme un autre, en position 3.)

| Écriture | Valeur |
|---|---|
| `s[-1]` | le dernier caractère |
| `s[-3:]` | les trois derniers |
| `s[:-4]` | tout sauf les quatre derniers |
| `s[-7:-4]` | du 7ᵉ avant la fin au 4ᵉ avant la fin, exclu |

C'est **la** façon d'attraper quelque chose qui est à la fin d'un texte dont on ne connaît pas la longueur. Vous en aurez besoin dans le devoir.
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

# ---------------------------------------------------------------- 9. Synthèse
md("""
## 9. Ce que vous savez faire

| Vous voulez... | Vous écrivez |
|---|---|
| afficher | `print("Capital :", capital)` |
| connaître un type | `type(x)` |
| convertir | `int("3")`, `float("2.5")`, `str(12)` |
| créer ou modifier une variable | `x = 5`, `x = x + 1` |
| appeler une fonction | `round(x, 2)`, `max(a, b)`, `len(s)` |
| charger un module | `import numpy as np`, puis `np.sqrt(2)` |
| une méthode sur une chaîne | `s.upper()`, `s.strip()`, `s.replace(",", ".")` |
| un morceau de chaîne | `s[0:3]`, `s[4:]` |
| la fin d'une chaîne | `s[-1]`, `s[-4:]`, `s[:-1]` |
| tout recalculer proprement | *Exécution → Redémarrer et tout exécuter* |

## Trois réflexes

1. **Seule la dernière ligne d'une erreur compte.**
2. **En cas de doute, Redémarrer et tout exécuter.** Le notebook retient l'ordre d'exécution, pas l'ordre d'affichage.
3. **Un résultat bizarre : `type()`.** Le type décide de ce que les opérations font.

## Pour la prochaine séance

Cinq cellules à prédire, deux à écrire. Corrigées en début de séance 2.
Le **bonus** en fin de notebook est facultatif.
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

# ---------------------------------------------------------------- Bonus
md("""
---

## Bonus — un convertisseur de devises

**Facultatif, non noté.** À faire chez vous si le cœur vous en dit. Rien dans la suite du cours n'en dépend.

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

# ---------------------------------------------------------------- écriture
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
