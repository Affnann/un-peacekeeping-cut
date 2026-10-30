# Main results (computed by code/01_analysis.py)

Main window: 2025-06 to 2026-07; dependence uses military spending of 2024.

UN rows with no number in the months used: 0

Total P: 61,299 -> 44,819 (change -16,480, -26.88%)
Total K: 56,779 -> 41,841 (change -14,938, -26.31%)
Countries with P>0 at t0: 117, at t1: 114; main sample (P0>=100): 55
Annualised change in payments owed (all countries): -259.56 million US$
Sum |dP| = 16,576.0; sum |E| = 16,483.0; sum |W| = 4,924.7; sum W = 0.000
Missions with no personnel at t0 but some at t1: [] (0 personnel)
Countries with D >= 10% at t0: 4; at t1 (2024 spending): 4
Main-sample countries without 2024 military spending: ['BTN', 'DJI']

## Regressions

                                       spec                                         test      coef       se            p     ci_lo     ci_hi       r2  n  n_missions
                                   main (P)                       H1 pct on exposure pct  1.105023 0.146967 5.525948e-14  0.816973  1.393073 0.119685 55         NaN
                                   main (P)                             H2 total on ln D -2.007542 0.478220 2.693475e-05 -2.944836 -1.070248 0.110068 53         NaN
                                   main (P)                     H2 exposure part on ln D -0.646382 0.198071 1.100920e-03 -1.034595 -0.258169 0.116103 53         NaN
                                   main (P)               H2 within-mission part on ln D -1.361159 0.547734 1.295244e-02 -2.434698 -0.287621 0.057428 53         NaN
                                   main (P)              H3 cell pct on ln D, mission FE -1.673394 0.666997 1.211261e-02 -2.980684 -0.366103 0.207551 94        10.0
                             C1_sep2025 (P)                       H1 pct on exposure pct  1.000119 0.200386 6.007912e-07  0.607370  1.392869 0.132385 55         NaN
                             C1_sep2025 (P)                             H2 total on ln D -2.089053 0.476677 1.173091e-05 -3.023323 -1.154782 0.121588 53         NaN
                             C1_sep2025 (P)                     H2 exposure part on ln D -0.667220 0.258422 9.825806e-03 -1.173718 -0.160722 0.093296 53         NaN
                             C1_sep2025 (P)               H2 within-mission part on ln D -1.421833 0.557631 1.077920e-02 -2.514769 -0.328897 0.064969 53         NaN
                             C1_sep2025 (P)              H3 cell pct on ln D, mission FE -1.731846 0.678725 1.072245e-02 -3.062123 -0.401569 0.217954 93        10.0
                             C3_placebo (P)                       H1 pct on exposure pct  0.094562 0.146710 5.192204e-01 -0.192985  0.382109 0.025424 55         NaN
                             C3_placebo (P)                             H2 total on ln D -0.043498 0.334125 8.964196e-01 -0.698370  0.611374 0.000273 53         NaN
                             C3_placebo (P)                     H2 exposure part on ln D  0.096708 0.284224 7.336664e-01 -0.460361  0.653776 0.000471 53         NaN
                             C3_placebo (P)               H2 within-mission part on ln D -0.140206 0.244024 5.655906e-01 -0.618485  0.338073 0.000852 53         NaN
                             C3_placebo (P)              H3 cell pct on ln D, mission FE -0.118021 0.341425 7.295905e-01 -0.787202  0.551161 0.697544 96        11.0
                          C2 contingent (K)                       H1 pct on exposure pct  1.007822 0.147135 7.404083e-12  0.719442  1.296202 0.106498 54         NaN
                          C2 contingent (K)                             H2 total on ln D -2.158773 0.474540 5.385209e-06 -3.088854 -1.228692 0.118311 52         NaN
                          C2 contingent (K)                     H2 exposure part on ln D -0.603076 0.215913 5.219748e-03 -1.026257 -0.179895 0.087939 52         NaN
                          C2 contingent (K)               H2 within-mission part on ln D -1.555697 0.555209 5.078677e-03 -2.643887 -0.467507 0.068758 52         NaN
                          C2 contingent (K)              H3 cell pct on ln D, mission FE -1.760614 0.680756 9.702333e-03 -3.094871 -0.426356 0.207077 93        10.0
                              C4 income (P)                H2 total on ln GDP per capita  2.899242 1.483369 5.064228e-02 -0.008107  5.806591 0.048273 55         NaN
                              C4 income (P)        H2 exposure part on ln GDP per capita  0.896783 0.462256 5.237781e-02 -0.009221  1.802788 0.047121 55         NaN
                              C4 income (P)  H2 within-mission part on ln GDP per capita  2.002458 1.413714 1.566432e-01 -0.768371  4.773288 0.026127 55         NaN
                              C4 income (P) H3 cell pct on ln GDP per capita, mission FE  2.967089 2.103973 1.584713e-01 -1.156622  7.090801 0.189138 98        10.0
C5 without separately decided drawdowns (P)                       H1 pct on exposure pct  1.473268 0.528007 5.266835e-03  0.438394  2.508143 0.117835 39         NaN
C5 without separately decided drawdowns (P)                             H2 total on ln D -1.913300 0.972165 4.905870e-02 -3.818708 -0.007891 0.044278 39         NaN
C5 without separately decided drawdowns (P)                     H2 exposure part on ln D -0.204776 0.231815 3.770421e-01 -0.659124  0.249573 0.009343 39         NaN
C5 without separately decided drawdowns (P)               H2 within-mission part on ln D -1.708524 0.937472 6.838216e-02 -3.545936  0.128887 0.039480 39         NaN
C5 without separately decided drawdowns (P)              H3 cell pct on ln D, mission FE -1.776367 1.184395 1.336636e-01 -4.097738  0.545004 0.090599 56         7.0
                          C6 unweighted (P)                       H1 pct on exposure pct  1.044360 0.130718 1.355790e-15  0.788157  1.300562 0.115230 55         NaN
                          C6 unweighted (P)                             H2 total on ln D -1.273405 1.475770 3.882062e-01 -4.165862  1.619051 0.017757 53         NaN
                          C6 unweighted (P)                     H2 exposure part on ln D -1.056993 0.416961 1.124493e-02 -1.874220 -0.239765 0.115425 53         NaN
                          C6 unweighted (P)               H2 within-mission part on ln D -0.216413 1.387975 8.760964e-01 -2.936794  2.503969 0.000580 53         NaN
                        C6 threshold 20 (P)                       H1 pct on exposure pct  1.129364 0.146833 1.454503e-14  0.841576  1.417152 0.121871 82         NaN
                        C6 threshold 20 (P)                             H2 total on ln D -1.979754 0.467969 2.331497e-05 -2.896957 -1.062551 0.108310 59         NaN
                        C6 threshold 20 (P)                     H2 exposure part on ln D -0.639071 0.192741 9.141372e-04 -1.016836 -0.261306 0.115417 59         NaN
                        C6 threshold 20 (P)               H2 within-mission part on ln D -1.340683 0.536328 1.242829e-02 -2.391867 -0.289499 0.056423 59         NaN

## Missions (main)

              x0       x1  change         g
mission                                    
MINUSCA  17106.0  12437.0 -4669.0 -0.272945
UNMISS   15457.0  10312.0 -5145.0 -0.332859
MONUSCO  11777.0   8744.0 -3033.0 -0.257536
UNIFIL    9920.0   7492.0 -2428.0 -0.244758
UNISFA    3298.0   2813.0  -485.0 -0.147059
UNDOF     1175.0    955.0  -220.0 -0.187234
UNFICYP    867.0    784.0   -83.0 -0.095732
UNTMIS     641.0    638.0    -3.0 -0.004680
UNAMI      244.0      0.0  -244.0 -1.000000
UNSMIL     234.0    170.0   -64.0 -0.273504
MINURSO    176.0    158.0   -18.0 -0.102273
UNVMC      156.0     88.0   -68.0 -0.435897
UNTSO      143.0    154.0    11.0  0.076923
UNMOGIP     42.0     41.0    -1.0 -0.023810
BINUH       19.0      5.0   -14.0 -0.736842
UNMIK       17.0     12.0    -5.0 -0.294118
UNSOS       13.0     13.0     0.0  0.000000
UNMHA       11.0      0.0   -11.0 -1.000000
UNOWAS       2.0      2.0     0.0  0.000000
UNAMA        1.0      1.0     0.0  0.000000

## Categories (main)

           category      t0      t1   change        pct
             troops 52466.0 38696.0 -13770.0 -26.245569
     staff_officers  1652.0  1100.0   -552.0 -33.414044
 experts_on_mission  1067.0   705.0   -362.0 -33.926898
  police_individual  1801.0  1173.0   -628.0 -34.869517
police_formed_units  4313.0  3145.0  -1168.0 -27.080918

## Top 20 (main)

                          country      x0      x1      dx        pct            E           W      dM_usd          D          B
iso3                                                                                                                           
NPL                         Nepal  6122.0  4285.0 -1837.0 -30.006534 -1756.167225  -80.832775 -30964032.0  23.614954   7.101223
RWA                        Rwanda  5882.0  4016.0 -1866.0 -31.723903 -1787.641743  -78.358257 -30564384.0  56.521143  17.433051
BGD                    Bangladesh  5705.0  4003.0 -1702.0 -29.833479 -1553.807318 -148.192682 -28027488.0   2.547883   0.747905
IND                         India  5387.0  4260.0 -1127.0 -20.920735 -1478.740103  351.740103 -18418560.0   0.104990   0.021518
IDN                     Indonesia  2784.0  1972.0  -812.0 -29.166667  -706.887044 -105.112956 -13240512.0   0.384047   0.110224
PAK                      Pakistan  2678.0  2085.0  -593.0 -22.143391  -665.788040   72.788040  -9122400.0   0.422111   0.088537
GHA                         Ghana  2631.0  1929.0  -702.0 -26.681870  -667.409924  -34.590076 -11433408.0  15.667570   4.167042
CHN                         China  1862.0  1651.0  -211.0 -11.331901  -518.427015  307.427015  -3579456.0   0.009894   0.001148
MAR                       Morocco  1702.0  1332.0  -370.0 -21.739130  -450.284348   80.284348  -6046848.0   0.520306   0.109605
ETH                      Ethiopia  1533.0   921.0  -612.0 -39.921722  -510.272692 -101.727308 -10321344.0   3.704191   1.473737
TZA   United Republic of Tanzania  1533.0  1004.0  -529.0 -34.507502  -402.442650 -126.557350  -8635872.0   2.731197   0.929093
SEN                       Senegal  1296.0   828.0  -468.0 -36.111111  -345.945769 -122.054231  -7419552.0   3.283038   1.161439
EGY                         Egypt  1216.0  1019.0  -197.0 -16.200658  -327.884028  130.884028  -2658528.0   0.775189   0.110845
CMR                      Cameroon  1123.0   783.0  -340.0 -30.276046  -306.361604  -33.638396  -5751456.0   3.475808   1.075227
ZAF                  South Africa  1055.0    73.0  -982.0 -93.080569  -272.081978 -709.918022 -17132736.0   0.587172   0.564831
ZMB                        Zambia   979.0   628.0  -351.0 -35.852911  -267.384773  -83.615227  -5595072.0   4.525815   1.603204
TUN                       Tunisia   931.0   676.0  -255.0 -27.389903  -253.438067   -1.561933  -3996480.0   1.100511   0.303863
MNG                      Mongolia   893.0   548.0  -345.0 -38.633819  -295.267091  -49.732909  -5612448.0   8.259674   3.127638
ITA                         Italy   888.0   775.0  -113.0 -12.725225  -216.171217  103.171217  -2032992.0   0.039619   0.005371
URY                       Uruguay   868.0   834.0   -34.0  -3.917051  -209.019820  175.019820   -364896.0   0.917594   0.023050

## Dependence groups (main)

                           countries       P0       P1      dM_usd  median_B_all  share_of_net_fall_pct  median_B_main_sample  countries_main_sample
group                                                                                                                                               
1% <= D < 10%                     13  16694.0  11047.0 -92266560.0      1.161439              35.546927              1.161439                     13
D < 1%                            95  28725.0  22404.0 -93152736.0     -0.000000              35.888338              0.006209                     36
D >= 10%                           4  15413.0  10991.0 -72927072.0      5.634132              28.096131              5.634132                      4
no military spending data          8    467.0    377.0  -1216320.0           NaN               0.468604                   NaN                      2

## Bangladesh

x0           5.705000e+03
x1           4.003000e+03
E           -1.553807e+03
dx          -1.702000e+03
W           -1.481927e+02
pct         -2.983348e+01
E_pct       -2.723589e+01
W_pct       -2.597593e+00
K0           5.495000e+03
K1           3.882000e+03
dM_usd      -2.802749e+07
milex_usd    3.747468e+09
D            2.547883e+00
D_t1         1.799979e+00
B            7.479047e-01
gdppc        2.593416e+03
