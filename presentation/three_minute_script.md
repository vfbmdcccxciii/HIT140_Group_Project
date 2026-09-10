# Three-minute discussion: Maximus Turner

Speak slides 1-4 only. Keep your face visible throughout. Start by showing your CDU student ID for approximately five seconds. Bracketed directions and the preparation notes below are not spoken. Rehearse at about 140 words per minute, allowing pauses, and finish within three minutes. Timings are targets, not a verified recording duration. Review docs/ai_acknowledgement.md before using the wording.

## Slide 1: 0:00-1:10, including ID

[Show CDU student ID, then begin.]

I'm Maximus Turner. My questions compare midfielders and forwards on running distance and direct-pressure share.

The source is FIFA's official World Cup 2026 player-statistics page. Its tables load through JavaScript, so ordinary pandas HTML extraction could not retrieve the populated table. Visible table records were captured into dated CSV files with source URLs. Checking the table sorted by minutes recovered 281 omitted records.

Python's pandas merged minutes, physical and defending data using player, team and position. Unique-key checks prevented duplicate matches. Records missing the required statistic were excluded rather than treated as zero.

Sampling was random without replacement, with fixed positional seeds for reproducibility. Each group had at least thirty players to support approximate inference about means.

Two-sided independent t-tests compare separate positional groups. They allow unequal variances and use the course's conservative degrees of freedom. For both questions, the null is equal means, tested at five percent significance.

## Slide 2: 1:10-1:50

For running, dividing kilometres by minutes and multiplying by ninety makes playing durations comparable. Requiring 180 minutes reduces instability from short appearances. Thirty players were sampled per position.

Midfielders averaged 9.74 kilometres per ninety, versus 9.22 for forwards. The chart shows ninety-five percent t confidence intervals, which express uncertainty about group means. The estimated difference is 0.52 kilometres, with an interval from 0.22 to 0.82.

With 29 degrees of freedom, p is 0.0012, so we reject the null.

## Slide 3: 1:50-2:30

For pressing, direct pressures divided by all pressures, multiplied by one hundred, describes pressure composition rather than success. Each player's percentage receives equal weight.

Players needed ninety minutes and positive recorded pressures, ensuring exposure and a valid denominator. Forty players were sampled per position.

Midfielders averaged 17.08 percent, versus 11.20 percent. The difference is 5.88 percentage points, with a ninety-five percent interval from 2.14 to 9.63. With 39 degrees of freedom, p is 0.0029. Again, we reject the null.

## Slide 4: 2:30-2:55

These findings remain exploratory because the second question followed inspection of alternatives. Partial source coverage, shared team tactics and skewed pressing data limit inference.

The lessons are that joins affect samples and denominators define questions. These samples suggest midfielders run farther and apply a greater share of pressure directly. Position does not establish causation.

[If another presenter follows, shorten the closing sentences to allow a brief handoff within three minutes.]

## Preparation notes: detail to understand, not read aloud

### Source and extraction

The source is [FIFA's official player-statistics page](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/statistics/player-statistics), including its metric glossary. The original CSV snapshots are dated 31 August 2026. The minutes supplement is dated 10 September 2026. The records came from the visible browser tables; the submission does not claim a fully automated Python web scraper.

For the repair, the minutes table was sorted by minutes and expanded to 550 visible rows, through 191 minutes. The 281 records absent from the earlier capture were preserved in a separate supplement. A checksum of the seven transcribed columns matched the browser-extracted text before adding provenance columns. The combined minutes file holds 1,033 observed players with positive minutes. This repair does not establish complete tournament coverage or guarantee completeness below the visible cutoff.

### Preparation and sampling choices

pandas validates unique player/team/position keys and performs one-to-one player-table joins, preventing duplicate combinations from inflating observations. The preparation script also retains existing attacking, distribution and progression fields, but the two selected questions use physical and defending measures. Missing focal metrics are excluded. Direct pressures must lie between zero and total pressures; a zero denominator cannot define a share.

The captured physical table has 350 rows, all matched to minutes. The defending table has 350 rows, of which 294 match minutes. The remaining 56 have unknown eligibility. The running frame contains 57 midfielders and 91 forwards; pressing contains 71 midfielders and 49 forwards. The original tables are partial captures, not random samples of all tournament players.

The random seeds are 2026 for midfielders and 2027 for forwards. Sampling without replacement avoids selecting a player twice within a task. Fixed seeds permit others to reproduce the selection; they do not make the source frame representative. The selected sample sizes are 30 per group for running and 40 for pressing. These support a CLT-based approximation for means, but neither sample size guarantees normality or independence. Large sampling fractions also mean these ordinary t intervals are approximate model-based course inference, not exact finite-population survey intervals.

### Statistical methods and why

Descriptive outputs include means, medians, sample standard deviations, quartiles, ranges and outlier counts. Python draws the mean/CI charts, boxplots and histograms. A mean CI uses the t distribution because the population standard deviation is unknown and is estimated from the sample. It describes uncertainty about a mean, not the range containing 95% of individual players.

The independent two-sample statistic divides the difference in means by sqrt(s_MF squared / n_MF + s_FW squared / n_FW). This avoids assuming equal population variances. The Week 4 conservative convention uses the smaller of n_MF minus one and n_FW minus one: 29 for running and 39 for pressing. The test is two-sided because the alternative asks whether the means differ in either direction. The resulting t statistics are 3.589 and 3.179 respectively, shown on the slides. SciPy's Welch degrees of freedom provide a sensitivity check, with p=0.000696 and p=0.002128; both decisions remain unchanged.

Running normalises duration, but does not control for tactics or match conditions. Pressing share is the unweighted mean of player percentages, not a pooled event ratio and not a success rate. Pressing distributions are right-skewed; plausible IQR outliers were retained. Players on the same team may be dependent. The reported p-values are nominal and exploratory because alternatives were inspected before selecting the second question. Neither a small p-value nor a confidence interval establishes causation.

See docs/max_analysis_notes.md for full calculations, limitations and the mapping to Weeks 1-7 and the Objective 1 brief. Week 8 regression is outside this presentation's required objective.
