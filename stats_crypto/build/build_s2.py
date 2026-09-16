"""Construit la séance 6 du cours : comparer, et douter (bloc stats, seconde partie).

    python3 stats_crypto/build/build_s2.py
"""
import json, os, textwrap

OUT = "stats_crypto/cours/seance2_cours.ipynb"
LOGO = '<img src="https://cdn.jsdelivr.net/gh/aureliensalas/python_finance@main/ressources/img/logo_macmia.png" alt="Banque des Territoires · France 2030 · MACMIA" width="520">'
BADGE = "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aureliensalas/python_finance/blob/main/stats_crypto/cours/seance2_cours.ipynb)"
BASE = "https://cdn.jsdelivr.net/gh/aureliensalas/python_finance@main/pandas_crypto/data/"
BASE_STATS = "https://cdn.jsdelivr.net/gh/aureliensalas/python_finance@main/stats_crypto/data/"

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

# Séance 6 : comparer, et douter

**Cours** · 2h · statistiques, seconde partie

> ⚠️ **Avant de taper quoi que ce soit :** *Fichier → Enregistrer une copie dans Drive*. Sinon votre travail sera perdu en fermant l'onglet.
>
> 📱 Sur tablette, faites d'abord les réglages de [Bien démarrer](https://github.com/aureliensalas/python_finance/blob/main/ressources/setup_tablette.md).
""")

md("""
## Objectifs

À la fin de cette séance, vous saurez :

- expliquer pourquoi une moyenne calculée sur des données n'est jamais exacte, même quand on a « toutes » les données
- donner une fourchette autour d'une moyenne, par rééchantillonnage
- comparer deux groupes avec un test t et lire sa p-value — en une phrase, la bonne
- distinguer « significatif » et « important »
- reconnaître le piège des tests répétés, et ne plus y tomber
- dire si un portefeuille est diversifié, avec la corrélation

## Les deux phrases du bloc

> **Un prix ne se compare pas. Un rendement, si.**

> **Une moyenne calculée sur des données n'est pas la vraie moyenne. C'est une estimation, et une estimation a une épaisseur.**

La première a organisé la séance 5. La seconde organise celle-ci.

> **Les cellules « Prédire ».** Avant de les exécuter, on annonce **à voix haute** la valeur attendue. Rien à écrire : on dit, on exécute, on compare.

Exécutez d'abord la cellule de setup.
""")

code(f"""
import numpy as np
import pandas as pd
from scipy import stats

pd.set_option("display.max_rows", 12)
BASE = "{BASE}"                # les données du bloc pandas
BASE_STATS = "{BASE_STATS}"    # un fichier de plus, pour la section 6


def verifier(nom, condition, indice=""):
    if condition:
        print("OK       -", nom)
    else:
        print("A REVOIR -", nom, ":", indice)
""")

# ---------------------------------------------------------------- 0. Échauffement
md("""
## 0. Échauffement

On recharge, et on reconstruit **la colonne de la séance 5** — avec le `groupby`, sinon vous savez ce qui arrive.

**1.** Chargez `crypto.csv`, convertissez la date, triez par monnaie puis date. Créez `crypto["r"]`, le rendement en pourcentage, correctement. Retirez les lignes sans rendement.
""")

code("")

code("""
verifier("rendement correct", abs(crypto["r"].max() - 354.67) < 0.01 and len(crypto) == 21318, "groupby('coin')['close'].pct_change() * 100, puis dropna(subset=['r'])")
""")

md("**2.** Les colonnes `annee` et `jour_sem`, et la table `btc`.")

code("")

code("""
verifier("colonnes", "annee" in crypto.columns and "jour_sem" in crypto.columns and len(btc) == 3164, ".dt.year, .dt.dayofweek, puis query sur BTC")
""")

md("""
**La question laissée ouverte.** Réaffichons-la.
""")

code("""
btc.groupby("jour_sem")["r"].mean()
""")

md("""
Lundi +0,31 %, **jeudi −0,25 %**. Le bitcoin baisse-t-il le jeudi ? **Votez à main levée.** On tranche à la fin de la séance.
""")

# ---------------------------------------------------------------- 1. Une moyenne a une épaisseur
md("""
## 1. Une moyenne a une épaisseur

### D'abord un cas où tout le monde est d'accord : le sondage

Une élection. 100 000 électeurs, et 52 % d'entre eux vont voter A. Personne ne les interroge tous : on en sonde **2 000**.

On fabrique cette population, et on regarde la vérité — celle qu'un vrai sondeur ne connaît jamais.
""")

code("""
electeurs = pd.Series(np.random.default_rng(0).random(100_000) < 0.52).astype(int)
electeurs.mean()
""")

md("""
52,1 % pour A. Maintenant, **un sondage** : 2 000 personnes tirées au hasard, et leur moyenne. `sample` tire au hasard dans une colonne ; `random_state` fixe le hasard pour que tout le monde ait le même.
""")

code("""
electeurs.sample(2000, random_state=0).mean()
""")

md("""
**49,5 %.** Ce sondage donne A **perdant**. Il n'est pas truqué : c'est juste que ces 2 000 personnes-là penchaient un peu de l'autre côté.

### Prédire

Deux autres sondages, `random_state=1` et `random_state=2`. Au-dessus ou en dessous de 50 % ?
""")

predire("electeurs.sample(2000, random_state=1).mean()",
        "electeurs.sample(2000, random_state=2).mean()")

md("""
**Le résultat du sondage dépend de qui on a interrogé.** Personne dans la salle ne conteste que c'est de l'incertitude. Elle a un nom : l'**incertitude d'échantillonnage**.

### Mille sondages

Pour la voir en entier : on refait le sondage mille fois. La boucle du bloc Python, une liste vide, `append`, et `pd.Series` à la fin.
""")

code("""
resultats = []
for i in range(1000):
    resultats.append(electeurs.sample(2000, random_state=i).mean() * 100)

sondages = pd.Series(resultats)
sondages.plot(kind="hist", bins=40, title="1000 sondages de 2000 personnes", xlabel="% pour A", figsize=(8, 4))
""")

code("""
sondages.min(), sondages.max(), (sondages < 50).sum()
""")

md("""
De 48,5 % à 55,2 %. Et **42 sondages sur 1 000 donnent A perdant**, alors qu'il a 52 % des voix. Voilà à quoi ressemble l'épaisseur d'une moyenne.

### Maintenant, le bitcoin — « mais on a tous les jours ! »

C'est l'objection, et elle est bonne. Le sondeur n'a que 2 000 personnes sur 100 000. Nous, nous avons **tous** les jours du bitcoin depuis 2018. Où est l'échantillon ?

On ne répond pas par la philosophie. On fait un `groupby`.
""")

code("""
btc.groupby("annee")["r"].mean()
""")

md("""
| année | par jour | ce que ça fait par an |
|---|---|---|
| 2018 | −0,26 % | **−62 %** |
| 2020 | +0,46 % | **+430 %** |
| 2022 | −0,23 % | **−56 %** |
| 2025 | +0,01 % | +2 % |

> Un analyste qui n'aurait eu que l'année 2020 aurait écrit que le bitcoin rapporte 430 % par an. Un autre, avec 2022 seulement, qu'il en perd 56. **Chacun a vu un échantillon de jours de bitcoin, et chacun s'est trompé** — exactement comme le sondage à 49,5 %.
>
> Nous en avons vu 3 164. C'est un échantillon plus grand, donc meilleur. **Ce n'est pas la totalité.** La question « quel est le rendement du bitcoin ? » porte sur **l'actif**, pas sur la fenêtre 2018-2026. La fenêtre est ce qu'on a pu observer de lui. On ne prédit rien : on reconnaît que notre moyenne est une estimation, et qu'une estimation a une épaisseur.

### Mesurer l'épaisseur quand on ne peut pas refaire le sondage

Pour les électeurs, on a retiré mille fois dans la population. Pour le bitcoin, on n'a **pas** la population : on n'a que nos 3 164 jours.

Le remède : tirer **dans ces 3 164 jours, avec remise**. C'est la façon standard d'imiter un tirage dans la population plus grande dont ils viennent.
""")

code("""
btc["r"].sample(5, replace=True, random_state=0)
""")

md("""
Trois arguments :

| Argument | Ce qu'il fait |
|---|---|
| `5` | combien de valeurs on tire |
| `replace=True` | **avec remise** : un même jour peut sortir deux fois, un autre pas du tout |
| `random_state=0` | fixe le hasard |

**Pourquoi avec remise ?** Sans elle, tirer 3 164 valeurs parmi 3 164 redonnerait les mêmes dans le désordre — donc toujours la même moyenne, donc aucune information sur l'épaisseur. La cellule suivante est fausse, exécutez-la et lisez la dernière ligne :
""")

code("""
btc["r"].sample(5000)
""")

md("""
```
ValueError: Cannot take a larger sample than population when 'replace=False'
```

Sans remise, on ne peut pas tirer plus de valeurs qu'il n'y en a. Avec remise, on peut en tirer autant qu'on veut.

### Mille moyennes possibles du bitcoin

La même boucle que pour les sondages. Seule différence : `replace=True`, et on tire autant de jours qu'il y en a.
""")

code("""
moyennes = []
for i in range(1000):
    moyennes.append(btc["r"].sample(len(btc), replace=True, random_state=i).mean())

boot = pd.Series(moyennes)
boot.plot(kind="hist", bins=40, title="1000 moyennes possibles du bitcoin", xlabel="% par jour", figsize=(8, 4))
""")

md("""
> Cette méthode s'appelle le **bootstrap**. Elle sert ici à **voir** l'incertitude d'une moyenne, sans aucune formule. C'est un outil pour comprendre, pas une technique à maîtriser : personne ne vous demandera jamais de choisir un nombre de tirages.
""")

# ---------------------------------------------------------------- 2. L'intervalle de confiance
md("""
## 2. L'intervalle de confiance

On garde les **95 % centraux** de ces mille moyennes : on écarte les 2,5 % les plus basses et les 2,5 % les plus hautes. Ce sont les quantiles de la séance 5.
""")

code("""
bas = boot.quantile(0.025)
haut = boot.quantile(0.975)
bas, haut
""")

md("""
**De +0,003 % à +0,22 % par jour.** Deux nombres difficiles à sentir. Alors on les traduit en rendement **annuel** : 365 jours de capitalisation.
""")

code("""
((1 + bas / 100) ** 365 - 1) * 100, ((1 + haut / 100) ** 365 - 1) * 100
""")

md("""
**De +1 % à +126 % par an.**

> Huit ans et demi de données, 3 164 jours, et voilà tout ce qu'on sait du rendement du bitcoin : quelque part **entre un livret d'épargne et un doublement annuel**.
>
> Deux choses en même temps, et retenez-les toutes les deux : **l'intervalle ne contient pas zéro** — le rendement est bien positif — et il est **inutilisable pour décider quoi que ce soit**. On y revient dans deux sections.

**Comment on le dit.** « Compte tenu de ce qu'on a observé, les valeurs plausibles du rendement moyen vont de +1 % à +126 % par an. » C'est une fourchette de plausibilité. Ce n'est pas « il y a 95 % de chances que la vraie valeur soit dedans ».

### Écrire

Le même intervalle pour l'ether : mille moyennes bootstrap dans `boot_eth`, puis `bas_eth` et `haut_eth`.
""")

code("")

code("""
verifier("boot_eth", len(boot_eth) == 1000, "la même boucle, sur les rendements de ETH")
verifier("intervalle", bas_eth < 0 < haut_eth, "quantile(0.025) et quantile(0.975) : pour ETH, l'intervalle contient zéro")
""")

md("""
Pour ETH, l'intervalle **contient zéro** : de −0,02 % à +0,28 % par jour. Avec huit ans et demi de données, on ne peut même pas affirmer que le rendement moyen de l'ether est positif. C'est le cas inverse de BTC, et il est plus fréquent qu'on ne croit.
""")

# ---------------------------------------------------------------- 3. Le test t
md("""
## 3. Comparer deux groupes : le test t

La question la plus fréquente en finance est une **comparaison** : deux moyennes, chacune avec son épaisseur — sont-elles vraiment différentes ?

On pourrait bootstrapper les deux et regarder si les fourchettes se recouvrent. Le **test t** fait ce travail en une ligne, et le résume en un nombre.

### D'abord une comparaison où la réponse est claire

Le bitcoin contre l'ether. `stats.ttest_ind` prend les deux colonnes.
""")

code("""
eth = crypto.query("coin == 'ETH'")
stats.ttest_ind(btc["r"], eth["r"], equal_var=False)
""")

md("""
Deux nombres. Celui qui nous intéresse est `pvalue`.
""")

code("""
stats.ttest_ind(btc["r"], eth["r"], equal_var=False).pvalue
""")

md("""
**p = 0,82.**

### Lire une p-value, en une phrase — et une seule

> **Si les deux groupes venaient en réalité de la même population, quelle serait la probabilité d'observer un écart au moins aussi grand que celui-ci, par le seul hasard de l'échantillon ?**

Ici, 82 %. Un écart comme celui entre BTC et ETH n'aurait **rien de surprenant** s'il n'y avait aucune différence réelle. On ne peut pas les distinguer.

Petite p-value : l'écart observé serait surprenant s'il n'y avait rien. Grande p-value : il n'aurait rien de surprenant.

Deux choses qu'une p-value **n'est pas**, parce que c'est l'erreur universelle :

- ce n'est **pas** la probabilité que « les deux groupes sont pareils » soit vrai ;
- le seuil de 5 % est une **convention**, pas une loi de la nature.

### Maintenant la vraie question : le jeudi
""")

code("""
jeudi = btc.query("jour_sem == 3")["r"]
autres = btc.query("jour_sem != 3")["r"]
stats.ttest_ind(jeudi, autres, equal_var=False).pvalue
""")

md("""
**p = 0,030.** Sous le seuil de 5 %. « Significatif. »

On laisse ce résultat à l'écran. **Alors, on vend le mercredi soir ?**

Ne répondez pas encore. Deux sections avant de trancher.

### Prédire
""")

predire('stats.ttest_ind(btc["r"], btc["r"], equal_var=False).pvalue',
        'stats.ttest_ind(crypto.query("coin == \'BTC\'")["r"], crypto.query("coin == \'DOGE\'")["r"], equal_var=False).pvalue < 0.05')

# ---------------------------------------------------------------- 4. Significatif ≠ important
md("""
## 4. Significatif ne veut pas dire important

Retour sur l'intervalle de la section 2. Deux lectures, côte à côte.

| Le bitcoin | |
|---|---|
| L'intervalle contient-il zéro ? | **Non** |
| Le rendement est-il « significativement positif » ? | **Oui** |
| Peut-on en faire quelque chose ? | **Non** : de +1 % à +126 % par an |

> **Significatif** répond à : peut-on distinguer cet écart du bruit ? **Important** répond à : cet écart change-t-il une décision ? Ce sont deux questions différentes. Seule la seconde intéresse celui qui met de l'argent.

Le complément, et il est contre-intuitif : **avec assez de données, n'importe quel écart devient significatif.** Un écart de 0,001 % par jour, sur un million de jours, aura une p-value minuscule — et ne vaudra toujours rien. La p-value mesure autant la **taille de l'échantillon** que la taille de l'effet. Trois mille jours, c'est déjà beaucoup.

C'est pourquoi on ne donne jamais une p-value seule. On donne **l'écart** (« le jeudi fait −0,25 % contre +0,17 % les autres jours »), et l'épaisseur autour.
""")

# ---------------------------------------------------------------- 5. Chercher jusqu'à trouver
md("""
## 5. Chercher jusqu'à trouver

### L'intuition

Un test au seuil de 5 % se trompe **une fois sur vingt** quand il n'y a rien à trouver. Lancez vingt tests sur du pur hasard : vous attendez une fausse découverte. Et elle sera **indiscernable** d'une vraie.

### La vérification, sur ce fichier

Sept monnaies, cinq jours ouvrés : trente-cinq tests. Cellule fournie — la boucle, le `query` avec f-string de la séance 4, le test. Exécutez-la.
""")

code("""
trouves = []
for m in ["BTC", "ETH", "SOL", "DOGE", "XRP", "BNB", "ADA"]:
    for j in range(5):
        a = crypto.query(f"coin == '{m}' and jour_sem == {j}")["r"]
        b = crypto.query(f"coin == '{m}' and jour_sem != {j}")["r"]
        if stats.ttest_ind(a, b, equal_var=False).pvalue < 0.05:
            trouves.append((m, j))

len(trouves), trouves
""")

md("""
**Quatre résultats « significatifs » sur trente-cinq.** Le hasard seul en prédisait 1,75.

Et regardez lesquels : ADA le jeudi, BTC le jeudi, ETH le jeudi, BNB le vendredi. **Le jeudi sort trois fois.** Ça ressemble à une découverte. Quelqu'un qui aurait cherché « le jour faible du marché crypto » l'aurait trouvé, l'aurait publié — et se serait trompé.

> **Le jeudi de la section 3 était l'un de ces quatre.** On l'a trouvé parce qu'on avait regardé sept jours de sept monnaies avant de choisir lequel tester. **Le seuil de 5 % vaut pour un test décidé avant de regarder les données.** Il ne vaut rien pour le meilleur de trente-cinq. Chercher jusqu'à trouver finit toujours par trouver.

### On tranche

**Non, le bitcoin ne baisse pas le jeudi.** Le seul résultat qui le suggère est celui qu'on a obtenu en fouillant, et c'est précisément celui qui ne compte pas. Et même en le prenant au sérieux, la section 2 a montré que l'écart serait noyé dans l'épaisseur de chaque moyenne.

Ceux qui ont voté « oui » au début n'ont pas eu tort de le penser : c'est exactement ce que les données montraient. Ils ont maintenant l'outil pour ne plus s'y laisser prendre.
""")

# ---------------------------------------------------------------- 6. Corrélation
md("""
## 6. Sept monnaies, un seul actif ?

Un étudiant détient les sept cryptomonnaies du fichier. Il se croit diversifié. **L'est-il ?**

### Le fichier large

Pour comparer les monnaies **jour par jour**, il faut les avoir côte à côte : une colonne par monnaie. C'est la même donnée, arrangée autrement. Le format **long** de `crypto.csv` — une ligne par monnaie et par jour — est celui de `groupby`. Le format **large** est celui de la corrélation. On vous livre le fichier ; passer de l'un à l'autre est une compétence pour plus tard.
""")

code("""
rendements = pd.read_csv(BASE_STATS + "rendements.csv")
rendements.head()
""")

md("""
### `corr`, et c'est la seule nouveauté

La corrélation entre deux colonnes va de −1 à +1 : +1, elles montent et descendent toujours ensemble ; 0, aucun lien ; −1, l'une monte quand l'autre descend. `corr()` sur une table donne toutes les paires d'un coup.
""")

code("""
monnaies = ["BTC", "ETH", "SOL", "DOGE", "XRP", "BNB", "ADA"]
rendements[monnaies].corr().round(2)
""")

md("""
BTC et ETH : **0,82**. La plus faible, SOL et DOGE : 0,25. La corrélation moyenne entre paires est de **0,53**.

> **La réponse : non.** Sept monnaies à 0,53 de corrélation moyenne, ce n'est pas sept actifs. C'est à peu près **un seul actif acheté sept fois**. La diversification ne se compte pas en lignes de portefeuille ; elle se mesure à ce que les lignes font **ensemble**.

### Prédire
""")

predire('rendements["BTC"].corr(rendements["ETH"])',
        'rendements["BTC"].corr(rendements["BTC"])')

md("""
### La question laissée ouverte à la séance 5

Les pires jours de chaque monnaie — sont-ils tombés le même jour ? Le 12 mars 2020, krach du Covid :
""")

code("""
rendements.query("date == '2020-03-12'")
""")

md("""
ETH −42,3 %. BNB −41,9 %. ADA −39,4 %. BTC −37,2 %. XRP −32,9 %. DOGE −31,8 %. SOL n'était pas encore coté : `NaN`.

> **Toutes ensemble, le même jour.** La corrélation moyenne de 0,53 est un chiffre calme. Le jour où l'on aurait eu besoin que les monnaies se compensent, elles sont tombées à l'unisson. **La corrélation grimpe exactement au moment où l'on voudrait qu'elle baisse.** C'est la propriété la plus désagréable des marchés, et la plus constante — et c'est la raison de ne jamais se fier à un coefficient sans regarder ce qui se passe dans les pires jours.

### Écrire

La corrélation de chaque monnaie avec le bitcoin, triée, dans `corr_btc`. Indication : la colonne `BTC` du tableau `corr()`.
""")

code("")

code("""
verifier("corr_btc", len(corr_btc) == 7 and abs(corr_btc["ETH"] - 0.82) < 0.01 and corr_btc.index[-1] == "BTC", "rendements[monnaies].corr()['BTC'].sort_values()")
""")

# ---------------------------------------------------------------- 7. Synthèse
md("""
## 7. Ce que vous savez faire

| Vous voulez... | Vous écrivez |
|---|---|
| tirer au hasard dans une colonne | `col.sample(n, random_state=0)` |
| tirer avec remise | `col.sample(len(col), replace=True, random_state=i)` |
| mille moyennes | une boucle, `append`, `pd.Series` |
| l'intervalle à 95 % | `boot.quantile(0.025)`, `boot.quantile(0.975)` |
| comparer deux groupes | `stats.ttest_ind(a, b, equal_var=False).pvalue` |
| toutes les corrélations | `table[colonnes].corr()` |
| une corrélation | `table["BTC"].corr(table["ETH"])` |
| un jour précis | `table.query("date == '2020-03-12'")` |

## Les deux phrases du bloc

1. **Un prix ne se compare pas. Un rendement, si.** Tout ce qu'on a comparé aujourd'hui, ce sont des rendements.
2. **Une moyenne calculée sur des données n'est pas la vraie moyenne.** Le bitcoin rapporte entre +1 % et +126 % par an : c'est ça, l'épaisseur.

## Quatre phrases à retenir

1. **Une moyenne a une épaisseur.** Toujours la fourchette, jamais le point seul.
2. **Une p-value dit « surprenant s'il n'y avait rien », pas « probablement vrai ».**
3. **Significatif n'est pas important.** Regardez la taille de l'effet.
4. **Le seuil de 5 % vaut pour un test décidé à l'avance.** Pas pour le meilleur de trente-cinq.

## La suite

Le bloc suivant pose l'autre question : ce que j'ai trouvé dans les données **marche-t-il sur des données jamais vues ?** Son rituel — le découpage entraînement / test — est le jumeau de l'intervalle de confiance : l'un protège du hasard de l'échantillon, l'autre du hasard de l'ajustement.

Le **bonus** ci-dessous est facultatif et ne sert pas à la suite.
""")

# ---------------------------------------------------------------- Bonus
md("""
---

## Bonus facultatif — le khi-deux

> **Facultatif. Non noté. Rien dans la suite du cours n'en dépend.** À faire chez vous si le cœur vous en dit. On n'y touche pas en classe.

Le test t compare des **moyennes**. Quand les deux variables sont des **catégories** — un jour de la semaine, une tranche de rendement — on compare des **effectifs**, et l'outil s'appelle le **khi-deux**. Deux outils de plus, expliqués sur place.

### Découper une colonne en tranches : `pd.cut`

On transforme le rendement, continu, en trois catégories : baisse (sous −1 %), stable, hausse (au-dessus de +1 %).
""")

code("""
btc = btc.copy()
btc["tranche"] = pd.cut(btc["r"], [-100, -1, 1, 1000], labels=["baisse", "stable", "hausse"])
btc["tranche"].value_counts()
""")

md("""
### Croiser deux catégories : `pd.crosstab`

Combien de jours de chaque tranche, pour chaque jour de la semaine ? Un tableau à double entrée.
""")

code("""
tableau = pd.crosstab(btc["jour_sem"], btc["tranche"])
tableau
""")

md("""
### Le test

Si le jour de la semaine ne changeait rien, chaque ligne aurait à peu près les mêmes proportions. Le khi-deux mesure l'écart entre ce tableau et celui qu'on aurait « si rien ». Il renvoie quatre choses ; on nomme celles qu'on garde et on jette le reste avec `_`.
""")

code("""
khi2, p, _, attendus = stats.chi2_contingency(tableau)
p
""")

md("""
**p ≈ 0.** Le test rejette, et massivement : le jour de la semaine **change** la répartition. Surprise ? Pas si vite. Le khi-deux dit qu'il y a une dépendance ; il ne dit pas **où**. Pour ça, on regarde les proportions ligne par ligne.
""")

code("""
(tableau.div(tableau.sum(axis=1), axis=0) * 100).round(0)
""")

md("""
Du lundi au vendredi, environ **un tiers** de jours « stables ». Le samedi : **60 %**. Le dimanche : 44 %.

> **La dépendance est là, et ce n'est pas celle qu'on cherchait.** Le week-end, le bitcoin bouge moins — moins de traders, moins de volume, moins d'amplitude. Le jour de la semaine change **l'agitation**, pas la **direction**. Le jeudi, lui, ressemble aux autres jours ouvrés.

On le vérifie en retirant le week-end :
""")

code("""
ouvres = btc.query("jour_sem <= 4")
tableau_ouvres = pd.crosstab(ouvres["jour_sem"], ouvres["tranche"])
stats.chi2_contingency(tableau_ouvres)[1]
""")

md("""
**p = 0,063.** Sur les cinq jours ouvrés, la répartition est compatible avec le hasard. **Le jeudi ne se distingue pas non plus par ce test** — le fil est refermé une dernière fois.

Ce que ce bonus enseigne, au-delà de l'outil : un test qui rejette ne confirme pas votre hypothèse. Il dit qu'il y a *quelque chose*. C'est à vous d'aller voir quoi, et c'est souvent autre chose.
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
