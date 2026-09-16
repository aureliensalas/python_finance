"""Construit le travail en autonomie du bloc 3 : la fiche de risque.

    python3 stats_crypto/build/build_a3.py

La fonction afficher_fiche() est lue depuis prototypes/fiche_risque.py :
une seule source, pour que la maquette et le notebook ne divergent pas.
"""
import json, os, re, textwrap

OUT = "stats_crypto/assignment/fiche_de_risque.ipynb"
LOGO = '<img src="https://cdn.jsdelivr.net/gh/aureliensalas/python_finance@main/ressources/img/logo_macmia.png" alt="Banque des Territoires · France 2030 · MACMIA" width="520">'
BADGE = "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aureliensalas/python_finance/blob/main/stats_crypto/assignment/fiche_de_risque.ipynb)"
BASE = "https://cdn.jsdelivr.net/gh/aureliensalas/python_finance@main/pandas_crypto/data/"

cells = []

def md(s):
    s = textwrap.dedent(s).strip("\n")
    cells.append({"cell_type": "markdown", "metadata": {}, "source": s.splitlines(keepends=True)})

def code(s):
    s = textwrap.dedent(s).strip("\n")
    cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
                  "source": s.splitlines(keepends=True)})

# la fonction de mise en page, telle quelle
src = open("prototypes/fiche_risque.py", encoding="utf-8").read()
FICHE = src[src.index("ENCRE, GRIS"):].rstrip()

# ---------------------------------------------------------------- en-tête
md(f"""
{LOGO}

{BADGE}

# La fiche de risque

**Travail en autonomie** · bloc 3 · à faire après les séances 5 et 6

> ⚠️ **Avant de taper quoi que ce soit :** *Fichier → Enregistrer une copie dans Drive*. Sinon votre travail sera perdu en fermant l'onglet.

Ce notebook n'est pas noté. Il sert à vérifier, seul, que vous savez faire ce que les deux séances ont montré — et à repartir avec quelque chose qui a de l'allure.
""")

md("""
## Ce que vous allez construire

Vous êtes analyste risque dans une société de gestion. Le comité d'investissement envisage d'ouvrir une ligne sur une cryptomonnaie et vous demande une **fiche de risque** : une page, quelques chiffres, deux graphiques, et un avis.

C'est un document réel. Un desk risque en produit un avant d'autoriser la moindre exposition.

**La mise en page est déjà écrite.** Une fonction vous est fournie : elle dessine la fiche. Votre travail est de **calculer ce qui va dedans** — et vous savez déjà tout faire.

Voici comment on va procéder :

1. on exécute la fonction tout de suite, alors que vous n'avez rien calculé : la fiche apparaît **vide** ;
2. à chaque étape, vous calculez un indicateur ;
3. on rappelle la fonction, et la fiche se remplit ;
4. à la fin, on en fait une petite application avec un champ de saisie.

Chaque étape dit **ce qu'on cherche** et **où c'était dans le cours**. Elle ne donne pas la réponse : c'est à vous de retrouver la ligne. Après chaque cellule à écrire, une cellule `verifier` vous dit si c'est juste — un `A REVOIR` n'est pas une faute, c'est une indication.

Exécutez d'abord les deux cellules ci-dessous.
""")

code(f"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

pd.set_option("display.max_rows", 12)
BASE = "{BASE}"


def verifier(nom, condition, indice=""):
    if condition:
        print("OK       -", nom)
    else:
        print("A REVOIR -", nom, ":", indice)
""")

md("""
La cellule suivante contient la fonction qui dessine la fiche. Elle est longue, et **vous n'avez pas à la lire** : exécutez-la, puis oubliez-la. On s'en servira comme d'un outil.
""")

code(FICHE)

# ---------------------------------------------------------------- la fiche vide
md("""
## Regardez ce qu'on va remplir

Choisissez votre monnaie. Les sept du fichier : `BTC`, `ETH`, `SOL`, `DOGE`, `XRP`, `BNB`, `ADA`.

Si vous hésitez, gardez `SOL` : c'est celle qui réserve les meilleures surprises.
""")

code("""
MONNAIE = "SOL"
""")

md("""
On charge le fichier, et on appelle la fonction en ne lui donnant que le nom.
""")

code("""
crypto = pd.read_csv(BASE + "crypto.csv")
crypto["date"] = pd.to_datetime(crypto["date"])
crypto = crypto.sort_values(["coin", "date"]).reset_index(drop=True)

afficher_fiche(MONNAIE)
plt.show()
""")

md("""
Voilà le squelette. Le bandeau est là, et **tout le reste attend** : cinq tuiles grises, deux cadres vides, et pas même la courbe du cours.

C'est normal : la fonction ne sait rien. Elle attend qu'on lui passe des valeurs, et elle affiche « à compléter » pour tout ce qu'on ne lui donne pas.

**À chaque étape, vous allez lui en donner une de plus.**
""")

# ---------------------------------------------------------------- étape 1
md("""
## Étape 1 — La table de votre monnaie, et sa colonne de rendement

Avant tout calcul, il faut deux choses : la table qui ne contient que votre monnaie, et la colonne des rendements quotidiens.

**Ce qu'on cherche.** Une table `t` avec les lignes de `MONNAIE` seulement, et une colonne `r` qui donne, pour chaque jour, la variation en pourcentage par rapport à la veille.

**Où c'était.** Séance 5, sections 1 et 3. Deux pièges à ne pas oublier :

- le rendement se calcule **par monnaie**, sinon la première ligne se compare au dernier jour de la monnaie précédente — c'est le piège des 933 041 % ;
- après le calcul, les premiers jours n'ont pas de veille : ils valent `NaN` et il faut les retirer.

Comme on ne garde qu'une monnaie, vous pouvez soit calculer le rendement sur toute la table puis filtrer, soit filtrer puis calculer. **Les deux marchent** — mais dans le second cas, faites bien attention à trier d'abord par date.

Une piste pour l'ordre des opérations : la table est déjà triée par monnaie puis par date.
""")

code("")

code("""
attendu = crypto.copy()
attendu["r"] = attendu.groupby("coin")["close"].pct_change() * 100
attendu = attendu.query("coin == @MONNAIE").dropna(subset=["r"])
verifier("la table ne contient qu'une monnaie", t["coin"].nunique() == 1 and t["coin"].iloc[0] == MONNAIE, "un query sur coin == MONNAIE")
verifier("le bon nombre de lignes", len(t) == len(attendu), "il faut retirer le premier jour, qui n'a pas de veille : dropna(subset=['r'])")
verifier("les rendements sont justes", abs(t["r"].sum() - attendu["r"].sum()) < 0.01, "le rendement se calcule par monnaie : groupby('coin')['close'].pct_change() * 100")
verifier("pas de rendement aberrant", t["r"].max() < 400, "un maximum énorme veut dire que le groupby a été oublié")
""")

md("""
### Le cours au fil du temps

Vous avez maintenant de quoi tracer le premier étage de la fiche. On le passe à la fonction avec l'argument `prix`, et on ajoute au passage l'argument `periode`, qui remplit la ligne sous le titre.
""")

code("""
periode = f"{len(t)} jours  ·  {t['date'].min().date()} → {t['date'].max().date()}"

afficher_fiche(MONNAIE, periode=periode, prix=t)
plt.show()
""")

md("""
La courbe est apparue. C'est le graphique que tout le monde regarde — celui qui raconte la trajectoire.

Il ne dit rien du risque : la montée écrase les journées à −40 %. Les étapes suivantes vont chercher ce qu'il cache.
""")

# ---------------------------------------------------------------- étape 2
md("""
## Étape 2 — Le rendement moyen et le rendement médian

**Ce qu'on cherche.** Deux nombres, dans `rendement_moyen` et `rendement_median` : la moyenne et la médiane de la colonne `r`.

**Pourquoi les deux.** Séance 5, section 2. La moyenne est tirée par les très gros jours ; la médiane décrit la journée ordinaire. Quand elles diffèrent beaucoup, c'est que quelques journées extrêmes font tout le travail — et c'est une information de première importance pour un comité d'investissement.

**Où c'était.** Séance 5, section 2. Deux méthodes, une ligne chacune.
""")

code("")

code("""
verifier("rendement moyen", abs(rendement_moyen - t["r"].mean()) < 1e-9, "la méthode .mean() sur la colonne r")
verifier("rendement median", abs(rendement_median - t["r"].median()) < 1e-9, "la méthode .median() sur la colonne r")
""")

md("""
Regardez vos deux nombres avant de continuer. Lequel est le plus grand ? De combien ?

Si votre monnaie a un rendement moyen **positif** et une médiane **négative**, ce n'est pas une erreur de calcul : ça veut dire qu'elle baisse plus d'un jour sur deux, et qu'elle doit tout à quelques journées d'envolée. C'est le cas de plusieurs des sept.
""")

# ---------------------------------------------------------------- étape 3
md("""
## Étape 3 — La volatilité et la VaR

Les deux chiffres de risque, ceux que le comité regardera en premier.

**Ce qu'on cherche.**

- `volatilite` : l'écart-type de la colonne `r`. C'est **la** mesure du risque en finance — l'ampleur typique d'une journée, à la hausse comme à la baisse.
- `var_95` : le quantile 5 % de la colonne `r`. C'est la **Value at Risk** : le seuil en dessous duquel tombe une journée sur vingt.

**Où c'était.** Séance 5, section 2, pour les deux.

**Attention au sens du quantile.** `quantile(0.05)` donne la valeur en dessous de laquelle se trouvent 5 % des journées. C'est donc un nombre **négatif** : c'est bien une perte.
""")

code("")

code("""
verifier("volatilite", abs(volatilite - t["r"].std()) < 1e-9, "la méthode .std() sur la colonne r")
verifier("VaR 95", abs(var_95 - t["r"].quantile(0.05)) < 1e-9, "la méthode .quantile(0.05) sur la colonne r")
verifier("la VaR est bien une perte", var_95 < 0, "si votre nombre est positif, vous avez sans doute pris quantile(0.95)")
""")

md("""
**Traduisez votre VaR en euros**, mentalement : sur une position de 10 000 €, un jour sur vingt fait perdre plus de ... € ? Un jour sur vingt, c'est environ une fois par mois.

C'est exactement la phrase que le comité attend. Pas « la volatilité est de 6,19 % » — mais « une fois par mois, on perd plus de 800 € sur 10 000 ».
""")

# ---------------------------------------------------------------- étape 4
md("""
## Étape 4 — La part de jours de hausse

**Ce qu'on cherche.** `part_hausse`, le pourcentage de journées où le rendement est positif. **En pourcentage**, donc entre 0 et 100 — pas entre 0 et 1.

**Où c'était.** Séance 5, section 3, exercice 1. Le raisonnement : une comparaison sur une colonne donne une colonne de `True` et `False` ; `True` vaut 1 et `False` vaut 0 ; donc la **moyenne** de cette colonne est la part de `True`.

Il ne restera qu'à multiplier par 100.
""")

code("")

code("""
verifier("part_hausse", abs(part_hausse - (t["r"] > 0).mean() * 100) < 1e-9, "(t['r'] > 0).mean() donne une part entre 0 et 1 ; la fiche attend un pourcentage")
verifier("l'ordre de grandeur", 30 < part_hausse < 70, "un résultat proche de 0.5 veut dire qu'il manque le * 100")
""")

md("""
### Les cinq tuiles

Vous avez les cinq indicateurs. On les passe tous à la fonction.
""")

code("""
afficher_fiche(MONNAIE, periode=periode, prix=t,
               rendement_moyen=rendement_moyen,
               rendement_median=rendement_median,
               volatilite=volatilite,
               var_95=var_95,
               part_hausse=part_hausse)
plt.show()
""")

md("""
Les cinq tuiles sont remplies. Remarquez ce que la fonction a ajouté toute seule, en petit sous chaque nombre :

- sous le rendement moyen, **ce que ça donne sur un an** — c'est le même rendement quotidien, composé 365 fois ;
- sous la volatilité, **la volatilité annualisée** — la convention du métier, qui multiplie la volatilité quotidienne par la racine de 365.

Vous n'aviez pas à les calculer. Mais regardez le rendement annuel affiché : il est probablement énorme. **Gardez-le pour l'étape 7** — la séance 6 a montré ce qu'il faut en penser.

Il reste les deux cadres du bas.
""")

# ---------------------------------------------------------------- étape 5
md("""
## Étape 5 — Le pire jour, et sa date

La distribution des rendements se trace toute seule dès qu'on donne la colonne `r` à la fonction. Mais on veut aussi **marquer le pire jour dessus**, avec sa date.

**Ce qu'on cherche.** `pire_jour`, la valeur du plus mauvais rendement, et `date_pire`, la date à laquelle il est arrivé.

La valeur, vous savez la trouver : `.min()` sur la colonne.

La date, non. C'est une méthode nouvelle, et la voici.

### `idxmin` : à quelle ligne se trouve le minimum ?

`t["r"].min()` répond à « **quelle est** la plus petite valeur ? ». Il existe une méthode qui répond à l'autre question : « **où** est-elle ? ».
""")

code("""
print(t["r"].min())        # quelle est la plus petite valeur
print(t["r"].idxmin())     # à quelle ligne elle se trouve
""")

md("""
`idxmin` ne donne pas une valeur : il donne **l'étiquette de la ligne** où se trouve le minimum. Un numéro de ligne, tel qu'il apparaît à gauche quand vous affichez la table.

### `.loc` : aller chercher une case précise

Ce numéro seul ne sert à rien. Il faut s'en servir pour **aller lire une autre colonne sur cette même ligne**. C'est le rôle de `.loc`, qui prend une étiquette de ligne et un nom de colonne :

```python
table.loc[numéro_de_ligne, "nom_de_colonne"]
```

Les deux ensemble :
""")

code("""
print(t.loc[t["r"].idxmin(), "date"])
""")

md("""
La date du pire jour. On peut l'alléger avec `.date()`, qui retire l'heure — inutile ici, puisque nos données sont quotidiennes.

> `idxmax` existe aussi, et fait la même chose pour le maximum. Retenez la paire : `min` / `max` donnent **la valeur**, `idxmin` / `idxmax` donnent **la ligne**.

### À vous

Rangez la valeur du pire jour dans `pire_jour`, et sa date dans `date_pire`. Pour la date, utilisez `.date()` à la fin pour n'avoir que le jour.
""")

code("")

code("""
verifier("pire_jour", abs(pire_jour - t["r"].min()) < 1e-9, "la méthode .min() sur la colonne r")
verifier("date_pire", str(date_pire) == str(t.loc[t["r"].idxmin(), "date"].date()), "t.loc[t['r'].idxmin(), 'date'].date()")
""")

# ---------------------------------------------------------------- étape 6
md("""
## Étape 6 — Situer votre monnaie parmi les sept

Un chiffre de risque tout seul ne veut rien dire. 6 % de volatilité quotidienne, est-ce beaucoup ? La seule façon de répondre est de comparer.

**Ce qu'on cherche.** `classement`, une Series qui donne la volatilité de **chacune des sept monnaies**, triée de la plus faible à la plus forte. Elle est calculée sur `crypto`, la table complète — pas sur `t`, qui ne contient qu'une monnaie.

**Attention.** `crypto` n'a pas de colonne `r` : vous ne l'avez créée que sur `t`. Commencez donc par la créer sur `crypto`, avec le même `groupby` qu'à l'étape 1.

**Où c'était.** Séance 5, section 3 : grouper par monnaie, résumer par l'écart-type, trier le résultat.
""")

code("")

code("""
ref = crypto.copy()
ref["r"] = ref.groupby("coin")["close"].pct_change() * 100
ref = ref.groupby("coin")["r"].std().sort_values()
verifier("sept monnaies", len(classement) == 7, "groupby('coin') sur la table complète")
verifier("les bonnes valeurs", abs(classement.sum() - ref.sum()) < 0.01, "la volatilité est l'écart-type des rendements : .std()")
verifier("c'est trié", list(classement.index) == list(ref.index), "sort_values() du plus petit au plus grand")
""")

# ---------------------------------------------------------------- la fiche complète
md("""
## La fiche complète

Tout est calculé. On passe l'ensemble à la fonction.
""")

code("""
afficher_fiche(MONNAIE, periode=periode, prix=t,
               rendement_moyen=rendement_moyen,
               rendement_median=rendement_median,
               volatilite=volatilite,
               var_95=var_95,
               part_hausse=part_hausse,
               pire_jour=pire_jour,
               date_pire=date_pire,
               rendements=t["r"],
               classement=classement)
plt.show()
""")

md("""
Voilà le document. Bandeau, trajectoire, cinq indicateurs, la forme des secousses avec la VaR et le pire jour marqués dessus, et la place de votre monnaie parmi les sept.

C'est une vraie fiche de risque. Vous l'avez remplie ligne par ligne.
""")

# ---------------------------------------------------------------- étape 7
md("""
## Étape 7 — Lire votre fiche

Le travail d'analyste commence ici. Répondez en double-cliquant sur cette cellule.

**1. Recommandez-vous d'ouvrir la ligne ? À quelle taille ?**
Appuyez-vous sur la VaR traduite en euros, et sur la place de votre monnaie dans le classement.

*[votre réponse]*

**2. Quel est le chiffre le moins fiable de votre fiche, et pourquoi ?**
Un indice : la séance 6 a mesuré l'épaisseur du rendement moyen du bitcoin. Elle allait de +1 % à +126 % par an. Regardez le rendement annuel affiché sur votre fiche, et demandez-vous ce qu'on peut en faire.

*[votre réponse]*

**3. Votre fiche décrit le passé. Qu'est-ce qui, dedans, a une chance de valoir pour demain — et qu'est-ce qui n'en a aucune ?**
Autrement dit : si vous deviez parier sur un seul de ces cinq chiffres pour l'année prochaine, lequel ? Et lequel refuseriez-vous d'utiliser ?

*[votre réponse]*
""")

# ---------------------------------------------------------------- bonus
md("""
## Pour finir — la fiche en petite application

Vous avez fait tout le travail pour **une** monnaie. Le refaire pour une autre voudrait dire remonter et tout réexécuter en changeant `MONNAIE`.

La cellule ci-dessous fait mieux. Elle ne contient rien de nouveau : ce sont **vos lignes**, dans l'ordre, rassemblées. Lisez-la, vous devriez tout reconnaître.
""")

code('''
def fiche_de(code):
    """Refait toutes les étapes de ce notebook pour la monnaie demandée."""
    tt = crypto.copy()
    tt["r"] = tt.groupby("coin")["close"].pct_change() * 100
    tt = tt.query("coin == @code").dropna(subset=["r"])

    classement_sept = crypto.copy()
    classement_sept["r"] = classement_sept.groupby("coin")["close"].pct_change() * 100
    classement_sept = classement_sept.groupby("coin")["r"].std().sort_values()

    afficher_fiche(code,
                   periode=f"{len(tt)} jours  ·  {tt['date'].min().date()} → {tt['date'].max().date()}",
                   prix=tt,
                   rendement_moyen=tt["r"].mean(),
                   rendement_median=tt["r"].median(),
                   volatilite=tt["r"].std(),
                   var_95=tt["r"].quantile(0.05),
                   part_hausse=(tt["r"] > 0).mean() * 100,
                   pire_jour=tt["r"].min(),
                   date_pire=tt.loc[tt["r"].idxmin(), "date"].date(),
                   rendements=tt["r"],
                   classement=classement_sept)
    plt.show()
''')

md("""
Essayez-la sur une autre monnaie que la vôtre :
""")

code("""
fiche_de("BTC")
""")

md("""
### Un champ de saisie

Dernière cellule, fournie elle aussi. Elle ajoute une zone de texte et un bouton : tapez le code d'une monnaie, cliquez, la fiche se recalcule.

Rien de neuf pour vous — c'est toujours `fiche_de` qui travaille. Seule la façon de l'appeler change.
""")

code('''
import ipywidgets as widgets
from IPython.display import display

champ = widgets.Text(value="SOL", description="Monnaie :")
bouton = widgets.Button(description="Afficher la fiche", button_style="primary")
sortie = widgets.Output()
dispo = sorted(crypto["coin"].unique())


def au_clic(_):
    with sortie:
        sortie.clear_output(wait=True)
        demande = champ.value.strip().upper()
        if demande not in dispo:
            print(f"« {demande} » n'est pas dans le fichier.")
            print("Les sept disponibles :", ", ".join(dispo))
        else:
            fiche_de(demande)


bouton.on_click(au_clic)
display(widgets.HBox([champ, bouton]), sortie)
au_clic(None)
''')

md("""
> Si cette dernière cellule n'affiche rien, ce n'est pas grave : le champ de saisie dépend d'un module d'affichage que Colab ne charge pas toujours. `fiche_de("BTC")` marche dans tous les cas.

## Ce que vous avez fait

À partir d'un fichier de prix et de rien d'autre, vous avez produit le document qu'un desk risque met sur la table avant d'autoriser une exposition : la trajectoire, cinq indicateurs, la forme des pertes, et une comparaison.

Chaque chiffre est venu d'une ligne des séances 5 et 6. La seule nouveauté du notebook tient en deux méthodes, `idxmin` et `.loc`, qui servent à retrouver **où** se trouve une valeur plutôt que **ce qu'elle vaut**.

## Avant de fermer

1. *Exécution → Redémarrer et tout exécuter*.
2. Toutes les cellules `verifier` affichent `OK`.
3. Les trois réponses de l'étape 7 sont écrites.
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
