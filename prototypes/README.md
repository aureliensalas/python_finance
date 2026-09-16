# Prototypes

Maquettes de travail, pas du matériel de cours. Rien ici n'est servi aux étudiants.

| Fichier | Rôle |
|---|---|
| `fiche_analyse.py` | la fonction `afficher_fiche(...)`, inlinée dans le travail en autonomie du bloc 3 par `build_a3.py` |
| `rendre_fiches.py` | régénère les images ci-dessous depuis `pandas_crypto/data/crypto.csv` |
| `analyse_vide.png` | l'état de départ : tout est gris, la fiche attend |
| `analyse_BTC.png` | verdict « on ne peut pas conclure » — la barre passe par zéro |
| `analyse_ADA.png` | verdict « effet détecté » — la barre est entièrement à droite |

```
python3 prototypes/rendre_fiches.py
```

La spécification du devoir est dans `PLAN_assignment_stats.md`.
