"""Checks added after the main results were seen (NOT in the analysis plan).

Each is labelled as such in tables/extra_checks.csv and in the paper:
  X1  H2 with ln P_c0 (contingent size) as a control: is it dependence or just size?
  X2  H2 without the four countries with D of 10% or more (influence of the most dependent group)
  X3  H2 leaving out one country at a time among the 10 largest contributors by June 2025 personnel
      (11 countries: Ethiopia and Tanzania tie for tenth place with 1,533 each; ties share the rank)
  X4  H2 without South Africa, whose contingent fell by 93%
  X5  H1 without South Africa (diagnostic for H1's low R-squared)
  X6  Placebo C3 with UNSOM and UNTMIS treated as one mission: S/RES/2753 (2024), para. 2, decided that
      UNSOM "shall be called" UNTMIS and that UNTMIS "shall begin the formal transition of its functions
      from 1 November 2024"; the UN's figures list the mission as UNTMIS from November 2024, and the plan's
      literal definitions treat UNSOM as closing and UNTMIS as new
  X7  The cut by contributor size (the 10 largest by June 2025 personnel, 11 countries because of the tie;
      other countries with 100 or more; 20 to 99; under 20), and a weighted quadratic in ln P_c0 with a
      joint Wald test of its two terms, to compare with Coleman and Li (2026). The size groups are the
      author's own and are no longer reported in the paper (see X11); the quadratic still is.
  X8  C5 with dependence D measured from all missions (in C5 every measure comes from the remaining missions)
  X9  C5 excluding only UNAMI, UNMHA and UNVMC, where the Council's decision itself removed personnel in the
      window; MINUSCA's and UNMISS's new ceilings were above their strength when adopted
  (X8 and X9 were decided before C5 was run.)
  X10 H3 with standard errors clustered by mission (CR1, t with G - 1 degrees of freedom) and a wild cluster
      bootstrap p-value (null imposed, Webb six-point weights), computed exactly over every combination of
      weights for the missions whose restricted residuals are not all zero (seven of the ten: the two
      single-cell missions and UNAMI, whose two cells both fell by 100 percent, have zero residuals, so their
      weights cannot change the statistic); the plan ruled out clustering because there are only ten missions
  X11 The cut by Coleman and Li's (2026, pp. 1130-1131) three types of troop contribution, replacing X7's
      size groups in the paper: military personnel (troops, staff officers, military experts on mission)
      by country and mission, in missions deploying at least 1,000 troops; "top" = every contribution of
      the UN's top 10 troop contributors (here ranked by military personnel in June 2025); "token" = a
      contribution of fewer than 40 troops and fewer than 10 military observers or staff officers
      (read as staff officers plus experts on mission below 10) by any other country; "other" = the rest.
      Classified in June 2025 and followed to July 2026. Output: tables/coleman_li_types.csv, and the
      same under two other readings (the token limit applied separately; Tanzania, level with Ethiopia in
      tenth place by all uniformed personnel, counted as a top contributor): tables/coleman_li_readings.csv
  X12 Bangladesh's fall in uniformed personnel by mission, September 2025 to July 2026, against the
      numbers that a UN letter of 14 October 2025 set out for each mission, as reported by Prothom Alo
      (19 October 2025). Output: tables/bangladesh_letter.csv

Usage: python code/02_extra_checks.py  (after code/01_analysis.py)
"""

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
cty = pd.read_csv(ROOT / "data" / "build" / "country_changes_main.csv", index_col="iso3")
s = cty[(cty["x0"] >= 100) & cty["D"].notna() & (cty["D"] > 0)].copy()
s["lnD"] = np.log(s["D"])
s["lnP0"] = np.log(s["x0"])


def fit(df, xcols):
    X = sm.add_constant(df[xcols].astype(float), has_constant="add")
    r = sm.WLS(df["pct"].astype(float), X, weights=df["x0"].astype(float)).fit(cov_type="HC1")
    return r


rows = []
r = fit(s, ["lnD", "lnP0"])
rows.append({"check": "X1 H2 with ln P0 control", "coef_lnD": r.params["lnD"], "se": r.bse["lnD"], "p": r.pvalues["lnD"],
             "coef_lnP0": r.params["lnP0"], "p_lnP0": r.pvalues["lnP0"], "n": int(r.nobs)})
s2 = s[s["D"] < 10]
r = fit(s2, ["lnD"])
rows.append({"check": "X2 H2 without D >= 10%", "coef_lnD": r.params["lnD"], "se": r.bse["lnD"], "p": r.pvalues["lnD"], "n": int(r.nobs),
             "dropped": ",".join(sorted(s[s["D"] >= 10].index))})
TOP10 = s.index[s["x0"].rank(method="min", ascending=False) <= 10]  # ties share the rank: 11 countries
for iso in s.loc[TOP10].sort_values("x0", ascending=False).index:
    r = fit(s.drop(index=iso), ["lnD"])
    rows.append({"check": f"X3 H2 without {iso}", "coef_lnD": r.params["lnD"], "se": r.bse["lnD"], "p": r.pvalues["lnD"], "n": int(r.nobs)})
r = fit(s.drop(index="ZAF"), ["lnD"])
rows.append({"check": "X4 H2 without ZAF", "coef_lnD": r.params["lnD"], "se": r.bse["lnD"], "p": r.pvalues["lnD"], "n": int(r.nobs)})

# X5: H1 without South Africa
h = cty[cty["x0"] >= 100].drop(index="ZAF")
X = sm.add_constant(h[["E_pct"]].astype(float), has_constant="add")
r = sm.WLS(h["pct"].astype(float), X, weights=h["x0"].astype(float)).fit(cov_type="HC1")
rows.append({"check": "X5 H1 without ZAF", "coef_lnD": np.nan, "slope_H1": r.params["E_pct"], "se": r.bse["E_pct"],
             "p": r.pvalues["E_pct"], "r2": r.rsquared, "n": int(r.nobs)})

# X6: placebo with UNSOM and UNTMIS merged
import importlib.util
spec = importlib.util.spec_from_file_location("a", ROOT / "code" / "01_analysis.py")
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
c = a.load_un()
c = c.copy()
c.loc[c["mission"].isin(["UNSOM", "UNTMIS"]), "mission"] = "UNSOM/UNTMIS"
milex = a.load_wb("MS.MIL.XPND.CD")
gdppc = a.load_wb("NY.GDP.PCAP.CD")
t0, t1, yr = a.WINDOWS["C3_placebo"]
res, *_ = a.run_tests(c, "X6 placebo, UNSOM and UNTMIS merged (P)", t0, t1, yr, a.P_CATS, milex, gdppc)
for x in res:
    if x["test"].startswith("H1") or x["test"].startswith("H2 total") or x["test"].startswith("H3"):
        rows.append({"check": f"X6 {x['test']}", "coef_lnD": x["coef"] if not x["test"].startswith("H1") else np.nan,
                     "slope_H1": x["coef"] if x["test"].startswith("H1") else np.nan,
                     "se": x["se"], "p": x["p"], "r2": x["r2"], "n": x["n"]})

# X7: size groups and a quadratic in ln P0
a7 = cty[cty["x0"] > 0].sort_values("x0", ascending=False).copy()
a7["rank"] = a7["x0"].rank(method="min", ascending=False)  # ties share the rank (Ethiopia and Tanzania, 10th)
a7["size_group"] = np.select(
    [a7["rank"] <= 10, a7["x0"] >= 100, a7["x0"] >= 20],
    ["1 top 10", "2 other, 100 or more", "3 20 to 99"], default="4 under 20")
sg = a7.groupby("size_group").agg(countries=("x0", "size"), P0=("x0", "sum"), P1=("x1", "sum"), median_pct=("pct", "median"))
sg["pct"] = 100 * (sg["P1"] - sg["P0"]) / sg["P0"]
sg.to_csv(ROOT / "tables" / "size_groups.csv")
q = cty[cty["x0"] >= 100].copy()
q["lnP0"] = np.log(q["x0"])
q["lnP0sq"] = q["lnP0"] ** 2
X = sm.add_constant(q[["lnP0", "lnP0sq"]].astype(float), has_constant="add")
r = sm.WLS(q["pct"].astype(float), X, weights=q["x0"].astype(float)).fit(cov_type="HC1")
wt = r.wald_test("lnP0 = 0, lnP0sq = 0", scalar=True)
rows.append({"check": "X7 weighted quadratic in ln P0", "coef_lnP0": r.params["lnP0"], "p_lnP0": r.pvalues["lnP0"],
             "coef_lnP0sq": r.params["lnP0sq"], "p_lnP0sq": r.pvalues["lnP0sq"], "n": int(r.nobs),
             "joint_chi2": float(wt.statistic), "joint_p": float(wt.pvalue)})

# X8 and X9: variants of C5
t0m, t1m, yrm = a.WINDOWS["main"]
c0 = a.load_un()
for tag, excl, dfrom in [("X8 C5 with D from all missions", a.C5_MISSIONS, cty["D"]),
                         ("X9 C5 without only UNAMI, UNMHA and UNVMC", ["UNAMI", "UNMHA", "UNVMC"], None)]:
    res, *_ = a.run_tests(c0, tag, t0m, t1m, yrm, a.P_CATS, milex, gdppc, exclude_missions=excl, d_from=dfrom)
    for x in res:
        if x["test"].startswith("H1") or x["test"].startswith("H2 total") or x["test"].startswith("H3"):
            rows.append({"check": f"{tag}: {x['test']}", "coef_lnD": x["coef"] if not x["test"].startswith("H1") else np.nan,
                         "slope_H1": x["coef"] if x["test"].startswith("H1") else np.nan,
                         "se": x["se"], "p": x["p"], "r2": x["r2"], "n": x["n"], "n_missions": x.get("n_missions", np.nan)})

# X10: H3 with standard errors clustered by mission, and a wild cluster bootstrap
cm0 = pd.read_csv(ROOT / "data" / "build" / "country_mission_main.csv")
h = cm0[cm0["x0"] >= a.MIN_CELL].merge(cty[["D"]], left_on="iso3", right_index=True, how="left")
h = h[h["D"].notna() & (h["D"] > 0)].copy()
h["pct"] = 100 * (h["x1"] - h["x0"]) / h["x0"]
h = h.reset_index(drop=True)
fe = pd.get_dummies(h["mission"], prefix="fe", drop_first=True, dtype=float)
Xu = sm.add_constant(pd.concat([pd.DataFrame({"x": np.log(h["D"])}), fe], axis=1), has_constant="add").astype(float)
Xr = sm.add_constant(fe, has_constant="add").astype(float)
y = h["pct"].astype(float).to_numpy()
w = h["x0"].astype(float).to_numpy()
groups = pd.factorize(h["mission"])[0]
G = groups.max() + 1
sw = np.sqrt(w)


def cr1_t(yv):
    """WLS of yv on Xu; returns the coefficient on x and its CR1 t statistic (clusters = missions)."""
    Xt = Xu.to_numpy() * sw[:, None]
    yt = yv * sw
    XtX_inv = np.linalg.inv(Xt.T @ Xt)
    b = XtX_inv @ Xt.T @ yt
    e = yt - Xt @ b
    meat = np.zeros((Xt.shape[1], Xt.shape[1]))
    for g in range(G):
        sg = Xt[groups == g].T @ e[groups == g]
        meat += np.outer(sg, sg)
    n, k = Xt.shape
    adj = G / (G - 1) * (n - 1) / (n - k)
    V = adj * XtX_inv @ meat @ XtX_inv
    j = list(Xu.columns).index("x")
    return b[j], b[j] / np.sqrt(V[j, j]), np.sqrt(V[j, j])


b_hat, t_hat, se_hat = cr1_t(y)
from scipy import stats
p_cr1 = 2 * stats.t.sf(abs(t_hat), G - 1)
# restricted model (null: coefficient on ln D is zero), weighted
rr = sm.WLS(y, Xr, weights=w).fit()
fit_r, e_r = rr.fittedvalues.to_numpy(), rr.resid.to_numpy()
webb = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])
# Exact wild cluster bootstrap. Under the null the bootstrap outcome is fit_r + e_r * v_g; t* is computed
# with the same CR1 variance as t_hat. Missions whose restricted residuals are all zero do not affect t*,
# so every combination of weights for the other missions is enumerated (each equally likely).
Xt = Xu.to_numpy() * sw[:, None]
XtX_inv = np.linalg.inv(Xt.T @ Xt)
jx = list(Xu.columns).index("x")
H = Xt @ XtX_inv[jx]                      # b_x = H . y (in the weighted space)
Mres = np.eye(len(y)) - Xt @ XtX_inv @ Xt.T  # residual maker
n_obs, k_par = Xt.shape
adj = G / (G - 1) * (n_obs - 1) / (n_obs - k_par)
Gmat = np.zeros((len(y), G))
Gmat[np.arange(len(y)), groups] = 1.0
yt_fit, et_r = fit_r * sw, e_r * sw
informative = [g for g in range(G) if np.abs(e_r[groups == g]).max() > 1e-9]
n_comb = 6 ** len(informative)
exceed = 0
for start in range(0, n_comb, 100_000):
    codes = np.arange(start, min(start + 100_000, n_comb))
    V = np.ones((len(codes), G))
    for pos, g in enumerate(informative):
        V[:, g] = webb[(codes // 6 ** pos) % 6]
    Ys = yt_fit[None, :] + et_r[None, :] * V[:, groups]
    bx = Ys @ H
    U = ((Ys @ Mres) * H[None, :]) @ Gmat
    t_star = bx / np.sqrt(adj * (U ** 2).sum(axis=1))
    exceed += int((np.abs(t_star) >= abs(t_hat) - 1e-12).sum())
p_wcb = exceed / n_comb
# check the vectorised statistic against a full re-estimation for a few weight combinations
for code in [0, 12345, n_comb - 1]:
    v = np.ones(G)
    for pos, g in enumerate(informative):
        v[g] = webb[(code // 6 ** pos) % 6]
    Ys1 = (yt_fit + et_r * v[groups])[None, :]
    U1 = ((Ys1 @ Mres) * H[None, :]) @ Gmat
    t1 = float((Ys1 @ H)[0] / np.sqrt(adj * (U1 ** 2).sum()))
    assert abs(t1 - cr1_t(fit_r + e_r * v[groups])[1]) < 1e-9
mission_names = pd.factorize(h["mission"])[1]
print(f"X10 wild cluster bootstrap: {len(informative)} informative missions "
      f"({', '.join(mission_names[g] for g in informative)}), {n_comb:,} combinations, p = {p_wcb:.4f}")
rows.append({"check": "X10 H3 clustered by mission (CR1; wild cluster bootstrap)", "coef_lnD": b_hat, "se": se_hat,
             "p": p_cr1, "p_wild_bootstrap": p_wcb, "n": len(h), "n_missions": int(G)})

# X11: the cut by Coleman and Li's (2026) types of troop contribution
MIL = ["troops", "staff_officers", "experts_on_mission"]


def mil_cells(month):
    d = c0[(c0["month"] == month) & c0["category"].isin(MIL)]
    p = d.pivot_table(index=["iso3", "mission"], columns="category", values="total", aggfunc="sum",
                      fill_value=0).reindex(columns=MIL, fill_value=0)
    p["mil"] = p[MIL].sum(axis=1)
    return p


def cl_types(token_rule="sum", extra_top=()):
    m0, m1 = mil_cells(t0m), mil_cells(t1m)
    troops_m = m0.groupby("mission")["troops"].sum()
    big = sorted(troops_m[troops_m >= 1000].index)  # missions "deploying at least 1000 troops"
    rank = m0.groupby("iso3")["mil"].sum().sort_values(ascending=False)
    assert rank.iloc[9] > rank.iloc[10], "tie at tenth place"
    top10 = list(rank.index[:10]) + list(extra_top)
    q = m0[m0.index.get_level_values("mission").isin(big) & (m0["mil"] > 0)].copy()
    q["mil1"] = m1["mil"].reindex(q.index).fillna(0)
    iso = q.index.get_level_values("iso3")
    so_ex = q["staff_officers"] + q["experts_on_mission"]
    small = (q["troops"] < 40) & ((so_ex < 10) if token_rule == "sum" else
                                  ((q["staff_officers"] < 10) & (q["experts_on_mission"] < 10)))
    q["type"] = np.select([iso.isin(top10), small], ["1 top 10", "3 token"], default="2 other")
    q["pct"] = 100 * (q["mil1"] - q["mil"]) / q["mil"]
    new = m1[m1.index.get_level_values("mission").isin(big) & ~m1.index.isin(q.index) & (m1["mil"] > 0)]
    return q, big, top10, new


def summarise(q):
    g = q.groupby("type")
    t = pd.DataFrame({
        "contributions": g.size(),
        "countries": g.apply(lambda d: d.index.get_level_values("iso3").nunique()),
        "mil_2025_06": g["mil"].sum(), "mil_2026_07": g["mil1"].sum(),
        "median_pct": g["pct"].median(), "ended": g.apply(lambda d: int((d["mil1"] == 0).sum())),
        "troops_2025_06": g["troops"].sum(), "staff_officers_2025_06": g["staff_officers"].sum(),
        "experts_2025_06": g["experts_on_mission"].sum()})
    t.loc["4 all"] = [len(q), q.index.get_level_values("iso3").nunique(), q["mil"].sum(), q["mil1"].sum(),
                      q["pct"].median(), int((q["mil1"] == 0).sum()), q["troops"].sum(),
                      q["staff_officers"].sum(), q["experts_on_mission"].sum()]
    t["pct"] = 100 * (t["mil_2026_07"] - t["mil_2025_06"]) / t["mil_2025_06"]
    t["share_2025_06"] = 100 * t["mil_2025_06"] / q["mil"].sum()
    ints = ["contributions", "countries", "mil_2025_06", "mil_2026_07", "ended", "troops_2025_06",
            "staff_officers_2025_06", "experts_2025_06"]
    t[ints] = t[ints].astype(int)
    return t


q11, big11, top11, new11 = cl_types("sum")
t11 = summarise(q11)
t11.round(4).to_csv(ROOT / "tables" / "coleman_li_types.csv")
print("X11 missions:", ", ".join(big11))
print("X11 top 10:", ", ".join(top11))
print("X11 cells only in July 2026:", len(new11), "with", int(new11["mil"].sum()), "military personnel")
print(t11.round(2).to_string())
# Other readings: the token rule applied to staff officers and experts separately; Tanzania, level with
# Ethiopia in tenth place by all uniformed personnel in June 2025, counted as a top contributor
var = []
for reading, kw in [("main", {}), ("token limit of 10 applied separately", {"token_rule": "each"}),
                    ("Tanzania also counted as a top contributor", {"extra_top": ("TZA",)})]:
    qv, *_ = cl_types(**kw)
    tv = summarise(qv)
    tv.insert(0, "reading", reading)
    var.append(tv[["reading", "contributions", "mil_2025_06", "mil_2026_07", "pct", "median_pct", "ended"]])
var = pd.concat(var)
var.loc["5 only in July 2026"] = ["main", len(new11), 0, int(new11["mil"].sum()), np.nan, np.nan, 0]
var.round(4).to_csv(ROOT / "tables" / "coleman_li_readings.csv")
print("X11 under other readings:")
print(var.round(2).to_string())
rows.append({"check": "X11 Coleman and Li (2026) contribution types: see tables/coleman_li_types.csv",
             "n": len(q11), "n_missions": len(big11)})

# X12: Bangladesh by mission against the reported UN letter of 14 October 2025
# Numbers to be withdrawn per mission, as reported by Prothom Alo, "UN fund crisis: 1,313 Bangladeshi
# peacekeepers to return home", 19 October 2025, https://en.prothomalo.com/bangladesh/70bdwl7uuz
LETTER = {"UNMISS": 617, "MINUSCA": 341, "UNISFA": 268, "MONUSCO": 79, "MINURSO": 8}
bgd = (c0[(c0["iso3"] == "BGD") & c0["month"].isin(["2025-09", "2026-07"]) & c0["category"].isin(a.P_CATS)]
       .pivot_table(index="mission", columns="month", values="total", aggfunc="sum", fill_value=0))
bgd["fall"] = bgd["2025-09"] - bgd["2026-07"]
bgd["letter"] = pd.Series(LETTER).reindex(bgd.index)
bgd.loc["total"] = bgd.sum()
bgd = bgd.astype("Int64")
bgd.to_csv(ROOT / "tables" / "bangladesh_letter.csv")
print("X12 Bangladesh, September 2025 to July 2026, against the reported letter:")
print(bgd.to_string())
rows.append({"check": "X12 Bangladesh by mission against the reported UN letter: see tables/bangladesh_letter.csv",
             "n": int(len(bgd) - 1)})

out = pd.DataFrame(rows)
(ROOT / "tables").mkdir(exist_ok=True)
out.to_csv(ROOT / "tables" / "extra_checks.csv", index=False)
print(out.to_string(index=False))
