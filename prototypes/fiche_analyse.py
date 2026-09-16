# -*- coding: utf-8 -*-
"""Fiche d'analyse complète : le risque d'une monnaie, puis le test d'une idée de stratégie.

Fournie aux étudiants. Ils calculent, elle met en page et tranche.
Tout argument omis affiche « à compléter ».
"""
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

ENCRE, GRIS, BLEU, ROUGE, VERT, ORANGE, FOND = "#1F2933", "#9AA5B1", "#1F4E79", "#B4341F", "#2E7D5B", "#B26B00", "#F5F7F9"
HALO = dict(facecolor="white", alpha=0.92, edgecolor="none", pad=2.2)
_vide = lambda v: v is None or (isinstance(v, float) and np.isnan(v))


def _attente(a, titre):
    a.set_xticks([]); a.set_yticks([])
    for s in ("top", "right", "bottom", "left"): a.spines[s].set_visible(False)
    a.add_patch(plt.Rectangle((0, 0), 1, 1, transform=a.transAxes, facecolor=FOND,
                              edgecolor="#DCE2E8", lw=1, zorder=0))
    a.set_title(titre, loc="left", fontsize=11, color=GRIS, fontweight="bold")
    a.text(0.5, 0.5, "à compléter", transform=a.transAxes, fontsize=12.5, color=GRIS,
           ha="center", va="center", style="italic")


def _tuiles(fig, gs, ligne, tuiles):
    for k, (titre, val, fmt, sous, mode) in enumerate(tuiles):
        t = fig.add_subplot(gs[ligne, k]); t.axis("off")
        t.add_patch(plt.Rectangle((0, 0), 1, 1, transform=t.transAxes, color=FOND, zorder=0))
        t.add_patch(plt.Rectangle((0, 0.93), 1, 0.07, transform=t.transAxes,
                                  color=GRIS if _vide(val) else BLEU, zorder=1))
        t.text(0.5, 0.74, titre, transform=t.transAxes, fontsize=7, color=GRIS,
               ha="center", fontweight="bold")
        if _vide(val):
            t.text(0.5, 0.38, "à compléter", transform=t.transAxes, fontsize=10, color=GRIS,
                   ha="center", style="italic")
        else:
            if mode == "neutre":
                coul = ENCRE
            elif mode == "seuil":
                coul = VERT if val < 0.05 else ORANGE
            else:
                coul = VERT if val > 0 else ROUGE
            t.text(0.5, 0.42, fmt % val, transform=t.transAxes, fontsize=15.5, color=coul,
                   ha="center", fontweight="bold")
            t.text(0.5, 0.13, sous(val) if callable(sous) else sous, transform=t.transAxes,
                   fontsize=7, color=GRIS, ha="center")


def _titre_section(fig, gs, ligne, texte):
    a = fig.add_subplot(gs[ligne, :]); a.axis("off")
    a.plot([0, 1], [0.5, 0.5], transform=a.transAxes, color="#DCE2E8", lw=1.2, zorder=0)
    a.text(0.0, 0.5, "  " + texte + "  ", transform=a.transAxes, fontsize=10.5, color=BLEU,
           va="center", fontweight="bold", bbox=dict(facecolor="white", edgecolor="none", pad=1))


def afficher_fiche(monnaie, periode=None, prix=None,
                   rendement_moyen=None, rendement_median=None, volatilite=None,
                   var_95=None, part_hausse=None, pire_jour=None, date_pire=None,
                   rendements=None, classement=None,
                   seuil=None, nb_occasions=None, gain_moyen=None, gain_autres=None,
                   borne_basse=None, borne_haute=None, p_value=None, boot=None, grille=None):

    if _vide(borne_basse) or _vide(borne_haute):
        verdict, coul_v = "EN ATTENTE", GRIS
    elif borne_basse > 0:
        verdict, coul_v = "EFFET DÉTECTÉ", VERT
    elif borne_haute < 0:
        verdict, coul_v = "EFFET INVERSE", ROUGE
    else:
        verdict, coul_v = "ON NE PEUT PAS CONCLURE", ORANGE

    fig = plt.figure(figsize=(11.5, 15.4), facecolor="white")
    gs = GridSpec(8, 4, figure=fig, height_ratios=[0.52, 1.55, 0.72, 1.55, 0.22, 1.05, 0.72, 1.55],
                  hspace=0.78, wspace=0.30, left=0.065, right=0.95, top=0.975, bottom=0.045)

    # ---------------------------------------------------------------- bandeau
    a = fig.add_subplot(gs[0, :]); a.axis("off")
    a.add_patch(plt.Rectangle((0, 0), 1, 1, transform=a.transAxes, color=BLEU, zorder=0))
    a.text(0.022, 0.60, monnaie, transform=a.transAxes, fontsize=24, color="white",
           fontweight="bold", va="center")
    a.text(0.022, 0.17, periode or "", transform=a.transAxes, fontsize=8.5, color="#C3D0DC", va="center")
    a.text(0.978, 0.50, "FICHE D'ANALYSE", transform=a.transAxes, fontsize=11, color="white",
           ha="right", va="center", fontweight="bold", alpha=0.9)

    # ---------------------------------------------------------------- le cours
    a = fig.add_subplot(gs[1, :])
    if prix is None:
        _attente(a, "Le cours, jour après jour")
    else:
        a.plot(prix["date"], prix["close"], color=BLEU, lw=1.4)
        a.fill_between(prix["date"], prix["close"], color=BLEU, alpha=0.08)
        a.set_title("Le cours, jour après jour", loc="left", fontsize=11, color=ENCRE, fontweight="bold")
        a.set_ylabel("dollars", fontsize=8.5); a.margins(x=0.01)
        for s in ("top", "right"): a.spines[s].set_visible(False)
        a.tick_params(labelsize=8, colors=GRIS)

    # ---------------------------------------------------------------- tuiles de risque
    _tuiles(fig, gs, 2, [
        ("RENDEMENT MOYEN", rendement_moyen, "%+.2f %%", lambda v: "%+.0f %% par an" % (((1 + v / 100) ** 365 - 1) * 100), "signe"),
        ("RENDEMENT MÉDIAN", rendement_median, "%+.2f %%", "le jour ordinaire", "signe"),
        ("VOLATILITÉ", volatilite, "%.2f %%", lambda v: "%.0f %% annualisée" % (v * np.sqrt(365)), "neutre"),
        ("VaR 95 %", var_95, "%.2f %%", "1 jour sur 20 fait pire", "neutre")])

    # ---------------------------------------------------------------- distribution + classement
    a = fig.add_subplot(gs[3, :2])
    if rendements is None:
        _attente(a, "La forme des journées")
    else:
        a.hist(rendements, bins=60, color=BLEU, alpha=0.78, edgecolor="none")
        haut = a.get_ylim()[1]
        if not _vide(var_95):
            a.axvline(var_95, color=ROUGE, lw=1.7, ls="--")
            a.text(var_95, haut * 0.97, "VaR  %.1f %%  " % var_95, color=ROUGE, fontsize=8.5,
                   fontweight="bold", ha="right", va="top", bbox=HALO)
        if not _vide(pire_jour):
            a.axvline(pire_jour, color=ENCRE, lw=1.2)
            txt = "pire jour  %.1f %%" % pire_jour + ("\n%s" % date_pire if date_pire else "")
            a.text(pire_jour, haut * 0.60, "  " + txt, color=ENCRE, fontsize=8, va="top", bbox=HALO)
        sous = "" if _vide(part_hausse) else "  —  %.0f %% de journées en hausse" % part_hausse
        a.set_title("La forme des journées" + sous, loc="left", fontsize=11, color=ENCRE, fontweight="bold")
        a.set_xlabel("% par jour", fontsize=8.5); a.set_ylabel("jours", fontsize=8.5)
        for s in ("top", "right"): a.spines[s].set_visible(False)
        a.tick_params(labelsize=8, colors=GRIS)

    a = fig.add_subplot(gs[3, 2:])
    if classement is None:
        _attente(a, "Où se situe %s ?" % monnaie)
    else:
        coul = [ROUGE if i == monnaie else "#C6CED6" for i in classement.index]
        a.barh(classement.index, classement.values, color=coul, height=0.66)
        a.set_title("Où se situe %s ?" % monnaie, loc="left", fontsize=11, color=ENCRE, fontweight="bold")
        a.set_xlabel("volatilité, % par jour", fontsize=8.5)
        a.tick_params(labelsize=8.5, colors=ENCRE)
        for s in ("top", "right"): a.spines[s].set_visible(False)

    # ---------------------------------------------------------------- second volet
    titre2 = "L'IDÉE DE STRATÉGIE" if _vide(seuil) else \
             "L'IDÉE DE STRATÉGIE  ·  acheter au lendemain d'une journée sous %d %%" % seuil
    _titre_section(fig, gs, 4, titre2 + "          verdict : " + verdict)

    ecart = None if (_vide(gain_moyen) or _vide(gain_autres)) else gain_moyen - gain_autres

    # ---------------------------------------------------------------- l'intervalle
    a = fig.add_subplot(gs[5, :])
    if _vide(borne_basse):
        _attente(a, "L'écart avec une journée ordinaire")
    else:
        a.axvline(0, color=ENCRE, lw=1.6, zorder=1)
        a.text(0, 1.24, "zéro : aucun effet", color=ENCRE, fontsize=8.5, ha="center", va="bottom")
        a.plot([borne_basse, borne_haute], [0, 0], lw=12, color=coul_v, alpha=0.30,
               solid_capstyle="butt", zorder=2)
        for b in (borne_basse, borne_haute):
            a.plot([b, b], [-0.32, 0.32], lw=2.2, color=coul_v, zorder=3)
            a.text(b, -0.66, "%+.2f %%" % b, color=coul_v, fontsize=9, ha="center", fontweight="bold")
        if not _vide(ecart):
            a.plot([ecart], [0], "o", ms=10, color=coul_v, zorder=4)
            a.text(ecart, 0.62, "mesuré  %+.2f %%" % ecart, color=ENCRE, fontsize=9,
                   ha="center", fontweight="bold", bbox=HALO)
        marge = max(abs(borne_basse), abs(borne_haute)) * 0.45
        a.set_xlim(min(borne_basse, 0) - marge, max(borne_haute, 0) + marge)
        a.set_ylim(-1.2, 1.6); a.set_yticks([])
        a.set_title("L'écart avec une journée ordinaire — la barre passe-t-elle par zéro ?", loc="left",
                    fontsize=11, color=ENCRE, fontweight="bold")
        a.set_xlabel("écart de rendement, points de %", fontsize=8.5)
        for s in ("top", "right", "left"): a.spines[s].set_visible(False)
        a.tick_params(labelsize=8, colors=GRIS)

    # ---------------------------------------------------------------- tuiles de test
    _tuiles(fig, gs, 6, [
        ("OCCASIONS", nb_occasions, "%d", "en 8 ans et demi", "neutre"),
        ("GAIN MOYEN", gain_moyen, "%+.2f %%", "le lendemain", "signe"),
        ("LES AUTRES JOURS", gain_autres, "%+.2f %%", "pour comparer", "signe"),
        ("p-VALUE", p_value, "%.3f", "seuil usuel : 0,05", "seuil")])

    # ---------------------------------------------------------------- bootstrap + grille
    a = fig.add_subplot(gs[7, :2])
    if boot is None:
        _attente(a, "Les 1 000 écarts possibles")
    else:
        a.hist(boot, bins=45, color=BLEU, alpha=0.78, edgecolor="none")
        a.axvline(0, color=ENCRE, lw=1.7)
        a.text(0, a.get_ylim()[1] * 0.97, " zéro ", color=ENCRE, fontsize=8.5,
               fontweight="bold", va="top", bbox=HALO)
        if not _vide(borne_basse):
            for b in (borne_basse, borne_haute):
                a.axvline(b, color=coul_v, ls="--", lw=1.4)
        a.set_title("Les 1 000 écarts possibles — %.0f %% sont négatifs" % ((np.asarray(boot) < 0).mean() * 100),
                    loc="left", fontsize=11, color=ENCRE, fontweight="bold")
        a.set_xlabel("écart, points de %", fontsize=8.5); a.set_ylabel("tirages", fontsize=8.5)
        for s in ("top", "right"): a.spines[s].set_visible(False)
        a.tick_params(labelsize=8, colors=GRIS)

    a = fig.add_subplot(gs[7, 2:])
    if grille is None:
        _attente(a, "Et si on avait cherché ailleurs ?")
    else:
        v = grille.values
        a.imshow(v < 0.05, cmap="RdYlGn_r", vmin=0, vmax=1, aspect="auto", alpha=0.55)
        for i in range(v.shape[0]):
            for j in range(v.shape[1]):
                a.text(j, i, "%.2f" % v[i, j], ha="center", va="center", fontsize=8,
                       color=ENCRE, fontweight="bold" if v[i, j] < 0.05 else "normal")
        a.set_xticks(range(v.shape[1])); a.set_xticklabels(grille.columns, fontsize=8)
        a.set_yticks(range(v.shape[0])); a.set_yticklabels(grille.index, fontsize=8)
        a.set_title("Et si on avait cherché ailleurs ? %d sur %d passent" % (int((v < 0.05).sum()), v.size),
                    loc="left", fontsize=11, color=ENCRE, fontweight="bold")
        a.set_xlabel("seuil de baisse de la veille", fontsize=8.5)
        a.tick_params(length=0, colors=ENCRE)
        for s in ("top", "right", "bottom", "left"): a.spines[s].set_visible(False)
    return fig
