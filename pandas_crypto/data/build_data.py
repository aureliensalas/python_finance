"""Construit crypto.csv (propre) et crypto_sale.csv (abîmé) pour le bloc pandas.

À lancer une seule fois ; les CSV produits sont figés dans le dépôt.
Nécessite yfinance (pip install yfinance). Construit le 14 septembre 2026.
"""
import json
import numpy as np
import pandas as pd
import yfinance as yf

DEBUT = "2018-01-01"
FIN = "2026-08-31"          # dernier mois complet à la date de construction
COINS = ["BTC", "ETH", "SOL", "DOGE", "XRP", "BNB", "ADA"]
GRAINE = 42

# ------------------------------------------------------------------ propre
brut = yf.download([c + "-USD" for c in COINS], start=DEBUT, end="2026-09-01",
                   progress=False, auto_adjust=True)
close = brut["Close"]
volume = brut["Volume"]

lignes = []
for c in COINS:
    s = pd.DataFrame({"close": close[c + "-USD"], "volume": volume[c + "-USD"]}).dropna()
    s = s[(s.index >= DEBUT) & (s.index <= FIN)]
    s = s[s["volume"] > 0]
    s["volume"] = s["volume"] / s["close"]      # Yahoo donne le volume en dollars ; on le veut en unités
    lignes.append(pd.DataFrame({"date": s.index.strftime("%Y-%m-%d"), "coin": c,
                                "close": s["close"].round(4).values,
                                "volume": s["volume"].round(0).values}))
crypto = pd.concat(lignes).sort_values(["date", "coin"]).reset_index(drop=True)

assert crypto.isna().sum().sum() == 0
assert crypto.duplicated().sum() == 0
assert crypto.duplicated(subset=["date", "coin"]).sum() == 0
crypto.to_csv("crypto.csv", index=False)

# ------------------------------------------------------------------ sale
rng = np.random.default_rng(GRAINE)
sale = crypto[crypto["date"].str.startswith("2024")].copy().reset_index(drop=True)
n = len(sale)

# 1. noms de monnaies abîmés sur un quart des lignes (avant les doublons : les copies restent exactes)
formes = [lambda c: c.lower(), lambda c: " " + c, lambda c: c.capitalize() + " "]
idx_coin = rng.choice(n, size=n // 4, replace=False)
choix = rng.integers(0, len(formes), size=len(idx_coin))
for i, k in zip(idx_coin, choix):
    sale.loc[i, "coin"] = formes[k](sale.loc[i, "coin"])

# 2. volumes manquants
idx_na = rng.choice(n, size=40, replace=False)
sale.loc[idx_na, "volume"] = np.nan

# 3. doublons : 30 lignes recopiées, puis retri par date
idx_dup = rng.choice(n, size=30, replace=False)
sale = pd.concat([sale, sale.loc[idx_dup]]).sort_values(["date", "coin"], kind="stable").reset_index(drop=True)

# 4. prix en texte à la française : "43 250,12 $"
def en_texte(x):
    entier, dec = f"{x:,.2f}".split(".")
    return entier.replace(",", " ") + "," + dec + " $"
sale["close"] = sale["close"].map(en_texte)

sale.to_csv("crypto_sale.csv", index=False)

# ------------------------------------------------------------------ valeurs de référence
c = crypto.copy()
c["date"] = pd.to_datetime(c["date"])
c["annee"] = c["date"].dt.year
btc = c[c["coin"] == "BTC"]
achats = btc[(btc["date"].dt.day == 1) & (btc["annee"] >= 2020)]
quantite = (100 / achats["close"]).sum()
dernier = btc["close"].iloc[-1]

def dca(coin):
    t = c[(c["coin"] == coin) & (c["date"].dt.day == 1) & (c["annee"] >= 2020)]
    q = (100 / t["close"]).sum()
    inv = 100 * len(t)
    val = q * c[c["coin"] == coin]["close"].iloc[-1]
    return {"investi": inv, "valeur": round(val, 2), "gain_pct": round(100 * (val / inv - 1), 1)}

ref = {
    "construction": "2026-09-14",
    "periode": [crypto["date"].min(), crypto["date"].max()],
    "nb_lignes": int(len(crypto)),
    "nb_par_coin": crypto["coin"].value_counts().to_dict(),
    "close_max": float(crypto["close"].max()),
    "close_min": float(crypto["close"].min()),
    "montant_max_m": round(float((crypto["close"] * crypto["volume"] / 1e6).max()), 1),
    "volume_total": float(crypto["volume"].sum()),
    "close_max_par_coin": crypto.groupby("coin")["close"].max().to_dict(),
    "part_gros_volume": round(float((crypto["volume"] > crypto["volume"].mean()).mean()), 4),
    "nb_jours_btc_100k": int(((crypto["coin"] == "BTC") & (crypto["close"] > 100000)).sum()),
    "nb_btc": int((crypto["coin"] == "BTC").sum()),
    "nb_sol": int((crypto["coin"] == "SOL").sum()),
    "eth_2024_mean": round(float(c[(c["coin"] == "ETH") & (c["annee"] == 2024)]["close"].mean()), 2),
    "part_doge_xrp": round(float(crypto["coin"].isin(["DOGE", "XRP"]).mean()), 4),
    "top_volume": crypto.sort_values("volume", ascending=False).head(5)[["date", "coin", "volume"]].to_dict("records"),
    "nb_2021": int((c["annee"] == 2021).sum()),
    "btc_max_2021": float(btc[btc["annee"] == 2021]["close"].max()),
    "moy_2024": c[c["annee"] == 2024].groupby("coin")["close"].mean().round(2).to_dict(),
    "premiere_annee_par_coin": c.groupby("coin")["annee"].min().to_dict(),
    "sale_nb_lignes": int(len(sale)),
    "sale_nb_na_volume": int(sale["volume"].isna().sum()),
    "sale_nb_doublons": int(sale.duplicated().sum()),
    "sale_nb_categories_coin": int(sale["coin"].nunique()),
    "sale_apres_dropna": int(len(sale.dropna(subset=["volume"]))),
    "sale_apres_dropna_puis_dedoublon": int(len(sale.dropna(subset=["volume"]).drop_duplicates())),
    "dca_btc": {"nb_achats": int(len(achats)), "investi": int(100 * len(achats)), "total_btc": round(float(quantite), 6),
                "dernier_prix": float(dernier), "valeur": round(float(quantite * dernier), 2),
                "gain_pct": round(float(100 * (quantite * dernier / (100 * len(achats)) - 1)), 1)},
    "dca_par_coin": {k: dca(k) for k in COINS},
    "lump_btc": {"prix_premier_achat": float(achats["close"].iloc[0]),
                 "valeur": round(float(100 * len(achats) / achats["close"].iloc[0] * dernier), 2)},
}
json.dump(ref, open("valeurs_reference.json", "w"), indent=1, ensure_ascii=False, default=str)
print(json.dumps(ref, indent=1, ensure_ascii=False, default=str))
