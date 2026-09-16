# -*- coding: utf-8 -*-
"""Prototype de la fiche de risque du travail noté du bloc 3.

Cette fonction sera FOURNIE aux étudiants : ils calculent les indicateurs,
elle les met en page. Tout argument omis affiche « à compléter ».
"""
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

ENCRE, GRIS, BLEU, ROUGE, VERT, FOND = "#1F2933", "#9AA5B1", "#1F4E79", "#B4341F", "#2E7D5B", "#F5F7F9"
HALO = dict(facecolor="white", alpha=0.92, edgecolor="none", pad=2.2)   # fond blanc sous les étiquettes


def _attente(a, titre):
    """Un panneau encore vide : le titre, un cadre discret, et rien d'autre."""
    a.set_xticks([]); a.set_yticks([])
    for s in ("top", "right", "bottom", "left"): a.spines[s].set_visible(False)
    a.add_patch(plt.Rectangle((0, 0), 1, 1, transform=a.transAxes, facecolor=FOND,
                              edgecolor="#DCE2E8", lw=1, zorder=0))
    a.set_title(titre, loc="left", fontsize=11.5, color=GRIS, fontweight="bold")
    a.text(0.5, 0.5, "à compléter", transform=a.transAxes, fontsize=13, color=GRIS,
           ha="center", va="center", style="italic")


def afficher_fiche(nom, periode=None, prix=None, rendement_moyen=None, rendement_median=None,
                   volatilite=None, var_95=None, part_hausse=None, pire_jour=None,
                   date_pire=None, rendements=None, classement=None):
    fig = plt.figure(figsize=(11.5, 10.6), facecolor="white")
    gs = GridSpec(4, 5, figure=fig, height_ratios=[0.52, 2.05, 0.95, 2.05],
                  hspace=0.62, wspace=0.30, left=0.065, right=0.95, top=0.965, bottom=0.06)

    # ---------------------------------------------------------------- bandeau
    a = fig.add_subplot(gs[0, :]); a.axis("off")
    a.add_patch(plt.Rectangle((0, 0), 1, 1, transform=a.transAxes, color=BLEU, zorder=0))
    a.text(0.022, 0.62, nom, transform=a.transAxes, fontsize=30, color="white", fontweight="bold", va="center")
    a.text(0.022, 0.20, periode or "", transform=a.transAxes, fontsize=9.5, color="#C3D0DC", va="center")
    a.text(0.978, 0.50, "FICHE DE RISQUE", transform=a.transAxes, fontsize=11.5, color="white",
           ha="right", va="center", fontweight="bold", alpha=0.9)

    # ---------------------------------------------------------------- le cours
    a = fig.add_subplot(gs[1, :])
    if prix is not None:
        a.plot(prix["date"], prix["close"], color=BLEU, lw=1.5)
        a.fill_between(prix["date"], prix["close"], color=BLEU, alpha=0.08)
        a.set_title("Le cours, jour après jour", loc="left", fontsize=11.5, color=ENCRE, fontweight="bold")
        a.set_ylabel("dollars", fontsize=9)
        a.margins(x=0.01)
        for s in ("top", "right"): a.spines[s].set_visible(False)
        a.tick_params(labelsize=8.5, colors=GRIS)
    else:
        _attente(a, "Le cours, jour après jour")

    # ---------------------------------------------------------------- tuiles
    def vide(v): return v is None or (isinstance(v, float) and np.isnan(v))
    tuiles = [("RENDEMENT MOYEN", rendement_moyen, "%+.2f %%", lambda v: "%+.0f %% par an" % (((1 + v / 100) ** 365 - 1) * 100)),
              ("RENDEMENT MÉDIAN", rendement_median, "%+.2f %%", lambda v: "le jour ordinaire"),
              ("VOLATILITÉ", volatilite, "%.2f %%", lambda v: "%.0f %% annualisée" % (v * np.sqrt(365))),
              ("VaR 95 %", var_95, "%.2f %%", lambda v: "1 jour sur 20 fait pire"),
              ("JOURS DE HAUSSE", part_hausse, "%.1f %%", lambda v: "sur la période")]
    for k, (titre, val, fmt, sous) in enumerate(tuiles):
        t = fig.add_subplot(gs[2, k]); t.axis("off")
        t.add_patch(plt.Rectangle((0, 0), 1, 1, transform=t.transAxes, color=FOND, zorder=0))
        t.add_patch(plt.Rectangle((0, 0.93), 1, 0.07, transform=t.transAxes,
                                  color=GRIS if vide(val) else BLEU, zorder=1))
        t.text(0.5, 0.74, titre, transform=t.transAxes, fontsize=7.2, color=GRIS, ha="center", fontweight="bold")
        if vide(val):
            t.text(0.5, 0.38, "à compléter", transform=t.transAxes, fontsize=10.5, color=GRIS, ha="center", style="italic")
        else:
            neutre = titre in ("VOLATILITÉ", "JOURS DE HAUSSE", "VaR 95 %")
            coul = ENCRE if neutre else (VERT if val > 0 else ROUGE)
            t.text(0.5, 0.42, fmt % val, transform=t.transAxes, fontsize=16.5, color=coul, ha="center", fontweight="bold")
            t.text(0.5, 0.13, sous(val), transform=t.transAxes, fontsize=7.2, color=GRIS, ha="center")

    # ---------------------------------------------------------------- distribution
    a = fig.add_subplot(gs[3, :3])
    if rendements is not None:
        a.hist(rendements, bins=70, color=BLEU, alpha=0.78, edgecolor="none")
        haut = a.get_ylim()[1]
        if not vide(var_95):
            a.axvline(var_95, color=ROUGE, lw=1.8, ls="--")
            a.text(var_95, haut * 0.97, "VaR 95 %%  %.1f %%  " % var_95, color=ROUGE, fontsize=9,
                   fontweight="bold", ha="right", va="top", bbox=HALO)
        if not vide(pire_jour):
            a.axvline(pire_jour, color=ENCRE, lw=1.3)
            txt = "pire jour  %.1f %%" % pire_jour + ("\n%s" % date_pire if date_pire else "")
            a.text(pire_jour, haut * 0.62, "  " + txt, color=ENCRE, fontsize=8.5, va="top", bbox=HALO)
        a.set_title("Les secousses : distribution des rendements quotidiens", loc="left",
                    fontsize=11.5, color=ENCRE, fontweight="bold")
        a.set_xlabel("% par jour", fontsize=9); a.set_ylabel("nombre de jours", fontsize=9)
        for s in ("top", "right"): a.spines[s].set_visible(False)
        a.tick_params(labelsize=8.5, colors=GRIS)
    else:
        _attente(a, "Les secousses : distribution des rendements quotidiens")

    # ---------------------------------------------------------------- classement
    a = fig.add_subplot(gs[3, 3:])
    if classement is not None:
        coul = [ROUGE if i == nom else "#C6CED6" for i in classement.index]
        a.barh(classement.index, classement.values, color=coul, height=0.66)
        a.set_title("Où se situe %s ?" % nom, loc="left", fontsize=11.5, color=ENCRE, fontweight="bold")
        a.set_xlabel("volatilité, % par jour", fontsize=9)
        a.tick_params(labelsize=9, colors=ENCRE)
        for s in ("top", "right"): a.spines[s].set_visible(False)
    else:
        _attente(a, "Où se situe %s ?" % nom)
    return fig
