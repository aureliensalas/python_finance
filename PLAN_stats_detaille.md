# Statistiques en 4h : plan détaillé, section par section

Suite de `PLAN_python_detaille.md` et `PLAN_pandas_detaille.md`. Même format : durée par section, texte du cours en quelques phrases, cellules de démonstration, exercices avec énoncé et valeur attendue, points de coupe.

Mêmes données que le bloc pandas : `crypto.csv`, propre, 21 325 lignes, sept monnaies, du 1er janvier 2018 au 31 août 2026. Un seul fichier ajouté, `rendements.csv`, pour la dernière section de S2 (voir 0). Toutes les valeurs de ce plan ont été calculées sur ces fichiers le 16 septembre 2026 et sont reportées en section 7.

---

## 0. Décisions prises

**Budget.** Deux séances de 2h, S1 et S2. Un travail noté ensuite, sur le budget révision, comme pour les deux blocs précédents.

**Le fil.** Le bloc répond à une seule question : *ce que je vois dans les données est-il réel, ou est-ce le hasard ?* S1 apprend à décrire ce qu'on voit. S2 apprend à en douter. Le bloc ML posera l'autre question — *est-ce que ça marche sur des données jamais vues ?* — avec son propre rituel, le découpage entraînement/test.

**Une règle d'écriture, tenue dans chaque section : une question, une réponse.** Les outils n'apparaissent que si la question les exige, et chaque interprétation est écrite en toutes lettres, pas laissée au lecteur. C'est ce qui a marché aux blocs 1 et 2, et c'est ce que la première version de ce plan avait perdu.

**La colonne qui manque : le rendement.** Un prix ne se compare pas ; un rendement si. C'est l'objet central de la finance quantitative, et c'est la première chose que S1 construit — en 15 minutes, pas plus. Tout le reste du bloc, et tout le bloc ML, travaille sur cette colonne.

**Le bootstrap, et comment on l'amène.** Le problème est réel : sur le bitcoin, on a *tous* les jours, alors que dans un sondage on n'a que 2 000 électeurs sur 47 millions. Dire « imaginez d'autres histoires possibles » ne convainc personne. On procède donc en deux temps. D'abord un **sondage simulé** où l'échantillonnage est incontestable. Puis le transfert **par les données** : le rendement moyen du bitcoin calculé par un analyste qui n'aurait vu qu'une seule année va de −62 % à +430 % par an selon l'année. Chacun de ces analystes a vu *un échantillon de jours de bitcoin* et s'est trompé. Nous en avons vu 3 164 : un échantillon plus grand, pas la totalité. La question « quel est le rendement du bitcoin ? » **porte sur l'actif, pas sur la fenêtre 2018-2026**. Ce n'est ni une prédiction ni un multivers : c'est une estimation, et une estimation a une épaisseur. Le bootstrap est l'outil qui la mesure quand on ne peut pas refaire le sondage.

**Le p-hacking reste, en 12 minutes.** Raison décisive : le test t sur « le bitcoin baisse-t-il le jeudi ? » donne **p = 0,030**, seul. Si la séance s'arrête là, l'étudiant repart avec une fausse croyance que le cours vient de confirmer. La section « chercher jusqu'à trouver » n'est pas un supplément méthodologique, c'est la correction de cette croyance. Si on la coupe, il faut abandonner tout le fil du jeudi et n'utiliser que BTC contre ETH (p = 0,82) — cohérent, mais on perd le seul moment où l'étudiant tombe lui-même dans le piège.

**Pas de `pivot_table`.** La corrélation entre monnaies demande la table large, une colonne par monnaie. Au lieu d'enseigner la transformation, on livre le fichier : `rendements.csv`, date puis sept colonnes. Un `read_csv` connu, un `.corr()` nouveau. On dit en une phrase qu'une même donnée s'arrange de deux façons — la longue pour `groupby`, la large pour `corr` — sans apprendre à passer de l'une à l'autre.

**Ce qu'on retire de l'ancien bloc 3.** Le **khi-deux** sort du temps de classe (bonus facultatif en fin de S2). **Spearman** sort. La **parabole** `x ** 2` sort : le krach du Covid porte déjà l'avertissement « ne croyez pas le coefficient », et il le porte mieux. La **moyenne pondérée** sort. La **régression `statsmodels`** sort entièrement : la régression n'apparaît qu'une fois, au bloc ML, avec `scikit-learn`.

**Doctrine de tracé.** Un graphique est une méthode appelée sur un résultat : `resultat.plot(...)`. **Jamais `plt.` dans une cellule étudiante.** `title=`, `xlabel=`, `ylabel=`, `figsize=` et `bins=` passent directement dans `.plot()` et couvrent tout le bloc. Au-delà, la cellule est fournie pré-codée. Deux graphiques sont démontrés en S1, pas quatre types : l'histogramme et les barres à deux colonnes.

**Nouveautés du bloc.** `shift`, `pct_change`, `describe`, `quantile`, `std`, `.agg([...])`, `sample(replace=True)`, `stats.ttest_ind`, `corr`. Neuf, et rien d'autre.

---

## 1. Les deux phrases du bloc

> **Un prix ne se compare pas. Un rendement, si.**

> **Une moyenne calculée sur des données n'est pas la vraie moyenne. C'est une estimation, et une estimation a une épaisseur.**

La première organise S1. La seconde organise S2.

---

## 2. Séance S1 (2h) : décrire le risque

| Section | Minutes | Cumul |
|---|---|---|
| S1.0 Échauffement | 10 | 10 |
| S1.1 La colonne qui manque | 15 | 25 |
| S1.2 À quoi ressemble une journée de bitcoin ? | 20 | 45 |
| S1.3 Et les autres ? `groupby` | 40 | 85 |
| S1.4 Voir | 20 | 105 |
| S1.5 La fiche d'identité d'une monnaie | 10 | 115 |
| S1.6 Synthèse | 5 | 120 |

Points de coupe si retard, dans l'ordre : S1.5 passe en devoir ; l'exercice 2 de S1.3 passe en devoir ; S1.4 garde l'histogramme seul.

### S1.0 Échauffement, 10 min

Setup identique aux blocs précédents, plus `from scipy import stats` — « on s'en servira à la séance suivante ». Chargement, conversion de la date, et **le tri**, expliqué en une phrase parce que toute la section suivante en dépend : on veut que les jours d'une même monnaie se suivent.

```python
crypto = pd.read_csv(BASE + "crypto.csv")
crypto["date"] = pd.to_datetime(crypto["date"])
crypto = crypto.sort_values(["coin", "date"]).reset_index(drop=True)
```

Deux cellules de reprise : un `query`, un `groupby("coin")["close"].mean()`.

### S1.1 La colonne qui manque, 15 min

**La question.** Le 31 août 2026, BTC vaut 78 548 $ et DOGE 0,21 $. Laquelle a fait la meilleure journée ? Pas de réponse tant qu'on regarde des prix : les échelles n'ont rien à voir. Il faut la variation **en pourcentage** par rapport à la veille. C'est le rendement, et c'est l'unité de compte de la finance.

**À la main, sur cinq lignes.**

```python
jouet = pd.DataFrame({"close": [100.0, 110.0, 99.0, 99.0, 148.5]})
```

Au tableau : +10 %, −10 %, 0 %, +50 %. La formule, que tout le monde sait écrire : `(aujourd'hui − hier) / hier × 100`. Il ne manque que le prix d'hier **sur la même ligne** qu'aujourd'hui.

**`shift`, la seule idée nouvelle.** Décaler la colonne d'un cran vers le bas.

```python
jouet["hier"] = jouet["close"].shift(1)
jouet
```

La première ligne vaut `NaN` : le premier jour n'a pas de veille. C'est juste, pas un bug.

**Ils écrivent le rendement.** Cellule vide, `verifier` sur les quatre valeurs.

```python
jouet["r"] = (jouet["close"] - jouet["hier"]) / jouet["hier"] * 100
```

**Le raccourci.** Comme `sum(flux)` après la boucle accumulateur du bloc 1 :

```python
jouet["close"].pct_change() * 100
```

Même colonne. `pct_change` fait le `shift`, la soustraction et la division. Le `* 100` reste à notre charge.

**Le piège.** Sur la vraie table, appliqué tel quel, puis **un seul réflexe : regarder le max.**

```python
crypto["r"] = crypto["close"].pct_change() * 100
crypto["r"].max()
```

**933 041 %.** Aucun actif n'a jamais fait ça en un jour. Quelque chose est faux, et rien ne le disait dans `head()`.

D'où ça vient : la table est triée par monnaie puis par date. À chaque changement de monnaie, `pct_change` compare le premier jour de l'une au dernier jour de l'autre. **Six lignes fausses sur 21 325**, invisibles à l'œil, catastrophiques dans un maximum.

> **L'erreur silencieuse du bloc.** Elle ne lève rien, elle ne se voit pas dans un aperçu, et elle se trouve en regardant les extrêmes. **Après avoir créé une colonne, on regarde son `max` et son `min` avant de s'en servir.**

**La correction.** `groupby`, réutilisé pour ce qu'il est — « fais le calcul séparément dans chaque groupe ».

```python
crypto["r"] = crypto.groupby("coin")["close"].pct_change() * 100
crypto["r"].max()
```

**354,67 %.** DOGE, le 28 janvier 2021, le jour où Reddit s'en est emparé. Vrai, vérifiable.

Puis `crypto = crypto.dropna(subset=["r"])`. Attendu : 21 318 lignes, sept premiers jours en moins.

### S1.2 À quoi ressemble une journée de bitcoin ?, 20 min

**Une seule question, et une réponse qui surprend.** On isole le bitcoin et on demande son rendement moyen.

```python
btc = crypto.query("coin == 'BTC'")
btc["r"].mean()
```

**+0,111 % par jour.** Est-ce que ça décrit une journée de bitcoin ? On va voir que non.

**`describe`, pour tout voir d'un coup.** Première apparition, et on lit les huit nombres ensemble.

```python
btc["r"].describe()
```

**Trois interprétations, chacune écrite en toutes lettres.**

*La moyenne n'est pas le milieu.* Médiane +0,063 %, moyenne +0,111 % : la moyenne fait presque le double. Quelques très gros jours de hausse la tirent vers le haut. **La médiane dit ce que fait un jour ordinaire ; la moyenne dit ce que fait le portefeuille sur la durée.** Deux questions différentes, deux nombres différents, et on aura besoin des deux.

*L'écart-type, c'est le risque — et il écrase la tendance.* 3,33 %. En finance, `std` n'est pas un indicateur technique : **c'est la définition du risque.** Et le rapport entre les deux nombres est la phrase à retenir de la section :

> **La tendance est de +0,11 % par jour. Le bruit est de ±3,3 %. Le bruit est trente fois plus grand que la tendance.** Une journée de bitcoin, ce n'est pas +0,11 % : c'est n'importe quoi entre −3 % et +3 %, avec une infime dérive vers le haut qu'on ne peut pas sentir au jour le jour. C'est pour ça que la séance suivante parlera d'incertitude.

*Le quantile 5 %, c'est le mauvais jour habituel.*

```python
btc["r"].quantile(0.05)
```

**−5,02 %.** Un jour sur vingt, le bitcoin perd plus de 5 %. Sur 10 000 € placés, 500 € partis dans la journée, à peu près une fois par mois. On dit le nom : c'est une **Value at Risk** à 95 %, l'indicateur que toute salle de marché calcule chaque soir — et ils viennent de l'obtenir par une méthode, sans formule.

**Exercice.** La même chose pour ETH : moyenne, médiane, écart-type, quantile 5 %.
Attendus : +0,13 %, +0,06 %, 4,37 %, −6,59 %. **Et la phrase** : ETH rapporte un peu plus que BTC et fait perdre plus les mauvais jours — c'est le premier arbitrage rendement-risque, et il revient tout de suite.

### S1.3 Et les autres ? `groupby`, 40 min

**La section la plus longue, et c'est voulu.** Toutes les questions intéressantes sur un jeu de données financier sont des questions **par groupe**, et ils ont déjà l'outil. On le pousse.

Rappel de la forme en une ligne : `table.groupby("ce qui groupe")["ce qu'on résume"].fonction()`.

**Question 1 — quelle monnaie rapporte, et laquelle fait peur ?** Trois cellules qui s'enchaînent naturellement.

```python
crypto.groupby("coin")["r"].mean().sort_values()
```

```python
crypto.groupby("coin")["r"].std().sort_values()
```

Et les deux d'un coup — **`.agg`, seule nouveauté de la section** : une liste de noms de fonctions à la place d'un appel.

```python
crypto.groupby("coin")["r"].agg(["mean", "std"])
```

| coin | rendement | risque |
|---|---|---|
| BTC | 0,11 | **3,33** |
| ETH | 0,13 | 4,37 |
| BNB | 0,25 | 4,78 |
| SOL | 0,39 | 6,19 |
| DOGE | **0,32** | **8,93** |

> **L'interprétation, et elle est la leçon centrale de la séance.** Classez par rendement, puis par risque : c'est presque le même ordre. BTC rapporte le moins et bouge le moins ; DOGE et SOL rapportent le plus et bougent le plus. **On ne gagne pas plus sans accepter de perdre plus.** Ce n'est pas une règle du cours, c'est ce que les données disent, et ils viennent de le lire dans deux colonnes.

Le résultat est une **DataFrame à deux colonnes** — on le note, S1.4 s'en servira.

**Question 2 — le marché se calme-t-il ?** On groupe par une colonne qu'on fabrique.

```python
crypto["annee"] = crypto["date"].dt.year
crypto.groupby("annee")["r"].std()
```

2018 : 6,54 %. 2021 : **10,55 %**. 2023 : 3,60 %. 2026 : 3,23 %. Oui, il se calme — sauf 2021, qui dépasse tout.

**Et pourquoi 2021 ?** On regarde les extrêmes, réflexe de S1.1.

```python
crypto.query("annee == 2021").nlargest(3, "r")[["date", "coin", "r"]]
```

Le +354 % de DOGE. On le retire par la pensée : la volatilité 2021 tombe à **7,89 %**.

> **Un jour sur 2 555 a déplacé l'écart-type de l'année de 25 %.** C'est la propriété la plus traître de l'écart-type : il donne un poids énorme aux extrêmes. **On ne commente jamais un écart-type sans avoir regardé ce qu'il y a dedans.**

**Question 3 — y a-t-il un jour de la semaine à éviter ?** On prépare S2 sans le dire.

```python
crypto["jour_sem"] = crypto["date"].dt.dayofweek
btc = crypto.query("coin == 'BTC'")
btc.groupby("jour_sem")["r"].mean()
```

Lundi +0,313 %, jeudi **−0,253 %**. Plus d'un demi-point par jour d'écart : annualisé, c'est énorme. On pose la question — **le bitcoin baisse-t-il le jeudi ?** — et **on ne répond pas**. On saura à la fin de la prochaine séance.

**Exercice 1 — la part de jours de hausse par monnaie.** Indication : une comparaison sur une colonne donne des booléens, et la moyenne de booléens est une part (bloc pandas).

```python
crypto["hausse"] = crypto["r"] > 0
crypto.groupby("coin")["hausse"].mean()
```

Attendus : BNB 52,0 %, BTC 51,0 %, ETH 50,9 %, SOL 49,6 %, XRP 48,6 %, ADA 48,4 %, **DOGE 39,9 %**.

> **À commenter en classe : c'est le plus beau résultat de la séance.** DOGE ne monte que quatre jours sur dix — le pire des sept — et affiche pourtant le deuxième rendement moyen. Il monte rarement, et énormément quand il monte. Moyenne et médiane, S1.2 : elles ne racontent pas la même histoire, et c'est la médiane qui dit la vérité du quotidien. Un étudiant qui aurait acheté du DOGE sur son rendement moyen aurait passé six jours sur dix à perdre.

**Exercice 2 — le pire jour de chaque monnaie.** `groupby("coin")["r"].min()`.
Attendu : six des sept entre −37 % et −42,4 %. Et une question laissée ouverte : sont-ils tombés le même jour ? Réponse en S2.

### S1.4 Voir, 20 min

**La règle, en une phrase.** Un graphique est une **méthode appelée sur un résultat** — une colonne ou un `groupby`. On écrit `resultat.plot(...)`, et rien d'autre. Trois arguments pour habiller : `title=`, `xlabel=` ou `ylabel=`, `figsize=`. **Jamais `plt.`**

**Graphique 1 — la forme d'une journée.** L'histogramme des rendements du bitcoin, et c'est le graphique le plus important du bloc.

```python
btc["r"].plot(kind="hist", bins=60, title="Rendements quotidiens du bitcoin", xlabel="% par jour", figsize=(8, 4))
```

On lit ensemble. Une cloche, centrée à peine au-dessus de zéro : la tendance de S1.2, invisible. Large : le bruit de S1.2. Et **deux queues longues et fines**, à gauche jusqu'à −37 %, à droite jusqu'à +19 %.

**Compter ce qu'il y a dans les queues.**

```python
(btc["r"].abs() > 3 * btc["r"].std()).sum()
```

**62 jours** au-delà de trois écarts-types. Si les rendements suivaient la cloche parfaite qu'on apprend en cours de maths, on en attendrait **8,5**. Sept fois trop.

> **Les marchés ne sont pas gaussiens.** Les journées extrêmes sont beaucoup plus fréquentes que la cloche ne le prédit, et toujours plus violentes à la baisse. C'est pour ça que les modèles de risque se trompent tous dans le même sens : ils sous-estiment le pire. Retenez l'image : la cloche est là, mais ses queues sont grasses.

**Graphique 2 — rendement et risque côte à côte.** Deux séries sur un graphique, ce n'est pas deux appels : c'est **une DataFrame à deux colonnes**, et S1.3 l'a déjà produite.

```python
crypto.groupby("coin")["r"].agg(["mean", "std"]).sort_values("std").plot(kind="bar", figsize=(9, 4), title="Rendement et risque par monnaie")
```

L'arbitrage de S1.3 devient une image : les barres montent ensemble.

**Les autres graphiques**, dans un tableau, sans démonstration : `kind="bar"` pour comparer des catégories (déjà vu), `kind="line"` pour suivre dans le temps, `kind="scatter"` avec `x=` et `y=` pour relier deux colonnes. Ils serviront au bloc ML.

**Exercice.** L'histogramme des rendements de DOGE, même habillage. Attendu : une cloche beaucoup plus large que celle de BTC, et une queue droite qui part très loin. Une phrase de comparaison avec le graphique 1.

### S1.5 La fiche d'identité d'une monnaie, 10 min

**Exercice de synthèse**, cellule vide, tout ce qui précède. Pour la monnaie de leur choix, produire et afficher en f-strings :

- le rendement moyen et la médiane ;
- l'écart-type ;
- la VaR à 95 % ;
- la part de jours de hausse ;
- le pire jour et sa date.

C'est ce qu'un analyste produit quand on lui demande « parle-moi de cet actif ». Cinq nombres, et ils savent maintenant ce que chacun veut dire.

### S1.6 Synthèse, 5 min

Tableau « Vous voulez... / Vous écrivez », et trois réflexes :

1. **Un prix ne se compare pas, un rendement si.**
2. **Après avoir créé une colonne, regardez son `max` et son `min`.**
3. **Jamais un écart-type sans regarder ce qu'il y a dedans.** Un seul jour a déplacé celui de 2021 de 25 %.

---

## 3. Séance S2 (2h) : comparer, et douter

| Section | Minutes | Cumul |
|---|---|---|
| S2.0 Échauffement | 10 | 10 |
| S2.1 Une moyenne a une épaisseur | 30 | 40 |
| S2.2 L'intervalle de confiance | 15 | 55 |
| S2.3 Comparer deux groupes : le test t | 20 | 75 |
| S2.4 Significatif ne veut pas dire important | 10 | 85 |
| S2.5 Chercher jusqu'à trouver | 12 | 97 |
| S2.6 Sept monnaies, un seul actif ? | 15 | 112 |
| S2.7 Synthèse | 5 | 117 |

Trois minutes de marge. Points de coupe : S2.4 fusionne dans S2.3 ; l'exercice de S2.2 passe en devoir.

### S2.0 Échauffement, 10 min

Setup, et la colonne `r` reconstruite en trois cellules **avec le `groupby`** — on réinstalle le piège dans les doigts. Puis la question laissée ouverte, réaffichée :

```python
btc.groupby("jour_sem")["r"].mean()
```

**Le bitcoin baisse-t-il le jeudi ?** Lundi +0,313 %, jeudi −0,253 %. Vote à main levée. On y revient à la fin.

### S2.1 Une moyenne a une épaisseur, 30 min

**Premier temps — le sondage, là où c'est évident.** Une élection : 100 000 électeurs, 52 % pour A. Personne n'interroge les 100 000 ; on en sonde 2 000.

```python
electeurs = pd.Series(np.random.default_rng(0).random(100_000) < 0.52).astype(int)
electeurs.mean()
```

52,1 %. C'est la vérité, qu'on ne connaît jamais en vrai. Maintenant un sondage :

```python
electeurs.sample(2000, random_state=0).mean()
```

**49,5 %.** Le sondage donne A perdant. Un deuxième, `random_state=1` : 51,0 %. Un troisième : 50,7 %. **Le résultat du sondage dépend de qui on a interrogé**, et personne dans la salle ne conteste que c'est de l'incertitude. C'est *l'incertitude d'échantillonnage*.

Mille sondages, avec la boucle du bloc 1 :

```python
resultats = []
for i in range(1000):
    resultats.append(electeurs.sample(2000, random_state=i).mean() * 100)

pd.Series(resultats).plot(kind="hist", bins=40, title="1000 sondages de 2000 personnes", xlabel="% pour A")
```

De 48,5 % à 55,2 %. **42 sondages sur 1 000 donnent A perdant** alors qu'il a 52 %. Voilà à quoi ressemble l'épaisseur d'une moyenne.

**Deuxième temps — le transfert, par les données.** « Sur le bitcoin, on a tous les jours. Où est l'échantillon ? » On ne répond pas par la philosophie, on fait un `groupby`.

```python
btc.groupby("annee")["r"].mean()
```

| année | par jour | par an |
|---|---|---|
| 2018 | −0,264 % | **−62 %** |
| 2020 | +0,458 % | **+430 %** |
| 2022 | −0,226 % | **−56 %** |
| 2025 | +0,006 % | +2 % |

> Un analyste qui n'aurait eu que 2020 aurait écrit que le bitcoin rapporte 430 % par an. Un autre, avec 2022 seulement, qu'il en perd 56. **Chacun a vu un échantillon de jours de bitcoin, et chacun s'est trompé** — exactement comme le sondage à 49,5 %.
>
> Nous en avons vu 3 164. C'est un échantillon plus grand, donc meilleur. Ce n'est pas la totalité : la question « quel est le rendement du bitcoin ? » **porte sur l'actif, pas sur la fenêtre 2018-2026**. La fenêtre est ce qu'on a pu observer de lui. On ne prédit rien ; on reconnaît que notre moyenne est une estimation, et qu'une estimation a une épaisseur.

**Troisième temps — mesurer l'épaisseur quand on ne peut pas refaire le sondage.** Pour les électeurs, on a re-tiré dans la population. Pour le bitcoin, on n'a pas la population : on n'a que nos 3 164 jours. Le remède est de **tirer dans ces 3 164 jours, avec remise** — c'est la façon standard d'imiter un tirage dans la population plus grande dont ils viennent.

```python
btc["r"].sample(5, replace=True, random_state=0)
```

Pourquoi avec remise : sans elle, tirer 3 164 valeurs parmi 3 164 redonne les mêmes dans le désordre, donc toujours la même moyenne, donc aucune information. L'erreur volontaire, `btc["r"].sample(5000)`, le montre en une ligne : `ValueError: Cannot take a larger sample than population when 'replace=False'`.

La boucle, identique à celle du sondage :

```python
moyennes = []
for i in range(1000):
    moyennes.append(btc["r"].sample(len(btc), replace=True, random_state=i).mean())

boot = pd.Series(moyennes)
boot.plot(kind="hist", bins=40, title="1000 moyennes possibles du bitcoin", xlabel="% par jour")
```

> On dit le nom : **bootstrap**. C'est un outil pour **voir** l'incertitude, pas une technique à maîtriser. Personne ne vous demandera jamais de choisir un nombre de tirages.

### S2.2 L'intervalle de confiance, 15 min

On garde les 95 % centraux — les quantiles de S1.2.

```python
bas, haut = boot.quantile(0.025), boot.quantile(0.975)
```

**+0,0032 % à +0,2231 % par jour.** Puis la cellule qui fait la séance : on annualise les deux bornes.

```python
((1 + bas / 100) ** 365 - 1) * 100, ((1 + haut / 100) ** 365 - 1) * 100
```

**+1 % à +126 % par an.**

> Huit ans et demi de données, 3 164 jours, et voilà tout ce qu'on sait du rendement du bitcoin : quelque part entre un livret d'épargne et un doublement annuel. **L'intervalle ne contient pas zéro** — le rendement est bien positif — et il est **inutilisable pour décider quoi que ce soit**. Retenez ce double constat, il revient dans deux sections.

Comment on le dit : « compte tenu de ce qu'on a observé, les valeurs plausibles vont de X à Y ». Une fourchette de plausibilité.

**Exercice.** Le même intervalle pour ETH. Attendu : [−0,023 % ; +0,278 %], qui **contient zéro**. Une phrase : avec ETH, on ne peut même pas affirmer que le rendement moyen est positif.

### S2.3 Comparer deux groupes : le test t, 20 min

**La question de finance la plus fréquente est une comparaison.** Deux moyennes, chacune avec son épaisseur : sont-elles vraiment différentes ?

On commence par une comparaison où la réponse est claire : BTC contre ETH.

```python
eth = crypto.query("coin == 'ETH'")
stats.ttest_ind(btc["r"], eth["r"], equal_var=False)
```

**p = 0,82.**

**Lire une p-value, en une phrase et une seule :**

> Si les deux groupes venaient en réalité de la même population, quelle serait la probabilité d'observer un écart au moins aussi grand, par le seul hasard de l'échantillon ? Ici 82 % : un écart pareil n'aurait rien de surprenant. **On ne peut pas distinguer BTC de ETH.**

Petite p-value : l'écart serait surprenant s'il n'y avait rien. Grande : il n'aurait rien de surprenant. **Ce n'est pas la probabilité que l'hypothèse soit vraie** — on le dit, parce que c'est l'erreur universelle. Le seuil de 5 % est une convention, pas une loi.

**Maintenant la vraie question : le jeudi.**

```python
jeudi = btc.query("jour_sem == 3")["r"]
autres = btc.query("jour_sem != 3")["r"]
stats.ttest_ind(jeudi, autres, equal_var=False)
```

**p = 0,030.** Sous le seuil. « Significatif. »

On laisse le résultat à l'écran et on demande à la salle : **alors, on vend le mercredi soir ?** On ne répond pas encore. Deux sections avant de trancher.

### S2.4 Significatif ne veut pas dire important, 10 min

Retour sur S2.2, les deux lectures côte à côte.

| BTC | |
|---|---|
| L'intervalle contient-il zéro ? | Non |
| Donc « significatif » ? | Oui |
| Peut-on en faire quelque chose ? | **Non** : de +1 % à +126 % par an |

> **Significatif** répond à « peut-on distinguer cet écart du bruit ? ». **Important** répond à « cet écart change-t-il une décision ? ». Deux questions différentes, et seule la seconde intéresse celui qui met de l'argent.

Le complément : avec assez de données, **n'importe quel écart devient significatif**. La p-value mesure autant la taille de l'échantillon que la taille de l'effet. Trois mille jours, c'est beaucoup.

### S2.5 Chercher jusqu'à trouver, 12 min

**L'intuition en trois phrases.** Un test au seuil de 5 % se trompe une fois sur vingt quand il n'y a rien à trouver. Lancez vingt tests sur du bruit pur : vous attendez une fausse découverte. Elle sera indiscernable d'une vraie.

**La vérification, cellule fournie, ils l'exécutent.** Sept monnaies, cinq jours ouvrés : trente-cinq tests.

```python
trouves = []
for m in ["BTC", "ETH", "SOL", "DOGE", "XRP", "BNB", "ADA"]:
    for j in range(5):
        a = crypto.query(f"coin == '{m}' and jour_sem == {j}")["r"]
        b = crypto.query(f"coin == '{m}' and jour_sem != {j}")["r"]
        if stats.ttest_ind(a, b, equal_var=False).pvalue < 0.05:
            trouves.append((m, j))
trouves
```

**Quatre résultats significatifs sur 35.** Le hasard seul en prédisait 1,75. Et lesquels : ADA jeudi, BTC jeudi, ETH jeudi, BNB vendredi. **Le jeudi sort trois fois.** Ça ressemble à une découverte.

> **Le jeudi de S2.3 était l'un de ces quatre.** On l'a trouvé parce qu'on a regardé sept jours de sept monnaies avant de choisir lequel tester. Le seuil de 5 % vaut pour **un** test décidé **avant** de regarder les données. Il ne vaut rien pour le meilleur de trente-cinq. **Chercher jusqu'à trouver finit toujours par trouver.**

**On tranche.** Non, le bitcoin ne baisse pas le jeudi. Le seul résultat qui le suggère est celui qu'on a obtenu en fouillant, et c'est exactement celui qui ne compte pas. Et même en le prenant au sérieux, S2.2 a montré que l'écart serait noyé dans l'épaisseur de chaque moyenne.

### S2.6 Sept monnaies, un seul actif ?, 15 min

**La question.** Un étudiant détient les sept cryptomonnaies du fichier. Il se croit diversifié. L'est-il ?

**Le fichier large.** Pour comparer les monnaies jour par jour, il faut les avoir **côte à côte**, une colonne chacune. C'est la même donnée, arrangée autrement : le format long de `crypto.csv` est celui de `groupby` ; le format large est celui de la corrélation. On livre le fichier, on ne fabrique pas la transformation.

```python
rendements = pd.read_csv(BASE + "rendements.csv")
rendements.head()
```

**`corr`, et c'est la seule nouveauté.**

```python
rendements.drop(columns="date").corr().round(2)
```

| | BTC | ETH | DOGE |
|---|---|---|---|
| BTC | 1,00 | **0,82** | 0,41 |
| ETH | 0,82 | 1,00 | 0,39 |

Corrélation moyenne entre paires : **0,53**. BTC-ETH : 0,82.

> **La réponse : non.** Sept monnaies à 0,53 de corrélation moyenne, ce n'est pas sept actifs, c'est à peu près un seul actif acheté sept fois. **La diversification ne se compte pas en lignes de portefeuille, elle se mesure à ce que les lignes font ensemble.**

**Et la démonstration qui cloue — la question laissée ouverte à l'exercice 2 de S1.3.** Les pires jours sont-ils tombés le même jour ?

```python
crypto[crypto["date"] == "2020-03-12"][["coin", "r"]]
```

**12 mars 2020**, krach du Covid : ETH −42,3 %, BNB −41,9 %, ADA −39,4 %, BTC −37,2 %, XRP −32,9 %, DOGE −31,8 %.

> **Toutes ensemble, le même jour.** La corrélation moyenne de 0,53 est un chiffre calme. Le jour où l'on aurait eu besoin que les monnaies se compensent, elles sont tombées à l'unisson. **La corrélation grimpe exactement quand on voudrait qu'elle baisse.** C'est la propriété la plus désagréable des marchés, et la plus constante — et c'est la raison de ne jamais se fier à un coefficient sans regarder ce qui se passe dans les pires jours.

### S2.7 Synthèse, 5 min

Tableau « Vous voulez... / Vous écrivez », et quatre phrases :

1. **Une moyenne a une épaisseur.** Toujours la fourchette, jamais le point seul.
2. **Une p-value dit « surprenant s'il n'y avait rien », pas « probablement vrai ».**
3. **Significatif ≠ important.** Regardez la taille de l'effet.
4. **Le seuil de 5 % vaut pour un test décidé à l'avance.** Pas pour le meilleur de trente-cinq.

---

## 4. Le bonus facultatif : le khi-deux

En fin de notebook S2, dans la forme du bonus convertisseur du bloc 1 : **facultatif, non noté, rien n'en dépend, on n'y touche pas en classe.**

Environ 20 minutes chez soi : `pd.cut` pour découper le rendement de BTC en trois tranches (baisse, stable, hausse), `pd.crosstab` pour croiser avec le jour de semaine, `stats.chi2_contingency` pour tester. **Le test rejette massivement (p ≈ 10⁻²²)** — et c'est la leçon : la dépendance existe, mais ce n'est pas celle qu'on cherchait. Les proportions par ligne montrent que le week-end est beaucoup plus calme (60 % de jours « stables » le samedi contre un tiers en semaine). Le jour de la semaine change l'agitation, pas la direction. Sur les cinq jours ouvrés seuls, p = 0,063 : le jeudi ne se distingue pas. Un test qui rejette ne confirme pas l'hypothèse qu'on avait en tête ; il dit qu'il y a quelque chose, et c'est souvent autre chose.

---

## 5. Ce que le bloc ML peut supposer acquis

- la colonne de rendement : `shift`, `pct_change`, et le `groupby` obligatoire avant ; le réflexe `max` / `min` après création
- `describe`, `mean`, `median`, `std`, `quantile`, et leurs interprétations financières : risque, VaR, bruit contre tendance
- `groupby` avec `.agg([...])`, groupement par colonne fabriquée
- `plot` avec `kind="hist"` et `kind="bar"`, `title=` / `xlabel=` / `ylabel=` / `figsize=` / `bins=` ; `line` et `scatter` connus de nom
- `sample(n, replace=True, random_state=)` et la boucle de rééchantillonnage ; l'intervalle par quantiles
- `stats.ttest_ind` et la lecture d'une p-value
- `corr` sur une table large
- les trois réflexes de méfiance : l'épaisseur d'une estimation, significatif contre important, le coût des tests répétés

Le bloc ML ouvre sur le découpage entraînement/test, présenté comme **le rituel jumeau** de l'intervalle de confiance.

---

## 6. Ce qu'on ne fait pas, et pourquoi

| Écarté | Raison |
|---|---|
| Khi-deux en classe | Jamais utilisé en finance ; coûte `pd.cut` + `crosstab`. Bonus. |
| Spearman | Le nuage de points diagnostique la même chose sans vocabulaire neuf. |
| La parabole `x ** 2` | Rien n'en dépend ; le krach du Covid porte mieux l'avertissement. |
| `pivot_table` | Le fichier large est livré. |
| Régression `statsmodels` | Une seule régression, au bloc ML, avec `scikit-learn`. |
| Moyenne pondérée | Cas particulier sans usage dans la suite. |
| `plt.` dans les cellules étudiantes | Tout passe par `.plot()`. |
| Quatre types de graphiques démontrés | Deux suffisent ; les autres sont nommés. |

---

## 7. Valeurs de référence

Calculées sur `crypto.csv` le 16 septembre 2026, rendements en %, `groupby("coin")` avant `pct_change`, 21 318 lignes après `dropna`.

**Par monnaie** — rendement moyen / écart-type / minimum / part de jours de hausse : ADA 0,10 / 5,39 / −39,39 / 48,4 · BNB 0,25 / 4,78 / −41,90 / 52,0 · BTC 0,11 / 3,33 / −37,17 / 51,0 · DOGE 0,32 / 8,93 / −40,25 / **39,9** · ETH 0,13 / 4,37 / −42,35 / 50,9 · SOL 0,39 / 6,19 / −42,28 / 49,6 · XRP 0,12 / 5,38 / −42,33 / 48,6. Maximum : DOGE **+354,67 %** le 28 janvier 2021.

**Bitcoin** — médiane +0,063 % ; quantile 5 % **−5,02 %** ; quantile 1 % −9,73 % ; **62 jours** au-delà de 3 écarts-types contre 8,5 attendus sous une loi normale. ETH : quantile 5 % −6,59 %.

**Le piège de S1.1** — sans `groupby` : 6 lignes fausses, maximum apparent **933 041 %**.

**Par année, BTC, rendement moyen par jour** — 2018 −0,264 · 2019 +0,242 · 2020 **+0,458** · 2021 +0,216 · 2022 **−0,226** · 2023 +0,283 · 2024 +0,256 · 2025 +0,006 · 2026 −0,014. Annualisé : de **−62 %** à **+430 %**.

**Volatilité par année, toutes monnaies** — 2018 6,54 · 2019 4,05 · 2020 5,72 · 2021 **10,55** · 2022 4,75 · 2023 3,60 · 2024 4,04 · 2025 4,23 · 2026 3,23. Sans le jour DOGE, 2021 : **7,89**.

**Jour de semaine, BTC** — lundi +0,313 · mardi −0,014 · mercredi +0,335 · jeudi **−0,253** · vendredi +0,228 · samedi +0,148 · dimanche +0,022.

**Sondage simulé** — 100 000 électeurs à 52,1 % ; sondages de 2 000, `random_state=0,1,2` : 49,5 / 51,0 / 50,7 % ; 1 000 sondages : de 48,5 à 55,2 %, **42 donnent A sous 50 %**.

**Bootstrap, 1 000 tirages, `random_state=i`** — BTC : **[+0,0032 % ; +0,2231 %]** par jour, **[+1 % ; +126 %]** par an. ETH : [−0,023 % ; +0,278 %], contient zéro.

**Tests t** — BTC contre ETH : **p = 0,82**. BTC jeudi contre autres jours : **p = 0,030**.

**Tests répétés** — 35 tests, **4 significatifs** (ADA jeudi, BNB vendredi, BTC jeudi, ETH jeudi), attendu par hasard 1,75.

**Corrélations** — sur les 3 164 jours du fichier large (SOL manquant avant avril 2020, `corr` l'ignore paire par paire) : moyenne entre paires **0,53**, minimum 0,25 (SOL-DOGE), maximum **0,82** (BTC-ETH).

**12 mars 2020** — ETH −42,3 · BNB −41,9 · ADA −39,4 · BTC −37,2 · XRP −32,9 · DOGE −31,8.

---

## 8. Production

1. `stats_crypto/data/build_rendements.py` → `rendements.csv` : date en première colonne, sept colonnes de rendements en %, 3 164 lignes (SOL vide avant avril 2020). Déterministe, à partir de `crypto.csv`. **Fait.**
2. `stats_crypto/build/build_s1.py` → `stats_crypto/cours/seance1_cours.ipynb`, avec `sol_s1.json`.
3. `stats_crypto/build/build_s2.py` → `stats_crypto/cours/seance2_cours.ipynb`, avec `sol_s2.json`, bonus khi-deux en fin.
4. `run_nb.py` recopié, les deux notebooks testés de bout en bout.
5. Valeurs de la section 7 dans `stats_crypto/data/valeurs_reference.json`.
6. Travail noté du bloc, à spécifier ensuite. Piste : la fiche de risque d'un portefeuille de deux ou trois monnaies, avec le test de sa diversification.
