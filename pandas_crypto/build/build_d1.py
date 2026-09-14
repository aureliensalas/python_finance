import json, os, textwrap

OUT = "pandas_crypto/cours/seance1_cours.ipynb"
LOGO = '<img src="https://cdn.jsdelivr.net/gh/aureliensalas/python_finance@main/ressources/img/logo_macmia.png" alt="Banque des Territoires · France 2030 · MACMIA" width="520">'
BADGE = "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aureliensalas/python_finance/blob/main/pandas_crypto/cours/seance1_cours.ipynb)"
BASE = "https://cdn.jsdelivr.net/gh/aureliensalas/python_finance@main/pandas_crypto/data/"

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

# Séance 3 : des Series à la table

**Cours** · 2h · pandas, première partie

> ⚠️ **Avant de taper quoi que ce soit :** *Fichier → Enregistrer une copie dans Drive*. Sinon votre travail sera perdu en fermant l'onglet.
>
> 📱 Sur tablette, faites d'abord les réglages de [Bien démarrer](https://github.com/aureliensalas/python_finance/blob/main/ressources/setup_tablette.md).
""")

md("""
## Objectifs

À la fin de cette séance, vous saurez :

- faire un calcul sur toutes les valeurs d'une Series d'un coup
- assembler des Series en une table, et retrouver une colonne dans la table
- charger un fichier et dire en trente secondes ce qu'il contient
- compter les lignes qui remplissent une condition
- ne garder que les lignes qui remplissent une condition, avec `query`
- trier une table

## Les deux phrases du bloc

> **Tout ce que vous savez faire sur une valeur, vous le faites maintenant sur une colonne entière.**

> **Tout ce que pandas fait, vous pourriez l'écrire vous-même avec une colonne de booléens et une boucle.**

La première organise cette séance. La seconde organise la suivante.

## Les questions de la séance

Le fichier de la séance contient huit ans et demi de cours quotidiens de sept cryptomonnaies. Quatre questions, qu'on saura poser à la fin du bloc :

- combien de jours le bitcoin a-t-il clôturé au-dessus de 100 000 dollars ?
- quelle monnaie a le plus de jours dans le fichier, et pourquoi pas toutes le même nombre ?
- quel a été le cours moyen de chaque monnaie en 2024 ?
- si vous aviez acheté 100 dollars de bitcoin le premier de chaque mois depuis 2020, combien auriez-vous aujourd'hui ?

Exécutez d'abord la cellule de setup.
""")

code(f"""
import numpy as np
import pandas as pd

pd.set_option("display.max_rows", 12)      # affichage court sur petit écran
BASE = "{BASE}"


def verifier(nom, condition, indice=""):
    if condition:
        print("OK       -", nom)
    else:
        print("A REVOIR -", nom, ":", indice)
""")

# ---------------------------------------------------------------- 0. Échauffement
md("""
## 0. Échauffement

Trois cellules sur la séance 2.

**1.** Voici des prix. Avec une boucle et `append`, construisez `doubles`, la liste des prix multipliés par 2.
""")

code("prix_liste = [42000, 2300, 100, 0.08, 0.5]")

code("")

code("""
verifier("doubles", doubles == [84000, 4600, 200, 0.16, 1.0], "une liste vide avant, append dedans")
""")

md("**2.** Transformez `doubles` en Series, dans `serie`. Puis sa moyenne dans `moyenne` et son maximum dans `maximum`.")

code("")

code("""
verifier("serie", type(serie) == pd.Series and len(serie) == 5, "pd.Series(liste)")
verifier("moyenne et maximum", abs(moyenne - 17760.232) < 0.01 and maximum == 84000, ".mean() et .max()")
""")

md("**3.** Cette cellule est fausse. Exécutez, lisez la dernière ligne, réparez.")

code("""
for p in prix_liste
    print(p)
""")

# ---------------------------------------------------------------- 1. Series
md("""
## 1. La Series, et les calculs dessus

Une **Series**, c'est une liste avec une **étiquette** par valeur, qui sait faire des maths sur elle-même.
""")

code("""
prix = pd.Series([42000, 2300, 100, 0.08, 0.5], index=["BTC", "ETH", "SOL", "DOGE", "XRP"])
prix
""")

md("""
Deux morceaux :

- à gauche, les **étiquettes** : c'est l'**index** ;
- à droite, les **valeurs**.

`prix["ETH"]` va chercher par étiquette. Sans `index=`, pandas numérote de 0 à 4, comme une liste.

Ce qu'on savait faire sur **une** valeur, on le fait sur **toute la Series** d'un coup.
""")

code("prix * 2")

code("prix / 1000")

code("prix.sum(), prix.max(), prix.min(), prix.mean()")

md("""
Une comparaison, qui donnait un `bool` sur une valeur, donne **une Series de `bool`** : une réponse par étiquette.
""")

code("prix > 1000")

md("`True` vaut 1. Donc `.sum()` compte les `True`, et `.mean()` donne leur part.")

code("(prix > 1000).sum(), (prix > 1000).mean()")

md("### Prédire")

predire('prix["SOL"]', "prix * 1000", "prix < 1", "(prix < 1).sum()", "prix.max() - prix.min()")

# ---------------------------------------------------------------- 2. DataFrame
md("""
## 2. Trois Series côte à côte : la DataFrame

Une **table**, c'est plusieurs Series côte à côte, qui partagent les mêmes étiquettes de lignes. On la construit.
""")

code("""
coin   = pd.Series(["BTC", "ETH", "SOL", "BTC", "ETH", "SOL"])
close  = pd.Series([42000, 2300, 100, 44000, 2400, 95])
volume = pd.Series([20, 10, 5, 25, 12, 4])
""")

code("""
jouet = pd.DataFrame({"coin": coin, "close": close, "volume": volume})
jouet
""")

md("""
Regardez ce qui s'affiche :

- des **colonnes**, qui ont des **noms** : ceux qu'on a donnés entre les accolades ;
- des **lignes**, qui ont des **étiquettes** : `0` à `5`. Ce sont celles des Series de départ, qui n'avaient pas d'`index=`.

C'est une **DataFrame** : trois Series, un nom chacune, les mêmes étiquettes de lignes.

`jouet` est petite exprès. Toutes les cellules « Prédire » de la séance portent sur elle : six lignes, tout se calcule de tête.

### Choisir une colonne

C'est **retrouver une des Series de départ**.
""")

code('jouet["close"]')

code('type(jouet["close"])')

md("Plusieurs colonnes : une **liste** de noms entre les crochets. Le résultat est une DataFrame plus étroite.")

code('jouet[["coin", "close"]]')

md("""
### Calculer sur une colonne

C'est faire les calculs de la section 1 sur une des Series.
""")

code('jouet["close"] * 2')

code('jouet["close"] * jouet["volume"]')

code('jouet["close"].max(), jouet["volume"].sum(), jouet["close"].mean()')

md("""
Colonne et nombre, colonne et colonne, fonction de colonne : les trois formes vues sur `prix`.

En séance 2, ça prenait une boucle avec `append`. Ici, une ligne. **C'est la première phrase du bloc.**

### Créer une colonne

Une **affectation**, avec un nom de colonne qui n'existe pas encore entre les crochets. C'est l'affectation de la séance 1, sur une table. Et c'est ajouter une quatrième Series à côté des trois autres.
""")

code("""
jouet["montant"] = jouet["close"] * jouet["volume"]
jouet
""")

md("`.round(1)` arrondit chaque valeur d'une colonne.")

code('(jouet["close"] / 1000).round(1)')

md("### Prédire")

predire('jouet["volume"]', 'jouet["close"] / 1000', 'jouet["close"] > 1000', '(jouet["close"] > 1000).sum()',
        'jouet["volume"].sum()', 'jouet["close"].mean()', 'jouet["montant"].max()', 'jouet[["coin", "montant"]]')

md("""
### Prédire la forme

Avant d'exécuter, dites à voix haute : **Series, DataFrame, ou un nombre ? Combien de lignes ?**
""")

predire('jouet["coin"]', 'jouet[["coin", "close"]]', 'jouet["close"] * 2', 'jouet["close"].max()')

md("""
### Écrire

**1.** Créez la colonne `close_k`, le cours en milliers.
""")

code("")

code("""
verifier("close_k", abs(jouet["close_k"].sum() - 90.895) < 0.001, "close divisé par 1000")
""")

md("**2.** Créez la colonne `part`, la part de chaque ligne dans le volume total. Sa somme doit valoir 1.")

code("")

code("""
verifier("part", abs(jouet["part"].sum() - 1) < 1e-9, "volume divisé par la somme des volumes")
""")

md("**3.** Construisez une table `perso` à partir de deux Series de votre choix, trois lignes chacune, puis ajoutez-lui une colonne calculée à partir des deux premières.")

code("")

code("""
verifier("perso", type(perso) == pd.DataFrame and len(perso) == 3 and len(perso.columns) == 3, "deux Series, pd.DataFrame, puis une affectation")
""")

md("""
### Corriger

Chaque cellule est fausse. Exécutez, lisez la dernière ligne, réparez.
""")

code('jouet["Close"]')

md("Le réflexe quand un nom de colonne est refusé : `jouet.columns`, la liste exacte des noms.")

code("jouet.columns")

code('jouet["coin", "close"]')

code('jouet["close"] + jouet["coin"]')

# ---------------------------------------------------------------- 3. Charger
md("""
## 3. Charger une table qu'on ne connaît pas

`jouet`, on l'a construite : on sait ce qu'il y a dedans. Une vraie table, on la **reçoit** : un fichier, fabriqué par quelqu'un d'autre. On la charge, et la première chose à faire est de la découvrir.
""")

code("""
crypto = pd.read_csv(BASE + "crypto.csv")
crypto
""")

md("""
`pd.read_csv(...)` a la forme `alias.fonction(argument)` de la séance 1. Le résultat est une DataFrame, comme `jouet`, en beaucoup plus grand : des colonnes avec des noms, des lignes numérotées.

### Ce qu'on veut savoir d'une table qu'on ne connaît pas

Toujours les mêmes questions, dans cet ordre.

| Question | Commande |
|---|---|
| combien de lignes, combien de colonnes ? | `crypto.shape` |
| comment s'appellent les colonnes ? | `crypto.columns` |
| quel est le type de chaque colonne, et manque-t-il des valeurs ? | `crypto.info()` |
| à quoi ressemblent le début et la fin ? | `crypto.head()`, `crypto.tail()` |
| une ligne, c'est quoi ? | on regarde, et on se le dit en français |
""")

code("crypto.shape")

code("crypto.columns")

code("crypto.info()")

md("""
Lire `info()` :

- `non-null` : combien de valeurs sont remplies. Ici, toutes.
- `Dtype` : le type. `float64` est un `float`, `int64` un `int`, `object` du **texte**.

`date` est donc du texte pour l'instant. On le note ; on y revient à la séance suivante.
""")

code("crypto.head(3)")

code("crypto.tail(3)")

md("""
La fin dit jusqu'où va le fichier : le 31 août 2026.

**Une ligne, c'est une monnaie, un jour.** 21 325 lignes : sept monnaies fois environ huit ans et demi de jours, sauf SOL qui commence en avril 2020.

| Colonne | Contenu |
|---|---|
| `date` | le jour |
| `coin` | la monnaie : `BTC`, `ETH`, `SOL`, `DOGE`, `XRP`, `BNB`, `ADA` |
| `close` | le cours de clôture, en dollars |
| `volume` | le nombre d'unités échangées ce jour-là |

`len(crypto)` marche aussi : le nombre de lignes, comme sur une liste.
""")

code("len(crypto)")

md("""
### Dire la question, écrire le code

Au tableau, ensemble, de gauche à droite :

- le volume total échangé sur tout le fichier ;
- le cours le plus haut de tout le fichier ;
- une colonne `montant`, le cours fois le volume : les dollars échangés ce jour-là.
""")

code("")

md("""
### Écrire

**1.** Créez `crypto["montant_m"]`, le montant en millions de dollars, arrondi à 1 décimale. Rangez le plus grand dans `montant_max`.
""")

code("")

code("""
verifier("montant_max", abs(montant_max - 350967.9) < 0.1, "close * volume / 1e6, .round(1), puis .max()")
""")

md("**2.** Le cours le plus élevé et le plus bas de tout le fichier, dans `close_max` et `close_min`.")

code("")

code("""
verifier("close_max", abs(close_max - 124752.5312) < 0.01, ".max() sur la colonne close")
verifier("close_min", abs(close_min - 0.0015) < 1e-6, ".min() sur la colonne close")
""")

# ---------------------------------------------------------------- 4. Compter
md("""
## 4. Compter avec une comparaison

Sur `prix` et sur `jouet`, une comparaison donnait une Series de `bool`. Sur 21 325 lignes, pareil : une réponse par ligne.
""")

code('crypto["close"] > 100000')

md("`.sum()` compte les `True`. `.mean()` donne leur part.")

code('(crypto["close"] > 100000).sum()')

code('(crypto["coin"] == "BTC").mean()')

md("""
La première ligne répond à « combien de jours au-dessus de 100 000 dollars, toutes monnaies confondues ». La seconde à « quelle part du fichier concerne BTC ».

Compter, et mesurer une part : ces deux gestes reviendront jusqu'au bloc machine learning.

### Écrire

La part des lignes dont le volume dépasse le volume moyen, dans `part_gros_volume`.
""")

code("")

code("""
verifier("part_gros_volume", abs(part_gros_volume - 0.2034) < 0.001, "une comparaison entre la colonne et sa moyenne, puis .mean()")
""")

# ---------------------------------------------------------------- 5. query
md("""
## 5. Filtrer avec `query`

Compter les lignes qui remplissent une condition, on sait. Maintenant on veut **les garder** : la table réduite aux jours de BTC, par exemple.

C'est `query`. On lui donne la condition **entre guillemets**, écrite exactement comme une condition de la séance 2.
""")

code("""
btc = crypto.query("coin == 'BTC'")
btc.shape
""")

md("""
Le résultat est une DataFrame : les mêmes colonnes, moins de lignes. On la range dans une variable, ou on enchaîne.

### Les guillemets

Toute la condition est un texte, entre guillemets **doubles**. Un texte à l'intérieur, comme `BTC`, se met entre guillemets **simples**.

```python
crypto.query("coin == 'BTC'")
```

C'est la seule difficulté de syntaxe de la section.

### Tout ce que vous savez écrire dans un `if` s'écrit dans `query`

Les six comparaisons, `and`, `or`, `not`, `in`. Rien de nouveau.
""")

code('crypto.query("close > 100000")')

code("""crypto.query("coin == 'BTC' and close > 100000")""")

code("""crypto.query("coin == 'BTC' or coin == 'ETH'")""")

code("""crypto.query("coin in ['BTC', 'ETH']")""")

code("""crypto.query("not coin == 'BTC'")""")

md("Les dates ISO se comparent comme du texte, et ça marche parce que l'année vient en premier.")

code("""crypto.query("date >= '2024-01-01'")""")

md("""
### Compter avec `query`

`len` sur le résultat.
""")

code("""len(crypto.query("coin == 'BTC' and close > 100000"))""")

md("""
Comparez avec la section 4 : `((crypto["coin"] == "BTC") & (crypto["close"] > 100000)).sum()` donnerait le même nombre. Deux chemins, un résultat. On garde `query` pour filtrer, la comparaison pour compter.

### Les étiquettes ne bougent pas

Regardez la colonne de gauche de `btc` : les étiquettes ne recommencent pas à 0. Ce sont celles que ces lignes avaient dans `crypto`. Un filtre **garde** des lignes, il ne les renumérote pas.
""")

code("btc.head(3)")

md("""
### Enchaîner

Filtrer, puis choisir une colonne, puis calculer. Une ligne pandas se lit **de gauche à droite**, un point à la fois :

```
crypto.query("coin == 'ETH'")["close"].max()
│      │                      │        │
│      │                      │        └─ le plus grand
│      │                      └─ de la colonne close
│      └─ les lignes où coin vaut ETH
└─ dans la table crypto
```
""")

code("""crypto.query("coin == 'ETH'")["close"].max()""")

md("### Prédire")

predire("""jouet.query("coin == 'SOL'")""",
        """len(jouet.query("volume > 10"))""",
        """jouet.query("coin == 'ETH' and close > 2350")""",
        """jouet.query("coin in ['BTC', 'SOL']")["volume"].sum()""",
        """jouet.query("not coin == 'BTC'")["close"].max()""",
        """jouet.query("close < 0")""",
        """jouet.query("coin == 'BTC'")["close"].mean()""",
        """jouet.query("volume >= 10 or close < 100")""")

md("""
Une table vide, comme à l'avant-dernière cellule, n'est pas une erreur : aucune ligne ne remplit la condition.

### Lire le code, dire la question

Pour chaque ligne, à l'oral : à quelle question répond-elle ?
""")

code("""crypto.query("coin == 'DOGE'")["volume"].mean()""")

code("""len(crypto.query("close > 1000"))""")

code("""crypto.query("coin == 'BTC' and date >= '2024-01-01'")["close"].min()""")

code("""crypto.query("coin in ['SOL', 'ADA']").shape""")

md("""
### Dire la question, écrire le code

Au tableau, ensemble :

- le cours moyen de SOL ;
- le nombre de jours où ETH a dépassé 4 000 dollars ;
- le volume total de BTC en 2021.
""")

code("")

md("""
### Écrire

**1.** Combien de jours BTC a-t-il clôturé au-dessus de 100 000 dollars ? Dans `nb_jours_100k`.
""")

code("")

code("""
verifier("nb_jours_100k", nb_jours_100k == 217, "len d'un query à deux conditions")
""")

md("**2.** Combien de lignes pour BTC, combien pour SOL ? Dans `nb_btc` et `nb_sol`. Pourquoi la différence ?")

code("")

code("""
verifier("nb_btc", nb_btc == 3165, "len(crypto.query(...))")
verifier("nb_sol", nb_sol == 2335, "SOL commence en 2020")
""")

md("**3.** Le cours moyen de ETH en 2024, dans `eth_2024`. Deux conditions sur les dates en texte : au moins le 1er janvier 2024, avant le 1er janvier 2025.")

code("")

code("""
verifier("eth_2024", abs(eth_2024 - 3044.93) < 0.01, "date >= '2024-01-01' and date < '2025-01-01', puis .mean()")
""")

md("**4.** La part des lignes du fichier qui concernent DOGE ou XRP, dans `part_doge_xrp`. Deux chemins possibles : `len` d'un `query` divisé par `len(crypto)`, ou `.mean()` d'une comparaison. Faites les deux et comparez.")

code("")

code("""
verifier("part_doge_xrp", abs(part_doge_xrp - 0.2968) < 0.001, "in ['DOGE', 'XRP'], puis len(...) / len(crypto)")
""")

md("### Corriger")

code("""crypto.query("coin == BTC")""")

code("""crypto.query(date >= '2024-01-01')""")

code("""crypto.query("coin == 'BTC' and close > 100000)""")

# ---------------------------------------------------------------- 6. Trier
md("""
## 6. Trier

`sort_values` trie la table selon une colonne. Du plus petit au plus grand par défaut.
""")

code('crypto.sort_values("close")')

code('crypto.sort_values("close", ascending=False).head(5)')

md("La table `crypto` elle-même ne change pas si on ne réaffecte pas :")

code("crypto.head(2)")

md("""
### Écrire

**1.** Les cinq jours de plus gros montant échangé, dans `top_montant`. Quelle monnaie, quelle année ? La colonne `montant_m` existe depuis la section 3.
""")

code("")

code("""
verifier("top_montant", len(top_montant) == 5 and top_montant["coin"].iloc[0] == "BTC", "sort_values sur montant_m, ascending=False, puis head(5)")
""")

md("**2.** Les cinq jours de plus bas cours pour ETH, dans `bas_eth`. Un `query`, puis un tri, puis `head`.")

code("")

code("""
verifier("bas_eth", len(bas_eth) == 5 and (bas_eth["coin"] == "ETH").sum() == 5 and bas_eth["close"].iloc[0] <= bas_eth["close"].iloc[4], "query, sort_values, head(5)")
""")

# ---------------------------------------------------------------- 7. Synthèse
md("""
## 7. Ce que vous savez faire

| Vous voulez... | Vous écrivez |
|---|---|
| une Series | `pd.Series([1, 2, 3], index=["a", "b", "c"])` |
| un calcul sur toutes les valeurs | `serie * 2`, `serie.sum()`, `serie.mean()` |
| assembler des Series en table | `pd.DataFrame({"nom": serie1, "autre": serie2})` |
| charger un fichier | `pd.read_csv(BASE + "crypto.csv")` |
| découvrir une table | `df.shape`, `df.columns`, `df.info()`, `df.head()`, `df.tail()` |
| une colonne | `df["close"]` |
| plusieurs colonnes | `df[["coin", "close"]]` |
| créer une colonne | `df["montant"] = df["close"] * df["volume"]` |
| compter les lignes qui remplissent une condition | `(df["close"] > 100000).sum()` |
| leur part | `(df["coin"] == "BTC").mean()` |
| garder ces lignes | `df.query("coin == 'BTC' and close > 100000")` |
| une liste de valeurs | `df.query("coin in ['BTC', 'ETH']")` |
| enchaîner | `df.query("coin == 'ETH'")["close"].max()` |
| trier | `df.sort_values("close", ascending=False)` |

## Les deux phrases du bloc

1. **Tout ce que vous savez faire sur une valeur, vous le faites maintenant sur une colonne entière.**
2. **Tout ce que pandas fait, vous pourriez l'écrire vous-même avec une colonne de booléens et une boucle.** C'est la séance suivante.

## Pour la prochaine séance

Trois questions à traduire en une ligne chacune, sur `crypto` :

1. Le cours maximum de DOGE, dans `q1`.
2. Le nombre de jours où BNB a dépassé 600 dollars, dans `q2`.
3. Le volume moyen de XRP en 2025, dans `q3`.
""")

code("")

code("""
verifier("q1", abs(q1 - crypto.query("coin == 'DOGE'")["close"].max()) < 1e-6, "query puis .max()")
verifier("q2", q2 == len(crypto.query("coin == 'BNB' and close > 600")), "len d'un query")
verifier("q3", abs(q3 - crypto.query("coin == 'XRP' and date >= '2025-01-01' and date < '2026-01-01'")["volume"].mean()) < 1, "trois conditions, puis .mean()")
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
