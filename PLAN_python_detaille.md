# Python en 4h : plan détaillé, cellule par cellule

Ce document remplace les sections Python de `PLAN_python_pandas_20h.md`, qui reste la référence pour la méthode générale (section 1) et pour pandas (sections 7 à 11).

Public : étudiants en finance, niveau programmation nul, Colab sur ordinateur ou tablette.
Format : deux notebooks de cours avec exercices inclus, un notebook d'assignment, corrections publiées après.

---

## 0. Décisions prises

**Budget.** 20h au total : Python 4h, pandas 4h, stats 4h, ML 4h, révision 4h. Sur les 4h de révision, 1h sert à lancer en classe l'assignment Python noté, qui se termine à la maison.

**Ce qu'on bourrine.** Appels de fonctions, booléens, `if`, `for`, Series. Pas les chaînes : 20 minutes, parce qu'un étudiant en finance n'en a besoin que pour trois méthodes.

**Ce qu'on n'enseigne pas.** `//`, `%`, indices négatifs, tuples, dicts, `while`, `def`, compréhensions, `input()`, `break`. Les chaînes de formatage se limitent à `{x:.2f}` et `{x:.1%}`.

**Ton.** Manuel, neutre. Une définition en une phrase, un ou deux exemples, on avance. Pas de « Votre mission », pas de chute dramatique, pas d'emojis de catégorie. Les énoncés sont à l'impératif : « Calculez ... Rangez le résultat dans `x`. »

**Exercices.** Jamais de texte à trous. Trois formats seulement :

- *Prédire* : l'étudiant écrit en commentaire ce que la cellule va afficher, puis exécute. Pas de cellule de vérification.
- *Écrire* : une cellule vide, un énoncé d'une ou deux lignes, une cellule `verifier` après.
- *Corriger* : une cellule fausse, à exécuter, lire, réparer.

`verifier(nom, condition, indice)` garde la forme actuelle. L'indice renvoie à la section du cours, jamais à la réponse. Les comparaisons de flottants passent par `abs(a - b) < 0.01`.

**Vocabulaire fixe.** Huit mots, jamais de synonyme : expression, valeur, type, variable, affectation, appel, argument, méthode. Glossaire en tête de chaque notebook.

**Convertisseur.** Petit exercice de 15 minutes en fin de P1, non noté, en mode démonstration guidée.

**Assignment.** Simulateur de prêt, section 3. Un taux réel récupéré chez la BCE, des paramètres qui arrivent en texte, `if`, `for`, Series, courbe.

---

## 1. Séance P1 (2h) : Python calcule

| Section | Minutes | Cumul |
|---|---|---|
| P1.0 Colab | 10 | 10 |
| P1.1 Expressions et valeurs | 5 | 15 |
| P1.2 Types | 15 | 30 |
| P1.3 Conversions | 5 | 35 |
| P1.4 Expression et statement | 5 | 40 |
| P1.5 Variables et affectation | 15 | 55 |
| P1.6 Ordre d'exécution | 5 | 60 |
| P1.7 Appels de fonctions et modules | 20 | 80 |
| P1.8 Chaînes | 20 | 100 |
| P1.9 Convertisseur | 15 | 115 |
| P1.10 Synthèse | 5 | 120 |

Points de coupe si retard, dans l'ordre : le convertisseur devient une démonstration de 5 minutes faite par l'enseignant ; la pause-exercice 3 de P1.7 passe en devoir ; les exercices de chaînes passent en échauffement de P2.

### P1.0 Colab, 10 min

Cellule texte : « Fichier, Enregistrer une copie dans Drive ». Cellule texte et cellule code. `Maj + Entrée` exécute et passe à la suivante. `+ Code` ajoute une cellule. Sur tablette, la page « Bien démarrer » d'abord.

Une cellule code à exécuter :

```python
print("Bonjour")
```

On ne présente pas Markdown. On dit que les cellules de texte se tapent en texte brut et que `##` fait un titre, c'est tout.

Cellule de setup, à exécuter sans la comprendre, annoncée comme telle :

```python
import numpy as np
import pandas as pd

def verifier(nom, condition, indice=""):
    if condition:
        print("OK -", nom)
    else:
        print("A REVOIR -", nom, ":", indice)
```

### P1.1 Expressions et valeurs, 5 min

Texte : une expression représente quelque chose. Python l'évalue et la transforme en valeur, comme une calculatrice. Colab affiche la valeur de la dernière ligne de la cellule.

```python
2.2
```

```python
(3 * 7 + 1) / 10
```

Texte : deux expressions différentes, la même valeur. Opérateurs : `+ - * / **` et les parenthèses. Puissance avant multiplication et division, avant addition et soustraction, comme en maths.

Pas d'exercice.

### P1.2 Types, 15 min

Texte :

```python
3 + 4
```

```python
"Hello" + "World"
```

Le même signe `+`, et deux choses de nature différente : une addition, une mise bout à bout. Python a fait ça parce que les valeurs n'ont pas le même type. C'est l'idée de base de la programmation : chaque valeur a un type, et le type décide de ce que les opérations font.

Définition : un type, c'est un ensemble de valeurs et des opérations sur ces valeurs. `type(...)` donne le type d'une valeur.

```python
type(3), type("Hello")
```

Les quatre types du cours, une cellule texte de trois lignes et une cellule code pour chacun :

**`int`.** Valeurs : les nombres entiers, sans point. Opérations : `+ - * / **`. La division `/` donne toujours un `float`.

```python
type(7), type(7 / 7)
```

**`float`.** Valeurs : les nombres avec un point décimal. `2` et `2.0` ont la même valeur mathématique et pas le même type. Opérations : `+ - * / **`.

```python
type(2), type(2.0), 2 == 2.0
```

**`bool`.** Valeurs : `True` et `False`, majuscule obligatoire. Opérations : `and`, `or`, `not`. Ce qui en produit : les comparaisons `< <= > >= == !=`. On y revient en P2.

```python
3 > 2, type(3 > 2)
```

**`str`.** Valeurs : du texte, entre guillemets doubles ou simples. Opération : `+`, qui met bout à bout, entre deux `str` seulement.

```python
"Hello" + " " + "World", type("Hello")
```

On ne montre pas `"3" + "4"`, ni `2 * "3"`, ni `3 + "4"`. Le piège des nombres en texte attend la séance pandas de nettoyage.

**Pause-exercice 1, 5 min.** *Prédire* le type, puis vérifier avec `type(...)` :

```python
7
```
```python
7.0
```
```python
7 / 7
```
```python
7 > 3
```
```python
"7"
```
```python
"sept" + "huit"
```

### P1.3 Conversions, 5 min

Texte : on change le type d'une valeur avec un appel de la forme `type(expression)`.

```python
float(2), int(2.6), str(2), float("2.5")
```

Les types s'emboîtent du plus étroit au plus large : `bool` dans `int` dans `float`. Vers le plus large, Python convertit tout seul, parce qu'on ne perd rien :

```python
1 / 2.0
```

Vers le plus étroit, Python ne le fait jamais seul, parce qu'on perd de l'information : `int(2.6)` donne `2`, il faut l'écrire.

Pas d'exercice.

### P1.4 Expression et statement, 5 min

Texte : une expression représente quelque chose, Python l'évalue, le résultat est une valeur : `2.3`, `3 + 5 / 4`. Un statement fait quelque chose, Python l'exécute, et il n'y a pas forcément de valeur au bout.

```python
print("Hello")
```

Dans Colab, la dernière expression d'une cellule s'affiche. Un statement n'affiche rien par lui-même.

### P1.5 Variables et affectation, 15 min

Texte : une variable, c'est une boîte. Elle a un nom, et une valeur dedans.

Dessin dans une cellule texte (bloc HTML coloré, ou image dans `ressources/img/`) :

```
 x                    capital
┌───────┐            ┌──────────┐
│   5   │  int       │  1000.1  │  float
└───────┘            └──────────┘
```

On crée la boîte par une affectation. C'est un statement : rien ne s'affiche.

```python
x = 5
```

Une variable s'utilise dans une expression. Python va lire la valeur dans la boîte.

```python
x + 1
```

Une variable peut changer de valeur. Python évalue d'abord la droite, puis range le résultat dans la boîte de gauche.

```python
x = x + 1
x
```

Une variable peut même changer de type. Beaucoup de langages l'interdisent, Python le permet, donc on vérifie ses types.

```python
x = "cinq"
type(x)
```

Une affectation peut contenir n'importe quelle expression.

```python
capital = 1000 * (1 + 0.03) ** 5
capital
```

Une variable n'existe pas avant son affectation. Lire la dernière ligne du message.

```python
print(capitale)
```

Règles de nommage en une ligne : minuscules, `_`, pas d'espace, pas d'accent, pas de chiffre en premier.

**Exercice papier, 5 min.** Sur une feuille. Dessinez la boîte `x` avec `5` dedans. On exécute `x = x + 2` : dessinez la boîte après. Puis `x = 3.0 * x + 1.0` : dessinez la boîte et écrivez son type. Puis `x = str(x)` : même chose. Ensuite seulement, on exécute.

```python
x = 5
x = x + 2
x = 3.0 * x + 1.0
x = str(x)
x, type(x)
```

### P1.6 Ordre d'exécution, 5 min

Deux cellules, la démonstration du cours actuel :

```python
# Cellule A
benefice = revenu - cout
benefice
```

```python
# Cellule B
cout = 9000
```

Consigne : exécuter A, puis B, puis remonter exécuter A. Le résultat de A a changé sans qu'on la modifie. Le notebook retient ce qui a été exécuté, dans l'ordre où ça l'a été, pas dans l'ordre d'affichage. Réflexe : « Exécution, Redémarrer et tout exécuter ».

Il faut que `revenu` et `cout` existent : une cellule au-dessus, `revenu = 12500` et `cout = 5000`.

### P1.7 Appels de fonctions et modules, 20 min

Première section à bourriner.

Texte : un appel de fonction ressemble à une fonction mathématique : `nom(argument, argument)`. Les arguments sont des expressions, pas seulement des valeurs, séparés par des virgules.

```python
round(2 * 3.14159, 2)
```

Un appel est une expression : il produit une valeur. Donc il se range dans une variable, et il se met dans un autre appel.

```python
resultat = round(max(1.234, 2.345), 1)
resultat
```

On en a déjà utilisé : `type`, `int`, `float`, `str`. Les autres du cours :

```python
round(2.5678, 2), abs(-250), max(3, 8, 5), min(3, 8, 5), len("finance")
```

`print` est à part : il affiche et ne renvoie rien d'utile. Il prend plusieurs arguments, séparés par des virgules, et les affiche séparés par des espaces.

```python
capital = 1000
print("Capital :", capital, "euros")
```

Modules : certaines fonctions sont rangées dans des modules, qu'on charge avec `import`. Forme `alias.fonction(arguments)`.

```python
import numpy as np
np.sqrt(2), np.log(1.05), np.exp(0.05)
```

Finance en une cellule : capitalisation continue et rendement logarithmique.

```python
1000 * np.exp(0.05 * 3), np.log(105 / 100)
```

En séance pandas, `pd.read_csv(...)` aura exactement cette forme.

**Pause-exercice 2, 5 min.** *Prédire* :

```python
round(2.5678, 1)
```
```python
max(3, 8, 5)
```
```python
len("finance")
```
```python
round(1000 / 3)
```
```python
type(round(2.7))
```
```python
round(np.sqrt(2), 3)
```

**Pause-exercice 3, 5 min.** *Écrire* :

1. La valeur finale d'un capital de 1 000 € placé à 3 % pendant 5 ans, arrondie à 2 décimales, en un seul appel imbriqué. Rangez-la dans `valeur_finale`. Attendu : `1159.27`.
2. La mensualité d'un prêt de 200 000 € à 3 % sur 20 ans. Formule : `capital * t / (1 - (1 + t) ** -n)`, avec `t` le taux mensuel (le taux annuel divisé par 12) et `n` le nombre de mois. Arrondie à 2 décimales dans `mensualite`. Attendu : `1109.20`.

*Corriger* :

```python
round(3.14159, 2
```
```python
Round(2.5)
```

### P1.8 Chaînes, 20 min

On y arrive par les fonctions : les chaînes ont des fonctions à elles.

**Ce qu'on peut faire sur une chaîne, 10 min.**

Opérations et fonctions :

```python
s = "2.5 EUR"
s + " aujourd'hui", len(s), "EUR" in s, s == "2.5 EUR"
```

`+` ne marche qu'entre deux `str`. C'est l'usage de `str()` :

```python
"Prix : " + str(12.5)
```

Méthodes : une deuxième façon d'appeler une fonction, `valeur.methode(arguments)`. La fonction est attachée à la valeur devant le point. Ça marche comme un appel : c'est une expression, elle produit une valeur. Tout le cours pandas est fait de méthodes.

```python
s.upper(), s.lower(), "  AIR  ".strip(), "12-03-2024".replace("-", "/")
```

Les appels s'enchaînent de gauche à droite :

```python
"1 250,50".replace(" ", "").replace(",", ".")
```

Positions : les caractères sont numérotés à partir de 0. `s[0]` est le premier, `s[2:5]` va de la position 2 incluse à 5 exclue, `s[4:]` va jusqu'au bout. `s.find(morceau)` donne la position où commence le morceau.

```python
s[0], s[0:3], s[4:], s.find(" ")
```

On dit que ce numéro s'appelle un index et que les listes et les tableaux en auront un aussi.

**Exercices, 10 min.**

*Prédire* :

```python
"abc".upper()
```
```python
"12-03-2024".replace("-", "/")
```
```python
"finance"[2:5]
```
```python
"2.5 EUR".find("EUR")
```
```python
"Prix : " + 12.5
```

*Écrire* :

1. `"2 500,75 €"` en nombre, dans `prix`. Attendu : `2500.75`.
2. L'année de `"2024-03-12"`, dans `annee`, en texte. Attendu : `"2024"`.

### P1.9 Le convertisseur, 15 min

Exercice guidé, non noté. L'enseignant fait les étapes 1 à 3 en direct, les étudiants font 4 et 5, puis tout le monde joue avec 6.

Service : Frankfurter, données BCE, sans clé. Testé le 11 septembre 2026.

Étape 1, fournie :

```python
devise_depart = "USD"
devise_arrivee = "EUR"
montant = 2.5
```

Étape 2, ensemble : l'adresse, par concaténation. `str(montant)` obligatoire.

```python
url = "https://api.frankfurter.dev/v1/latest?amount=" + str(montant) + "&from=" + devise_depart + "&to=" + devise_arrivee
url
```

Étape 3, fournie, annoncée comme une recette :

```python
import requests
reponse = requests.get(url).text
print(reponse)
```

Affiche : `{"amount":2.5,"base":"USD","date":"2026-09-11","rates":{"EUR":2.1567}}`

Étape 4, *écrire* : le nombre. La consigne dit : « le nombre commence juste après le texte `"EUR":` et se termine juste avant `}`. Utilisez `find`, `len`, un slicing, `float`. Rangez-le dans `resultat`. »

```python
debut = reponse.find('"EUR":') + len('"EUR":')
fin = reponse.find("}")
resultat = float(reponse[debut:fin])
resultat
```

Étape 5, *écrire* : la phrase, par concaténation, dans `phrase`. Attendu : `Vous pouvez échanger 2.5 USD contre 2.16 EUR.`

```python
phrase = "Vous pouvez échanger " + str(montant) + " " + devise_depart + " contre " + str(round(resultat, 2)) + " " + devise_arrivee + "."
print(phrase)
```

Étape 6, la machine : changer les trois valeurs de l'étape 1, « Redémarrer et tout exécuter ». Avec `"GBP"`, ça plante à l'étape 4 : le texte cherché est `"EUR":`. On fait remplacer `'"EUR":'` par `'"' + devise_arrivee + '":'`, et ça marche pour tout.

Cellule de secours si le réseau tombe : `reponse = '{"amount":2.5,"base":"USD","date":"2026-09-11","rates":{"EUR":2.1567}}'`.

### P1.10 Synthèse, 5 min

Tableau « vous voulez / vous écrivez » : afficher, connaître un type, convertir, créer une variable, appeler une fonction, importer un module, une méthode sur une chaîne.

Devoir, cinq cellules à prédire et deux à écrire, sur P1.5 et P1.7. Corrigé à l'échauffement de P2.

---

## 2. Séance P2 (2h) : Python décide et répète

| Section | Minutes | Cumul |
|---|---|---|
| P2.0 Échauffement | 10 | 10 |
| P2.1 Booléens | 20 | 30 |
| P2.2 if, elif, else | 25 | 55 |
| P2.3 Listes | 20 | 75 |
| P2.4 for | 30 | 105 |
| P2.5 Passerelle Series | 10 | 115 |
| P2.6 Synthèse, annonce de l'assignment | 5 | 120 |

Points de coupe : la démonstration « ajouter 1 à chaque élément » de P2.4 ; `index()` dans P2.3 ; le deuxième exercice de P2.2.

### P2.0 Échauffement, 10 min

Correction du devoir à l'oral. Puis trois cellules : une chaîne à nettoyer en nombre, un appel imbriqué à écrire, une erreur à corriger (`print(capital` sans parenthèse fermante).

### P2.1 Booléens, 20 min

**Cours, 5 min.**

Deux valeurs, `True` et `False`. Trois opérations, `and`, `or`, `not`. Table de vérité au tableau, quatre lignes.

Ce qui produit un booléen : les comparaisons `< <= > >= == !=`, et `in`. `=` affecte, `==` compare.

```python
3 > 2, 3 == 3.0, "EUR" in "2.5 EUR"
```

Un booléen se range dans une variable comme n'importe quelle valeur, et s'utilise ensuite.

```python
rendement = 0.05
positif = rendement > 0
positif, positif and rendement < 0.1
```

`True` vaut aussi 1 et `False` vaut 0. C'est ce qui permettra de compter des lignes dans un tableau.

```python
int(True), True + True, True == 1
```

**Bourrinage, 15 min.** Vingt cellules à *prédire*, en cinq paquets. On corrige paquet par paquet.

Comparaisons :

```python
3 > 2
```
```python
3 == 3.0
```
```python
3 == "3"
```
```python
"EUR" == "eur"
```
```python
2.5 >= 2.5
```

Opérateurs :

```python
True and False
```
```python
True or False
```
```python
not (3 > 2)
```
```python
(3 > 2) or (2 > 3)
```
```python
True and not False
```

Avec variables (`rendement = 0.05` au-dessus) :

```python
rendement > 0 and rendement < 0.1
```
```python
rendement > 0.1 or rendement < -0.1
```
```python
not rendement > 0
```

Arithmétique :

```python
True + True + False
```
```python
(3 > 2) + (2 > 1)
```
```python
int(False), float(True)
```

Chaînes :

```python
"EUR" in "2.5 EUR"
```
```python
"eur" in "2.5 EUR"
```
```python
"2.5 EUR".find("$") == -1
```

*Écrire* : `eligible = revenu > 30000 and age < 65`, avec `revenu = 42000` et `age = 40`. Attendu : `True`.

*Corriger* : `True and false`.

### P2.2 if, elif, else, 25 min

**Cours, 12 min.**

Texte : jusqu'ici, toutes les lignes s'exécutent. Avec `if`, certaines ne s'exécutent pas. Il faut distinguer la structure du programme, ce qui est écrit, et son flux, ce qui s'exécute. On l'a déjà vu autrement : les cellules s'exécutent dans l'ordre où on les exécute, pas dans l'ordre où elles sont écrites.

Forme :

```
if expression:
    statement
    statement
```

Si l'expression vaut `True`, Python exécute les statements décalés en dessous. Sinon, il les saute. Le `:` et le décalage de 4 espaces font partie de la syntaxe.

Trois formes, chacune avec son cas d'usage et un exemple.

`if` seul : une action optionnelle. Il peut ne rien se passer.

```python
van = -1500
if van < 0:
    print("Le projet détruit de la valeur.")
print("Analyse terminée.")
```

`if / else` : deux issues, exactement une s'exécute. Rien n'est optionnel.

```python
if van > 0:
    print("On investit.")
else:
    print("On n'investit pas.")
```

`if / elif / else` : une extension du `if / else` quand il y a une condition de plus.

```python
rendement = 0.12
if rendement > 0.10:
    verdict = "excellent"
elif rendement > 0:
    verdict = "positif"
else:
    verdict = "perte"
verdict
```

Le piège de l'ordre : Python s'arrête à la première condition vraie.

```python
if rendement > 0:
    verdict = "positif"
elif rendement > 0.10:
    verdict = "excellent"
else:
    verdict = "perte"
verdict
```

Avec `0.12`, la deuxième branche est inatteignable. Si on veut que plusieurs conditions puissent être vraies en même temps, on écrit plusieurs `if` séparés.

```python
if rendement > 0.10:
    print("Rendement excellent.")
if rendement > 0.08:
    print("Au-dessus de l'objectif.")
```

f-strings, ici, pour afficher un verdict avec des nombres dedans. Deux formats seulement.

```python
print(f"Rendement de {rendement:.1%} : {verdict}.")
print(f"Mensualité : {1109.2:.2f} euros.")
```

**Exercices, 13 min.**

*Écrire* :

1. Le maximum de deux nombres, sans `max`. Avec `a = 12` et `b = 7`, comparez-les et rangez le plus grand dans `plus_grand`. Attendu : `12`.
2. Le maximum de trois nombres, sans `max`. `a = 12`, `b = 7`, `c = 15`. Rangez-le dans `plus_grand_3`. Attendu : `15`. C'est un `if / elif / else`.
3. Le signe d'un rendement : `"hausse"`, `"baisse"` ou `"stable"`, dans `signe`, pour `rendement = -0.02`. Attendu : `"baisse"`.

*Corriger* :

```python
if taux = 0.03:
    print("trois pour cent")
```
```python
if taux > 0.03
    print("plus de trois pour cent")
```
```python
if taux > 0.03:
print("plus de trois pour cent")
```

### P2.3 Listes, 20 min

**Cours, 12 min.**

Texte : une liste est une suite de valeurs entre crochets, séparées par des virgules.

```python
flux = [500, 700, 400, 200]
```

On y accède comme aux caractères d'une chaîne : même syntaxe, même numérotation à partir de 0, même `len`.

```python
flux[1], flux[1:3], len(flux)
```
```python
s = "abcd"
s[1], s[1:3], len(s)
```

Une chaîne et une liste sont deux sortes de conteneurs : quelque chose qui contient des valeurs numérotées. La différence est ce qu'on peut mettre dedans, et une chose de plus.

Une liste est modifiable. Une chaîne ne l'est pas.

```python
flux[1] = 800
flux
```
```python
s[1] = "x"
```

La deuxième cellule donne `TypeError`. On lit la dernière ligne.

Ajouter à la fin : `append`, une méthode de la liste.

```python
flux.append(300)
flux
```

Fonctions utiles, les mêmes que sur les nombres :

```python
sum(flux), max(flux), min(flux), 400 in flux
```

La position d'une valeur : `index`, une méthode.

```python
flux.index(400)
```

**Exercices, 8 min.**

*Prédire* :

```python
[1, 2, 3] + [4]
```
```python
[10, 20, 30][2]
```
```python
len([])
```
```python
[1, 2, 3] * 2
```

On garde le résultat de la dernière en tête : on la reverra en P2.5.

*Écrire* : quatre flux de trésorerie `[1200, 800, 1500, 900]` dans `flux`. Remplacez le troisième par `1600`. Ajoutez `700`. Rangez la somme dans `total` et la position du plus grand dans `position_max`. Attendus : `5200`, `2`.

### P2.4 for, 30 min

**Cours, 18 min.**

Texte : on veut calculer la somme d'une liste nous-mêmes, sans `sum`. Problème : une liste peut avoir n'importe quelle taille. On ne peut pas écrire `flux[0] + flux[1] + ...` sans savoir où s'arrêter. Il faut une instruction qui passe sur chaque élément, quelle que soit la taille.

La boucle la plus simple du monde :

```python
for x in flux:
    print(x)
```

Trois morceaux, à nommer et à répéter : l'itérable (`flux`, ce sur quoi on passe), la variable de boucle (`x`, qui prend chaque valeur à tour de rôle), le corps (les lignes décalées, exécutées une fois par valeur).

L'itérable doit être quelque chose sur quoi on peut passer. Un nombre, non :

```python
for x in 5:
    print(x)
```

`TypeError: 'int' object is not iterable`. Une liste, oui. Une chaîne, oui aussi.

La somme, avec un accumulateur : une variable qui part de zéro et reçoit chaque élément.

```python
total = 0
for x in flux:
    total = total + x
total
```

On compare avec `sum(flux)`. Même résultat. `sum` fait exactement ça.

Pourquoi on ne peut pas modifier la liste en passant dessus. On veut ajouter 1 à chaque élément :

```python
for x in flux:
    x = x + 1
flux
```

La liste n'a pas changé. `x` est une boîte à part, remplie à chaque tour avec une copie de la valeur. Modifier `x` ne touche pas la liste. Deux solutions.

Première solution, un accumulateur qui est une liste : on construit une copie modifiée avec `append`.

```python
plus_un = []
for x in flux:
    plus_un.append(x + 1)
plus_un
```

Deuxième solution, passer sur les positions et non sur les valeurs. `range(n)` fabrique l'itérable des positions `0, 1, ..., n-1`. C'est son seul rôle.

```python
list(range(4))
```
```python
for i in range(len(flux)):
    flux[i] = flux[i] + 1
flux
```

Et `range(n)` sert aussi à répéter `n` fois, sans liste du tout :

```python
capital = 1000
for annee in range(10):
    capital = capital * 1.03
capital
```

Résumé en une phrase : une boucle sert à faire quelque chose de façon répétée. Le motif qui reviendra tout le cours : une liste vide avant, `append` dedans, le résultat après.

**Exercices, 12 min.**

*Écrire* :

1. La moyenne de `flux` sans `sum` ni `len` dans le corps : un accumulateur pour le total, un compteur pour le nombre, la division après la boucle. Rangez dans `moyenne`.
2. Un capital de 1 000 € à 3 %, année par année pendant 10 ans : rangez la valeur de chaque fin d'année dans une liste `historique`. Attendu : `len(historique) == 10`, dernier élément `1343.92` à 2 décimales près.
3. La mensualité pour chaque taux de `taux = [0.02, 0.03, 0.04, 0.05]`, capital 200 000 € sur 20 ans, avec la formule de P1.7, dans une liste `mensualites`. Attendu : premier élément `1011.77`, dernier `1319.91`.

*Corriger* :

```python
for x in flux
    print(x)
```
```python
resultats = []
for x in flux:
    resultats.append(x * 2)
    resultats
```

Le second n'est pas une erreur : rien ne s'affiche, parce que le `resultats` final est dans le corps. On le fait sortir.

### P2.5 Passerelle Series, 10 min

```python
import pandas as pd
serie = pd.Series(mensualites, index=taux)
serie
```

Une Series, c'est une liste qui a une étiquette par valeur et qui sait faire des maths sur elle-même. La démonstration qui ferme la boucle des types :

```python
[1, 2, 3] * 2
```
```python
pd.Series([1, 2, 3]) * 2
```

Même signe, types différents, opérations différentes : c'est la définition d'un type, vue en P1.2.

```python
serie.mean(), serie.max()
```
```python
serie.plot()
```

Le premier graphique du cours, en une ligne.

### P2.6 Synthèse et annonce, 5 min

Tableau « vous voulez / vous écrivez » pour `if`, listes, `for`, Series.

Annonce de l'assignment : sujet, date, barème, lancement à la séance suivante.

---

## 3. L'assignment noté : le simulateur de prêt

Lancement en classe, 1h, sur le budget révision. Fin à la maison. Rendu : le notebook, avec toutes les cellules exécutées, dans un délai d'une semaine.

### 3.1 Ce que ça produit

À la fin, l'étudiant a : une offre de prêt calculée sur le taux directeur de la BCE du jour, un verdict d'acceptation, le tableau d'amortissement complet, la courbe du capital restant dû, le coût total du crédit, et un graphique des mensualités selon la durée. Tout ça à partir de trois nombres et d'un revenu.

Ce qui le rend intéressant :

- le taux vient d'une vraie source, en direct ; deux étudiants qui font le devoir à une semaine d'écart peuvent avoir des taux différents ;
- avec les valeurs par défaut, le prêt est refusé (taux d'effort 37 %). L'étudiant doit chercher la durée qui le fait passer, et la partie 6 le lui montre ;
- le bonus « héritage » répond à une question qu'on se pose vraiment : que change un remboursement anticipé ?

### 3.2 Énoncé, partie par partie

**Partie 0, fournie.** Cellule de setup avec `numpy`, `pandas`, `requests`, `verifier`.

**Partie 1, les paramètres (3 points).**

Les données arrivent d'un formulaire, en texte :

```python
capital_txt = "200 000 €"
duree_txt = "20 ans"
revenu_txt = "3 200 €"
```

1a. Convertissez-les en nombres : `capital` (float), `duree_annees` (int), `revenu_mensuel` (float). Méthodes `replace`, fonctions `float` et `int`. (1 point)

1b. Le taux. La Banque centrale européenne publie son taux directeur. Cellules fournies :

```python
url_bce = "https://data-api.ecb.europa.eu/service/data/FM/B.U2.EUR.4F.KR.MRR_FR.LEV?lastNObservations=1&format=csvdata"
reponse = requests.get(url_bce).text
print(reponse)
```

La réponse est un texte de deux lignes ; la dernière se termine par la date puis le taux : `...MRR_FR.LEV,2026-09-16,2.65`. Consigne : « Le taux commence 11 caractères après le texte `LEV,` (la date fait 10 caractères, plus la virgule) et va jusqu'à la fin. Utilisez `find`, `len`, un slicing sans borne de fin, `float`. Rangez-le dans `taux_bce`. » (1 point)

Cellule de secours fournie, commentée : `# taux_bce = 2.65   # si le réseau ne répond pas`.

1c. La banque prend une marge de 1,2 point : `taux_annuel = taux_bce + 1.2`. Puis `taux_mensuel` (le taux annuel divisé par 100 puis par 12) et `nb_mois`. (1 point)

Vérifications : `capital == 200000`, `duree_annees == 20`, `type(duree_annees) == int`, `taux_bce` entre 0 et 10, `nb_mois == 240`.

**Partie 2, la mensualité (3 points).**

Formule donnée : `mensualite = capital * t / (1 - (1 + t) ** -n)`. Calculez `mensualite`. Affichez avec une f-string : `Pour 200 000 € sur 20 ans à 3.85 %, la mensualité est de 1196.21 €.` Attendu avec un taux BCE de 2,65 : `1196.21`.

**Partie 3, le verdict (3 points).**

`taux_effort = mensualite / revenu_mensuel`. Un `if / elif / else` : au-dessus de 35 %, `verdict = "refus"` ; au-dessus de 30 %, `"accord sous réserve"` ; sinon `"accord"`. Affichez le taux d'effort en pourcentage et le verdict.

Puis, indépendamment, deux `if` séparés qui peuvent tous les deux s'exécuter : un avertissement si la durée dépasse 25 ans, un autre si la mensualité dépasse 1 000 €.

Avec les valeurs par défaut : `taux_effort = 0.374`, verdict `"refus"`. La consigne le dit : « Le prêt est refusé. Vous chercherez en partie 6 une durée qui le fait accepter. »

**Partie 4, le tableau d'amortissement (6 points).**

4a. À la main, dans une cellule texte : pour les deux premiers mois, calculez les intérêts (`capital_restant * taux_mensuel`), la part de capital remboursé (`mensualite - interets`), et le capital restant après paiement. Deux lignes de chiffres. (1 point)

4b. La boucle. Trois listes vides `interets_liste`, `capital_liste`, `restant_liste`, une variable `capital_restant = capital`. Une boucle `for mois in range(nb_mois)` qui, à chaque tour, calcule les trois valeurs, met à jour `capital_restant`, et les ajoute aux trois listes. (4 points)

Vérifications : `len(restant_liste) == nb_mois`, `abs(restant_liste[-1]) < 0.01` (le prêt est soldé ; la consigne donne `restant_liste[nb_mois - 1]` pour ne pas introduire l'indice négatif), `abs(interets_liste[0] - 641.67) < 0.01`.

4c. Le tableau. Cellule fournie, à exécuter :

```python
tableau = pd.DataFrame({"interets": interets_liste, "capital": capital_liste, "restant": restant_liste})
tableau.round(2).head(12)
```

On dit que c'est un tableau à trois colonnes construit à partir des trois listes, et qu'on apprendra à s'en servir en séance pandas. (1 point pour l'avoir exécuté et commenté en une phrase : que remarque-t-on sur la colonne intérêts ?)

**Partie 5, les résultats (3 points).**

5a. `pd.Series(restant_liste).plot()` avec un titre. La courbe du capital restant dû. (1 point)

5b. Le coût total du crédit : `sum(interets_liste)`, affiché en f-string. Attendu : `87090.68`. (1 point)

5c. Le premier mois où la part de capital dépasse la part d'intérêts. Une boucle sur `range(nb_mois)` avec un `if capital_liste[i] > interets_liste[i] and premier == 0:` qui range `i + 1` dans `premier`. Attendu : `25`. (1 point)

**Partie 6, les scénarios (2 points).**

Pour chaque durée de `[10, 15, 20, 25]`, la mensualité, dans une liste `mensualites`, puis `pd.Series(mensualites, index=[10, 15, 20, 25]).plot(kind="bar")`. Puis, en texte : quelle durée fait passer le taux d'effort sous 35 % ? Attendus : `2010.68`, `1464.39`, `1196.21`, `1039.18` ; réponse 25 ans (effort 32,5 %, accord sous réserve).

**Bonus, hors barème.** Au choix :

- Un héritage de 30 000 € arrive au mois 60 et rembourse une partie du capital. Refaites la boucle avec un `if mois == 59:` qui retire 30 000 du capital restant, et un `if capital_restant < 0: capital_restant = 0`. Tracez les deux courbes sur le même graphique (deux appels à `.plot()` dans la même cellule). Combien d'intérêts économisés ?
- La mensualité en francs suisses avec le convertisseur de P1.9.

### 3.3 Barème

| Partie | Points |
|---|---|
| 1. Paramètres | 3 |
| 2. Mensualité | 3 |
| 3. Verdict | 3 |
| 4. Tableau | 6 |
| 5. Résultats | 3 |
| 6. Scénarios | 2 |
| Total | 20 |

Les cellules `verifier` sont dans le sujet : l'étudiant sait où il en est. La correction regarde en plus la lisibilité (noms de variables, une idée par cellule) sans point dédié.

### 3.4 Corrigé de référence

Vérifié le 12 septembre 2026 avec un taux BCE de 2,65.

```python
capital = float(capital_txt.replace(" €", "").replace(" ", ""))
duree_annees = int(duree_txt.replace(" ans", ""))
revenu_mensuel = float(revenu_txt.replace(" €", "").replace(" ", ""))

pos = reponse.find("LEV,") + len("LEV,") + 11
taux_bce = float(reponse[pos:])

taux_annuel = taux_bce + 1.2
taux_mensuel = taux_annuel / 100 / 12
nb_mois = duree_annees * 12

mensualite = capital * taux_mensuel / (1 - (1 + taux_mensuel) ** -nb_mois)
print(f"Pour {capital:.0f} € sur {duree_annees} ans à {taux_annuel:.2f} %, la mensualité est de {mensualite:.2f} €.")

taux_effort = mensualite / revenu_mensuel
if taux_effort > 0.35:
    verdict = "refus"
elif taux_effort > 0.30:
    verdict = "accord sous réserve"
else:
    verdict = "accord"
print(f"Taux d'effort : {taux_effort:.1%}, verdict : {verdict}.")

interets_liste = []
capital_liste = []
restant_liste = []
capital_restant = capital
for mois in range(nb_mois):
    interets = capital_restant * taux_mensuel
    rembourse = mensualite - interets
    capital_restant = capital_restant - rembourse
    interets_liste.append(interets)
    capital_liste.append(rembourse)
    restant_liste.append(capital_restant)

premier = 0
for i in range(nb_mois):
    if capital_liste[i] > interets_liste[i] and premier == 0:
        premier = i + 1

mensualites = []
for d in [10, 15, 20, 25]:
    n = d * 12
    mensualites.append(capital * taux_mensuel / (1 - (1 + taux_mensuel) ** -n))
```

Valeurs : mensualité `1196.21`, effort `0.374`, intérêts totaux `87090.68`, premier mois `25`, mensualités par durée `2010.68`, `1464.39`, `1196.21`, `1039.18`.

Les `verifier` du sujet doivent tolérer un taux BCE différent : on vérifie les relations (`nb_mois == 240`, `restant_liste` soldé, `len` des listes, cohérence `mensualite * nb_mois == capital + sum(interets_liste)` à 1 € près) plutôt que les valeurs absolues, sauf pour la partie 1a qui ne dépend pas du taux.

---

## 4. Ce que pandas peut supposer acquis

Après P1, P2 et l'assignment, et rien d'autre :

- expression, valeur, type, `type()`, `int` `float` `bool` `str`, conversions ;
- variable, affectation, ordre d'exécution des cellules ;
- appel de fonction, arguments, `round` `abs` `max` `min` `len` `print`, `import ... as`, `np.sqrt` `np.log` `np.exp` ;
- chaînes : `+`, `in`, `len`, `upper` `lower` `strip` `replace` `find`, `s[i]`, `s[a:b]` ;
- booléens : comparaisons, `and` `or` `not`, `True + True` ;
- `if / elif / else`, plusieurs `if` séparés, f-strings `{x:.2f}` et `{x:.1%}` ;
- listes : littéral, `[i]`, `[a:b]`, `len` `sum` `max` `min` `in`, `append`, `index`, mutabilité ;
- `for x in liste`, `for i in range(n)`, accumulateur, liste de résultats ;
- `pd.Series(liste, index=...)`, `.mean()`, `.max()`, `.plot()` ; `pd.DataFrame({...})` vu une fois comme recette.

---

## 5. Production

1. Notebook P1 : 11 sections, environ 45 cellules. Cellule de setup, glossaire, tableau de synthèse.
2. Notebook P2 : 7 sections, environ 55 cellules dont 20 de prédiction.
3. Notebook assignment : parties 0 à 6 plus bonus, `verifier` relationnels, cellule de secours pour le taux.
4. Corrections des trois, générées depuis les notebooks de cours.
5. Image des boîtes pour P1.5 dans `ressources/img/`.
6. Page « Bien démarrer » réduite aux réglages.
