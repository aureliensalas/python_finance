# -*- coding: utf-8 -*-
"""Régénère les rendus de la fiche de risque.

    python3 prototypes/rendre_fiches.py

Nécessite pandas et matplotlib. Lit pandas_crypto/data/crypto.csv.
"""
import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
from fiche_risque import afficher_fiche

c = pd.read_csv(os.path.join(ICI, "..", "pandas_crypto", "data", "crypto.csv"))
c["date"] = pd.to_datetime(c["date"])
c = c.sort_values(["coin", "date"]).reset_index(drop=True)
c["r"] = c.groupby("coin")["close"].pct_change() * 100
c = c.dropna(subset=["r"])
classement = c.groupby("coin")["r"].std().sort_values()

def periode(t):
    return "%d jours  ·  %s → %s" % (len(t), t["date"].min().date(), t["date"].max().date())

for m in ["SOL", "BTC", "DOGE"]:
    t = c[c["coin"] == m]
    afficher_fiche(m, periode=periode(t), prix=t,
                   rendement_moyen=t["r"].mean(), rendement_median=t["r"].median(),
                   volatilite=t["r"].std(), var_95=t["r"].quantile(0.05),
                   part_hausse=(t["r"] > 0).mean() * 100, pire_jour=t["r"].min(),
                   date_pire=t.loc[t["r"].idxmin(), "date"].date(),
                   rendements=t["r"], classement=classement)
    plt.savefig(os.path.join(ICI, "fiche_%s.png" % m), dpi=105, facecolor="white")
    plt.close()

t = c[c["coin"] == "SOL"]
afficher_fiche("SOL", periode=periode(t), prix=t)     # l'état de la partie 1
plt.savefig(os.path.join(ICI, "fiche_vide.png"), dpi=105, facecolor="white")
plt.close()
print("écrit : fiche_vide.png, fiche_SOL.png, fiche_BTC.png, fiche_DOGE.png")
