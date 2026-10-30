# Analysis plan: who bore the 2025-26 cut in UN peacekeeping?

Kazi Affnann Azom. Written on 30 October 2026, before any of the analyses below were run.

## 1. What was already known when this plan was written

This paper builds on two of the author's data projects, and some descriptive figures from them were already public:

- **peacekeeping-tracker v1.0.0** (https://doi.org/10.5281/zenodo.23752307). Its README reports that UN uniformed personnel fell by 16,480 (27%) between June 2025 and July 2026, mostly from October to December 2025; that Bangladesh's contingent fell from 5,705 to 4,003 (30%) and it slipped to fourth place; and that the standard-rate reimbursement owed for Bangladesh's troops and formed police units fell from an estimated US$96.5 million in 2024-25 to US$78.8 million in 2025-26. The tracker also contains a table of June 2025 against July 2026 for the 20 largest contributors (`tables/cut_2025.csv`). That table is not used for any test below.
- **peacekeeping-for-profit-update v1.0.0** (https://doi.org/10.5281/zenodo.23768250). It reports Coleman and Nyblade's (2018) first condition each December from 2015 to 2025: in December 2025 four countries' estimated UN payments came to 10% or more of their military spending (Rwanda, Nepal, Ghana and Malawi).

None of the decompositions, regressions or checks in sections 4 and 5 had been run when this plan was written.

## 2. Question

Which contributing countries bore the 2025-26 reduction in UN uniformed personnel, in people and in UN payments, and did it fall harder on the countries that depend most on those payments?

## 3. Data and definitions

**Data.**
- UN uniformed personnel by month, contributing country, mission and personnel category: the full dataset rebuilt with peacekeeping-tracker v1.0.0 (306,172 rows, November 1990 to July 2026; all of the tracker's checks pass).
- Military expenditure in current US dollars (World Bank indicator MS.MIL.XPND.CD, based on SIPRI) and GDP per capita in current US dollars (NY.GDP.PCAP.CD), as downloaded on 29 October 2026 in peacekeeping-for-profit-update v1.0.0.
- The UN standard reimbursement rate of US$1,448 per person per month (General Assembly resolution 76/276, paragraph 9), in force from July 2022 to June 2026.

**Months.** Baseline *t*0 = June 2025, the last month of the UN fiscal year 2024-25. End *t*1 = July 2026, the latest month in the data.

**Personnel.** *P* = all uniformed personnel: troops, staff officers, military experts on mission, individual police and formed police units. *K* = contingent personnel, troops plus formed police units, the personnel the UN reimburses at its standard monthly rate.

**Country and mission changes.** For country *c* and mission *m*, *P*_cm0 and *P*_cm1 are personnel at *t*0 and *t*1; *P*_c0 and *P*_m0 are country and mission totals at *t*0.
- Country change: Δ*P*_c = *P*_c1 - *P*_c0; percentage change 100 × Δ*P*_c / *P*_c0.
- Mission rate: *g*_m = (*P*_m1 - *P*_m0) / *P*_m0 for every mission with *P*_m0 > 0 (*g*_m = -1 for a mission with no personnel at *t*1).
- Exposure: *E*_c = Σ_m *P*_cm0 × *g*_m, the change country *c* would have had if every contributor to each mission had changed at that mission's rate.
- Within-mission part: *W*_c = Δ*P*_c - *E*_c. Deployments to missions with no personnel at *t*0 fall in *W*_c. Without new missions, Σ_c *W*_c = 0: the within-mission part only moves the cut between contributors to the same mission.

**Payments.**
- Annualised change in standard-rate payments owed: Δ*M*_c = (*K*_c1 - *K*_c0) × 12 × 1,448 US dollars. The July 2026 rate (US$1,474.68) is not used, so Δ*M* measures the change in personnel only.
- Dependence: *D*_c = 100 × *K*_c0 × 12 × 1,448 / military expenditure of *c* in 2024, the annualised baseline payment as a percentage of the previous calendar year's military spending (as in peacekeeping-for-profit-update, which uses the previous year's spending).
- Burden relative to the military budget: *B*_c = -100 × Δ*M*_c / military expenditure of *c* in 2024.
- Payments are standard-rate amounts owed, not cash paid, and exclude contingent-owned equipment.

**Samples.** Totals use every country. The cross-country tests use countries with *P*_c0 of at least 100 (the main sample); tests that use *D* also need 2024 military expenditure, and countries without it are listed. The country-mission test uses country-mission cells with *P*_cm0 of at least 50.

## 4. Hypotheses and tests

All tests are two-sided at the 5% level. Regressions are weighted least squares with heteroskedasticity-robust (HC1) standard errors.

**H1 (mission exposure).** Most of the variation between contributors in the size of their cut comes from the missions they served in. Test: regress the percentage change, 100 × Δ*P*_c / *P*_c0, on the exposure-predicted percentage change, 100 × *E*_c / *P*_c0, weighted by *P*_c0, in the main sample. H1 holds if the slope is positive and significant and the weighted R² is at least 0.5. Also reported: Σ_c |Δ*P*_c|, Σ_c |*E*_c| and Σ_c |*W*_c| over all countries.

**H2 (dependence).** The percentage cut is related to dependence on UN payments. Test: regress 100 × Δ*P*_c / *P*_c0 on ln *D*_c, weighted by *P*_c0, in the main sample with *D* available. A negative coefficient means that more dependent contributors lost a larger share of their personnel. The coefficient is split into its exposure and within-mission parts by running the same regression with 100 × *E*_c / *P*_c0 and with 100 × *W*_c / *P*_c0 as the dependent variable; the two coefficients add up to the total.

**H3 (within-mission differences).** Within the same mission, the contingents of more dependent contributors were cut by a different percentage from others. Test: at the country-mission level, regress 100 × (*P*_cm1 - *P*_cm0) / *P*_cm0 on ln *D*_c with mission fixed effects, weighted by *P*_cm0, in cells with *P*_cm0 of at least 50.

**Descriptive results (no test).**
- (a) Totals at *t*0 and *t*1, and the change, by mission and by personnel category.
- (b) The 20 largest contributors at *t*0: *P*_c0, *P*_c1, Δ*P*_c, the percentage change, *E*_c, *W*_c, Δ*M*_c and *B*_c.
- (c) Δ*M*_c summed by dependence group (*D* of 10% or more, 1% to under 10%, under 1%), each group's share of the total fall in payments, and the median *B*_c in each group.
- (d) The number of countries with *D* of 10% or more at *t*0 and at *t*1, both computed with 2024 military spending (Coleman and Nyblade's first condition, read as in peacekeeping-for-profit-update).
- (e) Bangladesh: the actual and exposure-predicted change, *W*_c, Δ*M*_c and *B*_c.

## 5. Checks

- **C1. Alternative baseline:** September 2025, the last month before the October 2025 announcement, instead of June 2025.
- **C2. Contingent only:** *K* instead of *P* in H1 to H3.
- **C3. Placebo window:** May 2024 to June 2025, the 13 months before the main window, for H1 to H3, with *D* computed from May 2024 contingents and 2023 military spending.
- **C4. Income instead of dependence:** ln GDP per capita in 2024 instead of ln *D* in H2 and H3.
- **C5. Separately decided drawdowns:** H1 to H3 without the missions whose reduction during the window was decided separately by the Security Council (a mandated closure or a lower authorised strength), identified from Security Council resolutions before this check is run, and listed with the results.
- **C6. Sample and weights:** H1 and H2 unweighted, and with a lower threshold of *P*_c0 of at least 20.

## 6. Reporting rules

- Every result set out above is reported, whether or not it supports a hypothesis.
- Any analysis added after this plan is labelled as not in the plan.
- UN numbers are used exactly as published; nothing is imputed or filled in.
- Changes to this plan after any result is seen are recorded in a dated change log at the end of this file.

## Change log

- **30 October 2026, after the main results were seen.** No test, window, measure or check in sections 3 to 5 was changed. Added, and labelled in the paper as not in the plan: H2 with the logarithm of June 2025 personnel as a control; H2 without the four countries with *D* of 10% or more; H2 leaving out each of the ten largest contributors in turn; H1 and H2 without South Africa; and the placebo window (C3) with UNSOM and its successor UNTMIS counted as one mission (the mandate was transferred by Security Council resolution 2753 of 30 October 2024; the definitions above treat UNSOM as closing and UNTMIS as new). The p-values reported use the normal approximation, statsmodels' default for HC1 standard errors.
- **30 October 2026, later the same day.** Added, also labelled as not in the plan: the cut by contributor size (the ten largest contributors in June 2025, other countries with 100 or more, 20 to 99, under 20) and a weighted quadratic in the logarithm of June 2025 personnel, to compare the result with Coleman and Li (2026).
