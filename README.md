# HIT140 Group Project — FIFA World Cup 2026 Player Analysis

This branch implements the four distinct Objective 1 analytic tasks in the HIT140 project brief. The primary data source is FIFA's [official player-statistics table](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/statistics/player-statistics), supplemented by FIFA's [official standings and knockout bracket](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/standings).

## Important design decision

The original ideas included paired comparisons between group and knockout matches and between first and second halves. They cannot be core tasks for this brief:

- the brief permits a one-sample t-test or an independent two-sample t-test, not a paired t-test;
- FIFA's player-statistics page contains cumulative tournament totals, not player-by-match or half-by-half records;
- treating cumulative totals as paired observations would invent data that the source does not provide.

The revised questions retain the shooting and passing themes, add distinct defensive and physical focal points, and use only the permitted independent two-sample test.

## Questions, rationale and hypotheses

### Task 1 — Shooting and tournament progression

**Question:** For outfield players who played at least 90 minutes, does mean attempts at goal per 90 differ between players from knockout teams and players from group-stage exits?

**Why chosen:** This is the closest valid version of the requested group-stage/knockout shooting question. Per-90 rates control for different playing time and for knockout teams playing additional matches.

- H0: μ(knockout team) = μ(group-stage exit)
- H1: μ(knockout team) ≠ μ(group-stage exit)

### Task 2 — Passing by position

**Question:** For players who played at least 180 minutes, does mean passing accuracy differ between midfielders and defenders?

**Why chosen:** Passing is a separate technical focal point, and the positions have different roles and spatial pressures.

- H0: μ(midfielders) = μ(defenders)
- H1: μ(midfielders) ≠ μ(defenders)

### Task 3 — Defensive work by position

**Question:** For players who played at least 90 minutes, does mean forced turnovers per 90 differ between midfielders and forwards?

**Why chosen:** Forced turnovers measure defensive work rather than shooting, passing, or physical workload. The 90-minute threshold also provides enough eligible observations for balanced random samples.

- H0: μ(midfielders) = μ(forwards)
- H1: μ(midfielders) ≠ μ(forwards)

### Task 4 — Physical workload by position

**Question:** For players who played at least 180 minutes, does mean total distance covered per 90 differ between midfielders and forwards?

**Why chosen:** Distance is a distinct physical focal point and the positional comparison has a clear football interpretation.

- H0: μ(midfielders) = μ(forwards)
- H1: μ(midfielders) ≠ μ(forwards)

## Data acquisition and audit trail

FIFA's statistics table is rendered by JavaScript. A normal Python request retrieves the page shell but not the table, so the Module 1/2 technique pandas.read_html(URL) cannot read it. The modules do not teach requests, BeautifulSoup, Selenium, Playwright, or FIFA's private API.

To avoid claiming that pandas scraped data it cannot access:

1. the visible official FIFA tables were expanded completely and preserved as dated raw CSV snapshots;
2. each raw player file includes the official source URL and retrieval date (2026-08-31);
3. team progression was derived from the official 32-team knockout bracket and recorded for all 48 teams;
4. the submitted preparation and analysis code uses the taught pandas, SciPy, math, matplotlib, and seaborn workflow.

This is a transparent source-capture boundary: raw acquisition is auditable, while every wrangling, sampling, calculation, confidence interval, test, and plot is reproducible in Python. No unlisted third-party scraping package is hidden in the submission.

## Preparation and sampling plan

The target population is FIFA World Cup 2026 players who appeared in at least one match. The task-specific eligible population is formed after:

1. loading the dated CSVs with pandas.read_csv();
2. validating unique player/team/position keys;
3. merging minutes, attacking, distribution, defending, physical, and team-progression data with pandas.merge();
4. excluding goalkeepers where the question concerns outfield players;
5. applying the minimum-minutes rule;
6. removing records missing the focal statistic;
7. calculating per-90 rates where required.

The scripts then take equal-size simple random samples without replacement from each comparison group. pandas.DataFrame.sample() uses random_state=2026, so every user receives the same sample and result.

| Task | Eligible rows | Sample |
|---|---:|---:|
| Shooting | 328 | 60 per progression group |
| Passing | 147 | 50 per position |
| Defending | 92 | 40 per position |
| Physical | 105 | 30 per position |

For each sample, the code reports count, mean, median, sample standard deviation, minimum, maximum, and a 95% t confidence interval for each group mean. It then applies a two-sided Welch independent two-sample t-test at α = 0.05. Welch's form is selected through scipy.stats.ttest_ind(equal_var=False), avoiding an unsupported equal-variance assumption.

## Findings

Results below are estimates from the reproducible random samples, not claims that a non-significant result proves the population means identical.

| Task | Group means and 95% CIs | Welch test | Decision at α = 0.05 |
|---|---|---:|---|
| Shooting | Knockout 1.418 attempts/90 [1.208, 1.628]; group exit 1.520 [1.296, 1.743] | t = -0.662, p = 0.5090 | Fail to reject H0 |
| Passing | Midfielders 87.52% [86.29, 88.75]; defenders 88.66% [87.14, 90.18] | t = -1.172, p = 0.2443 | Fail to reject H0 |
| Defending | Midfielders 4.485 turnovers/90 [3.773, 5.196]; forwards 4.202 [3.532, 4.873] | t = 0.584, p = 0.5607 | Fail to reject H0 |
| Physical | Midfielders 9.851 km/90 [9.685, 10.016]; forwards 9.367 [9.111, 9.622] | t = 3.250, p = 0.0021 | Reject H0 |

Interpretation:

- The samples do not provide sufficient evidence that shooting volume differs by whether a player's team reached the knockout stage.
- The samples do not provide sufficient evidence of different mean passing accuracy between midfielders and defenders.
- The samples do not provide sufficient evidence of different mean forced-turnover rates between midfielders and forwards.
- Midfielders in the physical-workload sample covered about 0.484 km more per 90 than forwards on average. The observed difference is statistically significant, and both the plot and confidence intervals show the same direction.

Statistical significance does not establish a causal effect of playing position. Team tactics, substitutions, match state, and selection are possible confounders.

## Unit-taught tools

| Tool | Project use | Where covered |
|---|---|---|
| Python in Anaconda/VS Code | Scripts, functions, conditions, calculations | Module 1, Week 1 |
| Jupyter via VS Code | Optional interactive execution and presentation | Module 2, Week 7 |
| pandas | CSV input, DataFrames, filtering, joins, sampling, missing-data handling, derived columns, grouped summaries | Module 1, Week 2; Module 2, Weeks 5–7 |
| scipy.stats | t critical values and independent two-sample t-tests | Module 1, Weeks 3–4 |
| math.sqrt | Confidence-interval standard errors | Module 1, Week 3 |
| matplotlib | Figure creation, labels, titles, and saved plots | Module 1, Week 2; Module 2, Weeks 6–7 |
| seaborn | Comparative boxplots and swarmplots | Module 2, Week 6 |

## How to run

Python 3.10 or newer is recommended. Jupyter is optional; the analysis is implemented as ordinary Python scripts so it can run from a VS Code terminal.

~~~bash
git clone https://github.com/vfbmdcccxciii/HIT140_Group_Project.git
cd HIT140_Group_Project
git switch fifa-player-analysis

python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

python src/prepare_data.py
python src/task1_shooting.py
python src/task2_passing.py
python src/task3_defending.py
python src/task4_physical.py
~~~

On Windows PowerShell, activate the environment with:

~~~powershell
.venv\Scripts\Activate.ps1
~~~

Each task prints its results and writes:

- the reproducible sampled rows to outputs/*_sample.csv;
- descriptive statistics and confidence intervals to outputs/*_descriptive_and_ci.csv;
- the Welch test result to outputs/*_welch_t_test.csv;
- a boxplot with all sampled points to outputs/*_plot.png.

The committed result tables provide a check against a fresh run. The processed dataset, sample files, and plots are deterministic generated artifacts and are recreated by the commands above.

## Repository structure

~~~text
data/raw/                              dated official FIFA snapshots
data/processed/fifa_player_analysis.csv generated merged dataset
src/prepare_data.py                    validation, joins and features
src/analysis_common.py                 sampling, CIs, tests and plots
src/task1_shooting.py
src/task2_passing.py
src/task3_defending.py
src/task4_physical.py
outputs/*_descriptive_and_ci.csv       committed numerical summaries
outputs/*_welch_t_test.csv             committed hypothesis-test results
requirements.txt
README.md
~~~

## Scope boundary

This branch completes Objective 1. Objective 2 requires separate match-level datasets with exactly eight pre-match explanatory variables for 104 match rows and 208 team-match rows; those regression datasets and models are not included here.
