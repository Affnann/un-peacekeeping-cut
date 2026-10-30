"""Checks added after the main results were seen (NOT in the analysis plan).

Each is labelled as such in tables/extra_checks.csv and in the paper:
  X1  H2 with ln P_c0 (contingent size) as a control: is it dependence or just size?
  X2  H2 without the four countries with D of 10% or more (influence of the most dependent group)
  X3  H2 leaving out one country at a time among the 10 largest weights (influence)
  X4  H2 without South Africa, whose contingent fell by 93%
  X5  H1 without South Africa (diagnostic for H1's low R-squared)
  X6  Placebo C3 with UNSOM and its successor UNTMIS (S/RES/2753 (2024)) treated as one mission;
      the plan's literal definitions treat UNSOM as closing and UNTMIS as new

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
for iso in s.sort_values("x0", ascending=False).head(10).index:
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

out = pd.DataFrame(rows)
(ROOT / "tables").mkdir(exist_ok=True)
out.to_csv(ROOT / "tables" / "extra_checks.csv", index=False)
print(out.to_string(index=False))
