# pandas en 4h : plan détaillé, cellule par cellule

Suite de `PLAN_python_detaille.md`. Même format : durée par section, texte du cours en quelques phrases, cellules de démonstration, exercices avec énoncé, points de coupe.

Les données sont figées (14 septembre 2026) et les valeurs attendues des exercices sont reportées ici et dans `pandas_crypto/data/valeurs_reference.json`.

---

## 0. Décisions prises

**Budget.** Deux séances de 2h, D1 et D2, puis un exercice de synthèse d'environ 45 minutes suivi de sa correction, fait en classe sur le budget révision, comme l'assignment Python. Après ça, 10h sont passées et pandas est fini.

**La base.** Cours quotidiens de cryptomonnaies, un seul fichier, format long. Le fichier réel sera propre ; le fichier sale est fabriqué par nous. Schéma en section 2.

**La progression de D1.** On ne charge pas de fichier avant d'avoir construit soi-même une DataFrame. Une Series, des calculs dessus, puis trois Series assemblées côte à côte : c'est une DataFrame. Choisir une colonne, c'est retrouver une des Series de départ. Calculer sur une colonne, c'est refaire les calculs de la Series. Seulement ensuite on charge une table qu'on n'a pas fabriquée, et c'est là que `shape`, `columns`, `info` ont un sens : on ne la connaît pas.

**Filtrer avec `query`, pas avec un masque entre crochets.** La condition s'écrit entre guillemets, dans la syntaxe déjà connue : `and`, `or`, `not`, `in`, les six comparaisons. Pas de `&`, `|`, `~`, `isin`, pas de parenthèses obligatoires. Un seul nouveau mot, `query`. La colonne de booléens reste enseignée, mais pour **compter** : une comparaison sur une colonne donne une colonne de `bool`, `.sum()` compte, `.mean()` donne une part. Pour filtrer sur un booléen calculé (`isna`, `duplicated`), on **crée une colonne** et on la passe à `query` : `sale.query("manquant == False")`. Ça réutilise la création de colonne et la syntaxe connue, sans rien ajouter.

**`value_counts` entre dans le bloc.** Il arrive au moment où l'on parle des colonnes de texte : dans une table d'analyse, le texte, ce sont des catégories, et la première question sur une catégorie est « combien par catégorie ». `describe`, `corr`, histogramme et nuage de points restent au bloc stats.

**Ce qu'on retire du cours actuel.** `loc`, `iloc`, le masque entre crochets, `&` / `|` / `~`, `isin`, `merge`, `crosstab`, `unstack`, `agg` nommé, `np.where`, `np.select`, `pd.cut`, `to_numeric`, `describe`, `corr`, histogramme, nuage de points, valeurs aberrantes, la section « lire une erreur », la présentation des bibliothèques.

**Ce qui reste.** Treize nouveautés : `pd.DataFrame` pour assembler des Series, `read_csv`, `shape` / `columns` / `info`, `head` / `tail`, `query`, `isna`, `duplicated`, `.str` devant une méthode, `astype`, `value_counts` / `unique` / `nunique`, `to_datetime` avec `.dt`, `sort_values`, `groupby`, `plot` avec `x=`, `y=` et `kind="bar"`. Tout le reste est déjà connu : arithmétique, comparaisons, `and` / `or` / `not` / `in`, `sum` / `max` / `min` / `mean`, `len`, `replace` / `strip` / `upper`, `float`, la boucle avec `append`, les f-strings, `pd.Series`.

---

## 1. Le fil, et comment faire participer

### 1.1 Les deux phrases du bloc

Écrites en tête de D1, rappelées en tête de D2, et chaque section y renvoie.

> **Tout ce que vous savez faire sur une valeur, vous le faites maintenant sur une colonne entière.**

> **Tout ce que pandas fait, vous pourriez l'écrire vous-même avec une colonne de booléens et une boucle.**

La première organise D1 : arithmétique sur une colonne, comparaison sur une colonne, fonctions sur une colonne, condition de `query` dans la syntaxe de la séance 2. La seconde organise D2 : `dropna`, `drop_duplicates` et `groupby` sont d'abord construits avec une colonne de booléens, `query` et la boucle de la séance 2, puis remplacés par la ligne pandas.

### 1.2 La table jouet, construite à partir de Series

Sur 20 000 lignes, on ne peut rien prédire de tête. Sur six lignes affichées, si. Et cette fois la table jouet n'est pas fournie : **on la construit devant eux**, en D1.2, à partir de quatre Series. C'est à la fois la définition de la DataFrame et l'outil de prédiction du bloc.

```python
coin   = pd.Series(["BTC", "ETH", "SOL", "BTC", "ETH", "SOL"])
date   = pd.Series(["2024-01-01", "2024-01-01", "2024-01-01", "2024-01-02", "2024-01-02", "2024-01-02"])
close  = pd.Series([42000, 2300, 100, 44000, 2400, 95])
volume = pd.Series([20, 10, 5, 25, 12, 4])

jouet = pd.DataFrame({"coin": coin, "date": date, "close": close, "volume": volume})
jouet
```

On dit : `pd.DataFrame` assemble des Series côte à côte, et on donne un nom à chacune entre les accolades. On n'explique pas les accolades au-delà de ça. En D2, la même cellule est fournie en tête de notebook.

Toutes les cellules « Prédire » du bloc portent sur `jouet`. Les exercices « Écrire » portent sur le vrai fichier.

### 1.3 Quatre formats de participation

- **Prédire la valeur**, sur `jouet`. « Qu'affiche `jouet["close"] > 1000` ? » L'étudiant écrit la réponse en commentaire, on exécute.
- **Prédire la forme.** Avant d'exécuter : « Series ou DataFrame ? Combien de lignes ? » C'est la question la plus utile de tout pandas, et elle se pose à voix haute sur n'importe quelle cellule, y compris sur le vrai fichier.
- **Lire le code, dire la question.** On affiche une ligne, `crypto.query("coin == 'BTC'")["close"].max()`, et on demande : « À quelle question cette ligne répond-elle ? » Réponse en français.
- **Dire la question, écrire le code.** L'inverse. « Le volume moyen de SOL » : on écrit la ligne au tableau ensemble, de gauche à droite.

Les deux derniers formats remplacent la prédiction quand le résultat n'est pas calculable de tête. Ils entraînent exactement la compétence attendue : traduire une question en une ligne pandas, et retour.

### 1.4 La lecture de gauche à droite

Une ligne pandas se lit comme une phrase, un point à la fois. Au tableau, une fois par séance au moins :

```
crypto.query("coin == 'BTC'")["close"].max()
│      │                      │        │
│      │                      │        └─ le plus grand
│      │                      └─ de la colonne close
│      └─ les lignes où coin vaut BTC
└─ dans la table crypto
```

---

## 2. Les données

### 2.1 Le fichier propre : `crypto.csv`

| Colonne | Type | Contenu |
|---|---|---|
| `date` | texte ISO `2024-01-15` | le jour |
| `coin` | texte | `BTC`, `ETH`, `SOL`, `DOGE`, `XRP`, `BNB`, `ADA` |
| `close` | float | cours de clôture en dollars |
| `volume` | float | nombre d'unités échangées dans la journée (le montant en dollars est `close * volume`) |

Une ligne = une monnaie un jour. Du 1er janvier 2018 au 31 août 2026, 21 325 lignes : 3 165 par monnaie, 2 335 pour SOL. SOL commence en 2020 : une raison naturelle de compter les lignes par monnaie. Pas de valeur manquante, pas de doublon.

Construit le 14 septembre 2026 par `pandas_crypto/data/build_data.py` avec yfinance, figé dans le dépôt, servi par le CDN. Les valeurs de référence sont dans `pandas_crypto/data/valeurs_reference.json`.

### 2.2 Le fichier sale : `crypto_sale.csv`

Fabriqué par nous à partir de l'année 2024 du fichier propre, 2 592 lignes, avec exactement quatre défauts, un par outil de D2 :

| Défaut | Forme | Outil |
|---|---|---|
| volumes manquants | 41 cases vides | `isna`, `dropna` |
| lignes en double | 30 lignes recopiées, réparties dans le fichier | `duplicated`, `drop_duplicates` |
| prix en texte | `"43 250,12 $"` : espace, virgule, symbole | `.str.replace`, `astype(float)` |
| noms de monnaies incohérents | `"btc"`, `" BTC"`, `"Btc "` sur un quart des lignes, 28 catégories pour 7 monnaies | `value_counts`, `.str.strip().str.upper()` |

Les dates restent propres et ISO. Pas de prix aberrant. Après `dropna` : 2 551 lignes ; après `drop_duplicates` en plus : 2 522.

### 2.3 Les questions qui portent le bloc

Posées en tête de D1, elles reviennent comme exercices :

- combien de jours BTC a-t-il clôturé au-dessus de 100 000 dollars ?
- quelle monnaie a le plus de jours dans le fichier, et pourquoi pas toutes le même nombre ?
- quel a été le cours moyen de chaque monnaie en 2024 ?
- si vous aviez acheté 100 dollars de bitcoin le premier de chaque mois depuis 2020, combien auriez-vous aujourd'hui ?

La dernière est l'exercice de synthèse.

---

## 3. Séance D1 (2h) : des Series à la table

| Section | Minutes | Cumul |
|---|---|---|
| D1.0 Échauffement | 10 | 10 |
| D1.1 La Series, et les calculs dessus | 15 | 25 |
| D1.2 Trois Series côte à côte : la DataFrame | 25 | 50 |
| D1.3 Charger une table qu'on ne connaît pas | 15 | 65 |
| D1.4 Compter avec une comparaison | 10 | 75 |
| D1.5 Filtrer avec `query` | 30 | 105 |
| D1.6 Trier | 10 | 115 |
| D1.7 Synthèse | 5 | 120 |

Points de coupe : l'exercice 3 de D1.2 ; le « dire la question » de D1.5 ; D1.6 passe en échauffement de D2.

### D1.0 Échauffement, 10 min

Cellule de setup. Trois cellules sur la séance 2 : une boucle avec `append` sur une liste de prix, `pd.Series` sur le résultat, `.mean()` et `.max()` dessus. On repart de là où Python s'est arrêté.

### D1.1 La Series, et les calculs dessus, 15 min

Texte : une Series, c'est une liste avec une étiquette par valeur, qui sait faire des maths sur elle-même.

```python
prix = pd.Series([42000, 2300, 100, 0.08, 0.5], index=["BTC", "ETH", "SOL", "DOGE", "XRP"])
prix
```

Deux morceaux : à gauche les **étiquettes**, c'est l'index ; à droite les **valeurs**. `prix["ETH"]` va chercher par étiquette. Sans `index=`, pandas numérote de 0 à 4, comme une liste.

Ce qu'on savait faire sur une valeur, on le fait sur toute la Series d'un coup :

```python
prix * 2
```

```python
prix / 1000
```

```python
prix.sum(), prix.max(), prix.min(), prix.mean()
```

Et une comparaison, qui donnait un `bool` sur une valeur, donne **une Series de `bool`** : une réponse par étiquette.

```python
prix > 1000
```

`True` vaut 1, donc `.sum()` compte les `True`, et `.mean()` donne la part.

```python
(prix > 1000).sum(), (prix > 1000).mean()
```

**Prédire** (5 cellules) : `prix["SOL"]`, `prix * 1000`, `prix < 1`, `(prix < 1).sum()`, `prix.max() - prix.min()`.

### D1.2 Trois Series côte à côte : la DataFrame, 25 min

Texte : une table, c'est plusieurs Series côte à côte, qui partagent les mêmes étiquettes de lignes. On la construit.

```python
coin   = pd.Series(["BTC", "ETH", "SOL", "BTC", "ETH", "SOL"])
close  = pd.Series([42000, 2300, 100, 44000, 2400, 95])
volume = pd.Series([20, 10, 5, 25, 12, 4])
```

```python
jouet = pd.DataFrame({"coin": coin, "close": close, "volume": volume})
jouet
```

Regardez ce qui s'affiche :

- des **colonnes**, qui ont des noms : ceux qu'on a donnés entre les accolades ;
- des **lignes**, qui ont des étiquettes : `0` à `5`. Ce sont celles des Series de départ, qui n'avaient pas d'`index=`.

C'est une **DataFrame**. Trois Series, un nom chacune, les mêmes étiquettes de lignes.

**Choisir une colonne**, c'est retrouver une des Series de départ :

```python
jouet["close"]
```

```python
type(jouet["close"])
```

Plusieurs colonnes : une liste de noms entre les crochets, et le résultat est une DataFrame plus étroite.

```python
jouet[["coin", "close"]]
```

**Calculer sur une colonne**, c'est faire les calculs de D1.1 sur une des Series :

```python
jouet["close"] * 2
```

```python
jouet["close"] * jouet["volume"]
```

```python
jouet["close"].max(), jouet["volume"].sum(), jouet["close"].mean()
```

Colonne et nombre, colonne et colonne, fonction de colonne : les trois formes qu'on a vues sur `prix`. En séance 2, ça prenait une boucle avec `append` ; ici, une ligne. **C'est la première phrase du bloc.**

**Créer une colonne.** Une affectation, avec un nom de colonne qui n'existe pas encore entre les crochets. C'est l'affectation de la séance 1, sur une table. Et c'est ajouter une quatrième Series à côté des trois autres.

```python
jouet["montant"] = jouet["close"] * jouet["volume"]
jouet
```

`.round(1)` arrondit chaque valeur d'une colonne.

**Prédire** (8 cellules, tout se calcule de tête) : `jouet["volume"]`, `jouet["close"] / 1000`, `jouet["close"] > 1000`, `(jouet["close"] > 1000).sum()`, `jouet["volume"].sum()`, `jouet["close"].mean()`, `jouet["montant"].max()`, `jouet[["coin", "montant"]]`.

**Prédire la forme** (à l'oral) : `jouet["coin"]`, `jouet[["coin", "close"]]`, `jouet["close"] * 2`, `jouet["close"].max()`. Series, DataFrame, Series, un nombre.

**Écrire**, sur `jouet` :

1. Une colonne `close_k`, le cours en milliers. Attendu : `jouet["close_k"].sum() == 90.895`.
2. Une colonne `part`, la part de chaque ligne dans le volume total. Sa somme doit valoir 1.
3. Construisez vous-même une table `perso` à partir de deux Series de votre choix, trois lignes, puis ajoutez-lui une colonne calculée.

**Corriger** : `jouet["Close"]` (majuscule, `KeyError`, réflexe `jouet.columns`, qu'on introduit là) ; `jouet["coin", "close"]` (crochets simples pour deux colonnes) ; `jouet["close"] * jouet["coin"]` (`TypeError` : on relit les types).

### D1.3 Charger une table qu'on ne connaît pas, 15 min

Texte : `jouet`, on l'a construite, on sait ce qu'il y a dedans. Une vraie table, on la reçoit : un fichier, fabriqué par quelqu'un d'autre. On la charge, et la première chose à faire est de la découvrir.

```python
BASE = "https://cdn.jsdelivr.net/gh/.../pandas_crypto/data/"
crypto = pd.read_csv(BASE + "crypto.csv")
crypto
```

`pd.read_csv(...)` a la forme `alias.fonction(argument)` de la séance 1. C'est la même chose qu'une DataFrame construite à la main, en beaucoup plus grand : des colonnes avec des noms, des lignes numérotées.

**Ce qu'on veut savoir d'une table qu'on ne connaît pas.** Toujours les mêmes questions, dans cet ordre :

| Question | Commande |
|---|---|
| combien de lignes, combien de colonnes ? | `crypto.shape` |
| comment s'appellent les colonnes ? | `crypto.columns` |
| quel est le type de chaque colonne, et manque-t-il des valeurs ? | `crypto.info()` |
| à quoi ressemblent le début et la fin ? | `crypto.head()`, `crypto.tail()` |
| une ligne, c'est quoi ? | on regarde, et on se le dit en français |

```python
crypto.shape
```

```python
crypto.columns
```

```python
crypto.info()
```

Lire `info()` : `non-null` dit combien de valeurs sont remplies ; `Dtype` dit le type. `float64` est un `float`, `int64` un `int`, `object` du texte. `date` est donc du texte pour l'instant ; on y revient en D2.

```python
crypto.head(3)
```

```python
crypto.tail(3)
```

La fin dit jusqu'où va le fichier. Une ligne, c'est **une monnaie, un jour**. 21 325 lignes : sept monnaies fois environ huit ans et demi de jours, sauf SOL qui commence en avril 2020.

`len(crypto)` marche aussi : le nombre de lignes, comme sur une liste.

**Dire la question, écrire le code** (au tableau) : « le volume total échangé sur tout le fichier » ; « le cours le plus haut de tout le fichier » ; « une colonne `montant` égale au cours fois le volume ».

**Écrire** :

1. Créez `crypto["montant_m"]`, le montant en millions de dollars, arrondi à 1 décimale. Le plus grand, dans `montant_max`. Attendu : `350967.9`, BTC le 26 février 2021.
2. Le cours le plus élevé et le plus bas de tout le fichier, dans `close_max` et `close_min`. Attendus : `124752.5312` et `0.0015`.

### D1.4 Compter avec une comparaison, 10 min

Texte : sur `prix` et sur `jouet`, une comparaison donnait une Series de `bool`. Sur 20 000 lignes, pareil : une réponse par ligne, et `.sum()` les compte.

```python
crypto["close"] > 100000
```

```python
(crypto["close"] > 100000).sum()
```

```python
(crypto["coin"] == "BTC").mean()
```

La deuxième répond à « combien de jours au-dessus de 100 000 dollars, toutes monnaies confondues ». La troisième à « quelle part du fichier concerne BTC ». Compter et mesurer une part, c'est ça, et ça reviendra jusqu'au bloc ML.

**Écrire** : la part des lignes dont le volume dépasse le volume moyen, dans `part_gros_volume`. Attendu : `0.2034`.

### D1.5 Filtrer avec `query`, 30 min

Section à marteler, et la plus importante du bloc.

Texte : compter les lignes qui remplissent une condition, on sait. Maintenant on veut **les garder** : la table réduite aux jours de BTC, par exemple. C'est `query`. On lui donne la condition **entre guillemets**, écrite exactement comme une condition de la séance 2.

```python
btc = crypto.query("coin == 'BTC'")
btc.shape
```

Le résultat est une DataFrame, avec les mêmes colonnes et moins de lignes. On la range dans une variable, ou on enchaîne.

**Les guillemets.** Toute la condition est un texte, entre guillemets doubles. Un texte à l'intérieur, comme `BTC`, se met entre guillemets simples. C'est la seule difficulté de syntaxe de la section, et on la répète.

**Tout ce que vous savez écrire dans un `if` s'écrit dans `query`.** Les six comparaisons, `and`, `or`, `not`, `in`. Rien de nouveau.

```python
crypto.query("close > 100000")
```

```python
crypto.query("coin == 'BTC' and close > 100000")
```

```python
crypto.query("coin == 'BTC' or coin == 'ETH'")
```

```python
crypto.query("coin in ['BTC', 'ETH']")
```

```python
crypto.query("not coin == 'BTC'")
```

Les dates ISO se comparent comme du texte, et ça marche parce que l'année vient en premier :

```python
crypto.query("date >= '2024-01-01'")
```

**Compter avec `query`.** `len` sur le résultat.

```python
len(crypto.query("coin == 'BTC' and close > 100000"))
```

C'est le même nombre que `.sum()` sur la comparaison en D1.4. Deux chemins, un résultat : on le vérifie ensemble.

**L'aparté sur les étiquettes.** Regardez la colonne de gauche de `btc` : les étiquettes ne recommencent pas à 0. Ce sont celles que ces lignes avaient dans `crypto`. Un filtre garde des lignes, il ne les renumérote pas.

**Enchaîner.** Filtrer, puis choisir une colonne, puis calculer. La lecture de gauche à droite, au tableau :

```python
crypto.query("coin == 'ETH'")["close"].max()
```

**Prédire** sur `jouet` (8 cellules) : `jouet.query("coin == 'SOL'")`, `len(jouet.query("volume > 10"))`, `jouet.query("coin == 'ETH' and close > 2350")`, `jouet.query("coin in ['BTC', 'SOL']")["volume"].sum()`, `jouet.query("not coin == 'BTC'")["close"].max()`, `jouet.query("close < 0")`, `jouet.query("coin == 'BTC'")["close"].mean()`, `jouet.query("volume >= 10 or close < 100")`.

L'avant-dernière donne une table vide : on la montre, parce qu'ils la rencontreront.

**Lire le code, dire la question** (4 lignes, à l'oral) :

- `crypto.query("coin == 'DOGE'")["volume"].mean()`
- `len(crypto.query("close > 1000"))`
- `crypto.query("coin == 'BTC' and date >= '2024-01-01'")["close"].min()`
- `crypto.query("coin in ['SOL', 'ADA']").shape`

**Dire la question, écrire le code** (au tableau) : « le cours moyen de SOL » ; « le nombre de jours où ETH a dépassé 4 000 dollars » ; « le volume total de BTC en 2021 ».

**Écrire** :

1. Combien de jours BTC a-t-il clôturé au-dessus de 100 000 dollars ? Dans `nb_jours_100k`. Attendu : `217`.
2. Combien de lignes pour BTC, combien pour SOL ? Dans `nb_btc` et `nb_sol`. Pourquoi la différence ? Attendus : `3165` et `2335`.
3. Le cours moyen de ETH en 2024, dans `eth_2024`. Deux conditions sur les dates en texte. Attendu : `3044.93`.
4. La part des lignes du fichier qui concernent DOGE ou XRP, en pourcentage, dans `part_doge_xrp`. Deux chemins possibles : `len` d'un `query`, ou `.mean()` d'une comparaison. Faites les deux.

**Corriger** : `crypto.query("coin == BTC")` sans guillemets simples (l'erreur dit que `BTC` n'est pas défini : on lit) ; `crypto.query(coin == 'BTC')` sans guillemets doubles (`NameError`) ; `crypto.query("coin = 'BTC'")` avec un seul `=` (erreur de syntaxe dans la condition, la même qu'en séance 2).

### D1.6 Trier, 10 min

```python
crypto.sort_values("close")
```

```python
crypto.sort_values("close", ascending=False).head(5)
```

La table `crypto` elle-même ne change pas si on ne réaffecte pas : `crypto.head(2)` après le tri le montre.

**Écrire** : les cinq jours de plus gros volume du fichier, dans `top_volume`. Quelle monnaie et quelle année ? Puis les cinq jours de plus bas cours pour ETH.

### D1.7 Synthèse, 5 min

Le tableau « vous voulez / vous écrivez ». Les deux phrases du bloc. Devoir : trois questions en français à traduire en une ligne chacune, sur le vrai fichier.

---

## 4. Séance D2 (2h) : nettoyer et regrouper

| Section | Minutes | Cumul |
|---|---|---|
| D2.0 Échauffement | 10 | 10 |
| D2.1 Le fichier sale | 10 | 20 |
| D2.2 Manquants | 15 | 35 |
| D2.3 Doublons | 10 | 45 |
| D2.4 Texte vers nombre | 10 | 55 |
| D2.5 Le texte, c'est des catégories | 15 | 70 |
| D2.6 Dates | 10 | 80 |
| D2.7 Grouper | 30 | 110 |
| D2.8 Tracer | 5 | 115 |
| D2.9 Synthèse | 5 | 120 |

Points de coupe : le « dire la question » de D2.7 ; l'exercice 2 de D2.5 ; D2.8 fusionne avec l'exercice de synthèse.

### D2.0 Échauffement, 10 min

Setup, la cellule `jouet` fournie (quatre Series, avec `date`), chargement de `crypto`. Puis trois `query` à écrire sur le vrai fichier, un tri, une erreur à corriger.

### D2.1 Le fichier sale, 10 min

Texte : `crypto.csv` était propre. Un export réel ne l'est jamais. Voici le même fichier pour l'année 2024, tel qu'il sortirait d'un système mal réglé.

```python
sale = pd.read_csv(BASE + "crypto_sale.csv")
sale.head(8)
```

```python
sale.info()
```

**Le diagnostic**, ensemble, à voix haute :

- `close` est de type `object` : du texte. On voit pourquoi dans `head` : `43 250,12 $`.
- `volume` a moins de `non-null` que de lignes : des valeurs manquantes.
- `coin` est du texte, normal, mais les valeurs ne sont pas cohérentes : `btc`, ` BTC`.
- Et il y a peut-être des lignes en double : `info()` ne le dit pas.

Quatre défauts, quatre sections. Le plan de la séance est écrit par le diagnostic.

**La seconde phrase du bloc**, annoncée ici : pour chaque défaut, on répare d'abord avec ce qu'on sait, puis on voit la fonction pandas qui fait pareil.

### D2.2 Manquants, 15 min

`isna()` pose une question à chaque case : « es-tu vide ? ». Sur une colonne, ça donne une Series de `bool`, comme une comparaison.

```python
sale["volume"].isna()
```

Compter, comme en D1.4 :

```python
sale["volume"].isna().sum()
```

Sur la table entière, une réponse par colonne :

```python
sale.isna().sum()
```

**Réparez-le vous-même.** On veut garder les lignes où le volume n'est **pas** manquant. On a une Series de `bool` ; on en fait une colonne, et `query` sait filtrer sur une colonne.

```python
sale["manquant"] = sale["volume"].isna()
sans_trous = sale.query("manquant == False")
len(sale), len(sans_trous)
```

**L'aparté `if True`.** Une colonne de `bool`, c'est la liste des réponses qu'un `if` donnerait ligne par ligne. Un `if` accepte un booléen tout seul : `if True:` s'exécute toujours, `if False:` jamais. `query("manquant == False")`, c'est ce `if` fait sur chaque ligne d'un coup.

```python
if True:
    print("toujours")
if False:
    print("jamais")
```

**La fonction pandas.** `dropna` fait exactement ce que vous venez d'écrire, sans colonne intermédiaire.

```python
propre = sale.dropna(subset=["volume"])
len(propre)
```

`subset` dit sur quelle colonne regarder. Sans lui, une ligne avec un trou n'importe où serait retirée.

On note le nombre de lignes avant et après. On le fera à chaque étape : c'est ce qu'on rapporte à la fin.

**Prédire** sur `jouet2`, une version de `jouet` avec deux volumes manquants (cellule fournie) : `jouet2["volume"].isna()`, `jouet2["volume"].isna().sum()`, `len(jouet2.dropna(subset=["volume"]))`, `jouet2.dropna(subset=["volume"])["volume"].sum()`.

**Écrire** : sur `sale`, le nombre de lignes avec un volume manquant dans `nb_trous`, puis `net`, la table sans ces lignes, par la méthode de votre choix. Vérification : `len(net) == len(sale) - nb_trous`.

### D2.3 Doublons, 10 min

`duplicated()` pose une question à chaque ligne : « t'ai-je déjà vue plus haut ? ». Une Series de `bool`, encore.

```python
net.duplicated().sum()
```

**Réparez-le vous-même.** Même geste : une colonne, un `query`.

```python
net["doublon"] = net.duplicated()
sans_doublons = net.query("doublon == False")
len(net), len(sans_doublons)
```

**La fonction pandas.** Avant de l'appeler, on retire les deux colonnes de travail `manquant` et `doublon` en gardant les quatre colonnes de départ : sinon une ligne et sa copie ne sont plus identiques (`False` d'un côté, `True` de l'autre) et `drop_duplicates` ne voit plus rien. Le test de bout en bout l'a montré.

```python
net = net[["date", "coin", "close", "volume"]]
net = net.drop_duplicates()
len(net)
```

**Lire le code, dire la question** : `net.query("doublon == True")` (les doublons eux-mêmes, pour les regarder avant de supprimer).

**Écrire** : `sale2` est une copie de `sale`, fournie. Enlevez les doublons **puis** les lignes sans volume, et comparez le nombre final avec `net`. Identique : l'ordre des deux opérations ne change rien ici.

### D2.4 Texte vers nombre, 10 min

Texte : `close` est du texte. On ne peut rien calculer avec.

```python
net["close"].max()
```

Ça renvoie un texte, et le « maximum » de textes ne veut rien dire. En séance 1, on nettoyait un texte avec `replace` puis `float` :

```python
float("43 250,12 $".replace(" ", "").replace(",", ".").replace("$", ""))
```

Sur une colonne, même chose, avec une différence de syntaxe.

**Pourquoi `.str`.** `net["close"]` est une Series, pas un texte. Pour dire « applique la méthode de texte à chaque case », on écrit `.str` devant la méthode : `.str.replace(...)`. `.str` veut dire : traite chaque case comme une chaîne.

```python
texte = net["close"].str.replace(" ", "").str.replace(",", ".").str.replace("$", "")
texte.head(3)
```

Puis la conversion : `astype(float)`, la version colonne de `float()`.

```python
net["close"] = texte.astype(float)
net.info()
```

`close` est passé en `float64`. `net["close"].max()` a maintenant un sens.

**Prédire** sur `jouet3`, une version de `jouet` avec des prix en texte (cellule fournie) : `jouet3["close"].str.replace(" ", "")`, `jouet3["close"].str.replace(" ", "").str.replace(",", ".").astype(float).sum()`.

**Corriger** : `net["close"].replace(" ", "")` sans `.str` (pas d'erreur, rien ne change : on compare avant et après) ; `net["close"].astype(float)` avant d'avoir enlevé le `$` (`ValueError`, la dernière ligne cite la valeur fautive).

### D2.5 Le texte, c'est des catégories, 15 min

Texte : on vient de transformer du texte en nombres, parce que c'était des nombres mal écrits. Mais le plus souvent, le texte d'une table n'est pas un nombre déguisé. Dans une table d'analyse, une colonne de texte, c'est de deux choses l'une : une **date** (on s'en occupe à la section suivante), ou une **catégorie** : la monnaie, le pays, le secteur, le type de client. Ici, `coin` est une catégorie.

Et la première question qu'on pose à une catégorie, c'est : **combien de lignes par catégorie ?** C'est `value_counts`.

```python
crypto["coin"].value_counts()
```

Une Series : l'index, ce sont les catégories ; les valeurs, les effectifs, du plus fréquent au moins fréquent. On y lit que SOL a moins de jours : elle est apparue plus tard.

Les catégories elles-mêmes, et leur nombre :

```python
crypto["coin"].unique()
```

```python
crypto["coin"].nunique()
```

**Le texte incohérent.** La même chose sur le fichier sale :

```python
net["coin"].value_counts()
```

Vingt-huit catégories pour sept monnaies. Pour pandas, `"btc"` et `" BTC"` sont deux catégories, et chacune est sous-comptée. On répare avec `strip` et `upper`, en `.str`, comme en séance 1.

```python
net["coin"] = net["coin"].str.strip().str.upper()
net["coin"].value_counts()
```

Sept catégories. Le nettoyage d'une catégorie, c'est presque toujours ces deux méthodes.

**Prédire** sur `jouet` (4 cellules) : `jouet["coin"].value_counts()`, `jouet["coin"].nunique()`, `jouet["date"].value_counts()`, `jouet["coin"].str.lower().unique()`.

**Écrire** :

1. Combien de catégories `coin` avait-il dans `sale` avant nettoyage ? Dans `nb_avant`. Attendu : `28`.
2. Le volume moyen de BTC dans `net` nettoyé, dans `vol_btc`. Un `query` sur `coin`, qui ne marche que si le nettoyage est fait.

### D2.6 Dates, 10 min

`date` est du texte. On peut la comparer, on l'a fait en D1, mais on ne peut pas lui demander « quel mois ? ». `pd.to_datetime` la convertit en vraie date.

```python
net["date"] = pd.to_datetime(net["date"])
net.info()
```

Une fois convertie, `.dt` donne accès aux morceaux, comme `.str` donnait accès aux méthodes de texte.

```python
net["annee"] = net["date"].dt.year
net["mois"] = net["date"].dt.month
net.head(3)
```

`.dt.day` existe aussi ; l'exercice de synthèse s'en sert.

Même chose sur `crypto`, parce que la suite travaille dessus :

```python
crypto["date"] = pd.to_datetime(crypto["date"])
crypto["annee"] = crypto["date"].dt.year
```

**Écrire** : le nombre de lignes de `crypto` en 2021, dans `nb_2021`, avec la colonne `annee`. Puis le cours maximum de BTC en 2021, dans `btc_max_2021`. Attendus : `2555` et `67566.8281`.

### D2.7 Grouper, 30 min

Section à marteler, et la plus difficile du bloc. On y va pas à pas, sur `jouet` d'abord.

**La question.** « Le cours moyen de chaque monnaie. » Trois monnaies dans `jouet`, trois moyennes. Avec ce qu'on sait, on écrit un `query` par monnaie :

```python
jouet.query("coin == 'BTC'")["close"].mean()
```

Trois fois, sept fois sur le vrai fichier. Non : une boucle. La condition de `query` est un texte, donc on la fabrique avec une f-string, comme en séance 2.

```python
monnaies = ["BTC", "ETH", "SOL"]
moyennes = []
for m in monnaies:
    sous_table = jouet.query(f"coin == '{m}'")
    moyennes.append(sous_table["close"].mean())
pd.Series(moyennes, index=monnaies)
```

**Ce que fait la boucle**, dessiné. C'est le schéma à garder en tête, et il va dans une cellule texte, sous forme d'image ou de bloc HTML :

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

Trois temps : **découper** la table en une sous-table par valeur de la colonne choisie ; **calculer** une chose dans chaque sous-table ; **rassembler** les résultats dans une Series dont l'index est la catégorie.

**La ligne pandas.** `groupby` fait ces trois temps en une ligne.

```python
jouet.groupby("coin")["close"].mean()
```

Même résultat, à la ligne près. Lecture de gauche à droite, au tableau :

```
jouet.groupby("coin")["close"].mean()
│     │              │        │
│     │              │        └─ calculer : la moyenne dans chaque sous-table
│     │              └─ de la colonne close
│     └─ découper : une sous-table par valeur de coin
└─ la table
```

Le résultat est une **Series** : une valeur par groupe, l'index est le groupe. Tout ce qu'on sait faire sur une Series s'applique : `["ETH"]` pour un groupe, `sort_values`, `plot`.

**Sur le vrai fichier**, la même ligne :

```python
crypto.groupby("coin")["close"].mean()
```

**Ce qu'on met à la fin.** N'importe quelle fonction de colonne :

```python
crypto.groupby("coin")["close"].max()
```

```python
crypto.groupby("coin")["volume"].sum()
```

```python
crypto.groupby("coin")["close"].count()
```

`count` compte les lignes de chaque groupe : c'est `value_counts`, obtenu autrement.

**Grouper par autre chose.** Par année, avec la colonne créée en D2.6. Une catégorie, c'est n'importe quelle colonne qui prend peu de valeurs différentes.

```python
crypto.groupby("annee")["volume"].sum()
```

**Trier, aller chercher un groupe.**

```python
crypto.groupby("coin")["close"].mean().sort_values(ascending=False)
```

```python
crypto.groupby("coin")["close"].mean()["ETH"]
```

**Prédire** sur `jouet` (6 cellules) : `jouet.groupby("coin")["volume"].sum()`, `jouet.groupby("date")["volume"].sum()`, `jouet.groupby("coin")["close"].count()`, `jouet.groupby("coin")["close"].max().sort_values()`, `jouet.groupby("coin")["close"].mean()["ETH"]`, `jouet.groupby("coin")["close"].max() - jouet.groupby("coin")["close"].min()`.

Le dernier : deux Series avec le même index se soustraient étiquette par étiquette. L'amplitude de chaque monnaie, en une ligne.

**Lire le code, dire la question** (à l'oral) :

- `crypto.groupby("annee")["close"].max()`
- `crypto.query("coin == 'BTC'").groupby("annee")["close"].mean()`
- `crypto.groupby("coin")["annee"].min()`

La deuxième enchaîne un `query` puis un `groupby`. La troisième répond à « en quelle année chaque monnaie apparaît-elle ? ».

**Dire la question, écrire le code** (au tableau) : « le volume moyen par monnaie, du plus gros au plus petit » ; « le cours minimum de chaque année pour ETH ».

**Écrire** :

1. Le cours moyen de chaque monnaie en 2024, dans `moy_2024`. Un `query`, puis un `groupby`. Quelle monnaie est en tête ? Attendu : BTC à `65964.12`, puis ETH `3044.93`, BNB `543.25`, SOL `155.43`.
2. Le nombre de jours dans le fichier pour chaque monnaie, dans `nb_jours`, trié. Comparez avec `value_counts`. Attendu : `2335` pour SOL, `3165` pour les six autres.
3. Refaites `moy_2024` avec la boucle et les `query`, sans `groupby`, dans `moy_2024_boucle`. Vérification : les deux Series ont les mêmes valeurs à 0,01 près. Le but est de sentir que c'est la même chose.

**Corriger** : `crypto.groupby("coin").mean()` sans choisir de colonne (pas d'erreur, mais une table de moyennes de toutes les colonnes, date comprise : on choisit toujours la colonne) ; `crypto.groupby(annee)` sans guillemets (`NameError`).

### D2.8 Tracer, 5 min

Deux graphiques, deux lignes. Une Series de `groupby` se trace en barres :

```python
crypto.groupby("coin")["close"].mean().sort_values().plot(kind="bar")
```

Une évolution dans le temps se trace en courbe, en disant quelle colonne va en abscisse :

```python
crypto.query("coin == 'BTC'").plot(x="date", y="close")
```

**Écrire** : la courbe de ETH depuis 2023. Un `query` à deux conditions, puis `plot`.

### D2.9 Synthèse, 5 min

Le tableau « vous voulez / vous écrivez », sur une page. Les deux phrases du bloc. Et le paragraphe « ce que vous croiserez ailleurs » : `loc`, `iloc`, le masque entre crochets `df[df["col"] > 0]`, `merge`, `describe`, une ligne chacun, pour qu'ils les reconnaissent sans les avoir appris.

---

## 5. L'exercice de synthèse : 100 dollars par mois

> **Construit le 15 septembre 2026**, sous le titre « Assignment 2 : l'investissement programmé » — `pandas_crypto/assignment/investissement_programme.ipynb`, généré par `build/build_a2.py`, solutions dans `build/sol_a2.json`, valeurs de référence dans `data/valeurs_export.json`. Deux écarts avec la spécification ci-dessous. **(1)** Il part d'un export brut plein format, `crypto_export.csv` (construit par `data/build_export.py`), et commence par deux parties de diagnostic et de réparation : sans elles, l'exercice ne remobilisait que 30 des 120 minutes de D2 (ni le nettoyage, ni `groupby`). **(2)** Une partie « pourquoi ça marche » compare le prix moyen payé (28 258 $) au prix moyen du marché (49 051 $) et regroupe le bitcoin accumulé par année avec `groupby` — trois quarts viennent des trois années les moins chères. La partie « tout d'un coup » passe en bonus hors barème. Barème : 2 / 4 / 3 / 4 / 3 / 4. Durée visée : 60 à 75 min en classe, fin à la maison. Seule nouveauté hors cours : `.iloc[-1]`, présentée comme l'équivalent colonne de `liste[-1]`. Toutes les valeurs ci-dessous restent exactes sur la table nettoyée.

En classe, 45 minutes, puis correction. Sur le fichier propre `crypto.csv`, avec les dates converties. Même présentation que l'assignment Python : objectif d'ensemble, parties numérotées, indication guidée, cellule de vérification, point d'étape.

### 5.1 Ce que ça produit

La réponse à une question que tout le monde s'est posée : « si j'avais mis 100 dollars dans le bitcoin tous les mois depuis 2020, j'aurais combien aujourd'hui ? ». Puis la même chose pour les sept monnaies, dans un graphique en barres. Puis la comparaison avec « tout mettre d'un coup en janvier 2020 ».

Tout se fait avec `query`, `.dt`, l'arithmétique de colonnes, `sum`, `len`, une boucle avec `append` et une f-string, une Series et un `plot`. Rien de nouveau.

### 5.2 Énoncé, partie par partie

**Partie 0, fournie.** Setup, chargement, conversion de `date`, création de `annee`, `mois`, `jour`.

**Partie 1, le calendrier d'achat (3 points).** On achète le premier jour de chaque mois, à partir du 1er janvier 2020. Construisez `achats`, la table des lignes de BTC dont le jour est 1 et l'année au moins 2020. Un `query` à trois conditions reliées par `and`. Vérification : `len(achats)` vaut le nombre de mois écoulés, `80` (janvier 2020 à août 2026).

Point d'étape : chaque ligne de `achats` est un jour où l'on a acheté, et `close` est le prix payé ce jour-là.

**Partie 2, ce qu'on a acheté (4 points).** Avec 100 dollars à un prix `close`, on obtient `100 / close` bitcoins. Créez la colonne `achats["quantite"]`. Puis `total_btc`, la somme de la colonne, et `total_investi`, 100 fois le nombre d'achats. Vérifications : `total_investi == 100 * len(achats)` ; `total_btc` égal à la somme à 1e-9 près.

Point d'étape : on connaît le nombre de bitcoins accumulés et ce que ça a coûté. Il manque ce que ça vaut.

**Partie 3, ce que ça vaut aujourd'hui (3 points).** Le dernier cours de BTC du fichier, dans `dernier_prix`. Indication : `crypto.query("coin == 'BTC'").tail(1)["close"]`, ou le cours à la date maximale. Puis `valeur = total_btc * dernier_prix` et le gain en pourcentage. Affichez en f-string : `Investi : 8000 $. Valeur aujourd'hui : 22237.19 $. Gain : 178.0 %.` (0,283101 BTC au dernier cours de 78 548,63).

Point d'étape : la question est répondue pour BTC. Reste à savoir si c'était la bonne monnaie.

**Partie 4, les sept monnaies (6 points).** Une boucle sur la liste des monnaies. À chaque tour : le `query` à trois conditions pour cette monnaie, écrit avec une f-string comme en D2.7 ; la quantité ; le total ; le dernier prix de cette monnaie ; la valeur ; `append` de la valeur dans une liste. À la fin, `pd.Series(valeurs, index=monnaies).sort_values().plot(kind="bar")`. Attention à SOL, absente en janvier 2020 : `total_investi` diffère selon la monnaie, donc on compare des gains en pourcentage, chacun avec son propre investissement. La consigne le dit.

Vérification : sept valeurs, celle de BTC égale à celle de la partie 3. Gains attendus : SOL 1090 %, BNB 621 %, DOGE 472 %, BTC 178 %, XRP 161 %, ETH 151 %, ADA -17 %. SOL n'a que 76 achats.

Point d'étape : le graphique répond à « laquelle aurait-il fallu choisir ». On le commente en une phrase.

**Partie 5, tout d'un coup (4 points).** L'autre stratégie : le même montant total, `total_investi` de BTC, placé en une fois au premier jour d'achat de 2020. Le prix ce jour-là est la première ligne de `achats` : `achats.head(1)["close"]`. Quantité, valeur aujourd'hui, comparaison avec la partie 3. Laquelle des deux stratégies a le mieux marché sur BTC ? (8 000 $ au cours de 7 200,17 du 1er janvier 2020 valent 87 274,15 $ aujourd'hui, contre 22 237,19 en achats mensuels.) Deux lignes de texte pour répondre, et une pour dire pourquoi ce n'est pas une règle générale.

### 5.3 Barème et corrigé

20 points, répartis comme ci-dessus. Le corrigé de référence est à écrire ; les valeurs sont dans `valeurs_reference.json`. Les cellules `verifier` testent des relations (longueurs, égalités entre deux façons de calculer) et les quelques valeurs absolues qui ne dépendent que du fichier.

---

## 6. Ce que le bloc stats peut supposer acquis

- `pd.Series`, `pd.DataFrame` à partir de Series, `read_csv`, `shape`, `columns`, `info`, `head`, `tail`, `len`
- une colonne, plusieurs colonnes, créer une colonne, arithmétique de colonnes, `round`
- `sum`, `mean`, `max`, `min`, `count` sur une colonne
- une comparaison sur une colonne donne des `bool` ; `.sum()` compte, `.mean()` donne une part
- `query` avec les six comparaisons, `and`, `or`, `not`, `in`, une f-string pour une condition variable
- `isna`, `dropna(subset=)`, `duplicated`, `drop_duplicates`
- `.str.replace`, `.str.strip`, `.str.upper`, `astype(float)`
- `value_counts`, `unique`, `nunique`
- `to_datetime`, `.dt.year`, `.dt.month`, `.dt.day`
- `sort_values`, `groupby("col")["col"].fonction()`, soustraction de deux Series de même index
- `plot(kind="bar")`, `plot(x=, y=)`

Le bloc stats ouvre avec `describe`, l'histogramme, le nuage de points, `corr`, puis `pct_change` pour les rendements, présentés comme des nouveautés avec le même cycle.

---

## 7. Production

1. `pandas_crypto/data/build_data.py` : fait. `crypto.csv`, `crypto_sale.csv`, `valeurs_reference.json` sont dans le dépôt.
2. Valeurs de référence reportées dans ce plan : fait.
3. Image du schéma découper / calculer / rassembler pour D2.7, dans `ressources/img/` (pour l'instant en ASCII dans le notebook).
4. Notebooks D1 (162 cellules, 25 de prédiction) et D2 (150 cellules, 18 de prédiction) : faits, dans `pandas_crypto/cours/`, générés par `pandas_crypto/build/build_d*.py`, testés de bout en bout avec `run_nb.py` et `sol_d*.json`.
5. Notebook de synthèse, parties 0 à 5, `verifier` relationnels.
6. Corrections générées depuis les scripts.
7. Aide-mémoire pandas réduit à la liste de la section 6.
