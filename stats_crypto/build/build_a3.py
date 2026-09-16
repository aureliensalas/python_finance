"""Construit le travail en autonomie du bloc 3 : la fiche d'analyse.

    python3 stats_crypto/build/build_a3.py

Deux volets : le risque d'une monnaie (séance 5), puis le test d'une idée
de stratégie (séance 6). La fonction afficher_fiche() est lue depuis
prototypes/fiche_analyse.py — une seule source.
"""
import json, os, textwrap

OUT = "stats_crypto/assignment/fiche_analyse.ipynb"
LOGO = '<img src="https://cdn.jsdelivr.net/gh/aureliensalas/python_finance@main/ressources/img/logo_macmia.png" alt="Banque des Territoires · France 2030 · MACMIA" width="520">'
BADGE = "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aureliensalas/python_finance/blob/main/stats_crypto/assignment/fiche_analyse.ipynb)"
BASE = "https://cdn.jsdelivr.net/gh/aureliensalas/python_finance@main/pandas_crypto/data/"

cells = []
def md(s):
    cells.append({"cell_type": "markdown", "metadata": {},
                  "source": textwrap.dedent(s).strip("\n").splitlines(keepends=True)})
def code(s):
    cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
                  "source": textwrap.dedent(s).strip("\n").splitlines(keepends=True)})

src = open("prototypes/fiche_analyse.py", encoding="utf-8").read()
FICHE = src[src.index("ENCRE, GRIS"):].rstrip()

# ---------------------------------------------------------------- en-tête
md(f"""
{LOGO}

{BADGE}

# La fiche d'analyse

**Travail en autonomie** · bloc 3 · à faire après les séances 5 et 6

> ⚠️ **Avant de taper quoi que ce soit :** *Fichier → Enregistrer une copie dans Drive*. Sinon votre travail sera perdu en fermant l'onglet.

Ce notebook n'est pas noté. Il sert à vérifier, seul, que vous savez faire ce que les deux séances ont montré — et à repartir avec un document qui a de l'allure.
""")

md("""
## La commande

Vous êtes analyste dans une société de gestion. Le comité d'investissement vous demande deux choses sur une cryptomonnaie :

1. **« Quel risque on prend ? »** — un portrait chiffré de l'actif.
2. **« Et cette idée qu'on nous a soufflée, elle tient ? »** — quelqu'un a lu sur un forum que *le cours rebondit après une grosse baisse, il suffit d'acheter le lendemain*. Vrai ou faux ?

Vous allez produire un seul document qui répond aux deux. C'est une **fiche d'analyse**, et c'est ce qu'un desk pose sur la table avant d'autoriser une exposition.

**Prenez position maintenant, avant de calculer :** croyez-vous au rebond ? Notez votre intuition quelque part. On y reviendra à la fin.

## Comment on va procéder

La **mise en page est déjà écrite** : une fonction vous est fournie, elle dessine la fiche. Votre travail est de calculer ce qui va dedans — et vous savez déjà tout faire.

1. on appelle la fonction tout de suite, alors que vous n'avez rien calculé : la fiche apparaît **vide** ;
2. à chaque étape, vous calculez un morceau ;
3. on rappelle la fonction, et la fiche se remplit ;
4. à la fin, on en fait une petite application avec un champ de saisie.

Chaque étape dit **ce qu'on cherche** et **où c'était dans le cours**. Elle ne donne pas la réponse : c'est à vous de retrouver la ligne. Après chaque cellule, une cellule `verifier` vous dit si c'est juste — un `A REVOIR` n'est pas une faute, c'est une indication.

Exécutez les deux cellules ci-dessous.
""")

code(f"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy import stats

pd.set_option("display.max_rows", 12)
BASE = "{BASE}"


def verifier(nom, condition, indice=""):
    if condition:
        print("OK       -", nom)
    else:
        print("A REVOIR -", nom, ":", indice)
""")

md("""
La cellule suivante contient la fonction qui dessine la fiche. Elle est longue, et **vous n'avez pas à la lire** : exécutez-la, puis oubliez-la.
""")

code(FICHE)

md("""
## Regardez ce qu'on va remplir

Choisissez votre monnaie parmi les sept : `BTC`, `ETH`, `SOL`, `DOGE`, `XRP`, `BNB`, `ADA`.

Si vous hésitez, gardez `SOL` : c'est celle qui réserve les meilleures surprises.
""")

code("""
MONNAIE = "SOL"
""")

code("""
crypto = pd.read_csv(BASE + "crypto.csv")
crypto["date"] = pd.to_datetime(crypto["date"])
crypto = crypto.sort_values(["coin", "date"]).reset_index(drop=True)

afficher_fiche(MONNAIE, seuil=-5)
plt.show()
""")

md("""
Voilà le squelette, en deux volets.

**En haut, le risque** : le cours, quatre indicateurs, la forme des journées et la place de votre monnaie parmi les sept.

**En bas, l'idée de stratégie** : un grand cadre pour l'intervalle de confiance, quatre indicateurs de test, et deux graphiques. Le verdict, à droite du séparateur, dit « EN ATTENTE ».

Tout est gris. La fonction ne sait rien : elle affiche « à compléter » pour ce qu'on ne lui donne pas. **À chaque étape, vous allez lui en donner un peu plus.**

---

# Premier volet — le risque
""")

# ---------------------------------------------------------------- étape 1
md("""
## Étape 1 — La table de votre monnaie, et sa colonne de rendement

**Ce qu'on cherche.** Une table `t` avec les lignes de `MONNAIE` seulement, et une colonne `r` : pour chaque jour, la variation en pourcentage par rapport à la veille.

**Où c'était.** Séance 5, sections 1 et 3. Deux pièges :

- le rendement se calcule **par monnaie**, sinon la première ligne se compare au dernier jour de la monnaie précédente — c'est le piège des 933 041 % ;
- après le calcul, le premier jour n'a pas de veille : il vaut `NaN`, il faut le retirer.

La table est déjà triée par monnaie puis par date. Créez la colonne sur `crypto` — le second volet en aura besoin aussi — puis filtrez dans `t`.
""")

code("")

code("""
att = crypto.copy()
att["r"] = att.groupby("coin")["close"].pct_change() * 100
att = att.query("coin == @MONNAIE").dropna(subset=["r"])
verifier("une seule monnaie dans t", t["coin"].nunique() == 1 and t["coin"].iloc[0] == MONNAIE, "un query sur coin == MONNAIE")
verifier("le bon nombre de lignes", len(t) == len(att), "retirez le premier jour, qui n'a pas de veille : dropna(subset=['r'])")
verifier("les rendements sont justes", abs(t["r"].sum() - att["r"].sum()) < 0.01, "groupby('coin')['close'].pct_change() * 100")
verifier("pas de rendement aberrant", t["r"].max() < 400, "un maximum énorme veut dire que le groupby a été oublié")
""")

md("""
On passe la table à la fonction, avec `periode` qui remplit la ligne sous le titre.
""")

code("""
periode = f"{len(t)} jours  ·  {t['date'].min().date()} → {t['date'].max().date()}"

afficher_fiche(MONNAIE, periode=periode, prix=t, seuil=-5)
plt.show()
""")

md("""
La courbe est apparue. C'est le graphique que tout le monde regarde — celui qui raconte la trajectoire.

Il ne dit rien du risque : la montée écrase les journées à −40 %. La suite va chercher ce qu'il cache.
""")

# ---------------------------------------------------------------- étape 2
md("""
## Étape 2 — Les quatre indicateurs de risque

Quatre nombres d'un coup, tous sur la colonne `r`. Ce sont ceux que le comité regardera en premier.

| Variable | Ce que c'est | Méthode |
|---|---|---|
| `rendement_moyen` | la tendance sur la durée | la moyenne |
| `rendement_median` | la journée ordinaire | la médiane |
| `volatilite` | **la** mesure du risque : l'ampleur typique d'une journée | l'écart-type |
| `var_95` | la **Value at Risk** : le seuil qu'une journée sur vingt dépasse à la baisse | le quantile 5 % |

**Où c'était.** Séance 5, section 2, pour les quatre. Une ligne chacun.

**Attention au sens du quantile.** `quantile(0.05)` donne la valeur en dessous de laquelle tombent 5 % des journées : c'est un nombre **négatif**, donc bien une perte.
""")

code("")

code("""
verifier("rendement moyen", abs(rendement_moyen - t["r"].mean()) < 1e-9, ".mean() sur la colonne r")
verifier("rendement median", abs(rendement_median - t["r"].median()) < 1e-9, ".median() sur la colonne r")
verifier("volatilite", abs(volatilite - t["r"].std()) < 1e-9, ".std() sur la colonne r")
verifier("VaR 95", abs(var_95 - t["r"].quantile(0.05)) < 1e-9, ".quantile(0.05) sur la colonne r")
verifier("la VaR est bien une perte", var_95 < 0, "si votre nombre est positif, vous avez pris quantile(0.95)")
""")

md("""
**Comparez la moyenne et la médiane.** Si la moyenne est positive et la médiane négative, ce n'est pas une erreur : votre monnaie baisse plus d'un jour sur deux et doit tout à quelques journées d'envolée.

**Traduisez votre VaR en euros**, mentalement : sur 10 000 €, une fois par mois environ, on perd plus de ... € ? C'est la phrase que le comité attend — pas « la volatilité est de 6,19 % ».
""")

code("""
afficher_fiche(MONNAIE, periode=periode, prix=t, seuil=-5,
               rendement_moyen=rendement_moyen, rendement_median=rendement_median,
               volatilite=volatilite, var_95=var_95)
plt.show()
""")

md("""
Les quatre tuiles sont remplies. Remarquez ce que la fonction a ajouté toute seule, en petit : le **rendement annuel**, et la **volatilité annualisée** — la convention du métier. Vous n'aviez pas à les calculer.

Gardez le rendement annuel en tête : on y revient tout à la fin.
""")

# ---------------------------------------------------------------- étape 3
md("""
## Étape 3 — La forme des journées, et le pire jour

Le graphique en bas à gauche du premier volet se trace tout seul dès qu'on donne la colonne `r`. Mais on veut aussi **la part de journées en hausse** et **marquer le pire jour dessus**, avec sa date.

**Ce qu'on cherche.** `part_hausse`, `pire_jour`, `date_pire`.

Pour `part_hausse` : **en pourcentage**, entre 0 et 100. Le raisonnement est celui de la séance 5, section 3 — une comparaison sur une colonne donne des `True` et des `False`, `True` vaut 1, donc la moyenne est la part.

Pour `pire_jour` : `.min()`, vous savez faire.

Pour `date_pire`, il faut une méthode nouvelle. La voici.

### `idxmin` : à quelle ligne se trouve le minimum ?

`t["r"].min()` répond à « **quelle est** la plus petite valeur ? ». Il existe une méthode qui répond à l'autre question : « **où** est-elle ? ».
""")

code("""
print(t["r"].min())        # quelle est la plus petite valeur
print(t["r"].idxmin())     # à quelle ligne elle se trouve
""")

md("""
`idxmin` ne donne pas une valeur : il donne **l'étiquette de la ligne** où se trouve le minimum — le numéro qui apparaît à gauche quand vous affichez la table.

### `.loc` : aller lire une case précise

Ce numéro seul ne sert à rien. Il faut s'en servir pour **lire une autre colonne sur cette même ligne**. C'est le rôle de `.loc`, qui prend une étiquette de ligne et un nom de colonne :

```python
table.loc[numéro_de_ligne, "nom_de_colonne"]
```

Les deux ensemble :
""")

code("""
print(t.loc[t["r"].idxmin(), "date"])
""")

md("""
La date du pire jour. On l'allège avec `.date()`, qui retire l'heure — inutile ici.

> `idxmax` existe aussi. Retenez la paire : `min` / `max` donnent **la valeur**, `idxmin` / `idxmax` donnent **la ligne**.

### À vous

Les trois variables : `part_hausse` en pourcentage, `pire_jour`, et `date_pire` avec `.date()` à la fin.
""")

code("")

code("""
verifier("part_hausse", abs(part_hausse - (t["r"] > 0).mean() * 100) < 1e-9, "(t['r'] > 0).mean() donne une part entre 0 et 1 ; la fiche attend un pourcentage")
verifier("l'ordre de grandeur", 30 < part_hausse < 70, "un résultat proche de 0.5 veut dire qu'il manque le * 100")
verifier("pire_jour", abs(pire_jour - t["r"].min()) < 1e-9, ".min() sur la colonne r")
verifier("date_pire", str(date_pire) == str(t.loc[t["r"].idxmin(), "date"].date()), "t.loc[t['r'].idxmin(), 'date'].date()")
""")

# ---------------------------------------------------------------- étape 4
md("""
## Étape 4 — Situer votre monnaie

Un chiffre de risque tout seul ne veut rien dire. 6 % de volatilité quotidienne, est-ce beaucoup ? La seule façon de répondre est de comparer.

**Ce qu'on cherche.** `classement`, une Series donnant la volatilité de **chacune des sept monnaies**, triée de la plus faible à la plus forte. Elle se calcule sur `crypto`, la table complète — pas sur `t`.

**Où c'était.** Séance 5, section 3 : grouper par monnaie, résumer par l'écart-type, trier.
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

md("""
Le premier volet est complet.
""")

code("""
afficher_fiche(MONNAIE, periode=periode, prix=t, seuil=-5,
               rendement_moyen=rendement_moyen, rendement_median=rendement_median,
               volatilite=volatilite, var_95=var_95,
               part_hausse=part_hausse, pire_jour=pire_jour, date_pire=date_pire,
               rendements=t["r"], classement=classement)
plt.show()
""")

md("""
Le portrait de risque est fait : la trajectoire, quatre chiffres, la forme des pertes, et la place de votre monnaie parmi les sept.

Reste la seconde question du comité.

---

# Second volet — l'idée de stratégie

> « Le cours rebondit toujours après une grosse baisse. J'achète le lendemain de chaque journée à −5 %, je revends 24 heures plus tard. Ça marche à tous les coups. »

C'est une affirmation **vérifiable**. On la vérifie.
""")

# ---------------------------------------------------------------- étape 5
md("""
## Étape 5 — Le rendement de la veille, et les deux paquets

Pour comparer « le lendemain d'une grosse baisse » aux autres jours, il faut d'abord, sur chaque ligne, **le rendement de la veille**.

**Ce qu'on cherche.**

- une colonne `r_hier` sur `crypto` : le rendement de la **veille**, sur la même ligne. La méthode qui décale une colonne d'un cran vers le bas est celle de la séance 5, section 1 — celle qui donnait le prix de la veille. Appliquez-la cette fois à `r`, et **par monnaie**, comme toujours.
- puis deux paquets de rendements, sur **votre** monnaie : `apres_baisse`, les journées dont la veille a fait moins de −5 % ; `autres_jours`, toutes les autres.
- et trois nombres : `nb_occasions`, `gain_moyen`, `gain_autres`.

Les deux paquets doivent être **complémentaires** : chaque journée est dans l'un ou dans l'autre, jamais dans les deux.

> Si votre monnaie est `SOL`, attention : elle n'existe qu'à partir de 2020, vous aurez donc moins d'occasions que les autres.
""")

code("")

code("""
cr = crypto.copy()
cr["r"] = cr.groupby("coin")["close"].pct_change() * 100
cr["r_hier"] = cr.groupby("coin")["r"].shift(1)
cr = cr.query("coin == @MONNAIE").dropna(subset=["r", "r_hier"])
verifier("la colonne r_hier", "r_hier" in crypto.columns, "une colonne r_hier sur crypto")
verifier("le decalage est fait par monnaie", abs(crypto.dropna(subset=["r_hier"])["r_hier"].sum() - cr["r_hier"].sum()) > -1, "groupby('coin')['r'].shift(1)")
verifier("le paquet 'apres baisse'", abs(apres_baisse.sum() - cr.query("r_hier < -5")["r"].sum()) < 0.01, "query sur coin == MONNAIE and r_hier < -5, puis la colonne r")
verifier("le paquet 'autres jours'", abs(autres_jours.sum() - cr.query("r_hier >= -5")["r"].sum()) < 0.01, "la condition inverse : r_hier >= -5")
verifier("les deux paquets couvrent tout", len(apres_baisse) + len(autres_jours) == len(cr), "aucune journée ne doit manquer ni compter deux fois")
verifier("nb_occasions et les moyennes", nb_occasions == len(apres_baisse) and abs(gain_moyen - apres_baisse.mean()) < 1e-9 and abs(gain_autres - autres_jours.mean()) < 1e-9, "len() et .mean() sur chaque paquet")
""")

code("""
afficher_fiche(MONNAIE, periode=periode, prix=t, seuil=-5,
               rendement_moyen=rendement_moyen, rendement_median=rendement_median,
               volatilite=volatilite, var_95=var_95,
               part_hausse=part_hausse, pire_jour=pire_jour, date_pire=date_pire,
               rendements=t["r"], classement=classement,
               nb_occasions=nb_occasions, gain_moyen=gain_moyen, gain_autres=gain_autres)
plt.show()
""")

md("""
Comparez vos deux moyennes. Le lendemain d'une grosse baisse rapporte **plusieurs fois** ce que rapporte une journée ordinaire.

Le forum a l'air d'avoir raison — et le verdict reste pourtant « EN ATTENTE ». C'est normal : **une moyenne seule ne permet de conclure à rien.** Il lui manque son épaisseur.
""")

# ---------------------------------------------------------------- étape 6
md("""
## Étape 6 — L'épaisseur du résultat

Ces journées ne sont pas « toutes les journées de rebond possibles ». C'est **un échantillon** : ce qui est arrivé, parmi ce qui aurait pu arriver. Avec d'autres journées, la moyenne aurait été différente. De combien ?

C'est la question de la séance 6, section 1. On rejoue l'échantillon.

**Attention à ce qu'on mesure.** La question n'est pas « la stratégie gagne-t-elle de l'argent » — presque toutes les journées de crypto en gagnent en moyenne. La question est : **gagne-t-elle plus qu'une journée ordinaire ?** C'est donc l'**écart** entre les deux paquets qu'il faut mesurer, et dont il faut trouver l'épaisseur.

**Ce qu'on cherche.**

- `boot` : une Series de **1 000 écarts**. À chaque tour de boucle, on tire un échantillon avec remise dans **chacun** des deux paquets, on prend les deux moyennes, et on range leur différence ;
- `borne_basse` et `borne_haute` : les quantiles 2,5 % et 97,5 % de `boot`.

**Où c'était.** Séance 6, sections 1 et 2. La boucle est celle du bloc Python : liste vide, `append` dedans, `pd.Series` à la fin. La seule différence avec le cours : deux tirages par tour au lieu d'un, et c'est leur **différence** qu'on range. Mettez `random_state=i` sur les deux.

> C'est la cellule la plus lente du notebook : mille tirages prennent quelques secondes.
""")

code("")

code("""
verifier("mille tirages", len(boot) == 1000, "une boucle for i in range(1000)")
verifier("le tirage est avec remise", boot.std() > 0, "sans replace=True, les 1000 écarts seraient identiques")
verifier("c'est bien un ecart", abs(boot.mean() - (gain_moyen - gain_autres)) < 0.35, "chaque tour range la différence des deux moyennes, pas la moyenne du seul paquet 'apres_baisse'")
verifier("les bornes", borne_basse < borne_haute and abs(borne_basse - boot.quantile(0.025)) < 1e-9, "quantile(0.025) et quantile(0.975)")
""")

# ---------------------------------------------------------------- étape 7
md("""
## Étape 7 — Le test, en un nombre

L'intervalle a déjà répondu. Le test t dit la même chose en un chiffre, et c'est celui qu'on vous demandera.

**Ce qu'on cherche.** `p_value`, la p-value du test comparant les deux paquets de l'étape 5.

**Où c'était.** Séance 6, section 3. Une ligne, avec `equal_var=False`, et on récupère l'attribut `.pvalue`.
""")

code("")

code("""
verifier("p_value", abs(p_value - stats.ttest_ind(apres_baisse, autres_jours, equal_var=False).pvalue) < 1e-9, "stats.ttest_ind(paquet1, paquet2, equal_var=False).pvalue")
""")

code("""
afficher_fiche(MONNAIE, periode=periode, prix=t, seuil=-5,
               rendement_moyen=rendement_moyen, rendement_median=rendement_median,
               volatilite=volatilite, var_95=var_95,
               part_hausse=part_hausse, pire_jour=pire_jour, date_pire=date_pire,
               rendements=t["r"], classement=classement,
               nb_occasions=nb_occasions, gain_moyen=gain_moyen, gain_autres=gain_autres,
               borne_basse=borne_basse, borne_haute=borne_haute, p_value=p_value, boot=boot)
plt.show()
""")

md("""
**Le verdict est tombé**, et il se lit d'un coup d'œil dans le grand cadre : la barre passe-t-elle par zéro ?

Si elle le fait, les écarts plausibles vont d'un nombre **négatif** à un nombre positif. Autrement dit : au vu de ces journées, on ne peut pas exclure que le lendemain d'une baisse soit **moins bon** qu'une journée ordinaire. L'histogramme en dessous le montre autrement — une partie des mille tirages est à gauche de zéro.

Et rappelez-vous la phrase exacte de la p-value : *si les deux paquets venaient de la même population, quelle serait la probabilité d'observer un écart au moins aussi grand, par le seul hasard ?*

> **Si votre intervalle et votre p-value se contredisent**, ce n'est pas une erreur de votre part. Les deux répondent à la même question par deux chemins : l'intervalle ne suppose rien, le test t suppose que les moyennes se comportent à peu près normalement. Quand une seule journée extrême domine les données — c'est le cas de `DOGE` et de son +354 % — cette supposition lâche, et les deux méthodes divergent. **C'est l'intervalle qu'il faut croire**, et la divergence elle-même est un signal : allez regarder vos extrêmes.
""")

# ---------------------------------------------------------------- étape 8
md("""
## Étape 8 — Et si on avait cherché ailleurs ?

Vous avez testé **une** monnaie à **un** seuil. Un analyste pressé, lui, aurait essayé plusieurs combinaisons jusqu'à en trouver une qui marche.

Faisons-le, pour voir. Cellule fournie : sept monnaies, quatre seuils, **vingt-huit tests**. Exécutez-la.
""")

code("""
SEUILS = [-4, -5, -7, -10]
MONNAIES = ["BTC", "ETH", "SOL", "DOGE", "XRP", "BNB", "ADA"]

lignes = []
for m in MONNAIES:
    ligne = []
    for s in SEUILS:
        x = crypto.query(f"coin == '{m}'").dropna(subset=["r", "r_hier"])
        a = x.query(f"r_hier < {s}")["r"]
        o = x.query(f"r_hier >= {s}")["r"]
        ligne.append(stats.ttest_ind(a, o, equal_var=False).pvalue)
    lignes.append(ligne)

grille = pd.DataFrame(lignes, index=MONNAIES, columns=[f"{s} %" for s in SEUILS])
grille.round(3)
""")

md("""
Comptez les cases sous 0,05.

**Au seuil de 5 %, un test sur vingt se déclenche même quand il n'y a rien à trouver.** Sur vingt-huit tests, le hasard seul en produirait un ou deux. Il y en a nettement plus.

Un analyste qui aurait commencé par cette grille aurait annoncé une découverte : il aurait choisi la case la plus basse, écrit une note, et se serait trompé — parce que **le seuil de 5 % ne vaut que pour un test décidé avant de regarder les données**.

Ajoutons la grille, la fiche est complète.
""")

code("""
afficher_fiche(MONNAIE, periode=periode, prix=t, seuil=-5,
               rendement_moyen=rendement_moyen, rendement_median=rendement_median,
               volatilite=volatilite, var_95=var_95,
               part_hausse=part_hausse, pire_jour=pire_jour, date_pire=date_pire,
               rendements=t["r"], classement=classement,
               nb_occasions=nb_occasions, gain_moyen=gain_moyen, gain_autres=gain_autres,
               borne_basse=borne_basse, borne_haute=borne_haute, p_value=p_value,
               boot=boot, grille=grille)
plt.show()
""")

md("""
**Sauf qu'une ligne de cette grille n'est pas comme les autres.** Regardez-la : une monnaie passe le test aux **quatre** seuils.

Ce n'est pas le profil du hasard — le hasard frappe au hasard, pas quatre fois dans la même ligne.
""")

# ---------------------------------------------------------------- étape 9
md("""
## Étape 9 — La seule façon d'en avoir le cœur net

Effet réel, ou coïncidence spectaculaire ? **On ne peut pas le savoir en regardant encore ces mêmes données.** On les a déjà fouillées ; elles ne peuvent plus nous surprendre.

Il n'existe qu'une sortie, et c'est la leçon la plus importante du bloc : **vérifier sur des données qu'on n'a pas regardées.**

On coupe l'histoire de cette monnaie en deux moitiés, dans l'ordre du temps. La première a servi à trouver l'idée. La seconde n'a jamais été consultée : c'est elle qui juge.

**Ce qu'on cherche.**

- `ada` : les lignes de `ADA`, sans les valeurs manquantes des colonnes `r` et `r_hier` ;
- `moitie1` et `moitie2` : les deux moitiés. Utilisez `.head()` et `.tail()` avec `len(ada) // 2` — la **division entière**, qui donne un nombre de lignes entier ;
- `p1` et `p2` : la p-value du test de l'étape 7, calculée dans chaque moitié séparément.
""")

code("")

code("""
a_ref = crypto.query("coin == 'ADA'").dropna(subset=["r", "r_hier"])
n_ref = len(a_ref) // 2
att = []
for part in (a_ref.head(n_ref), a_ref.tail(len(a_ref) - n_ref)):
    att.append(stats.ttest_ind(part.query("r_hier < -5")["r"], part.query("r_hier >= -5")["r"], equal_var=False).pvalue)
verifier("les deux moities", len(moitie1) + len(moitie2) == len(ada) and len(moitie1) == n_ref, "head(len(ada) // 2), puis tail du reste")
verifier("p1", abs(p1 - att[0]) < 1e-9, "le test de l'étape 7, appliqué à moitie1")
verifier("p2", abs(p2 - att[1]) < 1e-9, "le même test, appliqué à moitie2")
""")

md("""
### Le résultat

Les deux p-values sont sous 0,05. **L'effet tient sur la seconde moitié**, celle qui n'avait jamais servi.

Ce n'était donc pas du bruit. Cette monnaie rebondit vraiment après ses grosses baisses — et c'est cohérent : c'est l'une des plus agitées des sept, et les actifs très volatils exagèrent dans les deux sens.

Comparez avec le bitcoin :
""")

code("""
btc = crypto.query("coin == 'BTC'").dropna(subset=["r", "r_hier"])
n = len(btc) // 2
for nom, part in [("première moitié", btc.head(n)), ("seconde moitié", btc.tail(len(btc) - n))]:
    a = part.query("r_hier < -5")["r"]
    o = part.query("r_hier >= -5")["r"]
    print(nom, ":", round(stats.ttest_ind(a, o, equal_var=False).pvalue, 3))
""")

md("""
Rien, ni dans une moitié ni dans l'autre. Le bitcoin ne rebondit pas.
""")

# ---------------------------------------------------------------- l'application
md("""
---

## Pour finir — la fiche en petite application

Vous avez fait tout le travail pour **une** monnaie. La cellule ci-dessous ne contient rien de nouveau : ce sont **vos lignes**, dans l'ordre, rassemblées. Lisez-la, vous devriez tout reconnaître.
""")

code('''
def fiche_de(nom):
    """Refait toutes les étapes de ce notebook pour la monnaie demandée."""
    tt = crypto.query("coin == @nom").dropna(subset=["r"])
    ap = tt.dropna(subset=["r_hier"]).query("r_hier < -5")["r"]
    au = tt.dropna(subset=["r_hier"]).query("r_hier >= -5")["r"]
    bo = pd.Series([ap.sample(len(ap), replace=True, random_state=i).mean()
                    - au.sample(len(au), replace=True, random_state=i).mean() for i in range(1000)])
    cl = crypto.groupby("coin")["r"].std().sort_values()

    afficher_fiche(nom,
                   periode=f"{len(tt)} jours  ·  {tt['date'].min().date()} → {tt['date'].max().date()}",
                   prix=tt, seuil=-5,
                   rendement_moyen=tt["r"].mean(), rendement_median=tt["r"].median(),
                   volatilite=tt["r"].std(), var_95=tt["r"].quantile(0.05),
                   part_hausse=(tt["r"] > 0).mean() * 100, pire_jour=tt["r"].min(),
                   date_pire=tt.loc[tt["r"].idxmin(), "date"].date(),
                   rendements=tt["r"], classement=cl,
                   nb_occasions=len(ap), gain_moyen=ap.mean(), gain_autres=au.mean(),
                   borne_basse=bo.quantile(0.025), borne_haute=bo.quantile(0.975),
                   p_value=stats.ttest_ind(ap, au, equal_var=False).pvalue,
                   boot=bo, grille=grille)
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

Rien de neuf pour vous — c'est toujours `fiche_de` qui travaille.
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
> Si cette dernière cellule n'affiche rien, ce n'est pas grave : le champ de saisie dépend d'un module que Colab ne charge pas toujours. `fiche_de("BTC")` marche dans tous les cas.

## Ce que vous en retenez

Répondez en double-cliquant sur cette cellule.

**1. Reprenez l'intuition que vous aviez notée au début. Aviez-vous raison sur le rebond ?**

*[votre réponse]*

**2. Sur votre fiche, quel est le chiffre le moins fiable, et pourquoi ?**
Un indice : la séance 6 a mesuré l'épaisseur du rendement moyen du bitcoin — elle allait de +1 % à +126 % par an. Regardez le rendement annuel affiché sur votre fiche.

*[votre réponse]*

**3. Un collègue vous montre un backtest impressionnant. Quelles deux questions lui posez-vous avant de le croire ?**
Une porte sur ce qu'il a essayé **avant** de trouver ça ; l'autre sur les données qui lui ont servi à **vérifier**.

*[votre réponse]*

## La morale, en trois lignes

1. **Un écart impressionnant n'est pas un effet.** Six fois mieux que la normale, et l'intervalle passait quand même par zéro.
2. **Chercher jusqu'à trouver finit toujours par trouver.** Vingt-huit tests, sept qui passent, là où le hasard en prédit un ou deux.
3. **La seule preuve est une donnée qu'on n'a pas regardée.** C'est ce qui a séparé un vrai effet d'une coïncidence — et c'est exactement ce que fait le bloc suivant, à chaque modèle qu'il construit.

## Avant de fermer

1. *Exécution → Redémarrer et tout exécuter*.
2. Toutes les cellules `verifier` affichent `OK`.
3. Les trois réponses en texte sont écrites.
""")

nb = {"cells": cells,
      "metadata": {"colab": {"provenance": [], "toc_visible": True},
                   "kernelspec": {"display_name": "Python 3", "name": "python3"},
                   "language_info": {"name": "python"}},
      "nbformat": 4, "nbformat_minor": 0}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(nb, open(OUT, "w"), ensure_ascii=False, indent=1)
print("écrit", OUT, len(cells), "cellules")
