"""Rebranche tous les liens du cours sur votre dépôt GitHub.

    python3 set_repo.py votre-compte/votre-depot            # branche main
    python3 set_repo.py votre-compte/votre-depot a1b2c3d    # épinglé sur un commit
    python3 set_repo.py votre-compte/votre-depot --dry      # montre sans modifier

Remplace partout :
  - les liens Colab        https://colab.research.google.com/github/<slug>/blob/main/...
  - les liens GitHub       https://github.com/<slug>/blob/main/...
  - les fichiers servis    https://cdn.jsdelivr.net/gh/<slug>@<ref>/...
"""
import re
import sys

ANCIEN_SLUG = "maxischa/datacamp_test"
ANCIENS_REFS = ["5a33b79", "main"]        # le logo était épinglé, les données sur main

FICHIERS = [
    "README_cours_finance.md",
    "python/cours/seance1_cours.ipynb",
    "python/cours/seance2_cours.ipynb",
    "python/assignment/simulateur_pret.ipynb",
    "python/build/build_p1.py",
    "python/build/build_p2.py",
    "python/build/build_a1.py",
    "pandas_crypto/cours/seance1_cours.ipynb",
    "pandas_crypto/cours/seance2_cours.ipynb",
    "pandas_crypto/build/build_d1.py",
    "pandas_crypto/build/build_d2.py",
]


def main():
    args = [a for a in sys.argv[1:] if a != "--dry"]
    dry = "--dry" in sys.argv
    if not args or "/" not in args[0]:
        print(__doc__)
        return
    slug = args[0]
    ref = args[1] if len(args) > 1 else "main"

    total = 0
    for chemin in FICHIERS:
        try:
            texte = open(chemin, encoding="utf-8").read()
        except FileNotFoundError:
            print("absent  -", chemin)
            continue

        avant = texte
        # cdn.jsdelivr.net/gh/<slug>@<ref>  ->  nouveau slug + nouvelle ref
        texte = re.sub(r"cdn\.jsdelivr\.net/gh/" + re.escape(ANCIEN_SLUG) + r"@[\w.]+",
                       "cdn.jsdelivr.net/gh/" + slug + "@" + ref, texte)
        # tout le reste : colab, github, liens bruts
        texte = texte.replace(ANCIEN_SLUG, slug)

        n = sum(1 for a, b in zip(avant.split("\n"), texte.split("\n")) if a != b)
        if avant == texte:
            print("inchangé-", chemin)
            continue
        total += n
        if not dry:
            open(chemin, "w", encoding="utf-8").write(texte)
        print(("verrait " if dry else "modifié ") + "-", chemin, f"({n} lignes)")

    print()
    print(("Aucune écriture (--dry). " if dry else "") + f"{total} lignes concernées.")
    print(f"Dépôt : {slug}   ref des fichiers servis : @{ref}")
    if ref == "main":
        print("Note : jsDelivr garde une branche en cache environ 12 heures.")
        print("Pour un cours, épinglez un commit : python3 set_repo.py " + slug + " <hash>")


if __name__ == "__main__":
    main()
