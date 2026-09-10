# Analysis notes: Maximus Turner

## State: questions and variables

Q1: Among covered World Cup 2026 midfielders and forwards with at least 180 minutes, does mean distance covered per 90 minutes differ by position? Distance is continuous ratio-scale data, position a nominal grouping variable. Rate = distance_metres / 1000 / minutes_played * 90. This compares physical workload after normalising playing duration. It does not control for tactical or match differences.

Q2: Among covered midfielders and forwards with at least 90 minutes and positive recorded pressures, does mean direct-pressure share differ by position? Share = 100 * defensive_pressures_directly_applied / defensive_pressures_applied. The numeric response is bounded between 0 and 100. FIFA's directly applied pressure refers to pressure directly against the ball carrier. Total pressures also include other pressure actions. This question distinguishes pressure composition from pressure volume. It does not estimate the percentage of pressures that succeed. The statistic is the arithmetic mean of player percentages, not the pooled ratio across all actions.

For each task H0: the two eligible-group mean metrics are equal. H1: they differ. The hypotheses are two-sided, with alpha 0.05. The variables and questions are distinct focal analytic tasks, not the brief's excluded mean-goals-of-forwards example.

## Plan: acquisition, wrangling and sampling

The broad population of interest is tournament players, but the observed sampling frame is limited to records in the captured FIFA tables that meet each task's eligibility rules. Inference beyond that frame requires representativeness assumptions unsupported by these captures. Physical coverage is a partial leaderboard capture, originally ordered by top speed. The defending capture is also partial. Random selection within either table does not make it a random tournament sample.

The original minutes capture held 752 appearing players. On 10 September the official table was sorted by minutes and expanded to 550 visible rows, through 191 minutes. The 281 missing rows in that view (source ranks 1022-1302) were captured into a supplement. A checksum of the seven transcribed columns matched the browser-extracted text (FNV-1a 2995621861) before adding provenance columns. This repair improves joins for the selected tasks; it is not a guarantee of a complete minutes table below the visible cutoff. The two dates are retained because combining snapshots also assumes the published cumulative statistics were stable between captures.

Unique player/team/position keys protect against accidental many-to-many joins. Missing focal metrics are excluded, not imputed. Zero denominators cannot define a pressing share. The scripts report unmatched keys, and no player names or metric values are edited to improve a p-value. The original snapshots are preserved. The raw physical table has 350/350 matches; defending has 294/350. Eligibility of 56 unmatched defending rows remains unknown.

Q1 uses at least 180 minutes to limit unstable per-90 rates from very short appearances. Eligible MF=57, FW=91; select 30 each. Q2 uses at least 90 minutes and positive pressures to define exposure and a meaningful denominator. Eligible MF=71, FW=49; select 40 each. These thresholds remain substantive eligibility choices, not proof that all rates are equally reliable. A single player is one observation. pandas samples without replacement using MF seed 2026 and FW seed 2027, preserving the earlier seed convention. Selected players and full eligible-frame summaries are saved for audit.

## Solve: descriptive statistics and confidence intervals

| Task/group | n | Mean | Median | Sample SD | 95% mean CI |
|---|---:|---:|---:|---:|---|
| Running MF (km/90) | 30 | 9.738 | 9.725 | 0.513 | 9.546-9.929 |
| Running FW (km/90) | 30 | 9.217 | 9.242 | 0.608 | 8.990-9.444 |
| Pressing MF (%) | 40 | 17.083 | 14.835 | 8.780 | 14.276-19.891 |
| Pressing FW (%) | 40 | 11.199 | 10.588 | 7.742 | 8.723-13.675 |

Additional minimum, maximum, quartiles, skewness and IQR outlier counts are in the CSV outputs. Sample variance uses n-1. Each group interval is mean +/- t(0.975,n-1) * s/sqrt(n). Repeated use of this procedure under its assumptions would cover the population mean about 95% of the time. It is not an interval containing 95% of individual players and is not a 95% probability statement about a fixed parameter after observing the data.

The primary independent two-sample statistic is t=(mean_MF-mean_FW)/sqrt(s_MF^2/n_MF+s_FW^2/n_FW), with course df=min(n_MF-1,n_FW-1). The two-sided p-value is 2*P(T_df >= |t|). The difference CI uses the same standard error and conservative df. Welch-Satterthwaite df are reported separately because SciPy's default unequal-variance result differs from the taught conservative convention.

| Task | Difference MF-FW | t | Course df | Course p | 95% difference CI | Welch p |
|---|---:|---:|---:|---:|---|---:|
| Running | 0.521 km/90 | 3.589 | 29 | 0.001206 | 0.224 to 0.818 km/90 | 0.000696 |
| Pressing | 5.885 percentage points | 3.179 | 39 | 0.002888 | 2.141 to 9.628 points | 0.002128 |

## Assumptions and alternatives

Histograms and boxplots retain all selected observations. Running is approximately symmetric (sample skewness 0.126 MF, -0.391 FW), with one FW IQR outlier. Pressing is right-skewed (0.953 MF, 1.625 FW), with two IQR outliers per group. These are plausible bounded values and remain in the analysis. We do not claim the pressing observations are normally distributed. Group sizes of 40 make mean-based inference more plausible through the CLT, but do not guarantee an accurate approximation with skewness and clustering.

MF and FW groups do not share players within a task. Players on the same team may share tactics and match conditions, so independence between all observations is an approximation. Finite sampling fractions are large (especially 40/49 forwards). The course t method does not use finite-population corrections or model team clusters. CIs/p-values therefore describe approximate model-based inference, not exact finite-frame survey inference. Equal population variances are not assumed.

The full eligible-frame descriptive means have the same direction: running 9.785 MF vs 9.272 FW, and pressing 17.784% MF vs 11.184% FW. These census descriptions check direction within available data; they are not independent replication or another significance test. Welch sensitivity also retains both decisions. Neither check resolves incomplete coverage, team dependence or selection after seeing results.

Earlier unsuccessful shooting, passing and turnover questions remain documented in the archive. A further turnovers-per-100-pressures candidate, before the minutes repair, had course p approximately 0.6347. Direct-pressure share was selected after observing its result. All current p-values are nominal and exploratory, with no multiple-search adjustment. Independent new data or a prespecified follow-up would be needed for stronger confirmatory claims. Significance is not a scientific requirement for a useful question.

## Conclude

Reject both null hypotheses at nominal alpha 0.05 under the stated course model. Covered sampled midfielders average more running per 90 and a higher share of direct pressures. Statistical evidence does not show that changing a player's position would cause a change, nor that midfielders press more successfully. The most important lessons are that incomplete joins change the sample, denominator choice changes the meaning of a question, and uncertainty and design limitations must accompany a small p-value.

## Learning material and brief mapping

| Requirement or teaching | Evidence in this contribution |
|---|---|
| Week 1: data-science question and explanatory/response variables | Separate workload and pressing-composition questions with explicit variables |
| Week 2: measurement, descriptive statistics and spread | Nominal positions, numeric metrics, means/medians/sample SD, quartiles and distributions |
| Week 3: population/sample distinction, sampling, CLT and intervals | Eligible-frame definition, seeded samples of at least 30, t mean CIs and interpretation |
| Week 4: State, Plan, Solve, Conclude | Hypotheses, unequal-variance statistic, conservative df, two-sided p, decision and limits |
| Week 5: merging, missing data and feature construction | Validated joins, 281-record repair, denominator guards, rates and missing-metric exclusion |
| Week 6: EDA, outliers and noncausal interpretation | Histograms/boxplots, retained IQR outliers, skewness and confounding discussion |
| Week 7: clear statistical communication | Labelled Python mean/CI figures, correct units, concise presentation narrative |
| Week 8: regression | Reviewed, but excluded because this assessment requires Objective 1 |
| Brief: each task has question, wrangling, preparation/sampling, descriptive statistics, CI, permitted t-test | Both task scripts plus shared preparation/inference and saved outputs cover all six |
| Presentation: individual segment, findings, methodology, lessons and conclusion | Four narrated slides plus two optional reference slides and timed script |

Sources: CDU HIT140 Learning Materials Weeks 1-8 (Learnline, accessed 10 September 2026); [project brief](https://online.cdu.edu.au/ultra/courses/_66400_1/document/_7601188_1?view=content&state=view); [group presentation guide](https://online.cdu.edu.au/ultra/courses/_66400_1/assessment/_7601225_1/attempt/_47712_1?courseId=_66400_1); [FIFA player statistics and glossary](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/statistics/player-statistics). Learnline access requires unit enrolment.
