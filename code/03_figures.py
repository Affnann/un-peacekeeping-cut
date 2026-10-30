"""Figures for the paper. Usage: python code/03_figures.py (after code/01_analysis.py)."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
UN_FILE = ROOT / "external" / "peacekeeping-tracker" / "data" / "build" / "contributions_monthly.csv"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)
P_CATS = ["troops", "staff_officers", "experts_on_mission", "police_individual", "police_formed_units"]

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
INK = "#222222"
ACCENT = "#8B2E2E"
GREY = "#9A9A9A"

# Figure 1: monthly total
c = pd.read_csv(UN_FILE, dtype={"month": str})
m = c[c["category"].isin(P_CATS) & (c["month"] >= "2023-01")].groupby("month")["total"].sum()
x = pd.to_datetime(m.index + "-01")
fig, ax = plt.subplots(figsize=(6.5, 3.2))
ax.plot(x, m.values / 1000, color=INK, lw=1.8)
for d, lab, ha, dx in [("2025-06-01", "June 2025 ", "right", -8), ("2025-10-01", " October 2025", "left", 8)]:
    ax.axvline(pd.Timestamp(d), color=GREY, lw=1, ls="--")
    ax.text(pd.Timestamp(d) + pd.Timedelta(days=dx), m.values.max() / 1000 * 1.005, lab, ha=ha, va="bottom", fontsize=8, color="#555555")
ax.set_ylabel("Uniformed personnel (thousands)")
ax.set_ylim(40, max(m.values) / 1000 * 1.06)
ax.grid(axis="y", color="#E5E5E5", lw=0.8)
fig.tight_layout()
fig.savefig(FIG / "fig1_monthly_total.png", dpi=300)
plt.close(fig)

# Figure 2: mission changes (missions with at least 100 personnel in June 2025)
mis = pd.read_csv(ROOT / "tables" / "missions_main.csv", index_col="mission")
mis = mis[mis["x0"] >= 100].copy()
mis["pct"] = 100 * mis["g"]
mis = mis.sort_values("pct")
fig, ax = plt.subplots(figsize=(6.5, 3.6))
ax.barh(mis.index, mis["pct"], color=[ACCENT if p <= -20 else GREY for p in mis["pct"]])
def pct_label(p):
    v = round(p)
    return ("−" if v < 0 else "") + f"{abs(v):.0f}%"


for i, (p, x0) in enumerate(zip(mis["pct"], mis["x0"])):
    lab = f"{pct_label(p)} (of {x0:,.0f})"
    if p <= -60:
        ax.text(p + 2, i, lab, va="center", ha="left", fontsize=8, color="white")
    else:
        ax.text(p - 1 if p < 0 else p + 1, i, lab, va="center", ha="right" if p < 0 else "left", fontsize=8)
ax.axvline(0, color=INK, lw=0.8)
ax.set_xlabel("Change in uniformed personnel, June 2025 to July 2026 (%)")
ax.set_xlim(-115, 15)
fig.tight_layout()
fig.savefig(FIG / "fig2_missions.png", dpi=300)
plt.close(fig)

# Figure 3: percentage change against dependence
cty = pd.read_csv(ROOT / "data" / "build" / "country_changes_main.csv", index_col="iso3")
s = cty[(cty["x0"] >= 100) & cty["D"].notna() & (cty["D"] > 0)].copy()
fig, ax = plt.subplots(figsize=(6.5, 4.0))
ax.scatter(s["D"], s["pct"], s=s["x0"] / 25, color=ACCENT, alpha=0.55, edgecolor="white", lw=0.5)
X = sm.add_constant(np.log(s["D"]))
r = sm.WLS(s["pct"], X, weights=s["x0"]).fit()
xs = np.linspace(np.log(s["D"].min()), np.log(s["D"].max()), 50)
ax.plot(np.exp(xs), r.params["const"] + r.params["D"] * xs, color=INK, lw=1.2)
for iso in ["RWA", "NPL", "GHA", "BGD", "IND", "CHN", "ZAF", "PAK", "IDN", "URY"]:
    if iso in s.index:
        ax.annotate(iso, (s.loc[iso, "D"], s.loc[iso, "pct"]), fontsize=7, xytext=(4, 2), textcoords="offset points")
ax.set_xscale("log")
ax.set_xlabel("Baseline UN payments as % of 2024 military spending (log scale)")
ax.set_ylabel("Change in personnel (%)")
ax.axhline(0, color="#CCCCCC", lw=0.8)
ax.grid(color="#EEEEEE", lw=0.6)
fig.tight_layout()
fig.savefig(FIG / "fig3_dependence.png", dpi=300)
plt.close(fig)

# Figure 4: burden relative to military spending, top 15
b = cty[cty["B"].notna()].sort_values("B", ascending=False).head(15).copy()
names = c.drop_duplicates("iso3").set_index("iso3")["country"]
b["name"] = names.reindex(b.index).str.replace("United Republic of Tanzania", "Tanzania")
b = b.iloc[::-1]
fig, ax = plt.subplots(figsize=(6.5, 4.0))
ax.barh(b["name"], b["B"], color=ACCENT)
for i, v in enumerate(b["B"]):
    ax.text(v + 0.2, i, f"{v:.1f}", va="center", fontsize=8)
ax.set_xlabel("Annual UN payments lost, % of 2024 military spending")
fig.tight_layout()
fig.savefig(FIG / "fig4_burden.png", dpi=300)
plt.close(fig)
print("figures written:", sorted(p.name for p in FIG.glob("*.png")))
