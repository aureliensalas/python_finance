# -*- coding: utf-8 -*-
"""Régénère les rendus de la fiche d'analyse.

    python3 prototypes/rendre_fiches.py
"""
import os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
from fiche_analyse import afficher_fiche

SEUILS = [-4, -5, -7, -10]
MONNAIES = ["BTC", "ETH", "SOL", "DOGE", "XRP", "BNB", "ADA"]

c = pd.read_csv(os.path.join(ICI, "..", "pandas_crypto", "data", "crypto.csv"))
c["date"] = pd.to_datetime(c["date"])
c = c.sort_values(["coin", "date"]).reset_index(drop=True)
c["r"] = c.groupby("coin")["close"].pct_change() * 100
c["r_hier"] = c.groupby("coin")["r"].shift(1)
c = c.dropna(subset=["r", "r_hier"])

lignes = []
for m in MONNAIES:
    ligne = []
    for s in SEUILS:
        x = c.query(f"coin == '{m}'")
        ligne.append(stats.ttest_ind(x.query(f"r_hier < {s}")["r"],
                                     x.query(f"r_hier >= {s}")["r"], equal_var=False).pvalue)
    lignes.append(ligne)
grille = pd.DataFrame(lignes, index=MONNAIES, columns=[f"{s} %" for s in SEUILS])
classement = c.groupby("coin")["r"].std().sort_values()


def rendre(m, sortie):
    t = c.query(f"coin == '{m}'")
    a = t.query("r_hier < -5")["r"]
    o = t.query("r_hier >= -5")["r"]
    boot = pd.Series([a.sample(len(a), replace=True, random_state=i).mean()
                      - o.sample(len(o), replace=True, random_state=i).mean() for i in range(1000)])
    afficher_fiche(m, periode="%d jours  ·  %s → %s" % (len(t), t["date"].min().date(), t["date"].max().date()),
                   prix=t, rendement_moyen=t["r"].mean(), rendement_median=t["r"].median(),
                   volatilite=t["r"].std(), var_95=t["r"].quantile(0.05),
                   part_hausse=(t["r"] > 0).mean() * 100, pire_jour=t["r"].min(),
                   date_pire=t.loc[t["r"].idxmin(), "date"].date(),
                   rendements=t["r"], classement=classement,
                   seuil=-5, nb_occasions=len(a), gain_moyen=a.mean(), gain_autres=o.mean(),
                   borne_basse=boot.quantile(0.025), borne_haute=boot.quantile(0.975),
                   p_value=stats.ttest_ind(a, o, equal_var=False).pvalue, boot=boot, grille=grille)
    plt.savefig(os.path.join(ICI, sortie), dpi=98, facecolor="white")
    plt.close()


rendre("BTC", "analyse_BTC.png")
rendre("ADA", "analyse_ADA.png")
t = c.query("coin == 'SOL'")
afficher_fiche("SOL", periode="%d jours  ·  %s → %s" % (len(t), t["date"].min().date(), t["date"].max().date()), seuil=-5)
plt.savefig(os.path.join(ICI, "analyse_vide.png"), dpi=98, facecolor="white")
plt.close()
print("écrit : analyse_vide.png, analyse_BTC.png, analyse_ADA.png")
