<img src="https://cdn.jsdelivr.net/gh/maxischa/datacamp_test@main/ressources/img/logo_macmia.png" alt="Logo" width="520">

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

Deux séances de 2h. Le notebook de **cours** contient les exercices : on montre une notion, vous la refaites aussitôt. La **correction** est publiée après la séance.

| Séance | Sujet | Cours | Correction |
|---|---|---|---|
| 1.1 | Python calcule — expressions, types, variables, fonctions, chaînes | [▶](https://colab.research.google.com/github/maxischa/datacamp_test/blob/main/python/cours/seance1_cours.ipynb) | *après la séance* |
| 1.2 | Python décide et répète — booléens, `if`, listes, `for`, Series | [▶](https://colab.research.google.com/github/maxischa/datacamp_test/blob/main/python/cours/seance2_cours.ipynb) | *après la séance* |

### Travail noté — le simulateur de prêt

Lancé en classe, terminé à la maison. À partir de trois champs de formulaire et du taux directeur de la Banque centrale européenne du jour : une mensualité, un verdict d'acceptation, un tableau d'amortissement sur 240 mois, la courbe du capital restant dû et le coût du crédit.

| Sujet | Énoncé | Correction |
|---|---|---|
| Le simulateur de prêt | [▶](https://colab.research.google.com/github/maxischa/datacamp_test/blob/main/python/assignment/simulateur_pret.ipynb) | *après le rendu* |

---

## Bloc 2 — Manipuler des données avec pandas (4h)

Deux séances de 2h, sur huit ans et demi de cours quotidiens de cryptomonnaies.

| Séance | Sujet | Cours | Correction |
|---|---|---|---|
| 2.1 | Des Series à la table — charger, calculer, filtrer, trier | [▶](https://colab.research.google.com/github/maxischa/datacamp_test/blob/main/pandas_crypto/cours/seance1_cours.ipynb) | *après la séance* |
| 2.2 | Nettoyer et regrouper — valeurs manquantes, doublons, texte, dates, `groupby` | [▶](https://colab.research.google.com/github/maxischa/datacamp_test/blob/main/pandas_crypto/cours/seance2_cours.ipynb) | *après la séance* |

### Les données du bloc 2

Les fichiers se chargent **directement depuis le web** : rien à télécharger.

| Fichier | Lignes | Contenu |
|---|---|---|
| `crypto.csv` | 21 325 | Une monnaie un jour : `date`, `coin`, `close`, `volume`. Sept monnaies (BTC, ETH, SOL, DOGE, XRP, BNB, ADA), du 1er janvier 2018 au 31 août 2026 |
| `crypto_sale.csv` | 2 592 | L'année 2024, **volontairement abîmée** : prix en texte, volumes manquants, doublons, noms de monnaies incohérents |

Source : Yahoo Finance via [yfinance](https://github.com/ranaroussi/yfinance). Construction reproductible par [`pandas_crypto/data/build_data.py`](pandas_crypto/data/build_data.py).

---

## Bloc 3 — Décrire et relier des données (4h)

*À venir.*

---

## Bloc 4 — Introduction au machine learning (4h)

*À venir.*

---

## Comment ce dépôt est organisé

```
python/cours/            les deux notebooks de cours du bloc 1
python/assignment/       le travail noté
python/build/            les scripts qui génèrent ces notebooks
pandas_crypto/cours/     les deux notebooks de cours du bloc 2
pandas_crypto/data/      les CSV et le script qui les construit
pandas_crypto/build/     les scripts qui génèrent ces notebooks
ressources/              aide-mémoire, réglages tablette, images
```

Les notebooks ne s'écrivent pas à la main : chaque `build_*.py` produit son `.ipynb`. Pour modifier une séance, on modifie le script et on le relance.
