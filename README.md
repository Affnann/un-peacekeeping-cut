# un-peacekeeping-cut

Replication package for the working paper *The 2025–26 UN Peacekeeping Cuts and the Countries That Supply the Troops: Evidence from Monthly Deployment Data* (Kazi Affnann Azom, 2026).

Between June 2025 and July 2026 the number of uniformed personnel in UN missions fell by 16,480, or 26.9%, after the UN, short of cash because member states had not paid their contributions in full, told its peacekeeping missions in October 2025 to cut their spending by 15%. This package measures which contributing countries bore that cut, in people and in UN payments, and whether it fell harder on the countries that depend most on those payments.

## Main results

- **The cut fell harder on the countries most dependent on UN payments.** A country whose payments were ten times larger relative to its military budget lost about 4.6 percentage points more of its personnel (coefficient on ln *D* = -2.01, 95% interval -2.94 to -1.07). About a third of this came from the missions such countries served in, and two-thirds from within-mission differences: within the same mission, their contingents were cut more on average. At the level of country-mission cells this test is significant with heteroskedasticity-robust standard errors (p = 0.012) but not with standard errors clustered by mission (p = 0.146; wild cluster bootstrap p = 0.32), a check not in the plan.
- **Missions explain little of the variation between countries.** The four largest missions were each cut by 24.5% to 33.3%, so the change predicted from a country's missions varies little; the weighted R² of the actual on the predicted change is 0.12, below the 0.5 the analysis plan set, so H1 fails.
- **The money.** At the UN's standard rate of US$1,448 per person per month, payments owed to contributing governments fell by US$259.6 million a year. Rwanda's lost payments equal 17.4% of its 2024 military spending, Nepal's 7.1% and Ghana's 4.2%. Bangladesh's fell by US$28.0 million a year (0.75%).
- **Neither the largest nor the token contributors were shielded** (a comparison added after the main results, with the definitions of [Coleman and Li (2026)](https://doi.org/10.1080/13523260.2026.2704869), who found both relatively shielded from downsizing in 2010–2024). In the six missions with at least 1,000 troops, the military personnel of the ten largest troop contributors fell by 27.0% between June 2025 and July 2026, other contributions by 26.7% and token contributions (fewer than 40 troops and fewer than 10 staff officers and military experts) by 35.3%; 16 of the 154 token contributions ended.
- **Checks.** The results hold from a September 2025 baseline and for troops and formed police units only, and a placebo over the 13 months before the cut shows no dependence gradient. In checks added after the main results they also hold with a size control and without South Africa or the most dependent countries. Without the five missions whose reductions the Security Council decided separately, among them MINUSCA and UNMISS (check C5), the estimates keep their size but lose precision (H2 -1.91, p = 0.049; H3 -1.78, p = 0.134). Unweighted, the gradient is not significant and comes mostly from the missions countries served in: it rests on the large contingents.

The analysis plan was written before any of these results were computed and is the first commit of this repository: [`plan/analysis_plan.md`](plan/analysis_plan.md). Its change log records everything added later.

## What is in this repository

| Path | Contents |
|---|---|
| [`plan/analysis_plan.md`](plan/analysis_plan.md) | The dated analysis plan: question, definitions, hypotheses, checks |
| [`code/00_get_un_data.py`](code/00_get_un_data.py) | Rebuilds the UN personnel data with peacekeeping-tracker v1.0.0 (downloads the UN's files from the UN) |
| [`code/01_analysis.py`](code/01_analysis.py) | The analysis set out in the plan |
| [`code/02_extra_checks.py`](code/02_extra_checks.py) | Twelve analyses (X1 to X12) added after the main results were seen, labelled as such in the paper and recorded in the plan's change log |
| [`code/03_figures.py`](code/03_figures.py) | The four figures |
| [`data/worldbank/`](data/worldbank/) | World Bank military expenditure and GDP per capita files (CC BY 4.0), as downloaded on 29 October 2026 |
| [`tables/`](tables/) | Summary tables: missions, categories, the 20 largest contributors, dependence groups, size groups, Coleman and Li's types of contribution, Bangladesh's fall by mission against a reported UN letter, all regressions and checks |
| [`figures/`](figures/) | The figures (300 dpi) |
| [`results/main_results.md`](results/main_results.md) | Every number the analysis computes, in one file |

## Why the full UN dataset is not here

The UN's terms of use allow its data to be downloaded for personal, non-commercial use, but not redistributed. This repository therefore contains no UN files and no full country table. `code/00_get_un_data.py` downloads the files from the UN and rebuilds them with peacekeeping-tracker v1.0.0, whose own checks confirm the rebuild matches its release.

## Reproduce it

Needs Python 3.10 or later, git and an internet connection. The results were produced with Python 3.13, pandas 3.0.5, NumPy 2.5.3, SciPy 1.18.1, statsmodels 0.15.0 and Matplotlib 3.11.2.

```
pip install -r requirements.txt
python code/00_get_un_data.py
python code/01_analysis.py
python code/02_extra_checks.py
python code/03_figures.py
```

## Data sources

- United Nations, Peace and Security Data Hub: "Historical Uniformed Personnel Contribution" (DPO-UCHISTORICAL) and, for the historical comparisons, "Historical Uniformed Personnel Contribution prior to 2010" (DPPADPO-UCPre2010), via peacekeeping-tracker v1.0.0 (https://doi.org/10.5281/zenodo.23752307).
- World Bank, World Development Indicators: military expenditure, current US$ (MS.MIL.XPND.CD, based on SIPRI) and GDP per capita, current US$ (NY.GDP.PCAP.CD), as compiled in peacekeeping-for-profit-update v1.0.0 (https://doi.org/10.5281/zenodo.23768250). CC BY 4.0.
- UN standard reimbursement rate: General Assembly resolution 76/276 (29 June 2022), paragraph 9: US$1,448 per person per month from 1 July 2022.

## Read this first

- Payments are amounts owed at the standard rate, not cash paid. They exclude contingent-owned equipment, and the UN often pays late.
- Personnel are numbers as published by the UN; nothing is estimated or filled in.
- The results describe who bore the cut, not why. UN documents say missions, with headquarters departments, determined which contingents would be repatriated; they do not say how they chose among contributors.

## License

Code: MIT (see [`LICENSE`](LICENSE)). The author's text, plan, results, figures and calculated tables: CC BY 4.0 (see [`LICENSE-DATA`](LICENSE-DATA)); this covers only the author's contribution and does not change the UN's terms of use for the UN data the tables and figures are calculated from. The World Bank files: CC BY 4.0. Please credit the UN as well.
