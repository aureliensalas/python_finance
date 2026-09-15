"""Construit crypto_export.csv, l'export « brut » de l'assignment 2, à partir de crypto.csv.

Même famille de défauts que crypto_sale.csv, mais sur toute la période :
noms de monnaies incohérents, prix en texte à la française, doublons exacts,
volumes manquants, et quelques prix manquants sur des jours sans achat.

    python3 pandas_crypto/data/build_export.py

Déterministe (graine fixe). Écrit aussi valeurs_export.json, les chiffres
que les cellules verifier de l'assignment utilisent.
"""
import json
import os
import numpy as np
import pandas as pd

ICI = os.path.dirname(os.path.abspath(__file__))
GRAINE = 2026
rng = np.random.default_rng(GRAINE)

crypto = pd.read_csv(os.path.join(ICI, "crypto.csv"))
n = len(crypto)
export = crypto.copy()

# 1. noms de monnaies abîmés sur un quart des lignes (avant les doublons : les copies restent exactes)
formes = [lambda c: c.lower(), lambda c: " " + c, lambda c: c.capitalize() + " "]
idx_coin = rng.choice(n, size=n // 4, replace=False)
for i, k in zip(idx_coin, rng.integers(0, len(formes), size=len(idx_coin))):
    export.loc[i, "coin"] = formes[k](export.loc[i, "coin"])

# 2. volumes manquants : on n'en a pas besoin pour le devoir, on garde ces lignes
idx_vol = rng.choice(n, size=150, replace=False)
export.loc[idx_vol, "volume"] = np.nan

# 3. prix manquants : jamais un 1er du mois, jamais la dernière ligne d'une monnaie
dernieres = crypto.groupby("coin")["date"].idxmax().values
eligibles = crypto.index[~crypto["date"].str.endswith("-01")].difference(dernieres)
idx_close = rng.choice(eligibles, size=24, replace=False)
export.loc[idx_close, "close"] = np.nan

# 4. doublons : 120 lignes recopiées à l'identique, puis retri stable par date
idx_dup = rng.choice(n, size=120, replace=False)
export = pd.concat([export, export.loc[idx_dup]]).sort_values(["date", "coin"], kind="stable").reset_index(drop=True)

# 5. prix en texte à la française : "78 548,63 $", "0,7287 $"
def en_texte(x):
    if pd.isna(x):
        return np.nan
    entier, dec = f"{x:,.4f}".split(".")
    dec = dec.rstrip("0")
    dec = dec if len(dec) >= 2 else dec.ljust(2, "0")
    return entier.replace(",", " ") + "," + dec + " $"
export["close"] = export["close"].map(en_texte)

export.to_csv(os.path.join(ICI, "crypto_export.csv"), index=False)

# ------------------------------------------------------------------ le chemin de nettoyage du cours, pour les valeurs de référence
propre = export.copy()
propre["coin"] = propre["coin"].str.strip().str.upper()
propre["close"] = propre["close"].str.replace(" ", "").str.replace(",", ".").str.replace("$", "").astype(float)
nb_sans_prix_avant = int(propre["close"].isna().sum())
propre = propre.drop_duplicates()
nb_sans_prix = int(propre["close"].isna().sum())
propre = propre.dropna(subset=["close"])
propre["date"] = pd.to_datetime(propre["date"])
propre["annee"], propre["jour"] = propre["date"].dt.year, propre["date"].dt.day

# la table propre doit redonner crypto.csv moins les 24 prix retirés
temoin = crypto.drop(index=idx_close).sort_values(["date", "coin"]).reset_index(drop=True)
assert len(propre) == len(temoin) == n - 24
verif = propre.assign(date=propre["date"].dt.strftime("%Y-%m-%d")).sort_values(["date", "coin"]).reset_index(drop=True)
assert (verif["coin"].values == temoin["coin"].values).all()
assert np.allclose(verif["close"].values, temoin["close"].values)

def dca(m):
    t = propre.query(f"coin == '{m}' and jour == 1 and annee >= 2020")
    q = (100 / t["close"]).sum(); inv = 100 * len(t)
    dernier = propre.query(f"coin == '{m}'")["close"].iloc[-1]
    return {"nb_achats": int(len(t)), "investi": int(inv), "quantite": round(float(q), 6),
            "dernier_prix": float(dernier), "valeur": round(float(q * dernier), 2),
            "gain_pct": round(float(100 * (q * dernier / inv - 1)), 1)}

achats = propre.query("coin == 'BTC' and jour == 1 and annee >= 2020").copy()
achats["quantite"] = 100 / achats["close"]
ref = {
    "construction": "2026-09-15",
    "brut": {"nb_lignes": int(len(export)), "nb_noms_coin": int(export["coin"].nunique()),
             "nb_doublons": int(export.duplicated().sum()),
             "nb_volume_manquant": int(export["volume"].isna().sum()),
             "nb_close_manquant": int(export["close"].isna().sum())},
    "propre": {"nb_lignes": int(len(propre)), "nb_sans_prix_apres_dedoublon": nb_sans_prix,
               "close_max": float(propre["close"].max()), "nb_volume_manquant_garde": int(propre["volume"].isna().sum())},
    "dca_btc": dca("BTC"),
    "prix_moyen_paye": round(float(100 * len(achats) / achats["quantite"].sum()), 2),
    "prix_moyen_marche": round(float(achats["close"].mean()), 2),
    "btc_par_annee": achats.groupby("annee")["quantite"].sum().round(6).to_dict(),
    "dca_par_coin": {m: dca(m) for m in ["BTC", "ETH", "SOL", "DOGE", "XRP", "BNB", "ADA"]},
    "lump_btc": {"prix_premier_achat": float(achats["close"].iloc[0]),
                 "valeur": round(float(100 * len(achats) / achats["close"].iloc[0] * dca("BTC")["dernier_prix"]), 2)},
}
json.dump(ref, open(os.path.join(ICI, "valeurs_export.json"), "w"), indent=1, ensure_ascii=False, default=str)
print(json.dumps(ref, indent=1, ensure_ascii=False, default=str))
