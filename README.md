# HIT140 Group Project — FIFA World Cup 2026 Player Analysis

This branch develops the four distinct analytic tasks required by Objective 1 of the HIT140 FIFA World Cup 2026 project brief. The primary source is the [official FIFA player-statistics table](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/statistics/player-statistics).

## Scope and design constraints

Each task below includes a distinct analytic question, data wrangling, data preparation and sampling, descriptive statistics, a confidence interval, and an allowed inferential test.

The project brief permits a **one-sample t-test or an independent two-sample t-test**. It does not permit a paired t-test. FIFA's player-statistics page also reports cumulative tournament totals rather than player-by-match or first-half/second-half observations. Therefore:

- the proposed paired comparison of each player's group-stage and knockout-stage attempts cannot be used as a core task;
- the proposed paired first-half/second-half passing comparison cannot be calculated from this source;
- a team-level group-stage/knockout-stage attempts comparison would require match-level data from a different FIFA Match Centre source.

The revised questions preserve the intended shooting and passing themes while remaining compatible with the brief and the available FIFA table.

## Population, eligibility and sampling

The target population is players who appeared at the FIFA World Cup 2026. Players with fewer than the task-specific minimum minutes are excluded because a very small denominator makes per-90 rates unstable.

For each task:

1. construct the eligible population after merging the relevant FIFA category with minutes played and player details;
2. remove rows missing a required measurement rather than inventing values;
3. draw an independently reproducible sample from each comparison group with pandas DataFrame.sample and random_state=2026;
4. use at least 30 observations per group where the eligible group size permits, supporting the Central Limit Theorem treatment taught in Module 1;
5. retain the full eligible population only for a sensitivity check, not as a substitute for the required sampling stage.

## Analytic task 1 — Shooting and tournament progression

**Question:** Among forwards who played at least 90 minutes, does mean attempts at goal per 90 minutes differ between players whose teams reached the knockout stage and players whose teams exited in the group stage?

**Why this question:** It preserves the original interest in group-stage versus knockout football without pretending FIFA supplies paired per-match observations. Dividing cumulative attempts by minutes controls for unequal playing time and extra matches.

**Variables and preparation**

- FIFA attacking table: attempts at goal;
- FIFA Golden Boot table: position, team and minutes played;
- FIFA standings: whether the team reached the knockout stage;
- derived feature: attempts_at_goal_per90 = attempts_at_goal / minutes_played × 90.

**Hypotheses**

- H0: μ(knockout) = μ(group exit)
- H1: μ(knockout) ≠ μ(group exit)

**Analysis plan**

- stratified random sample from the two progression groups;
- describe(), mean, median, standard deviation, IQR and group boxplot/swarmplot;
- 95% confidence interval for each group mean;
- independent two-sample t-test using scipy.stats.ttest_ind().

## Analytic task 2 — Passing by playing position

**Question:** Among players who completed at least 180 minutes, does mean passing accuracy differ between midfielders and defenders?

**Why this question:** Passing is a separate technical focal point and the comparison has a clear football interpretation: midfielders typically pass under different spatial and defensive pressures from defenders.

**Variables and preparation**

- FIFA distribution table: passes, passes completed and passing accuracy;
- FIFA Golden Boot table: position and minutes played;
- exclude players below 180 minutes and records without passing accuracy.

**Hypotheses**

- H0: μ(midfielders) = μ(defenders)
- H1: μ(midfielders) ≠ μ(defenders)

**Analysis plan**

- independent reproducible samples of midfielders and defenders;
- descriptive statistics, histogram and boxplot/swarmplot;
- 95% confidence interval for each position's mean passing accuracy;
- independent two-sample t-test using scipy.stats.ttest_ind().

## Analytic task 3 — Defensive work by playing position

**Question:** Among outfield players who completed at least 180 minutes, does mean forced turnovers per 90 minutes differ between midfielders and forwards?

**Why this question:** Forced turnovers measure defensive work and are distinct from shooting, passing and physical workload. Comparing midfielders with forwards examines how role affects ball recovery.

**Variables and preparation**

- FIFA defending table: forced turnovers;
- FIFA Golden Boot table: position and minutes played;
- derived feature: forced_turnovers_per90 = forced_turnovers / minutes_played × 90.

**Hypotheses**

- H0: μ(midfielders) = μ(forwards)
- H1: μ(midfielders) ≠ μ(forwards)

**Analysis plan**

- independent reproducible samples of midfielders and forwards;
- descriptive statistics and comparative boxplot/swarmplot;
- 95% confidence interval for each group mean;
- independent two-sample t-test using scipy.stats.ttest_ind().

## Analytic task 4 — Physical workload by playing position

**Question:** Among outfield players who completed at least 180 minutes, does mean total distance covered per 90 minutes differ between midfielders and forwards?

**Why this question:** Distance is a physical-workload focal point and is not a duplicate of technical shooting, passing or defensive actions.

**Variables and preparation**

- FIFA physical table: total distance in metres;
- FIFA Golden Boot table: position and minutes played;
- derived feature: distance_metres_per90 = total_distance_metres / minutes_played × 90.

**Hypotheses**

- H0: μ(midfielders) = μ(forwards)
- H1: μ(midfielders) ≠ μ(forwards)

**Analysis plan**

- independent reproducible samples of midfielders and forwards;
- descriptive statistics and comparative boxplot/swarmplot;
- 95% confidence interval for each group mean;
- independent two-sample t-test using scipy.stats.ttest_ind().

## Data collection and wrangling plan

FIFA's player table is JavaScript-rendered. A normal Python request receives the page shell but not the table, so pandas.read_html(URL) cannot directly scrape it. Modules 1 and 2 do not teach requests, BeautifulSoup, Selenium, Playwright or FIFA's private web API. To keep the submitted analysis within taught tools:

1. preserve dated raw CSV snapshots of the visible official FIFA tables for Golden Boot, attacking, distribution, defending and physical statistics;
2. preserve a FIFA standings-derived team progression table;
3. use pandas.read_csv() to load the snapshots;
4. use pandas.merge() to join category tables on player, team and position;
5. use listwise deletion with dropna() for missing required values;
6. construct per-90 features with ordinary Python arithmetic and pandas columns;
7. save a clean analysis-ready CSV.

The repository will not claim that pandas alone scraped FIFA's dynamic website. The raw files will retain source URLs and a retrieval date so the acquisition step remains auditable.

## Unit-taught tools used

| Tool | Use in this project | Unit coverage |
|---|---|---|
| Anaconda/conda and VS Code | Python environment | Module 1, Week 1 practicals |
| Jupyter via VS Code | Run and present the analysis | Module 2, Week 7 practicals |
| pandas | CSV input, DataFrames, joins, filtering, sampling and derived columns | Module 1 Week 2; Module 2 Weeks 5–7 |
| numpy | percentiles, variance and standard deviation | Module 1, Week 2 practicals |
| scipy.stats | sample statistics, normal critical value and independent t-tests | Module 1, Weeks 3–4 practicals |
| math.sqrt | confidence-interval standard error | Module 1, Week 3 practicals |
| matplotlib | histograms and annotated charts | Module 1 Week 2; Module 2 Weeks 6–7 |
| seaborn | boxplots and swarmplots | Module 2, Week 6 practicals |

## Planned repository structure

~~~text
data/raw/                 Dated FIFA table snapshots
data/processed/           Merged analysis-ready data
src/prepare_data.py       Wrangling and feature construction
src/analysis_common.py    Shared taught statistical helpers
src/task_1_shooting.py
src/task_2_passing.py
src/task_3_defending.py
src/task_4_physical.py
requirements.txt
README.md
~~~

Findings and exact run instructions will be added only after the data and analyses have been executed and checked.
