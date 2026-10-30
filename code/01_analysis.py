"""Who bore the 2025-26 cut in UN peacekeeping? Main analysis.

Implements plan/analysis_plan.md (written 30 October 2026, before any result).

Inputs
  external/peacekeeping-tracker/data/build/contributions_monthly.csv
      UN uniformed personnel by month, country, mission and category, rebuilt
      with peacekeeping-tracker v1.0.0 (see code/00_get_un_data.py).
  data/worldbank/worldbank_MS.MIL.XPND.CD.json.gz   military expenditure, current US$
  data/worldbank/worldbank_NY.GDP.PCAP.CD.json.gz   GDP per capita, current US$

Outputs
  data/build/        full country and country-mission tables (contain UN figures; not in the repository)
  tables/            summary tables
  results/main_results.md

Usage: python code/01_analysis.py
"""

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
UN_FILE = ROOT / "external" / "peacekeeping-tracker" / "data" / "build" / "contributions_monthly.csv"
WB_DIR = ROOT / "data" / "worldbank"
BUILD = ROOT / "data" / "build"
TABLES = ROOT / "tables"
RESULTS = ROOT / "results"

RATE = 1448.0  # US$ per person per month, A/RES/76/276 para. 9 (July 2022 to June 2026)
P_CATS = ["troops", "staff_officers", "experts_on_mission", "police_individual", "police_formed_units"]
K_CATS = ["troops", "police_formed_units"]
MAIN_MIN_COUNTRY = 100
MIN_CELL = 50

WINDOWS = {
    "main": ("2025-06", "2026-07", 2024),
    "C1_sep2025": ("2025-09", "2026-07", 2024),
    "C3_placebo": ("2024-05", "2025-06", 2023),
}

# C5 (plan, section 5): missions whose reduction during the main window was decided separately by the
# Security Council, through a mandated closure or a lower authorised strength. Identified from the
# resolutions on 30 October 2026, before this check was run:
#   MINUSCA  S/RES/2800 (2025), 13 Nov 2025: up to 14,046 military and 2,999 police personnel
#            (from 14,400 and 3,020 in S/RES/2759 (2024))
#   UNMISS   S/RES/2820 (2026), 30 Apr 2026: troop ceiling 12,500 (from 17,000 in S/RES/2779 (2025));
#            police ceiling unchanged at 2,101
#   UNAMI    S/RES/2732 (2024): a final period to 31 Dec 2025, after which the mission ceased all work
#   UNMHA    S/RES/2813 (2026), 27 Jan 2026: a final period to 31 Mar 2026, then liquidation
#   UNVMC    S/RES/2798 (2025), 31 Oct 2025: discontinued the ceasefire-monitoring expansion of
#            S/RES/2694 (2023) "and its associated resources" (2694 had added up to 68 international observers)
# Not excluded: UNIFIL (S/RES/2790 (2025): operations cease on 31 Dec 2026, after the window), UNTMIS
# (S/RES/2809 (2025): operations cease on 31 Oct 2026, after the window), and the missions whose renewals
# in the window kept their ceilings (MONUSCO, S/RES/2808 (2025); UNISFA, S/RES/2802 (2025)) or set none
# (UNDOF, UNFICYP, MINURSO).
C5_MISSIONS = ["MINUSCA", "UNMISS", "UNAMI", "UNMHA", "UNVMC"]


# ---------------------------------------------------------------- data

def load_un() -> pd.DataFrame:
    c = pd.read_csv(UN_FILE, dtype={"month": str})
    return c


def load_wb(indicator: str) -> pd.DataFrame:
    raw = json.load(gzip.open(WB_DIR / f"worldbank_{indicator}.json.gz"))
    rows = raw[1] if isinstance(raw, list) else raw
    df = pd.DataFrame(
        {
            "iso3": [r.get("countryiso3code") for r in rows],
            "year": [int(r["date"]) for r in rows],
            "value": [r.get("value") for r in rows],
        }
    )
    df = df[df["iso3"].notna() & (df["iso3"] != "")]
    return df.dropna(subset=["value"])


def wb_year(df: pd.DataFrame, year: int) -> pd.Series:
    s = df[df["year"] == year].set_index("iso3")["value"].astype(float)
    return s[~s.index.duplicated()]


def cells(c: pd.DataFrame, month: str, cats: list) -> pd.Series:
    """Personnel by (iso3, mission) in one month, summed over the given categories.
    Rows with no number are missing and add nothing."""
    m = c[(c["month"] == month) & (c["category"].isin(cats))]
    s = m.groupby(["iso3", "mission"])["total"].sum(min_count=1).dropna()
    return s[s > 0]


# ---------------------------------------------------------------- window computations

def window_tables(c, t0, t1, cats):
    a = cells(c, t0, cats).rename("x0")
    b = cells(c, t1, cats).rename("x1")
    cm = pd.concat([a, b], axis=1).fillna(0.0).reset_index()
    mis = cm.groupby("mission")[["x0", "x1"]].sum()
    mis["change"] = mis["x1"] - mis["x0"]
    mis["g"] = np.where(mis["x0"] > 0, mis["change"] / mis["x0"].where(mis["x0"] > 0), np.nan)
    cm = cm.merge(mis[["g"]], left_on="mission", right_index=True, how="left")
    cm["exposure"] = np.where(cm["x0"] > 0, cm["x0"] * cm["g"], 0.0)
    cty = cm.groupby("iso3").agg(x0=("x0", "sum"), x1=("x1", "sum"), E=("exposure", "sum"))
    cty["dx"] = cty["x1"] - cty["x0"]
    cty["W"] = cty["dx"] - cty["E"]
    cty["pct"] = np.where(cty["x0"] > 0, 100 * cty["dx"] / cty["x0"].where(cty["x0"] > 0), np.nan)
    cty["E_pct"] = np.where(cty["x0"] > 0, 100 * cty["E"] / cty["x0"].where(cty["x0"] > 0), np.nan)
    cty["W_pct"] = np.where(cty["x0"] > 0, 100 * cty["W"] / cty["x0"].where(cty["x0"] > 0), np.nan)
    return cm, mis, cty


def add_money(c, cty, t0, t1, milex_year, milex, gdppc, gdppc_year):
    k0 = cells(c, t0, K_CATS).groupby(level=0).sum()
    k1 = cells(c, t1, K_CATS).groupby(level=0).sum()
    out = cty.copy()
    out["K0"] = k0.reindex(out.index).fillna(0.0)
    out["K1"] = k1.reindex(out.index).fillna(0.0)
    out["dM_usd"] = (out["K1"] - out["K0"]) * 12 * RATE
    mx = wb_year(milex, milex_year)
    out["milex_usd"] = mx.reindex(out.index)
    out["D"] = 100 * out["K0"] * 12 * RATE / out["milex_usd"]
    out["D_t1"] = 100 * out["K1"] * 12 * RATE / out["milex_usd"]
    out["B"] = -100 * out["dM_usd"] / out["milex_usd"]
    out["gdppc"] = wb_year(gdppc, gdppc_year).reindex(out.index)
    return out


# ---------------------------------------------------------------- regressions

def wls(y, x, w, fe=None):
    X = pd.DataFrame({"x": x})
    if fe is not None:
        d = pd.get_dummies(fe, prefix="fe", drop_first=True, dtype=float)
        X = pd.concat([X, d.set_index(X.index)], axis=1)
    X = sm.add_constant(X, has_constant="add")
    if w is None:
        res = sm.OLS(y.astype(float), X.astype(float)).fit(cov_type="HC1")
    else:
        res = sm.WLS(y.astype(float), X.astype(float), weights=w.astype(float)).fit(cov_type="HC1")
    return {
        "coef": res.params["x"],
        "se": res.bse["x"],
        "p": res.pvalues["x"],
        "ci_lo": res.conf_int().loc["x", 0],
        "ci_hi": res.conf_int().loc["x", 1],
        "r2": res.rsquared,
        "n": int(res.nobs),
    }


def run_tests(c, label, t0, t1, milex_year, cats, milex, gdppc, min_country=MAIN_MIN_COUNTRY,
              weighted=True, exclude_missions=None, use_gdppc=False, d_from=None):
    """d_from: optional Series of D by country to use instead of D computed from the data passed in
    (used for a C5 variant in which dependence is measured from all missions)."""
    cdat = c if not exclude_missions else c[~c["mission"].isin(exclude_missions)]
    cm, mis, cty = window_tables(cdat, t0, t1, cats)
    cty = add_money(cdat, cty, t0, t1, milex_year, milex, gdppc, milex_year)
    if d_from is not None:
        cty["D"] = d_from.reindex(cty.index)
    rows = []
    s = cty[cty["x0"] >= min_country]
    w = s["x0"] if weighted else None
    r = wls(s["pct"], s["E_pct"], w)
    rows.append({"spec": label, "test": "H1 pct on exposure pct", **r})
    # H2 / C4
    if use_gdppc:
        s2 = s[s["gdppc"].notna() & (s["gdppc"] > 0)]
        xvar = np.log(s2["gdppc"])
        name = "ln GDP per capita"
    else:
        s2 = s[s["D"].notna() & (s["D"] > 0)]
        xvar = np.log(s2["D"])
        name = "ln D"
    w2 = s2["x0"] if weighted else None
    for dep, tag in [("pct", "total"), ("E_pct", "exposure part"), ("W_pct", "within-mission part")]:
        r = wls(s2[dep], xvar, w2)
        rows.append({"spec": label, "test": f"H2 {tag} on {name}", **r})
    # H3 / C4
    cmc = cm[cm["x0"] >= MIN_CELL].merge(cty[["D", "gdppc"]], left_on="iso3", right_index=True, how="left")
    if use_gdppc:
        cmc = cmc[cmc["gdppc"].notna() & (cmc["gdppc"] > 0)]
        xv = np.log(cmc["gdppc"])
    else:
        cmc = cmc[cmc["D"].notna() & (cmc["D"] > 0)]
        xv = np.log(cmc["D"])
    cmc = cmc.copy()
    cmc["pct"] = 100 * (cmc["x1"] - cmc["x0"]) / cmc["x0"]
    if len(cmc) > 0 and cmc["mission"].nunique() > 1:
        r = wls(cmc["pct"], xv, cmc["x0"] if weighted else None, fe=cmc["mission"].reset_index(drop=True).set_axis(cmc.index))
        rows.append({"spec": label, "test": f"H3 cell pct on {name}, mission FE", **r,
                     "n_missions": int(cmc["mission"].nunique())})
    return rows, cm, mis, cty


# ---------------------------------------------------------------- main

def main():
    BUILD.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    c = load_un()
    milex = load_wb("MS.MIL.XPND.CD")
    gdppc = load_wb("NY.GDP.PCAP.CD")

    months_needed = {m for w in WINDOWS.values() for m in w[:2]}
    na_rows = c[c["month"].isin(months_needed) & c["total"].isna()]

    t0, t1, my = WINDOWS["main"]
    reg_rows = []

    # main, all personnel
    rows, cm, mis, cty = run_tests(c, "main (P)", t0, t1, my, P_CATS, milex, gdppc)
    reg_rows += rows
    cty_main, cm_main, mis_main = cty, cm, mis
    cty_main.to_csv(BUILD / "country_changes_main.csv")
    cm_main.to_csv(BUILD / "country_mission_main.csv", index=False)

    # checks
    for label, (a, b, yr) in WINDOWS.items():
        if label == "main":
            continue
        r, *_ = run_tests(c, f"{label} (P)", a, b, yr, P_CATS, milex, gdppc)
        reg_rows += r
    r, *_ = run_tests(c, "C2 contingent (K)", t0, t1, my, K_CATS, milex, gdppc)
    reg_rows += r
    r, *_ = run_tests(c, "C4 income (P)", t0, t1, my, P_CATS, milex, gdppc, use_gdppc=True)
    reg_rows += [x for x in r if not x["test"].startswith("H1")]
    r, *_ = run_tests(c, "C5 without separately decided drawdowns (P)", t0, t1, my, P_CATS, milex, gdppc,
                      exclude_missions=C5_MISSIONS)
    reg_rows += r
    r, *_ = run_tests(c, "C6 unweighted (P)", t0, t1, my, P_CATS, milex, gdppc, weighted=False)
    reg_rows += [x for x in r if x["test"].startswith("H1") or x["test"].startswith("H2 total")]
    r, *_ = run_tests(c, "C6 threshold 20 (P)", t0, t1, my, P_CATS, milex, gdppc, min_country=20)
    reg_rows += [x for x in r if x["test"].startswith("H1") or x["test"].startswith("H2 total")]

    reg = pd.DataFrame(reg_rows)
    reg.to_csv(TABLES / "regressions.csv", index=False)

    # descriptive (a): missions and categories
    mis_main.sort_values("x0", ascending=False).to_csv(TABLES / "missions_main.csv")
    catrows = []
    for cat in P_CATS:
        a = c[(c["month"] == t0) & (c["category"] == cat)]["total"].sum()
        b = c[(c["month"] == t1) & (c["category"] == cat)]["total"].sum()
        catrows.append({"category": cat, "t0": a, "t1": b, "change": b - a, "pct": 100 * (b - a) / a if a else np.nan})
    cats = pd.DataFrame(catrows)
    cats.to_csv(TABLES / "categories_main.csv", index=False)

    # descriptive (b) top 20 and (e) Bangladesh
    names = c[c["month"] == t1].drop_duplicates("iso3").set_index("iso3")["country"]
    names = names.combine_first(c[c["month"] == t0].drop_duplicates("iso3").set_index("iso3")["country"])
    top = cty_main.sort_values("x0", ascending=False).head(20).copy()
    top.insert(0, "country", names.reindex(top.index))
    top[["country", "x0", "x1", "dx", "pct", "E", "W", "K0", "K1", "dM_usd", "milex_usd", "D", "B"]].to_csv(TABLES / "top20_main.csv")

    # descriptive (c) and (d): dependence groups
    def grp(d):
        if pd.isna(d):
            return "no military spending data"
        if d >= 10:
            return "D >= 10%"
        if d >= 1:
            return "1% <= D < 10%"
        return "D < 1%"

    g = cty_main.copy()
    g["group"] = g["D"].map(grp)
    total_fall = -g.loc[g["dM_usd"] < 0, "dM_usd"].sum()
    net_fall = -g["dM_usd"].sum()
    gt = g.groupby("group").agg(
        countries=("x0", "size"),
        P0=("x0", "sum"),
        P1=("x1", "sum"),
        dM_usd=("dM_usd", "sum"),
        median_B_all=("B", "median"),
    )
    gt["share_of_net_fall_pct"] = 100 * (-gt["dM_usd"]) / net_fall
    main_s = g[g["x0"] >= MAIN_MIN_COUNTRY]
    gt["median_B_main_sample"] = main_s.groupby("group")["B"].median()
    gt["countries_main_sample"] = main_s.groupby("group")["x0"].size()
    gt.to_csv(TABLES / "dependence_groups_main.csv")
    n_d10_t0 = int((g["D"] >= 10).sum())
    n_d10_t1 = int((g["D_t1"] >= 10).sum())

    # report
    lines = []
    lines.append("# Main results (computed by code/01_analysis.py)\n")
    lines.append(f"Main window: {t0} to {t1}; dependence uses military spending of {my}.\n")
    lines.append(f"UN rows with no number in the months used: {len(na_rows)}\n")
    P0 = cty_main["x0"].sum(); P1 = cty_main["x1"].sum()
    K0 = cty_main["K0"].sum(); K1 = cty_main["K1"].sum()
    lines.append(f"Total P: {P0:,.0f} -> {P1:,.0f} (change {P1-P0:,.0f}, {100*(P1-P0)/P0:.2f}%)")
    lines.append(f"Total K: {K0:,.0f} -> {K1:,.0f} (change {K1-K0:,.0f}, {100*(K1-K0)/K0:.2f}%)")
    lines.append(f"Countries with P>0 at t0: {(cty_main['x0']>0).sum()}, at t1: {(cty_main['x1']>0).sum()}; main sample (P0>=100): {(cty_main['x0']>=100).sum()}")
    lines.append(f"Annualised change in payments owed (all countries): {cty_main['dM_usd'].sum()/1e6:,.2f} million US$")
    lines.append(f"Sum |dP| = {cty_main['dx'].abs().sum():,.1f}; sum |E| = {cty_main['E'].abs().sum():,.1f}; sum |W| = {cty_main['W'].abs().sum():,.1f}; sum W = {cty_main['W'].sum():,.3f}")
    new_m = mis_main[mis_main["x0"] == 0]
    lines.append(f"Missions with no personnel at t0 but some at t1: {list(new_m.index)} ({new_m['x1'].sum():,.0f} personnel)")
    lines.append(f"Countries with D >= 10% at t0: {n_d10_t0}; at t1 (2024 spending): {n_d10_t1}")
    nod = cty_main[(cty_main['x0'] >= 100) & (cty_main['milex_usd'].isna())]
    lines.append(f"Main-sample countries without {my} military spending: {list(nod.index)}")
    lines.append("\n## Regressions\n")
    lines.append(reg.to_string(index=False))
    lines.append("\n## Missions (main)\n")
    lines.append(mis_main.sort_values("x0", ascending=False).to_string())
    lines.append("\n## Categories (main)\n")
    lines.append(cats.to_string(index=False))
    lines.append("\n## Top 20 (main)\n")
    lines.append(top[["country", "x0", "x1", "dx", "pct", "E", "W", "dM_usd", "D", "B"]].to_string())
    lines.append("\n## Dependence groups (main)\n")
    lines.append(gt.to_string())
    bgd = cty_main.loc["BGD"]
    lines.append("\n## Bangladesh\n")
    lines.append(bgd.to_string())
    (RESULTS / "main_results.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:14]))


if __name__ == "__main__":
    main()
