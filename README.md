<img src="https://cdn.jsdelivr.net/gh/aureliensalas/python_finance@main/ressources/img/logo_macmia.png" alt="Logo" width="520">

# Data Camp Finance 2026/2027

Initiation à Python, à l'analyse de données et au machine learning pour des étudiants en finance — **20 heures**.

> ⚠️ À l'ouverture de chaque notebook : **Fichier → Enregistrer une copie dans Drive**, *avant* de taper quoi que ce soit. Sinon votre travail est perdu à la fermeture de l'onglet.

> 📱 **Vous travaillez sur tablette ?** Lisez d'abord **[Bien démarrer](ressources/setup_tablette.md)**. Cinq minutes de réglages vous éviteront la plupart des blocages.

---

## Le programme

| Bloc | Sujet | Heures |
|---|---|---|
| 1 | Python | 4h |
| 2 | Manipuler des données avec pandas | 4h |
| 3 | Décrire et relier des données | 4h |
| 4 | Introduction au machine learning | 4h |
| — | Travaux notés et révisions | 4h |

Rien à installer : tout se passe dans **Google Colab**, qui exécute le code sur les serveurs de Google. Il vous faut un compte Google et un navigateur.

---

## Bloc 1 — Python (4h)

Une séance de 2h, en un seul notebook. Il contient les exercices : on montre une notion, vous la refaites aussitôt. La **correction** est publiée après la séance.

| Séance | Sujet | Cours | Correction |
|---|---|---|---|
| 1 | Python — expressions, types, variables, fonctions, chaînes, booléens, `if`, listes, `for`, Series | [▶](https://colab.research.google.com/github/aureliensalas/python_finance/blob/main/python/cours/python_cours.ipynb) | *après la séance* |

### Travail noté — le simulateur de prêt

Lancé en classe, terminé à la maison. À partir de trois champs de formulaire et du taux directeur de la Banque centrale européenne du jour : une mensualité, un verdict d'acceptation, un tableau d'amortissement sur 240 mois, la courbe du capital restant dû et le coût du crédit.

| Sujet | Énoncé | Correction |
|---|---|---|
| Le simulateur de prêt | [▶](https://colab.research.google.com/github/aureliensalas/python_finance/blob/main/python/assignment/simulateur_pret.ipynb) | *après le rendu* |

---

## Bloc 2 — Manipuler des données avec pandas (4h)

Deux séances de 2h, sur huit ans et demi de cours quotidiens de cryptomonnaies.

| Séance | Sujet | Cours | Correction |
|---|---|---|---|
| 2.1 | Des Series à la table — charger, calculer, filtrer, trier | [▶](https://colab.research.google.com/github/aureliensalas/python_finance/blob/main/pandas_crypto/cours/seance1_cours.ipynb) | *après la séance* |
| 2.2 | Nettoyer et regrouper — valeurs manquantes, doublons, texte, dates, `groupby` | [▶](https://colab.research.google.com/github/aureliensalas/python_finance/blob/main/pandas_crypto/cours/seance2_cours.ipynb) | *après la séance* |

### Travail noté — l'investissement programmé

Lancé en classe, terminé à la maison. Une cliente demande ce qu'aurait donné 100 dollars par mois dans le bitcoin depuis 2020. L'export de données qu'on vous remet n'a pas été relu : il faut le diagnostiquer et le réparer avant de répondre — puis mesurer le résultat, expliquer pourquoi la méthode fonctionne, et comparer les sept monnaies.

| Sujet | Énoncé | Correction |
|---|---|---|
| L'investissement programmé | [▶](https://colab.research.google.com/github/aureliensalas/python_finance/blob/main/pandas_crypto/assignment/investissement_programme.ipynb) | *après le rendu* |

### Les données du bloc 2

Les fichiers se chargent **directement depuis le web** : rien à télécharger.

| Fichier | Lignes | Contenu |
|---|---|---|
| `crypto.csv` | 21 325 | Une monnaie un jour : `date`, `coin`, `close`, `volume`. Sept monnaies (BTC, ETH, SOL, DOGE, XRP, BNB, ADA), du 1er janvier 2018 au 31 août 2026 |
| `crypto_sale.csv` | 2 592 | L'année 2024, **volontairement abîmée** : prix en texte, volumes manquants, doublons, noms de monnaies incohérents |
| `crypto_export.csv` | 21 445 | Toute la période, **volontairement abîmée** de la même façon, plus quelques prix manquants. C'est l'export « brut » du travail noté |

Source : Yahoo Finance via [yfinance](https://github.com/ranaroussi/yfinance). Construction reproductible par [`pandas_crypto/data/build_data.py`](pandas_crypto/data/build_data.py), puis [`build_export.py`](pandas_crypto/data/build_export.py) pour l'export brut.

---

## Bloc 3 — Décrire le risque, et en douter (4h)

Deux séances de 2h, sur les mêmes cryptomonnaies. La première construit la colonne qui manquait — le rendement — et apprend à décrire un actif. La seconde apprend à douter d'une moyenne, à comparer deux groupes, et à ne pas se laisser piéger par un résultat trop beau.

| Séance | Sujet | Cours | Correction |
|---|---|---|---|
| 3.1 | Décrire le risque — rendement, `describe`, `groupby` sur plusieurs mesures, histogramme | [▶](https://colab.research.google.com/github/aureliensalas/python_finance/blob/main/stats_crypto/cours/seance1_cours.ipynb) | *après la séance* |
| 3.2 | Comparer, et douter — bootstrap, intervalle de confiance, test t, tests répétés, corrélation | [▶](https://colab.research.google.com/github/aureliensalas/python_finance/blob/main/stats_crypto/cours/seance2_cours.ipynb) | *après la séance* |

### Travail en autonomie — la fiche de risque

À faire après les deux séances, seul. Une fonction de mise en page est fournie ; l'étudiant calcule les cinq indicateurs de risque d'une cryptomonnaie et les voit remplir la fiche au fur et à mesure. Il termine avec une petite application à champ de saisie.

| Sujet | Énoncé |
|---|---|
| La fiche de risque | [▶](https://colab.research.google.com/github/aureliensalas/python_finance/blob/main/stats_crypto/assignment/fiche_de_risque.ipynb) |

### Les données du bloc 3

Le fichier `crypto.csv` du bloc 2, plus un seul fichier :

| Fichier | Lignes | Contenu |
|---|---|---|
| `rendements.csv` | 2 334 | Une ligne par jour, une colonne par monnaie : le rendement quotidien en %, sur les jours où les sept monnaies sont cotées. Construit par [`stats_crypto/data/build_rendements.py`](stats_crypto/data/build_rendements.py) |

---

## Bloc 4 — Introduction au machine learning (4h)

*À venir.*

---

## Comment ce dépôt est organisé

```
python/cours/            le notebook de cours du bloc 1
python/assignment/       le travail noté
python/build/            les scripts qui génèrent ces notebooks
pandas_crypto/cours/     les deux notebooks de cours du bloc 2
pandas_crypto/assignment/ le travail noté du bloc 2
pandas_crypto/data/      les CSV et les scripts qui les construisent
pandas_crypto/build/     les scripts qui génèrent ces notebooks
stats_crypto/cours/      les deux notebooks de cours du bloc 3
stats_crypto/assignment/ le travail en autonomie du bloc 3
stats_crypto/data/       le fichier large des rendements et son script
stats_crypto/build/      les scripts qui génèrent ces notebooks
ressources/              aide-mémoire, réglages tablette, images
```

Les notebooks ne s'écrivent pas à la main : chaque `build_*.py` produit son `.ipynb`. Pour modifier une séance, on modifie le script et on le relance.
