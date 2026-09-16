"""Construit la séance 5 du cours : décrire le risque (bloc stats, première partie).

    python3 stats_crypto/build/build_s1.py
"""
import json, os, textwrap

OUT = "stats_crypto/cours/seance1_cours.ipynb"
LOGO = '<img src="https://cdn.jsdelivr.net/gh/aureliensalas/python_finance@main/ressources/img/logo_macmia.png" alt="Banque des Territoires · France 2030 · MACMIA" width="520">'
BADGE = "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aureliensalas/python_finance/blob/main/stats_crypto/cours/seance1_cours.ipynb)"
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
    """Une cellule par expression, nue. On annonce la valeur à voix haute, puis on exécute."""
    for e in exprs:
        code(e)

# ---------------------------------------------------------------- en-tête
md(f"""
{LOGO}

{BADGE}

# Séance 5 : décrire le risque

**Cours** · 2h · statistiques, première partie

> ⚠️ **Avant de taper quoi que ce soit :** *Fichier → Enregistrer une copie dans Drive*. Sinon votre travail sera perdu en fermant l'onglet.
>
> 📱 Sur tablette, faites d'abord les réglages de [Bien démarrer](https://github.com/aureliensalas/python_finance/blob/main/ressources/setup_tablette.md).
""")

md("""
## Objectifs

À la fin de cette séance, vous saurez :

- construire la colonne qui manque à toute table de prix : le rendement
- repérer une colonne fausse en regardant ses extrêmes
- dire à quoi ressemble une journée d'un actif, avec cinq nombres et leur sens
- comparer des actifs entre eux avec `groupby`, sur plusieurs mesures à la fois
- tracer une distribution et y lire ce qui compte
- produire la fiche d'identité d'une monnaie

## Les deux phrases du bloc

> **Un prix ne se compare pas. Un rendement, si.**

> **Une moyenne calculée sur des données n'est pas la vraie moyenne. C'est une estimation, et une estimation a une épaisseur.**

La première organise cette séance. La seconde organise la suivante.

## Les questions de la séance

Le même fichier que le bloc pandas : sept cryptomonnaies, huit ans et demi. Vous savez déjà tout charger, filtrer, regrouper. Il manque **une colonne**, et avec elle on saura répondre à :

- quelle monnaie rapporte le plus, et laquelle fait le plus peur ?
- combien perd le bitcoin les mauvais jours ?
- le marché des cryptos se calme-t-il avec le temps ?
- y a-t-il un jour de la semaine à éviter ?

> **Les cellules « Prédire ».** Avant de les exécuter, on annonce **à voix haute** la valeur attendue. Rien à écrire : on dit, on exécute, on compare.

Exécutez d'abord la cellule de setup.
""")

code(f"""
import numpy as np
import pandas as pd
from scipy import stats                    # servira à la séance suivante

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

On charge, on convertit la date, et on **trie** : par monnaie, puis par date. Ce tri n'est pas cosmétique. Toute la section 1 en dépend : on veut que les jours d'une même monnaie se suivent, dans l'ordre.
""")

code("""
crypto = pd.read_csv(BASE + "crypto.csv")
crypto["date"] = pd.to_datetime(crypto["date"])
crypto = crypto.sort_values(["coin", "date"]).reset_index(drop=True)
crypto.head()
""")

md("""
Deux cellules de reprise du bloc pandas.

**1.** Le nombre de jours où le bitcoin a clôturé au-dessus de 100 000 dollars, dans `nb_100k`.
""")

code("")

code("""
verifier("nb_100k", nb_100k == len(crypto.query("coin == 'BTC' and close > 100000")), "un query à deux conditions, puis len")
""")

md("**2.** Le cours moyen de chaque monnaie, dans `cours_moyen`. Une ligne.")

code("")

code("""
verifier("cours_moyen", abs(cours_moyen["BTC"] - crypto.query("coin == 'BTC'")["close"].mean()) < 0.01, "groupby('coin')['close'].mean()")
""")

# ---------------------------------------------------------------- 1. La colonne qui manque
md("""
## 1. La colonne qui manque

Le 31 août 2026, le bitcoin vaut 78 548 dollars et le dogecoin 0,21 dollar. **Lequel des deux a fait la meilleure journée ?**

La question n'a pas de réponse tant qu'on regarde des prix. Les deux échelles n'ont rien à voir, et aucune moyenne, aucun tri, aucun `groupby` ne les rendra comparables. Ce qu'il faut, c'est la **variation en pourcentage par rapport à la veille**. On l'appelle le **rendement**, et c'est l'unité de compte de la finance : il se compare entre monnaies, entre années, entre n'importe quels actifs.

> **Un prix ne se compare pas. Un rendement, si.**

### À la main, sur cinq lignes

Comme toujours, on construit d'abord sur une table qu'on peut lire d'un coup d'œil.
""")

code("""
jouet = pd.DataFrame({"close": [100.0, 110.0, 99.0, 99.0, 148.5]})
jouet
""")

md("""
De 100 à 110 : **+10 %**. De 110 à 99 : **−10 %**. De 99 à 99 : **0 %**. De 99 à 148,5 : **+50 %**.

La formule, que tout le monde sait écrire : `(prix d'aujourd'hui − prix d'hier) / prix d'hier × 100`.

Il ne manque qu'une chose pour l'écrire sur une colonne : **le prix d'hier, sur la même ligne qu'aujourd'hui.**

### `shift` : décaler d'un cran

Une méthode, une idée : `shift(1)` fait descendre la colonne d'une ligne.
""")

code("""
jouet["hier"] = jouet["close"].shift(1)
jouet
""")

md("""
La première ligne vaut `NaN` : le premier jour n'a pas de veille. C'est juste, pas un bug — et vous savez depuis le bloc pandas ce qu'est un `NaN`.

### Écrire

Créez la colonne `jouet["r"]`, le rendement en pourcentage, avec la formule ci-dessus et les deux colonnes `close` et `hier`.
""")

code("")

code("""
verifier("rendements du jouet", abs(jouet["r"][1] - 10) < 1e-9 and abs(jouet["r"][2] + 10) < 1e-9 and abs(jouet["r"][4] - 50) < 1e-9, "(close - hier) / hier * 100")
""")

md("""
### Le raccourci

Comme `sum(flux)` après la boucle accumulateur du bloc Python : ce que vous venez d'écrire, pandas le fait déjà.
""")

code("""
jouet["close"].pct_change() * 100
""")

md("""
Même colonne. `pct_change` fait le `shift`, la soustraction et la division. Le `* 100` reste à notre charge : pandas donne une proportion, on veut des pourcentages.

### Sur la vraie table — et le piège

On applique, et on prend **un seul réflexe : regarder le maximum**.
""")

code("""
crypto["r"] = crypto["close"].pct_change() * 100
print(crypto["r"].max())
""")

md("""
**933 041 %.** Aucun actif n'a jamais fait ça en une journée. Quelque chose est faux — et rien ne le disait dans les cinq premières lignes.

D'où ça vient : la table est triée par monnaie puis par date. À chaque **changement de monnaie**, `pct_change` compare le premier jour de l'une au dernier jour de l'autre. Ça produit des valeurs énormes dans **les deux sens** : regardons les trois plus hautes et les trois plus basses.
""")

code("""
hautes = crypto.sort_values("r", ascending=False).head(3)[["date", "coin", "close", "r"]]
basses = crypto.sort_values("r").head(3)[["date", "coin", "close", "r"]]
display(hautes, basses)
""")

md("""
`display` affiche plusieurs tables l'une sous l'autre dans une même cellule ; la dernière expression, elle, n'en afficherait qu'une.

Ces six lignes sont **exactement** les six frontières : six changements de monnaie pour sept monnaies, toutes au premier jour de la monnaie suivante. Invisibles à l'œil dans un aperçu, catastrophiques dans un maximum, et elles auraient contaminé toutes les moyennes du cours.

> **L'erreur silencieuse de cette séance.** Elle ne lève aucune exception. Elle ne se voit pas dans `head()`. Elle se trouve en regardant les extrêmes. **Après avoir créé une colonne, on regarde son `max` et son `min` avant de s'en servir.**

### La correction

Il faut que le calcul reparte de zéro à chaque monnaie. C'est exactement ce que `groupby` sait faire : « fais le calcul **séparément dans chaque groupe** ».
""")

code("""
crypto["r"] = crypto.groupby("coin")["close"].pct_change() * 100
print(crypto["r"].max())
""")

md("""
**354,67 %.** C'est le dogecoin, le 28 janvier 2021 — le jour où Reddit s'en est emparé. Vrai, et vérifiable.

Il reste à retirer les sept premiers jours, un par monnaie, qui n'ont pas de veille.
""")

code("""
crypto = crypto.dropna(subset=["r"])
len(crypto)
""")

md("### Prédire")

predire('print(crypto["r"].min() < -30)',
        'print(crypto.query("coin == \'DOGE\'")["r"].max())',
        'len(crypto.query("r > 100"))')

# ---------------------------------------------------------------- 2. Une journée de bitcoin
md("""
## 2. À quoi ressemble une journée de bitcoin ?

Une seule question, et la réponse va surprendre. On isole le bitcoin, et on demande son rendement moyen.
""")

code("""
btc = crypto.query("coin == 'BTC'")
print(btc["r"].mean())
""")

md("""
**+0,111 % par jour.** Est-ce que ça décrit une journée de bitcoin ? On va voir que non, et pourquoi.

### `describe` : tout voir d'un coup

Huit nombres en une ligne. On les lit ensemble.
""")

code("""
btc["r"].describe()
""")

md("""
### Trois lectures, et chacune dit quelque chose de différent

**1. La moyenne n'est pas le milieu.** Médiane `50%` : +0,063 %. Moyenne : +0,111 %. La moyenne fait presque le **double** de la médiane. Elle est tirée vers le haut par quelques très gros jours de hausse.

> **La médiane dit ce que fait un jour ordinaire. La moyenne dit ce que fait le portefeuille sur la durée.** Deux questions différentes, deux nombres différents, et on aura besoin des deux.

**2. L'écart-type, c'est le risque — et il écrase la tendance.** `std` : 3,33 %. En finance, l'écart-type n'est pas un indicateur technique parmi d'autres : **c'est la définition du risque.** Et le rapport entre les deux nombres est la phrase à retenir de la séance :

> **La tendance est de +0,11 % par jour. Le bruit est de ±3,3 %. Le bruit est trente fois plus grand que la tendance.**
>
> Une journée de bitcoin, ce n'est pas +0,11 %. C'est n'importe quoi entre −3 % et +3 %, avec une infime dérive vers le haut qu'on ne peut pas sentir au jour le jour. C'est pour ça que la séance suivante parlera d'incertitude.

**3. Le quantile 5 %, c'est le mauvais jour habituel.**
""")

code("""
print(btc["r"].quantile(0.05))
""")

md("""
**−5,02 %.** Un jour sur vingt, le bitcoin perd plus de 5 %. Sur 10 000 euros placés, c'est 500 euros partis dans la journée, à peu près une fois par mois.

Ce nombre a un nom : c'est une **Value at Risk** à 95 %, l'indicateur que toute salle de marché calcule chaque soir. Vous venez de l'obtenir par une méthode, sans formule.

### Prédire
""")

predire('print(btc["r"].quantile(0.5) == btc["r"].median())',
        'print(btc["r"].quantile(0.01) < btc["r"].quantile(0.05))',
        'print((btc["r"] > 0).mean())')

md("""
### Écrire

La même chose pour l'ether. Dans `eth`, les lignes de ETH ; puis `eth_moyenne`, `eth_mediane`, `eth_std` et `eth_var` (le quantile 5 %).
""")

code("")

code("""
verifier("eth", len(eth) == 3164 and eth["coin"].nunique() == 1, "query sur coin == 'ETH'")
verifier("moyenne et mediane", abs(eth_moyenne - 0.13) < 0.01 and abs(eth_mediane - 0.06) < 0.01, ".mean() et .median()")
verifier("ecart-type", abs(eth_std - 4.37) < 0.01, ".std()")
verifier("VaR", abs(eth_var - (-6.59)) < 0.01, ".quantile(0.05)")
""")

md("""
ETH rapporte un peu plus que BTC (+0,13 % contre +0,11 %) et fait perdre davantage les mauvais jours (−6,59 % contre −5,02 %). C'est le premier **arbitrage rendement-risque** de la séance. Il revient tout de suite, sur les sept monnaies.
""")

# ---------------------------------------------------------------- 3. groupby
md("""
## 3. Et les autres ? `groupby`

Toutes les questions intéressantes sur un jeu de données financier sont des questions **par groupe** : par monnaie, par année, par jour. Vous avez l'outil depuis le bloc pandas. On le pousse.

Rappel de la forme, une ligne : `table.groupby("ce qui groupe")["ce qu'on résume"].fonction()`.

### Quelle monnaie rapporte, et laquelle fait peur ?
""")

code("""
crypto.groupby("coin")["r"].mean().sort_values()
""")

md("Le rendement. Et le risque, c'est la même ligne avec `std` :")

code("""
crypto.groupby("coin")["r"].std().sort_values()
""")

md("""
**Les deux d'un coup : `.agg`.** Seule nouveauté de la section, et elle est minuscule. Au lieu d'appeler une fonction, on passe une **liste de noms de fonctions**.
""")

code("""
crypto.groupby("coin")["r"].agg(["mean", "std"])
""")

md("""
Le résultat n'est plus une Series mais une **DataFrame à deux colonnes** : une par fonction. Retenez-le, la section 4 s'en servira.

> **L'interprétation — et c'est la leçon centrale de la séance.** Classez les monnaies par rendement, puis par risque : c'est presque le même ordre. BTC rapporte le moins et bouge le moins. DOGE et SOL rapportent le plus et bougent le plus.
>
> **On ne gagne pas plus sans accepter de perdre plus.** Ce n'est pas une règle du cours, c'est ce que les données disent, et vous venez de le lire dans deux colonnes.

### Le marché se calme-t-il ?

`groupby` ne groupe pas seulement par des colonnes reçues. Il groupe par n'importe quelle colonne — y compris celle qu'on vient de fabriquer.
""")

code("""
crypto["annee"] = crypto["date"].dt.year
crypto.groupby("annee")["r"].std()
""")

md("""
2018 : 6,5 %. 2023 : 3,6 %. 2026 : 3,2 %. Oui, le marché se calme. **Sauf 2021, à 10,5 %**, qui dépasse tout.

Pourquoi ? On applique le réflexe de la section 1 : on regarde les extrêmes.
""")

code("""
crypto.query("annee == 2021").sort_values("r", ascending=False).head(3)[["date", "coin", "r"]]
""")

md("""
Le +354 % du dogecoin. Retirons-le par la pensée :
""")

code("""
print(crypto.query("annee == 2021 and r < 300")["r"].std())
""")

md("""
**7,9 %** au lieu de 10,5 %.

> **Un seul jour sur 2 555 a déplacé l'écart-type de l'année de 25 %.** C'est la propriété la plus traître de l'écart-type : il donne un poids énorme aux valeurs extrêmes. **On ne commente jamais un écart-type sans avoir regardé ce qu'il y a dedans.**

### Y a-t-il un jour de la semaine à éviter ?

Une autre colonne fabriquée : le jour de la semaine, de 0 (lundi) à 6 (dimanche).
""")

code("""
crypto["jour_sem"] = crypto["date"].dt.dayofweek
btc = crypto.query("coin == 'BTC'")
btc.groupby("jour_sem")["r"].mean()
""")

md("""
Lundi : +0,31 %. **Jeudi : −0,25 %.** Plus d'un demi-point d'écart par jour — annualisé, c'est énorme.

**Le bitcoin baisse-t-il le jeudi ?** On pose la question. On n'y répond pas aujourd'hui. Gardez-la en tête : c'est le fil de la prochaine séance.

### Lire le code, dire la question

Pour chaque cellule, dites **en français** à quelle question elle répond, avant de l'exécuter.
""")

code("""
crypto.groupby("coin")["r"].max()
""")

code("""
crypto.groupby("annee")["r"].mean().sort_values(ascending=False)
""")

code("""
crypto.query("coin == 'SOL'").groupby("annee")["r"].std()
""")

md("""
### Écrire

**1.** La part de jours de hausse de chaque monnaie, dans `part_hausse`. Indication : une comparaison sur une colonne donne des booléens, et la moyenne d'une colonne de booléens est une part (bloc pandas, séance 3). Créez d'abord une colonne `hausse`.
""")

code("")

code("""
verifier("part_hausse", abs(part_hausse["DOGE"] - 0.399) < 0.001 and abs(part_hausse["BNB"] - 0.520) < 0.001, "une colonne de booléens r > 0, puis groupby('coin') et mean()")
""")

md("""
> **Le plus beau résultat de la séance.** Le dogecoin ne monte que **quatre jours sur dix** — le pire des sept — et affiche pourtant le deuxième rendement moyen. Il monte rarement, et énormément quand il monte. C'est la section 2 en acte : moyenne et médiane ne racontent pas la même histoire, et c'est la médiane qui dit la vérité du quotidien. Quelqu'un qui aurait acheté du DOGE sur son rendement moyen aurait passé six jours sur dix à perdre.

**2.** Le pire jour de chaque monnaie, dans `pire_jour`. Une ligne.
""")

code("")

code("""
verifier("pire_jour", abs(pire_jour["ETH"] + 42.35) < 0.01 and len(pire_jour) == 7, "groupby('coin')['r'].min()")
""")

md("""
Six des sept pires jours sont entre −37 % et −42 %. **Sont-ils tombés le même jour ?** Question laissée ouverte. Réponse à la prochaine séance.
""")

# ---------------------------------------------------------------- 4. Voir
md("""
## 4. Voir

Une règle, et elle tient tout le bloc :

> **Un graphique est une méthode appelée sur un résultat.** Le résultat est une colonne ou un `groupby`. On écrit `resultat.plot(...)`, et rien d'autre.

Trois arguments pour habiller, pas plus : `title=`, `xlabel=` ou `ylabel=`, `figsize=`.

### La forme d'une journée

L'histogramme des rendements du bitcoin. C'est le graphique le plus important du bloc.
""")

code("""
btc["r"].plot(kind="hist", bins=40, title="Rendements quotidiens du bitcoin", xlabel="% par jour", figsize=(8, 4))
""")

md("""
On lit ensemble. Une **cloche**, centrée à peine au-dessus de zéro : la tendance de la section 2, invisible. **Large** : le bruit de la section 2. Et **deux queues longues et fines**, à gauche jusqu'à −37 %, à droite jusqu'à +19 %.

### Compter ce qu'il y a dans les queues

Combien de jours sont à plus de trois écarts-types de la moyenne ?
""")

code("""
print((btc["r"].abs() > 3 * btc["r"].std()).sum())
""")

md("""
**62 jours.** Si les rendements suivaient la cloche parfaite qu'on apprend en cours de mathématiques, on en attendrait **8**. Sept fois trop.

> **Les marchés ne sont pas gaussiens.** Les journées extrêmes sont beaucoup plus fréquentes que la cloche ne le prédit, et toujours plus violentes à la baisse. C'est pour cela que les modèles de risque se trompent tous dans le même sens : ils sous-estiment le pire. Retenez l'image : la cloche est là, mais **ses queues sont grasses**.

### Rendement et risque côte à côte

Deux séries sur un graphique, ce n'est pas deux appels : c'est **une DataFrame à deux colonnes**. La section 3 l'a déjà produite.
""")

code("""
crypto.groupby("coin")["r"].agg(["mean", "std"]).sort_values("std").plot(kind="bar", title="Rendement et risque par monnaie", ylabel="% par jour", figsize=(9, 4))
""")

md("""
L'arbitrage de la section 3 devient une image : les deux barres montent ensemble.

### Les autres graphiques

Ils existent, on ne les démontre pas aujourd'hui. Une ligne chacun, pour les reconnaître :

| Je veux... | `kind=` | Sur quoi |
|---|---|---|
| comparer des catégories | `"bar"` | un résultat de `groupby` |
| voir la forme d'une distribution | `"hist"` | une colonne |
| suivre dans le temps | `"line"` | une table triée par date, avec `x="date", y=` |
| relier deux colonnes | `"scatter"` | une table, avec `x=` et `y=` |

### Écrire

L'histogramme des rendements du dogecoin, même habillage, dans une table `doge`.
""")

code("")

md("""
Comparez au graphique du bitcoin : une cloche beaucoup plus large, et une queue droite qui part très loin. Le risque de DOGE, c'est cette largeur.
""")

# ---------------------------------------------------------------- 5. Synthèse
md("""
## 5. Ce que vous savez faire

| Vous voulez... | Vous écrivez |
|---|---|
| le prix de la veille sur la même ligne | `df["close"].shift(1)` |
| le rendement, par groupe | `df.groupby("coin")["close"].pct_change() * 100` |
| vérifier une colonne neuve | `df["r"].max()`, `df["r"].min()` |
| huit statistiques d'un coup | `df["r"].describe()` |
| le jour ordinaire, la tendance | `.median()`, `.mean()` |
| le risque | `.std()` |
| le mauvais jour habituel | `.quantile(0.05)` |
| plusieurs mesures par groupe | `df.groupby("coin")["r"].agg(["mean", "std"])` |
| grouper par une colonne fabriquée | `df["annee"] = df["date"].dt.year`, puis `groupby("annee")` |
| une part | `(df["r"] > 0).mean()` |
| la forme d'une colonne | `df["r"].plot(kind="hist", bins=40)` |
| deux mesures côte à côte | `df.groupby(...)["r"].agg([...]).plot(kind="bar")` |
| habiller | `title=`, `xlabel=` / `ylabel=`, `figsize=` |

## Les deux phrases du bloc

1. **Un prix ne se compare pas. Un rendement, si.** La colonne `r` est celle sur laquelle tout le reste du semestre travaille.
2. **Une moyenne calculée sur des données n'est pas la vraie moyenne.** +0,11 % par jour, dans un bruit de ±3,3 % : la séance suivante mesure l'épaisseur de ce chiffre.

## Trois réflexes

1. **Après avoir créé une colonne, regardez son `max` et son `min`.** Les 933 041 % ne se voyaient nulle part ailleurs.
2. **Jamais un écart-type sans regarder ce qu'il y a dedans.** Un seul jour a déplacé celui de 2021 de 25 %.
3. **La médiane dit le quotidien, la moyenne dit la durée.** DOGE monte quatre jours sur dix et rapporte le deuxième mieux.

## Le travail noté

Vous allez produire la **fiche d'identité d'une monnaie** : les cinq nombres qu'un analyste donne quand on lui demande « parle-moi de cet actif », présentés comme une vraie fiche. Tout ce qu'il demande est dans cette séance.

## Pour la prochaine séance

Trois cellules à prédire, une à écrire.
""")

predire('print(crypto.groupby("coin")["r"].median()["DOGE"] < 0)',
        'print(crypto.groupby("annee")["r"].std().max() > 10)',
        'print(crypto["r"].quantile(0.95) > 5)')

md("""
La volatilité (écart-type des rendements) de chaque monnaie **en 2024 seulement**, triée de la plus faible à la plus forte, dans `vol_2024`.
""")

code("")

code("""
verifier("vol_2024", len(vol_2024) == 7 and vol_2024.index[0] == "BTC" and abs(vol_2024["BTC"] - 2.80) < 0.01, "query sur annee == 2024, groupby('coin')['r'].std(), sort_values()")
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
