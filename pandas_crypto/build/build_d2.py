import json, os, textwrap

OUT = "pandas_crypto/cours/seance2_cours.ipynb"
LOGO = '<img src="https://cdn.jsdelivr.net/gh/maxischa/datacamp_test@5a33b79/ressources/img/logo_macmia.png" alt="Banque des Territoires · France 2030 · MACMIA" width="520">'
BADGE = "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/maxischa/datacamp_test/blob/main/pandas_crypto/cours/seance2_cours.ipynb)"
BASE = "https://cdn.jsdelivr.net/gh/maxischa/datacamp_test@main/pandas_crypto/data/"

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

# Séance 4 : nettoyer et regrouper

**Cours** · 2h · pandas, seconde partie

> ⚠️ **Avant de taper quoi que ce soit :** *Fichier → Enregistrer une copie dans Drive*. Sinon votre travail sera perdu en fermant l'onglet.
>
> 📱 Sur tablette, faites d'abord les réglages de [Bien démarrer](https://github.com/maxischa/datacamp_test/blob/main/ressources/setup_tablette.md).
""")

md("""
## Objectifs

À la fin de cette séance, vous saurez :

- repérer les quatre défauts d'un fichier réel, et les réparer un par un
- faire sur une colonne de texte ce que vous faisiez sur une chaîne
- compter les lignes par catégorie
- transformer une colonne de texte en dates, et en tirer l'année ou le mois
- répondre à « combien par ... ? » avec `groupby`
- tracer une courbe et des barres

## Les deux phrases du bloc

> **Tout ce que vous savez faire sur une valeur, vous le faites maintenant sur une colonne entière.**

> **Tout ce que pandas fait, vous pourriez l'écrire vous-même avec une colonne de booléens et une boucle.**

La seconde organise cette séance : à chaque fois, on répare d'abord avec ce qu'on sait, puis on voit la fonction pandas qui fait pareil.

Exécutez d'abord la cellule de setup, puis la cellule `jouet`.
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

code("""
# La table jouet de la séance 3, avec une colonne date en plus
coin   = pd.Series(["BTC", "ETH", "SOL", "BTC", "ETH", "SOL"])
date   = pd.Series(["2024-01-01", "2024-01-01", "2024-01-01", "2024-01-02", "2024-01-02", "2024-01-02"])
close  = pd.Series([42000, 2300, 100, 44000, 2400, 95])
volume = pd.Series([20, 10, 5, 25, 12, 4])

jouet = pd.DataFrame({"coin": coin, "date": date, "close": close, "volume": volume})
jouet
""")

code("""
crypto = pd.read_csv(BASE + "crypto.csv")
crypto.shape
""")

# ---------------------------------------------------------------- 0. Échauffement
md("""
## 0. Échauffement

Sur la séance 3.

**1.** Le cours moyen de BNB, dans `moy_bnb`.
""")

code("")

code("""
verifier("moy_bnb", abs(moy_bnb - crypto.query("coin == 'BNB'")["close"].mean()) < 0.01, "query, colonne, .mean()")
""")

md("**2.** Le nombre de jours où DOGE a dépassé 0,50 dollar, dans `nb_doge`.")

code("")

code("""
verifier("nb_doge", nb_doge == len(crypto.query("coin == 'DOGE' and close > 0.5")), "len d'un query à deux conditions")
""")

md("**3.** Les trois jours de plus haut cours de SOL, dans `top_sol`.")

code("")

code("""
verifier("top_sol", len(top_sol) == 3 and (top_sol["coin"] == "SOL").sum() == 3 and top_sol["close"].iloc[0] >= top_sol["close"].iloc[2], "query, sort_values(ascending=False), head(3)")
""")

md("**4.** Cette cellule est fausse. Exécutez, lisez la dernière ligne, réparez.")

code("""crypto.query("coin == 'ETH' and close > 4000).shape""")

# ---------------------------------------------------------------- 1. Le fichier sale
md("""
## 1. Le fichier sale

`crypto.csv` était propre. Un export réel ne l'est jamais. Voici le même fichier pour l'année 2024, tel qu'il sortirait d'un système mal réglé.
""")

code("""
sale = pd.read_csv(BASE + "crypto_sale.csv")
sale.head(8)
""")

code("sale.info()")

md("""
### Le diagnostic

À partir de ces deux cellules, ensemble :

| Ce qu'on voit | Le défaut |
|---|---|
| `close` est de type `object`, et `head` montre `44 167,33 $` | des **nombres écrits en texte** |
| `volume` a moins de `non-null` que de lignes | des **valeurs manquantes** |
| `coin` contient `btc`, ` BTC`, `Btc ` | des **catégories incohérentes** |
| `info()` ne le dit pas, mais il faut vérifier | des **lignes en double** |

Quatre défauts, quatre sections. Le plan de la séance est écrit par le diagnostic.

Et **la seconde phrase du bloc** : pour chaque défaut, on répare d'abord avec ce qu'on sait, puis on voit la fonction pandas qui fait pareil.
""")

# ---------------------------------------------------------------- 2. Manquants
md("""
## 2. Les valeurs manquantes

`isna()` pose une question à chaque case : « es-tu vide ? ». Sur une colonne, ça donne une Series de `bool`, comme une comparaison.
""")

code('sale["volume"].isna()')

md("Compter, comme à la séance 3 :")

code('sale["volume"].isna().sum()')

md("Sur la table entière, une réponse par colonne :")

code("sale.isna().sum()")

md("""
### Réparez-le vous-même

On veut garder les lignes où le volume n'est **pas** manquant. On a une Series de `bool`. On en fait une **colonne**, et `query` sait filtrer sur une colonne.
""")

code("""
sale["manquant"] = sale["volume"].isna()
sans_trous = sale.query("manquant == False")
len(sale), len(sans_trous)
""")

md("""
### Un `if` sur chaque ligne

Une colonne de `bool`, c'est la liste des réponses qu'un `if` donnerait ligne par ligne. Et un `if` accepte un booléen tout seul :
""")

code("""
if True:
    print("toujours")
if False:
    print("jamais")
""")

md("""
`query("manquant == False")`, c'est ce `if` fait sur chaque ligne d'un coup : on garde la ligne si sa case vaut `False`.

### La fonction pandas

`dropna` fait exactement ce que vous venez d'écrire, sans colonne intermédiaire.
""")

code("""
propre = sale.dropna(subset=["volume"])
len(propre)
""")

md("""
`subset` dit sur quelle colonne regarder. Sans lui, une ligne avec un trou n'importe où serait retirée.

On note le nombre de lignes **avant** et **après**. On le fera à chaque étape : c'est ce qu'on rapporte à la fin.

### Prédire

`jouet2` est `jouet` avec deux volumes manquants.
""")

code("""
jouet2 = jouet.copy()
jouet2["volume"] = pd.Series([20, np.nan, 5, 25, np.nan, 4])
jouet2
""")

predire('jouet2["volume"].isna()', 'jouet2["volume"].isna().sum()', 'len(jouet2.dropna(subset=["volume"]))',
        'jouet2.dropna(subset=["volume"])["volume"].sum()')

md("""
### Écrire

Sur `sale` : le nombre de lignes avec un volume manquant, dans `nb_trous`. Puis `net`, la table sans ces lignes, par la méthode de votre choix.
""")

code("")

code("""
verifier("nb_trous", nb_trous == 41, "isna() puis .sum()")
verifier("net", len(net) == len(sale) - nb_trous, "dropna(subset=[...]) ou query sur une colonne de bool")
""")

# ---------------------------------------------------------------- 3. Doublons
md("""
## 3. Les doublons

`duplicated()` pose une question à chaque ligne : « t'ai-je déjà vue plus haut ? ». Une Series de `bool`, encore.
""")

code("net.duplicated().sum()")

md("### Réparez-le vous-même")

code("""
net["doublon"] = net.duplicated()
sans_doublons = net.query("doublon == False")
len(net), len(sans_doublons)
""")

md("""
### La fonction pandas

Avant, on retire les deux colonnes de travail, `manquant` et `doublon` : on garde les quatre colonnes de départ. Sinon, une ligne et sa copie ne seraient plus identiques (`False` d'un côté, `True` de l'autre), et `drop_duplicates` ne verrait plus de doublon.
""")

code("""
net = net[["date", "coin", "close", "volume"]]
net = net.drop_duplicates()
len(net)
""")

md("""
### Lire le code, dire la question

À quelle question répond cette ligne ?
""")

code('sans_doublons.query("doublon == True")')

md("Une table vide : dans `sans_doublons`, plus aucune ligne n'est un doublon. Et sur `net` avant nettoyage, la même question donnait les 30 lignes en double, à regarder avant de supprimer.")

md("""
### Écrire

`sale2` est une copie de `sale`. Enlevez les doublons **puis** les lignes sans volume, dans `net2`, et comparez avec `net`.
""")

code("sale2 = sale.copy()")

code("")

code("""
verifier("net2", len(net2) == 2522 and len(net2) == len(net), "l'ordre des deux opérations ne change rien ici")
""")

# ---------------------------------------------------------------- 4. Texte vers nombre
md("""
## 4. Des nombres écrits en texte

`close` est du texte. On ne peut rien calculer avec.
""")

code('net["close"].max()')

md("""
Ça renvoie un texte, et le « maximum » de textes ne veut rien dire.

En séance 1, on nettoyait **un** texte avec `replace` puis `float` :
""")

code('float("43 250,12 $".replace(" ", "").replace(",", ".").replace("$", ""))')

md("""
Sur une colonne, c'est la même chose, avec une différence de syntaxe.

### Pourquoi `.str`

`net["close"]` est une Series, pas un texte. Pour dire « applique la méthode de texte **à chaque case** », on écrit `.str` devant la méthode :

```python
net["close"].str.replace(" ", "")
```

`.str` veut dire : traite chaque case comme une chaîne.
""")

code("""
texte = net["close"].str.replace(" ", "").str.replace(",", ".").str.replace("$", "")
texte.head(3)
""")

md("Puis la conversion : `astype(float)`, la version colonne de `float()`.")

code("""
net["close"] = texte.astype(float)
net.info()
""")

md("`close` est passé en `float64`. Le maximum a maintenant un sens.")

code('net["close"].max()')

md("""
### Prédire

`jouet3` est `jouet` avec des prix en texte.
""")

code("""
jouet3 = jouet.copy()
jouet3["close"] = pd.Series(["42 000,00", "2 300,00", "100,00", "44 000,00", "2 400,00", "95,00"])
jouet3
""")

predire('jouet3["close"].str.replace(" ", "")',
        'jouet3["close"].str.replace(" ", "").str.replace(",", ".").astype(float).sum()')

md("### Corriger")

code("""
# Pas d'erreur, et pourtant rien ne change : comparez avec la cellule suivante
jouet3["close"].replace(" ", "")
""")

code('jouet3["close"].str.replace(" ", "")')

code("""
# Une erreur, et sa dernière ligne cite la valeur fautive
jouet3["close"].astype(float)
""")

# ---------------------------------------------------------------- 5. Catégories
md("""
## 5. Le texte, c'est des catégories

On vient de transformer du texte en nombres, parce que c'était des nombres mal écrits. Mais le plus souvent, le texte d'une table n'est pas un nombre déguisé.

Dans une table d'analyse, une colonne de texte, c'est de deux choses l'une :

- une **date** : on s'en occupe à la section suivante ;
- une **catégorie** : la monnaie, le pays, le secteur, le type de client.

Ici, `coin` est une catégorie. Et la première question qu'on pose à une catégorie, c'est : **combien de lignes par catégorie ?** C'est `value_counts`.
""")

code('crypto["coin"].value_counts()')

md("""
Une Series : l'index, ce sont les catégories ; les valeurs, les effectifs, du plus fréquent au moins fréquent. On y lit que SOL a moins de jours : elle est apparue plus tard.

Les catégories elles-mêmes, et leur nombre :
""")

code('crypto["coin"].unique()')

code('crypto["coin"].nunique()')

md("""
### Les catégories incohérentes

La même chose sur le fichier sale :
""")

code('net["coin"].value_counts()')

md("""
Vingt-huit catégories pour sept monnaies. Pour pandas, `"btc"` et `" BTC"` sont deux catégories, et chacune est sous-comptée.

On répare avec `strip` et `upper`, en `.str`, comme en séance 1.
""")

code("""
net["coin"] = net["coin"].str.strip().str.upper()
net["coin"].value_counts()
""")

md("""
Sept catégories. Le nettoyage d'une catégorie, c'est presque toujours ces deux méthodes.

### Prédire
""")

predire('jouet["coin"].value_counts()', 'jouet["coin"].nunique()', 'jouet["date"].value_counts()',
        'jouet["coin"].str.lower().unique()')

md("""
### Écrire

**1.** Combien de catégories `coin` avait-il dans `sale`, avant nettoyage ? Dans `nb_avant`.
""")

code("")

code("""
verifier("nb_avant", nb_avant == 28, "nunique() sur la colonne coin de sale")
""")

md("**2.** Le volume moyen de BTC dans `net`, dans `vol_btc`. Un `query` sur `coin`, qui ne marche que si le nettoyage est fait.")

code("")

code("""
verifier("vol_btc", abs(vol_btc - net.query("coin == 'BTC'")["volume"].mean()) < 1, "query sur coin == 'BTC', puis .mean() du volume")
""")

# ---------------------------------------------------------------- 6. Dates
md("""
## 6. Les dates

`date` est du texte. On peut la comparer, on l'a fait à la séance 3, mais on ne peut pas lui demander « quel mois ? ».

`pd.to_datetime` la convertit en vraie date.
""")

code("""
net["date"] = pd.to_datetime(net["date"])
net.info()
""")

md("""
Une fois convertie, `.dt` donne accès aux morceaux, comme `.str` donnait accès aux méthodes de texte.
""")

code("""
net["annee"] = net["date"].dt.year
net["mois"] = net["date"].dt.month
net.head(3)
""")

md("""
`.dt.day` existe aussi : le jour du mois.

Même chose sur `crypto`, parce que la suite travaille dessus :
""")

code("""
crypto["date"] = pd.to_datetime(crypto["date"])
crypto["annee"] = crypto["date"].dt.year
crypto.head(3)
""")

md("""
### Écrire

Le nombre de lignes de `crypto` en 2021, dans `nb_2021`, avec la colonne `annee`. Puis le cours maximum de BTC en 2021, dans `btc_max_2021`.
""")

code("")

code("""
verifier("nb_2021", nb_2021 == 2555, "query sur annee == 2021, puis len")
verifier("btc_max_2021", abs(btc_max_2021 - 67566.8281) < 0.01, "deux conditions, puis .max()")
""")

# ---------------------------------------------------------------- 7. Grouper
md("""
## 7. Regrouper : `groupby`

La section la plus importante du bloc. On y va pas à pas, sur `jouet` d'abord.

### La question

« Le cours moyen de chaque monnaie. » Trois monnaies dans `jouet`, trois moyennes. Avec ce qu'on sait, on écrit un `query` par monnaie :
""")

code("""jouet.query("coin == 'BTC'")["close"].mean()""")

md("""
Trois fois. Sept fois sur le vrai fichier. Non : **une boucle**.

La condition de `query` est un texte, donc on la fabrique avec une f-string, comme en séance 2.
""")

code("""
monnaies = ["BTC", "ETH", "SOL"]
moyennes = []
for m in monnaies:
    sous_table = jouet.query(f"coin == '{m}'")
    moyennes.append(sous_table["close"].mean())
pd.Series(moyennes, index=monnaies)
""")

md("""
### Ce que fait la boucle

```
       jouet                    découper                  calculer            rassembler
                               (une sous-table
   coin   close                 par monnaie)             (une moyenne         (une Series,
   BTC   42000                                            par sous-table)      une ligne
   ETH    2300          BTC │ 42000 │ 44000  ──►  43000                       par monnaie)
   SOL     100    ──►   ETH │  2300 │  2400  ──►   2350       ──►     BTC   43000.0
   BTC   44000          SOL │   100 │    95  ──►     97.5              ETH    2350.0
   ETH    2400                                                         SOL      97.5
   SOL      95
```

Trois temps :

1. **découper** la table en une sous-table par valeur de la colonne choisie ;
2. **calculer** une chose dans chaque sous-table ;
3. **rassembler** les résultats dans une Series dont l'index est la catégorie.

### La ligne pandas

`groupby` fait ces trois temps en une ligne.
""")

code('jouet.groupby("coin")["close"].mean()')

md("""
Même résultat, à la ligne près. Lecture de gauche à droite :

```
jouet.groupby("coin")["close"].mean()
│     │              │        │
│     │              │        └─ calculer : la moyenne dans chaque sous-table
│     │              └─ de la colonne close
│     └─ découper : une sous-table par valeur de coin
└─ la table
```

Le résultat est une **Series** : une valeur par groupe, l'index est le groupe. Tout ce qu'on sait faire sur une Series s'applique.

### Sur le vrai fichier

La même ligne.
""")

code('crypto.groupby("coin")["close"].mean()')

md("""
### Ce qu'on met à la fin

N'importe quelle fonction de colonne.
""")

code('crypto.groupby("coin")["close"].max()')

code('crypto.groupby("coin")["volume"].sum()')

code('crypto.groupby("coin")["close"].count()')

md("""
`count` compte les lignes de chaque groupe : c'est `value_counts`, obtenu autrement.

### Regrouper par autre chose

Par année, avec la colonne créée à la section 6. Une catégorie, c'est n'importe quelle colonne qui prend peu de valeurs différentes.
""")

code('crypto.groupby("annee")["volume"].sum()')

md("### Trier le résultat, aller chercher un groupe")

code('crypto.groupby("coin")["close"].mean().sort_values(ascending=False)')

code('crypto.groupby("coin")["close"].mean()["ETH"]')

md("### Prédire")

predire('jouet.groupby("coin")["volume"].sum()', 'jouet.groupby("date")["volume"].sum()',
        'jouet.groupby("coin")["close"].count()', 'jouet.groupby("coin")["close"].max().sort_values()',
        'jouet.groupby("coin")["close"].mean()["ETH"]',
        'jouet.groupby("coin")["close"].max() - jouet.groupby("coin")["close"].min()')

md("""
La dernière : deux Series avec le même index se soustraient étiquette par étiquette. L'amplitude de chaque monnaie, en une ligne.

### Lire le code, dire la question

Pour chaque ligne, à l'oral : à quelle question répond-elle ?
""")

code('crypto.groupby("annee")["close"].max()')

code("""crypto.query("coin == 'BTC'").groupby("annee")["close"].mean()""")

code('crypto.groupby("coin")["annee"].min()')

md("""
### Dire la question, écrire le code

Au tableau, ensemble :

- le volume moyen par monnaie, du plus gros au plus petit ;
- le cours minimum de chaque année pour ETH.
""")

code("")

md("""
### Écrire

**1.** Le cours moyen de chaque monnaie en 2024, dans `moy_2024`. Un `query`, puis un `groupby`. Quelle monnaie est en tête ?
""")

code("")

code("""
verifier("moy_2024", type(moy_2024) == pd.Series and len(moy_2024) == 7 and abs(moy_2024["BTC"] - 65964.12) < 0.01, "query sur annee == 2024, puis groupby('coin')['close'].mean()")
""")

md("**2.** Le nombre de jours dans le fichier pour chaque monnaie, dans `nb_jours`, trié. Comparez avec `value_counts`.")

code("")

code("""
verifier("nb_jours", len(nb_jours) == 7 and nb_jours["SOL"] == 2335 and nb_jours["BTC"] == 3165, "groupby('coin')['close'].count(), puis sort_values()")
""")

md("**3.** Refaites `moy_2024` avec la boucle et les `query`, sans `groupby`, dans `moy_2024_boucle`. Les deux Series doivent avoir les mêmes valeurs. Le but est de sentir que c'est la même chose.")

code("")

code("""
verifier("moy_2024_boucle", len(moy_2024_boucle) == 7 and all(abs(moy_2024_boucle[m] - moy_2024[m]) < 0.01 for m in moy_2024.index), "une liste vide, une boucle sur les monnaies, un query avec f-string, un append, une Series")
""")

md("""
### Corriger

La première cellule ne produit pas d'erreur. Regardez ce qu'elle renvoie, et dites pourquoi ce n'est pas ce qu'on voulait.
""")

code('crypto.groupby("coin").mean()')

code('crypto.groupby(annee)["close"].mean()')

# ---------------------------------------------------------------- 8. Tracer
md("""
## 8. Tracer

Deux graphiques, deux lignes.

Une Series de `groupby` se trace en **barres** :
""")

code('crypto.groupby("coin")["close"].mean().sort_values().plot(kind="bar")')

md("Une évolution dans le temps se trace en **courbe**, en disant quelle colonne va en abscisse :")

code("""crypto.query("coin == 'BTC'").plot(x="date", y="close")""")

md("""
### Écrire

La courbe de ETH depuis 2023. Un `query` à deux conditions, puis `plot`.
""")

code("")

# ---------------------------------------------------------------- 9. Synthèse
md("""
## 9. Ce que vous savez faire

| Vous voulez... | Vous écrivez |
|---|---|
| repérer les manquants | `df["col"].isna()`, `df.isna().sum()` |
| retirer les lignes incomplètes | `df.dropna(subset=["col"])` |
| repérer les doublons | `df.duplicated().sum()` |
| retirer les doublons | `df.drop_duplicates()` |
| une méthode de texte sur une colonne | `df["col"].str.replace(",", ".")`, `.str.strip()`, `.str.upper()` |
| texte vers nombre | `df["col"].astype(float)` |
| compter par catégorie | `df["col"].value_counts()` |
| les catégories, leur nombre | `df["col"].unique()`, `df["col"].nunique()` |
| texte vers date | `df["date"] = pd.to_datetime(df["date"])` |
| l'année, le mois, le jour | `df["date"].dt.year`, `.dt.month`, `.dt.day` |
| combien par catégorie, d'une autre colonne | `df.groupby("coin")["close"].mean()` |
| trier le résultat | `.sort_values(ascending=False)` |
| un groupe | `df.groupby("coin")["close"].mean()["ETH"]` |
| des barres | `serie.plot(kind="bar")` |
| une courbe | `df.plot(x="date", y="close")` |

## Les deux phrases du bloc

1. **Tout ce que vous savez faire sur une valeur, vous le faites maintenant sur une colonne entière.** `.str` et `.dt` sont la façon de le dire pour le texte et les dates.
2. **Tout ce que pandas fait, vous pourriez l'écrire vous-même avec une colonne de booléens et une boucle.** `dropna`, `drop_duplicates` et `groupby` : vous les avez écrits avant de les apprendre.

## Ce que vous croiserez ailleurs

Ces outils existent, vous les verrez dans des exemples en ligne. Une ligne chacun, pour les reconnaître :

| Vous verrez | Ce que ça fait |
|---|---|
| `df[df["close"] > 100]` | un `query` écrit autrement, avec `&` pour `and` et `\\|` pour `or` |
| `df.loc[3, "close"]`, `df.iloc[0]` | une case ou une ligne par son étiquette ou sa position |
| `df.merge(autre, on="col")` | coller deux tables qui partagent une colonne |
| `df.describe()` | huit statistiques d'un coup : c'est le début du bloc suivant |

## La suite

L'exercice de synthèse : si vous aviez acheté 100 dollars de bitcoin le premier de chaque mois depuis 2020, combien auriez-vous aujourd'hui ? Tout ce qu'il demande est dans ces deux séances.
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
