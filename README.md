# HIT140 Group Project:

This repository contains group work for CDU HIT140. This README documents **Maximus Turner (vfbmdcccxciii): two Objective 1 questions**, as agreed in the two-person allocation. Other contributors' files are maintained separately. Objective 2 regression is outside this presentation's scope.

## Selected questions and findings

Both questions compare the mean player-level statistic for midfielders (MF) and forwards (FW) in the eligible, captured FIFA records. For each: H0: mu(MF) = mu(FW); H1: mu(MF) differs from mu(FW). Tests are two-sided at alpha = 0.05.

| Question | Preparation and sample | Means with 95% t CIs | Course t-test |
|---|---|---|---|
| Does mean running distance per 90 minutes differ by position? | At least 180 minutes, recorded distance; 30 per group | MF 9.738 [9.546, 9.929]; FW 9.217 [8.990, 9.444] km/90 | t=3.589, df=29, p=0.001206; reject H0 |
| Does mean direct-pressure share differ by position? | At least 90 minutes, recorded positive total pressures; 40 per group | MF 17.083% [14.276, 19.891]; FW 11.199% [8.723, 13.675] | t=3.179, df=39, p=0.002888; reject H0 |

Running is a physical workload question. Dividing distance by minutes puts different playing durations on a common 90-minute scale. Pressing is a distinct tactical question: direct pressures as a percentage of all pressures describes how players apply pressure, rather than the amount of running or the success of their pressure. The unweighted average gives each sampled player equal weight.

The estimated MF-minus-FW difference is **0.521 km/90** (95% CI 0.224 to 0.818) for running and **5.885 percentage points** (95% CI 2.141 to 9.628) for pressing. These are observational, exploratory associations. They do not establish that position causes either difference.

## Data and reproducibility

[FIFA's official player statistics](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/statistics/player-statistics) is the source. Original dated CSV snapshots remain intact. The 10 September supplement adds 281 minute records omitted from the earlier capture, giving 1,033 observed players with positive minutes. Source URL and retrieval date accompany the records. Capture used the visible browser table; this is not a claim of a fully automated Python scraper or complete tournament coverage.

Python validates player/team/position keys, merges tables one-to-one, checks exposure, derives variables, filters missing focal statistics, samples, computes statistics and draws all analysis figures. Missing values are never converted to zero. The captured physical and defending tables contain 350 rows each. All 350 physical rows and 294 defending rows match observed minutes. The 56 unmatched defending rows are reported in outputs, with unknown eligibility rather than assumed zero minutes. The eligible running frame has 57 MF and 91 FW; pressing has 71 MF and 49 FW.

Sampling is without replacement within position, using **seed 2026 for MF and 2027 for FW**. The original seed convention was retained, not repeatedly changed to obtain significance. Random sampling within the captured frame cannot remove the source table's coverage bias. Samples are large fractions of these frames, so ordinary t intervals should be understood as approximate model-based course inference, not exact design-based finite-population intervals.

The Week 4 independent-samples formula uses unequal group variances and conservative df=min(n1-1,n2-1). This is the primary reported test. Software Welch degrees of freedom are a sensitivity check: p=0.000696 for running and p=0.002128 for pressing. See [analysis notes](docs/max_analysis_notes.md) for assumptions and interpretation.

**Exploratory selection:** earlier shooting, passing and turnover questions did not reject H0. A turnover-per-pressure alternative also did not reject H0. The pressing-share question was selected after inspecting results. Its nominal p-value is not independent confirmatory evidence and does not account for searching across questions. Previous results are preserved in [the archive](archive/2026-08-31). No unsuccessful result was changed into a significant one by editing observations.

## Run

Python 3.12 was used. From the repository root:

```sh
python -m venv .venv
python -m pip install -r requirements.txt
python src/run_max_analysis.py
python -m unittest discover -s tests -v
```

Activate the environment before installing/running: Windows PowerShell `.venv\Scripts\Activate.ps1`; macOS/Linux `source .venv/bin/activate`. Alternatively call `.venv\Scripts\python.exe` directly on Windows. There is no requirement to switch to an old analysis branch.

The runner builds both tasks. Individual entry points are `src/task1_running.py` and `src/task2_pressing.py` after preparation. `outputs/` contains selected samples, descriptive statistics, CIs, course/Welch test results, eligible-frame summaries, coverage audits and Python-generated figures. The generated merged dataset is excluded from Git because the source snapshots and preparation script recreate it.

## Presentation and assessment evidence

- [PowerPoint: Maximus Turner's segment](presentation/Maximus_Turner_HIT140.pptx)
- [Three-minute discussion script](presentation/three_minute_script.md)
- [Detailed analysis and learning-material mapping](docs/max_analysis_notes.md)
- [Contribution and decision record](docs/contributions_and_decisions.md)
- [Recording and submission checklist](docs/presentation_and_submission_checklist.md)
- [AI declaration drafting notes](docs/ai_acknowledgement.md)

The presentation uses Python figures, editable slide text and speaker notes. It addresses the two questions, preparation, sampling, descriptive statistics, confidence intervals, hypothesis testing, limitations and lessons learned. Week 8 regression is intentionally excluded because this is Objective 1. Recording, student-ID verification and signed declarations are separate submission steps, not completed by the code.
