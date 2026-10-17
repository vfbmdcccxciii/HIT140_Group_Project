# HIT140 A3 — report notes (Objective 2), Darwin Group 27
All numbers come from `python src/run_all.py` (seed 140). Validation uses repeated 5-fold CV (5 folds × 20 repeats), with out-of-fold predictions for the predicted-vs-actual plots.

## 1. Data (≈⅓ page)
- **104 matches** (72 group, 32 knockout; 9 went to extra time), 308 goals in total. Results come from openfootball and were cross-checked against eloratings.net: all 208 team scores agree.
- Every predictor is **known before kick-off**:
  - Static: pre-tournament FIFA rank, Transfermarkt average player value (log10), average age, number of World Cup participations, and host nation.
  - Dynamic: pre-match Elo rating, and goals for/against averaged over the **previous 10 internationals**. That window includes pre-tournament fixtures, so first matches use pre-tournament form rather than imputed values, as the lecturer advised.
- **Feature engineering:**
  - Log transforms of rank and market value (both are heavily skewed).
  - 2.1: team1 − team2 **difference** features.
  - 2.2: the team's own attack paired with the opponent's defence and strength.
- **Variable overlap:** 2.1 uses only difference variables and 2.2 uses only raw team/opponent values, so **0 variables are shared** (the limit is 4).

## 2. Model 2.1: goal difference (n = 104)
Variables (8): `elo_diff, log_rank_diff, log_value_diff, gf10_diff, ga10_diff, age_diff, wc_exp_diff, host_diff`
- **EDA:**
  - Goal difference has mean 0.48, SD 2.02 and range −4 to +6.
  - Strongest correlations: log_value_diff r = 0.68, log_rank_diff −0.63, elo_diff 0.63, wc_exp_diff 0.55, ga10_diff −0.48, gf10_diff 0.41.
  - The heatmap shows that Elo, rank and value are highly inter-correlated (VIF 4–7).
- **OLS fit:**
  - R² = 0.531, adjusted R² = 0.491, F-test p < 0.001.
  - Significant at 5%: **log_value_diff** (b = 1.65, p < 0.001; a 10× squad-value advantage is worth about +1.65 goals), **host_diff** (+0.96 goals for hosts, p = 0.027) and age_diff (+0.21 per year older, p = 0.043).
  - Elo and rank are not individually significant once value is included. That is multicollinearity: they carry the same "team strength" signal.
- **CV:**
  - R² = 0.379 ± 0.16, RMSE = 1.52, MAE = 1.23.
  - The mean-only baseline has RMSE 2.01, so the model cuts error by about 24%.
- **Predicted vs actual:**
  - The model gets the sign of goal difference right in **82.5% of decisive matches**.
  - W/D/L accuracy is 58.7%, using |pred| < 0.5 as a predicted draw.
  - Largest misses: Canada 6–0 Qatar, Canada vs Morocco (−3), USA vs Belgium (−3), USA 3–0 Paraguay, Germany 6–0 Curaçao. These are blow-outs and upsets, and a linear model regresses them toward the mean.
- **Competing models (CV RMSE):** Ridge 1.519 ≈ OLS 1.524 < Lasso 1.541 ≈ ElasticNet 1.543 < Random Forest 1.569 < Gradient Boosting 1.676 << baseline 2.013. Regularisation adds almost nothing, and tree models overfit with n = 104. The relationship is essentially linear.

## 3. Model 2.2: team goals (n = 208)
Variables (8): `elo_pre, opp_elo_pre, gf10, opp_ga10, log_avg_value, opp_log_avg_value, host, knockout`
- **EDA:**
  - Goals per team-match have mean 1.48 and are right-skewed (count data).
  - Correlations: log_avg_value 0.41, elo_pre 0.33, opp_elo_pre −0.33, opp_log_avg_value −0.31, gf10 0.28, opp_ga10 0.27.
- **OLS fit:**
  - R² = 0.306, adjusted R² = 0.278, F-test p < 0.001.
  - Significant: **log_avg_value** (b = 1.18, p < 0.001).
  - Borderline: opp_elo_pre (−0.002 per Elo point, i.e. about −0.2 goals per 100 points, p = 0.09) and host (+0.55, p = 0.09).
  - Knockout has no effect (p = 0.46).
- **CV:** R² = 0.210 ± 0.12, RMSE = 1.206, MAE = 0.955. The baseline RMSE is 1.390.
- **Competing models (CV RMSE):** Lasso 1.197 (best) ≈ ElasticNet 1.198 ≈ Ridge 1.202 ≈ Poisson GLM 1.202 < OLS 1.206 < RF 1.230 < GBM 1.303 << baseline 1.390.
  - Lasso shrinks elo_pre, gf10 and knockout to 0, keeping own value plus opponent Elo. This is a parsimony argument.
- **Interpretation:** a single team's goal count is noisier (Poisson-like) than goal difference, which explains the lower R². Goal difference cancels shared match factors.

## 4. Discussion / limitations
- Squad market value is the single best pre-match predictor in both models.
- Multicollinearity among strength proxies makes individual coefficients unstable, so interpret them as a group. Ridge/Lasso help here.
- The Transfermarkt values are **current (Oct 2026), not a pre-tournament snapshot**, which could cause mild leakage. State this, or replace them with a pre-tournament snapshot if a group member can find one.
- eloratings.net is not one of the listed sources. Justify its use, or ask the lecturer.
- Small n, count-valued targets and a non-normal residual tail (see the Q-Q plots).
- Possible extensions: Poisson/negative binomial models for goals, an ordinal model for W/D/L, and in-tournament xG.

## 5. Suggested figures (≈4 total to fit 4 pages)
1. `outputs/eda_2_1_heatmap.png` (or eda_2_1_scatter.png)
2. `outputs/model_2_1_pred_vs_actual.png`
3. `outputs/model_2_2_pred_vs_actual.png`
4. `outputs/compare_2_1.png` + `compare_2_2.png` (or the tables `compare_2_*.csv`)

Tables: `model_2_*_ols_coefficients.csv`, `model_2_*_metrics.csv`.
