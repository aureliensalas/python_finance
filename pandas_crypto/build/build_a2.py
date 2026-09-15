"""Construit l'assignment 2 du bloc pandas : l'investissement programmé.

    python3 pandas_crypto/build/build_a2.py
"""
import json, os, textwrap

OUT = "pandas_crypto/assignment/investissement_programme.ipynb"
LOGO = '<img src="https://cdn.jsdelivr.net/gh/aureliensalas/python_finance@main/ressources/img/logo_macmia.png" alt="Banque des Territoires · France 2030 · MACMIA" width="520">'
BADGE = "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aureliensalas/python_finance/blob/main/pandas_crypto/assignment/investissement_programme.ipynb)"
BASE = "https://cdn.jsdelivr.net/gh/aureliensalas/python_finance@main/pandas_crypto/data/"

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

# Assignment 2 : l'investissement programmé

**Travail noté** · lancé en séance, terminé à la maison

> ⚠️ **Avant de taper quoi que ce soit :** *Fichier → Enregistrer une copie dans Drive*. Sinon votre travail sera perdu en fermant l'onglet.

| | |
|---|---|
| **Rendu** | ce notebook, toutes les cellules exécutées, [date à fixer] |
| **Travail** | [seul ou en binôme, à fixer] |
| **Ressources** | les deux notebooks du bloc pandas et le notebook Python ; rien d'autre n'est nécessaire |
| **Barème** | 20 points, détaillé partie par partie |

Écrivez votre nom ici : **[nom]**
""")

md("""
## La demande

Vous êtes analyste dans une société de gestion de patrimoine. Une cliente vous pose une question qu'on entend souvent, formulée simplement :

> « Si j'avais mis 100 dollars dans le bitcoin le premier de chaque mois depuis janvier 2020, j'aurais combien aujourd'hui ? Et est-ce que j'aurais mieux fait de tout mettre d'un coup ? »

Investir un montant fixe à intervalle régulier, quel que soit le prix, s'appelle l'**investissement programmé** — en anglais *dollar-cost averaging*. C'est l'un des conseils les plus répandus de la profession. Vous allez mesurer ce qu'il vaut, sur des données réelles, et surtout expliquer **pourquoi** il produit ce qu'il produit.

Votre équipe données vous transmet un export de la plateforme de marché : `crypto_export.csv`. Personne ne l'a relu. Votre réponse à la cliente devra contenir des chiffres, des graphiques, et quelques phrases en français.

## Ce que vous allez construire

```
 export brut  →  table propre  →  calendrier d'achat  →  coût et valeur  →  pourquoi ça marche  →  les sept monnaies
 parties 1-2                        partie 3                partie 4              partie 5              partie 6
```

Chaque partie utilise le résultat de la précédente. Les cellules s'exécutent dans l'ordre, de haut en bas.

Tout ce qui est demandé a été vu dans les deux séances pandas, à **une** exception près, signalée à l'endroit où elle sert. Quand une partie renvoie à une section du cours, c'est là qu'est la réponse.

## Comment travailler

- Une idée par cellule. Une cellule qui fait trois choses est difficile à corriger.
- Après chaque exercice, une cellule `verifier` vous dit si le résultat est bon. Un `A REVOIR` n'enlève pas de points : il vous dit où regarder.
- Certaines cellules sont **fournies** : un graphique, une mise en forme. Exécutez-les, lisez-les, ne les modifiez pas.
- Avant de rendre : *Exécution → Redémarrer et tout exécuter*. Tout doit passer sans erreur, de haut en bas.

| Partie | Points |
|---|---|
| 1. Le diagnostic | 2 |
| 2. La réparation | 4 |
| 3. Le calendrier d'achat | 3 |
| 4. Ce que ça a coûté, ce que ça vaut | 4 |
| 5. Pourquoi ça marche | 3 |
| 6. Les sept monnaies | 4 |

Exécutez d'abord la cellule de setup.
""")

code(f"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.options.mode.copy_on_write = True
BASE = "{BASE}"


def verifier(nom, condition, indice=""):
    if condition:
        print("OK       -", nom)
    else:
        print("A REVOIR -", nom, ":", indice)
""")

# ---------------------------------------------------------------- Partie 0
md("""
## Partie 0 : l'export (fournie)

La cellule suivante charge le fichier transmis par l'équipe données. Exécutez-la et regardez les premières lignes.
""")

code("""
export = pd.read_csv(BASE + "crypto_export.csv")
export.head()
""")

md("""
À l'œil, il ressemble au `crypto.csv` des séances : une monnaie, un jour, un cours, un volume. Mais ce fichier sort d'une plateforme, pas d'un cours. Il n'a pas été vérifié, et les cinq premières lignes ne disent rien de ce qu'il y a dans les vingt mille suivantes.
""")

# ---------------------------------------------------------------- Partie 1
md("""
## Partie 1 : le diagnostic (2 points)

On n'écrit pas un chiffre à une cliente à partir d'une table qu'on n'a pas inspectée. L'inspection est la première chose qu'on fait sur une table qu'on n'a pas construite soi-même (séance 2.1, section 3) — et ici elle n'est pas une formalité : ce qu'elle révèle décide de tout ce qui suit.

### 1a. La forme et les types (1 point)

Combien de lignes, combien de colonnes, et de quel type est chaque colonne ? Utilisez `shape` et `info()`.

Rangez le nombre de lignes dans `nb_lignes_brut`.
""")

code("")

code("""
verifier("nombre de lignes", nb_lignes_brut == len(export), "shape donne (lignes, colonnes) ; ou len(export)")
""")

md("""
Lisez la sortie d'`info()` et répondez ici :

- Quelle colonne n'a **pas** le type qu'elle devrait avoir ? Lequel a-t-elle, lequel devrait-elle avoir ? [à compléter]
- Quelles colonnes ont des valeurs manquantes ? [à compléter]

### 1b. Les catégories et les doublons (1 point)

La colonne `coin` est une catégorie : la première question à lui poser est « combien de lignes par catégorie ? » (séance 2.2, section 5).

Affichez son `value_counts()`. Rangez dans `nb_noms_bruts` le nombre de noms différents qu'elle contient, avec `nunique()`. Puis rangez dans `nb_doublons` le nombre de lignes en double, avec `duplicated()` et `sum()` (séance 2.2, section 3).
""")

code("")

code("""
verifier("noms de monnaies", nb_noms_bruts == export["coin"].nunique() and nb_noms_bruts > 7, "nunique() sur la colonne coin ; il devrait y en avoir 7, il y en a plus")
verifier("doublons", nb_doublons == export.duplicated().sum(), "duplicated() donne une colonne de bool, sum() la compte")
""")

md("""
Écrivez le diagnostic, en trois lignes, comme vous le diriez à l'équipe données :

**Diagnostic :** [à compléter — combien de monnaies il devrait y avoir, combien le fichier en montre, et pourquoi ; ce qui ne va pas avec les prix ; combien de lignes en double]

### Point d'étape

Quatre défauts : des noms de monnaies écrits de plusieurs façons, des prix en texte, des lignes en double, des valeurs manquantes. **Aucun n'était visible sur les cinq premières lignes.** Et chacun, laissé en l'état, aurait faussé la réponse à la cliente — trois d'entre eux sans le moindre message d'erreur.
""")

# ---------------------------------------------------------------- Partie 2
md("""
## Partie 2 : la réparation (4 points)

On construit `crypto`, la table propre, à partir d'`export`. Un défaut par étape, une vérification après chaque.

Commencez par une copie de travail, pour garder l'export intact :
""")

code("""
crypto = export.copy()
""")

md("""
### 2a. Les noms de monnaies (1 point)

Sept monnaies, vingt-huit façons de les écrire. Harmonisez la colonne `coin` : sans espace autour, en majuscules (séance 2.2, section 5).

Pourquoi c'est la première chose à faire : sans cette étape, `query("coin == 'BTC'")` ne verrait ni `btc` ni `BTC ` — une partie des achats disparaîtrait **sans message d'erreur**. C'est le pire type de défaut : le silencieux.
""")

code("")

code("""
verifier("sept monnaies", crypto["coin"].nunique() == 7, ".str.strip() pour les espaces, .str.upper() pour la casse, dans cet ordre ou l'autre")
verifier("noms propres", sorted(crypto["coin"].unique()) == ["ADA", "BNB", "BTC", "DOGE", "ETH", "SOL", "XRP"], "les sept codes en majuscules, sans espace")
""")

md("""
### 2b. Les prix (1 point)

Les prix sont écrits à la française, avec une espace pour les milliers, une virgule pour les décimales et le symbole de la devise : `"78 548,63 $"`. Python ne peut rien calculer dessus.

Transformez la colonne `close` en nombres (séance 2.2, section 4). Trois choses à retirer, puis une conversion.
""")

code("")

code("""
verifier("prix numeriques", crypto["close"].dtype == float, ".str.replace pour l'espace, la virgule et le symbole, puis astype(float)")
verifier("ordre de grandeur", crypto["close"].max() > 100000 and crypto["close"].min() < 1, "le bitcoin a dépassé 100 000 $, DOGE et ADA valent moins de 1 $ : si ce n'est pas le cas, une virgule a été perdue")
""")

md("""
### 2c. Les doublons (1 point)

Une ligne recopiée, c'est un achat compté deux fois. Retirez les doublons (séance 2.2, section 3).
""")

code("")

code("""
verifier("plus de doublon", crypto.duplicated().sum() == 0, "drop_duplicates()")
verifier("nombre de lignes", len(crypto) == nb_lignes_brut - nb_doublons, "on doit avoir retiré exactement nb_doublons lignes")
""")

md("""
### 2d. Les valeurs manquantes (1 point)

Deux colonnes ont des trous. Elles ne se traitent pas de la même façon, et c'est un choix d'analyste, pas une règle mécanique :

- **`volume`** : il manque sur quelques lignes. On n'en a **pas besoin** pour répondre à la cliente. On garde ces lignes.
- **`close`** : il manque sur quelques lignes. Une ligne sans prix est inutilisable. On la retire.

Rangez d'abord dans `nb_sans_prix` le nombre de lignes dont le prix manque. Puis retirez ces lignes, et seulement celles-là (séance 2.2, section 2 : `dropna` avec `subset`).
""")

code("")

code("""
verifier("prix manquants comptes", nb_sans_prix == 24, "isna() sur la colonne close, puis sum()")
verifier("plus de prix manquant", crypto["close"].isna().sum() == 0, "dropna(subset=['close'])")
verifier("volumes manquants gardes", crypto["volume"].isna().sum() > 0, "vous avez retiré des lignes sans volume : dropna sans subset retire trop ; il faut subset=['close']")
verifier("nombre de lignes", len(crypto) == nb_lignes_brut - nb_doublons - nb_sans_prix, "on doit avoir retiré exactement nb_sans_prix lignes de plus")
""")

md("""
### Point d'étape

`crypto` a maintenant sept monnaies, des prix numériques, aucune ligne en double, aucune ligne sans prix — et ses volumes manquants, qu'on a choisi de garder en connaissance de cause. C'est la table que vous auriez dû recevoir. Tout ce qui suit se fait dessus, et rien de ce qui suit ne serait juste sans ce que vous venez de faire.
""")

# ---------------------------------------------------------------- Partie 3
md("""
## Partie 3 : le calendrier d'achat (3 points)

La cliente achète le **premier jour de chaque mois**, à partir du **1er janvier 2020**. Il faut isoler ces jours-là.

### 3a. Les dates (1 point)

La colonne `date` est du texte. Convertissez-la en vraie date, puis créez trois colonnes `annee`, `mois` et `jour` (séance 2.2, section 6).
""")

code("")

code("""
verifier("date convertie", str(crypto["date"].dtype).startswith("datetime"), "pd.to_datetime sur la colonne date")
verifier("trois colonnes", crypto["annee"].min() == 2018 and crypto["mois"].max() == 12 and crypto["jour"].max() == 31, ".dt.year, .dt.month, .dt.day")
""")

md("""
### 3b. Les jours d'achat (2 points)

Construisez `achats` : les lignes de `crypto` qui sont du bitcoin, dont le jour est le 1er, et dont l'année est 2020 ou après. Un seul `query`, trois conditions reliées par `and` (séance 2.1, section 5).

Chaque ligne d'`achats` est un jour où la cliente a acheté, et `close` est le prix qu'elle a payé ce jour-là.
""")

code("")

code("""
verifier("une ligne par mois", len(achats) == 80, "de janvier 2020 à août 2026, il y a 80 premiers du mois")
verifier("que du bitcoin", achats["coin"].nunique() == 1 and achats["coin"].unique()[0] == "BTC", "coin == 'BTC' dans le query")
verifier("que des premiers du mois", achats["jour"].max() == 1 and achats["annee"].min() == 2020, "jour == 1 and annee >= 2020")
""")

md("""
**Regardez vos 80 achats sur la courbe du bitcoin.** Cellule fournie : exécutez-la.
""")

code("""
btc = crypto.query("coin == 'BTC' and annee >= 2020")
ax = btc.plot(x="date", y="close", figsize=(11, 4), legend=False, color="#9AA5B1", linewidth=1)
ax.scatter(achats["date"], achats["close"], s=22, color="#1F4E79", zorder=3, label="un achat de 100 $")
ax.set_title("Bitcoin depuis 2020 : les 80 achats de la cliente", loc="left")
ax.set_xlabel("")
ax.set_ylabel("Cours (USD)")
ax.legend(frameon=False)
plt.show()
""")

md("""
### Point d'étape

Chaque point est un achat de 100 dollars. Certains sont tout en haut de la courbe, d'autres tout en bas. La cliente n'a jamais essayé de choisir : elle a acheté le 1er, c'est tout. Toute la question est de savoir si ça se compense — et dans quel sens.
""")

# ---------------------------------------------------------------- Partie 4
md("""
## Partie 4 : ce que ça a coûté, ce que ça vaut (4 points)

### 4a. Ce qu'elle a accumulé (2 points)

Avec 100 dollars à un prix `close`, on obtient `100 / close` bitcoin. Créez la colonne `achats["quantite"]` (séance 2.1, section 2).

Puis rangez dans `total_btc` la somme de cette colonne — tout le bitcoin accumulé — et dans `total_investi` le montant total versé : 100 dollars fois le nombre d'achats.
""")

code("")

code("""
verifier("quantite par achat", abs(achats["quantite"].sum() - (100 / achats["close"]).sum()) < 1e-9, "100 / close, colonne par colonne")
verifier("total investi", total_investi == 100 * len(achats), "100 fois le nombre de lignes d'achats")
verifier("total bitcoin", abs(total_btc - achats["quantite"].sum()) < 1e-9, "la somme de la colonne quantite")
""")

md("""
### 4b. Ce que ça vaut aujourd'hui (2 points)

Il faut le **dernier cours** connu du bitcoin : celui de la dernière ligne de `crypto` pour cette monnaie.

**La seule nouveauté de ce devoir.** Vous savez prendre le dernier élément d'une liste avec `liste[-1]`. Sur une colonne pandas, ça s'écrit `colonne.iloc[-1]`. C'est tout.

```python
crypto.query("coin == 'ETH'")["close"].iloc[-1]     # le dernier cours de l'ether
```

Rangez le dernier cours du bitcoin dans `dernier_prix`. Puis `valeur`, ce que vaut aujourd'hui le bitcoin accumulé, et `gain_pct`, le gain en pourcentage : `100 * (valeur / total_investi - 1)`.

Affichez le tout dans une f-string, sous cette forme :

```
Investi : 8000 $. Valeur aujourd'hui : 22237.19 $. Gain : 178.0 %.
```
""")

code("")

code("""
verifier("dernier prix", dernier_prix == crypto.query("coin == 'BTC'")["close"].iloc[-1], "la dernière ligne de BTC, colonne close, .iloc[-1]")
verifier("valeur", abs(valeur - total_btc * dernier_prix) < 0.01, "total_btc fois dernier_prix")
verifier("gain", abs(gain_pct - 100 * (valeur / total_investi - 1)) < 1e-6, "100 * (valeur / total_investi - 1)")
""")

md("""
### Point d'étape

La cliente a sa première réponse : **8 000 dollars versés, 22 237 aujourd'hui.** C'est le chiffre qu'elle attendait.

Un analyste ne s'arrête pas là. Le chiffre dit *combien* ; il ne dit pas *pourquoi*. Et c'est le pourquoi qui rend le conseil solide — ou pas.
""")

# ---------------------------------------------------------------- Partie 5
md("""
## Partie 5 : pourquoi ça marche (3 points)

### 5a. Deux prix moyens (1 point)

Deux questions qui se ressemblent et n'ont pas la même réponse :

- **À quel prix moyen la cliente a-t-elle acheté son bitcoin ?** C'est tout ce qu'elle a versé, divisé par tout ce qu'elle a obtenu : `total_investi / total_btc`. Rangez-le dans `prix_moyen_paye`.
- **Quel était le prix moyen du bitcoin sur ces 80 jours ?** C'est la moyenne de la colonne `close` d'`achats`. Rangez-la dans `prix_moyen_marche`.

Affichez les deux, arrondis à 2 décimales, dans une f-string.
""")

code("")

code("""
verifier("prix moyen paye", abs(prix_moyen_paye - total_investi / total_btc) < 0.01, "total_investi / total_btc")
verifier("prix moyen du marche", abs(prix_moyen_marche - achats["close"].mean()) < 0.01, "achats['close'].mean()")
verifier("l'ecart est dans le bon sens", prix_moyen_paye < prix_moyen_marche, "si le prix payé dépasse le prix du marché, une des deux variables est inversée")
""")

md("""
Cellule fournie : les deux prix moyens sur la courbe.
""")

code("""
ax = btc.plot(x="date", y="close", figsize=(11, 4), legend=False, color="#9AA5B1", linewidth=1)
ax.axhline(prix_moyen_marche, color="#B45F06", linestyle="--", linewidth=1.5, label=f"prix moyen du marché : {prix_moyen_marche:,.0f} $")
ax.axhline(prix_moyen_paye, color="#1F4E79", linewidth=2, label=f"prix moyen payé : {prix_moyen_paye:,.0f} $")
ax.set_title("Le prix moyen payé est sous le prix moyen du marché", loc="left")
ax.set_xlabel("")
ax.set_ylabel("Cours (USD)")
ax.legend(frameon=False, loc="upper left")
plt.show()
""")

md("""
Le prix moyen payé est **nettement** en dessous du prix moyen du marché — sur les mêmes 80 jours, sans aucun choix de moment. Expliquez pourquoi, en une phrase, en partant de ce que font 100 dollars fixes quand le prix est bas et quand il est haut :

**Explication :** [à compléter]

### 5b. D'où vient le bitcoin accumulé (2 points)

L'explication se vérifie. Regroupez `achats` par année et sommez la colonne `quantite` (séance 2.2, section 7). Rangez le résultat dans `btc_par_annee`, puis tracez-le en barres.
""")

code("")

code("""
verifier("une valeur par annee", len(btc_par_annee) == 7 and btc_par_annee.index.min() == 2020, "groupby('annee')['quantite'].sum()")
verifier("le compte y est", abs(btc_par_annee.sum() - total_btc) < 1e-9, "la somme par année doit redonner total_btc")
""")

md("""
Comparez ce graphique à la courbe du bitcoin de la partie 3. Quelles sont les trois années qui ont apporté le plus de bitcoin ? Qu'ont-elles en commun ?

**Réponse :** [à compléter]

### Point d'étape

Trois années fournissent les trois quarts du bitcoin accumulé : celles où il était le moins cher. L'investissement programmé ne **devine** pas les creux — il les **achète** mécaniquement, parce que 100 dollars achètent plus quand le prix est bas. C'est toute la raison d'être de la méthode, et vous venez de la mesurer.
""")

# ---------------------------------------------------------------- Partie 6
md("""
## Partie 6 : les sept monnaies (4 points)

La cliente aurait pu choisir une autre monnaie. Refaites le calcul pour les sept, et comparez.

Une boucle sur la liste ci-dessous. À chaque tour, pour la monnaie `m` :

1. les jours d'achat de cette monnaie : le `query` de la partie 3, où `'BTC'` est remplacé par la monnaie du tour, avec une f-string (séance 2.2, section 7) ;
2. la quantité accumulée : la somme de `100 / close` ;
3. le montant investi : 100 fois le nombre d'achats ;
4. le dernier cours de cette monnaie, avec `.iloc[-1]` ;
5. le gain en pourcentage, que vous ajoutez à la liste `gains`.

Puis assemblez `resultat = pd.Series(gains, index=monnaies)`, et tracez-le trié, en barres.

**Attention.** Le solana n'était pas coté en janvier 2020 : il a moins de jours d'achat que les autres, donc un montant investi plus faible. C'est pour ça qu'on compare des gains **en pourcentage**, chacun rapporté à son propre investissement — et non des valeurs en dollars.
""")

code("""
monnaies = ["BTC", "ETH", "SOL", "DOGE", "XRP", "BNB", "ADA"]
gains = []
""")

code("")

code("""
verifier("sept gains", len(gains) == 7, "un append par monnaie")
verifier("le bitcoin est coherent", abs(resultat["BTC"] - gain_pct) < 1e-6, "pour BTC, on doit retrouver le gain de la partie 4")
verifier("solana a moins d'achats", len(crypto.query("coin == 'SOL' and jour == 1 and annee >= 2020")) < 80, "SOL n'existe pas en janvier 2020")
""")

md("""
Deux lignes pour la cliente. Quelle monnaie a le mieux rémunéré l'investissement programmé ? Laquelle l'a fait perdre ? Et une troisième ligne, celle qu'un professionnel ajoute toujours : pourquoi ce classement ne dit **rien** de celui des sept prochaines années.

**Réponse :** [à compléter]
""")

# ---------------------------------------------------------------- Fin
md("""
## Ce que la cliente verra (fournie)

Le graphique qu'on met dans la note : mois après mois, ce qu'elle a versé, et ce que ça valait. Cellule fournie, exécutez-la.
""")

code("""
achats["verse_cumule"] = 100 * (achats["quantite"] * 0 + 1).cumsum()
achats["valeur_position"] = achats["quantite"].cumsum() * achats["close"]
ax = achats.plot(x="date", y=["verse_cumule", "valeur_position"], figsize=(11, 4), color=["#9AA5B1", "#1F4E79"], linewidth=2)
ax.fill_between(achats["date"], achats["verse_cumule"], achats["valeur_position"],
                where=achats["valeur_position"] >= achats["verse_cumule"], color="#1F4E79", alpha=0.08)
ax.set_title("100 dollars par mois dans le bitcoin depuis 2020", loc="left")
ax.set_xlabel("")
ax.set_ylabel("USD")
ax.legend(["versé", "valeur de la position"], frameon=False, loc="upper left")
plt.show()
""")

md("""
La courbe grise monte de 100 en 100, sans surprise. La courbe bleue est la valeur de tout ce qu'elle possède à chaque date. Elle passe **sous** la grise à plusieurs reprises : il y a eu des mois où la cliente était en perte. C'est ce qu'il faut lui dire aussi.

## Bonus, hors barème : tout d'un coup

La seconde question de la cliente : aurait-elle mieux fait de placer les 8 000 dollars **en une fois**, le 1er janvier 2020 ?

Le prix ce jour-là est celui de la première ligne d'`achats` : `achats["close"].iloc[0]`. Calculez la quantité qu'elle aurait obtenue, sa valeur au dernier cours, et comparez à la partie 4.

Puis répondez en trois lignes : laquelle des deux stratégies a le mieux marché sur cette période ? Pourquoi ce résultat n'est-il **pas** une règle générale ? Et pourquoi, même en le sachant, un conseiller recommande-t-il souvent l'investissement programmé ?
""")

code("")

md("""
**Réponse :** [à compléter]

## Ce que vous avez construit

À partir d'un export non relu, vous avez produit une réponse complète à une question de cliente : une table fiable, le calendrier des 80 achats, le montant versé et sa valeur aujourd'hui, l'explication du mécanisme avec le prix moyen payé et la répartition par année, la comparaison entre sept monnaies, et le graphique de la note. Chaque étape a utilisé un outil des deux séances pandas — plus `.iloc[-1]`, et rien d'autre.

Et vous savez maintenant ce que vaut un conseil très répandu : il marche, on sait pourquoi, et on sait aussi ce qu'il ne promet pas.

## Avant de rendre

1. *Exécution → Redémarrer et tout exécuter*.
2. Toutes les cellules `verifier` affichent `OK`.
3. Les réponses en texte sont remplies : le diagnostic de la partie 1, l'explication de la 5a, la réponse de la 5b, celle de la partie 6, et le bonus si vous l'avez fait.
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
