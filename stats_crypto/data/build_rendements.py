"""Construit rendements.csv, la table « large » du bloc stats, à partir de crypto.csv.

Une ligne par jour, une colonne par monnaie, rendement quotidien en %.
SOL est vide avant avril 2020 ; corr() ignore les manquants paire par paire.

    python3 stats_crypto/data/build_rendements.py

Écrit aussi valeurs_reference.json : les chiffres que les cellules verifier
des deux séances utilisent.
"""
import json
import os
import numpy as np
import pandas as pd

ICI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ICI, "..", "..", "pandas_crypto", "data", "crypto.csv")
COINS = ["BTC", "ETH", "SOL", "DOGE", "XRP", "BNB", "ADA"]

c = pd.read_csv(SRC)
c["date"] = pd.to_datetime(c["date"])
c = c.sort_values(["coin", "date"]).reset_index(drop=True)
c["r"] = c.groupby("coin")["close"].pct_change() * 100
c = c.dropna(subset=["r"]).reset_index(drop=True)

large = c.pivot_table(index="date", columns="coin", values="r")[COINS]   # SOL est NaN avant avril 2020, on garde tout
large.index = large.index.strftime("%Y-%m-%d")
large.round(4).to_csv(os.path.join(ICI, "rendements.csv"))

# ------------------------------------------------------------------ valeurs de référence
c["annee"] = c["date"].dt.year
c["jour_sem"] = c["date"].dt.dayofweek
btc = c.query("coin == 'BTC'")
eth = c.query("coin == 'ETH'")

def boot(s, n=1000):
    m = pd.Series([s.sample(len(s), replace=True, random_state=i).mean() for i in range(n)])
    return [float(m.quantile(0.025)), float(m.quantile(0.975))]

from scipy import stats
ref = {
    "construction": "2026-09-16",
    "nb_lignes_avec_rendement": int(len(c)),
    "max_faux_sans_groupby": float(c.sort_values(["coin", "date"])["close"].pct_change().max() * 100),
    "max_vrai": float(c["r"].max()),
    "par_coin": c.groupby("coin")["r"].agg(["mean", "median", "std", "min", "max"]).round(4).to_dict("index"),
    "part_hausse": (c.assign(h=c["r"] > 0).groupby("coin")["h"].mean() * 100).round(2).to_dict(),
    "btc": {"mean": float(btc["r"].mean()), "median": float(btc["r"].median()), "std": float(btc["r"].std()),
            "q05": float(btc["r"].quantile(0.05)), "q01": float(btc["r"].quantile(0.01)),
            "au_dela_3_sigma": int((btc["r"].abs() > 3 * btc["r"].std()).sum()),
            "par_annee_mean": btc.groupby("annee")["r"].mean().round(4).to_dict(),
            "par_jour_sem": btc.groupby("jour_sem")["r"].mean().round(4).to_dict(),
            "ic_bootstrap": boot(btc["r"])},
    "eth": {"mean": float(eth["r"].mean()), "median": float(eth["r"].median()), "std": float(eth["r"].std()),
            "q05": float(eth["r"].quantile(0.05)), "ic_bootstrap": boot(eth["r"])},
    "vol_par_annee": c.groupby("annee")["r"].std().round(4).to_dict(),
    "vol_2021_sans_doge": float(c.query("annee == 2021 and r < 300")["r"].std()),
    "ttest_btc_eth_p": float(stats.ttest_ind(btc["r"], eth["r"], equal_var=False).pvalue),
    "ttest_jeudi_p": float(stats.ttest_ind(btc.query("jour_sem == 3")["r"], btc.query("jour_sem != 3")["r"], equal_var=False).pvalue),
    "correlations": large.corr().round(4).to_dict(),
    "covid_2020_03_12": large.loc["2020-03-12"].round(2).to_dict() if "2020-03-12" in large.index else None,
    "rendements_csv_lignes": int(len(large)),
}
json.dump(ref, open(os.path.join(ICI, "valeurs_reference.json"), "w"), indent=1, ensure_ascii=False, default=str)
print("écrit rendements.csv :", len(large), "lignes ×", len(large.columns), "monnaies")
print("ETH médiane %.4f | khi-deux et query date vérifiés à part" % ref["eth"]["median"])
