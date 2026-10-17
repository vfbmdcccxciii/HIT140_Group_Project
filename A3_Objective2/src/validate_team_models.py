"""Independent validation of the two team-member models (Max Turner, HIT140 A3, Darwin Group 27).

Reads Stephen's 2.1 CSV and Quentin's 2.2 CSV UNCHANGED and re-evaluates each model exactly as its
author specified it (same features, same estimator), using the group's common validation design:
repeated 5-fold CV (5 folds x 20 repeats, seed 140) with the StandardScaler fitted inside each
training fold (sklearn Pipeline), so no information leaks from held-out matches.
Each model is compared with a mean-only baseline (predicts the training-fold mean).
Nothing in the members' code or datasets is modified; derived columns are built in memory only,
using the same formulas as the authors' scripts.
"""
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeCV, LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.model_selection import RepeatedKFold
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

SEED = 140
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"; OUT.mkdir(exist_ok=True)
# Locate the members' files: repo layout first, then the local copies on the box.
CANDIDATES_21 = [ROOT.parent / "Assessment 3 dataset and python codes (stephen Kenyi)" / "FIFA_2026_predictive_pre_match_world_cup_Datastats.csv",
                 Path("/workspace/hit140/stephen/FIFA_2026_predictive_pre_match_world_cup_Datastats.csv")]
CANDIDATES_22 = [ROOT.parent / "dataset_objective_2_2_208_rows.csv", Path("/workspace/hit140/quentin/q.csv")]
first = lambda c: next(p for p in c if p.exists())


def stephen_2_1():
    df = pd.read_csv(first(CANDIDATES_21))
    for col in ["Team_1_Name", "Team_2_Name", "Pre_Match_Elo_Advantage_Holder", "Tournament_Stage"]:
        df[col] = df[col].astype(str).str.strip()
    # same derived columns as MLR_Stage_Aware_Model_Python_Code.py (in memory only)
    df["Directional_Elo_Difference"] = np.where(df["Pre_Match_Elo_Advantage_Holder"] == df["Team_1_Name"],
                                                df["Pre_Match_Elo_Difference_Value"], -df["Pre_Match_Elo_Difference_Value"])
    df["Is_Knockout"] = np.where(df["Tournament_Stage"] == "Group stage", 0, 1)
    df["Elo_x_IsKnockout"] = df["Directional_Elo_Difference"] * df["Is_Knockout"]
    df["Big5_Roster_x_IsKnockout"] = df["Elite_Big5_League_Player_Count_Diff"] * df["Is_Knockout"]
    base8 = ["Directional_Elo_Difference", "Historical_H2H_Win_Diff", "Scored_First_Percentage_Diff",
             "Fouls_Committed_Per90_Fewer_Diff", "Rest_Days_Advantage", "Average_Squad_Travel_Distance_KM_Diff",
             "Elite_Big5_League_Player_Count_Diff", "Historical_Squad_Distance_Covered_Km_Per90_Diff"]
    full11 = base8 + ["Is_Knockout", "Elo_x_IsKnockout", "Big5_Roster_x_IsKnockout"]
    return df, base8, full11, "Final_Goal_Difference"


def quentin_2_2():
    df = pd.read_csv(first(CANDIDATES_22))
    feats = ["team_fifa_rank", "opp_fifa_rank", "is_host_or_home", "rest_days",
             "squad_mean_age", "veteran_scorer_ratio", "pre_match_scoring_form", "squad_attacking_depth"]
    return df, feats, "team_goals"


def repeated_cv(est, X, y, n_splits=5, n_repeats=20):
    rows = []
    for tr, te in RepeatedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=SEED).split(X):
        est.fit(X.iloc[tr], y.iloc[tr]); p = est.predict(X.iloc[te])
        rows.append((r2_score(y.iloc[te], p), mean_squared_error(y.iloc[te], p) ** 0.5, mean_absolute_error(y.iloc[te], p)))
    a = np.array(rows)
    return dict(cv_r2=a[:, 0].mean(), cv_r2_sd=a[:, 0].std(), cv_r2_min=a[:, 0].min(), cv_r2_max=a[:, 0].max(),
                cv_rmse=a[:, 1].mean(), cv_mae=a[:, 2].mean(), folds=len(a))


def main():
    ridge = lambda: make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-3, 3, 100)))
    ols = lambda: make_pipeline(StandardScaler(), LinearRegression())
    base = lambda: DummyRegressor(strategy="mean")
    rows = []
    d1, base8, full11, t1 = stephen_2_1()
    rows.append(dict(model="2.1 Stephen: Ridge, 11 terms as specified", n=len(d1), k=len(full11), **repeated_cv(ridge(), d1[full11], d1[t1])))
    rows.append(dict(model="2.1 Stephen: Ridge, 8 base variables only (sensitivity)", n=len(d1), k=8, **repeated_cv(ridge(), d1[base8], d1[t1])))
    rows.append(dict(model="2.1 mean-only baseline", n=len(d1), k=0, **repeated_cv(base(), d1[full11], d1[t1])))
    d2, f2, t2 = quentin_2_2()
    rows.append(dict(model="2.2 Quentin: OLS, 8 variables as specified", n=len(d2), k=len(f2), **repeated_cv(ols(), d2[f2], d2[t2])))
    rows.append(dict(model="2.2 mean-only baseline", n=len(d2), k=0, **repeated_cv(base(), d2[f2], d2[t2])))
    # NB: 2.2 rows are two per match; plain KFold can put both rows of a match in different folds.
    # Report a match-grouped variant as a robustness check.
    from sklearn.model_selection import GroupKFold
    g = d2["match_id"].values; rs = []
    rng = np.random.default_rng(SEED)
    for r in range(20):
        perm = rng.permutation(np.unique(g)); remap = {m: i for i, m in enumerate(perm)}
        gg = np.array([remap[m] for m in g])
        for tr, te in GroupKFold(5).split(d2, groups=gg):
            e = ols().fit(d2[f2].iloc[tr], d2[t2].iloc[tr]); p = e.predict(d2[f2].iloc[te])
            rs.append((r2_score(d2[t2].iloc[te], p), mean_squared_error(d2[t2].iloc[te], p) ** 0.5, mean_absolute_error(d2[t2].iloc[te], p)))
    a = np.array(rs)
    rows.append(dict(model="2.2 Quentin: OLS, match-grouped 5-fold (robustness)", n=len(d2), k=8, cv_r2=a[:, 0].mean(), cv_r2_sd=a[:, 0].std(),
                     cv_r2_min=a[:, 0].min(), cv_r2_max=a[:, 0].max(), cv_rmse=a[:, 1].mean(), cv_mae=a[:, 2].mean(), folds=len(a)))
    res = pd.DataFrame(rows).round(4)
    res.to_csv(OUT / "validate_team_models.csv", index=False)
    print(res.to_string(index=False))

    # Data-consistency audit (read-only): shared variables, host-flag coverage, Elo agreement with Max's pull
    shared = sorted(set(map(str.lower, full11)) & set(f2))
    notes = [f"Exact-name shared variables 2.1(Stephen) vs 2.2(Quentin): {shared or 'none'}",
             "Conceptual overlap: rest days (Rest_Days_Advantage vs rest_days) = 1 shared concept (limit 4).",
             f"Quentin is_host_or_home = 1 in {d2['is_host_or_home'].mean():.1%} of rows; "
             f"rows for true hosts USA/Mexico/Canada: {d2['team'].isin(['USA','United States','Mexico','Canada']).sum()}"]
    mx = ROOT / "data" / "processed" / "matches_104.csv"
    if mx.exists():
        m = pd.read_csv(mx)
        alias = {"bosnia and herzegovina": "bosnia & herzegovina", "cabo verde": "cape verde", "congo dr": "dr congo",
                 "czechia": "czech republic", "côte d'ivoire": "ivory coast", "ir iran": "iran", "türkiye": "turkey",
                 "united states": "usa"}
        nm = lambda x: alias.get(str(x).strip().lower(), str(x).strip().lower())
        recs = []
        lookup = {}
        for _, r in m.iterrows():
            lookup.setdefault((nm(r.team1), nm(r.team2)), []).append(r.elo_diff)
            lookup.setdefault((nm(r.team2), nm(r.team1)), []).append(-r.elo_diff)
        for _, r in d1.iterrows():
            k = (nm(r.Team_1_Name), nm(r.Team_2_Name))
            if k in lookup and lookup[k]:
                recs.append((r.Team_1_Name, r.Team_2_Name, r.Directional_Elo_Difference, lookup[k].pop(0)))
        j = pd.DataFrame(recs, columns=["Team_1_Name", "Team_2_Name", "Directional_Elo_Difference", "elo_diff"])
        diff = (j["Directional_Elo_Difference"] - j["elo_diff"]).abs()
        notes.append(f"Elo gap agreement (Stephen vs eloratings pull, {len(j)} matches): median |diff| = {diff.median():.0f} pts, "
                     f">50 pts in {(diff > 50).sum()} matches, corr = {j['Directional_Elo_Difference'].corr(j['elo_diff']):.2f}; "
                     f"match 1 (Mexico v South Africa): {j.iloc[0]['Directional_Elo_Difference']:.0f} vs {j.iloc[0]['elo_diff']:.0f}")
    (OUT / "validate_team_models_audit.txt").write_text("\n".join(notes) + "\n")
    print("\n".join(notes))


if __name__ == "__main__":
    main()


def plot_comparison():
    """One compact figure: repeated 5-fold CV R2 for every candidate model of each objective."""
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    v = pd.read_csv(OUT / "validate_team_models.csv").set_index("model")
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.3))
    for ax, tag, mem, label in [(axes[0], "2_1", "2.1 Stephen: Ridge, 11 terms as specified", "Stephen Ridge (11 terms)"),
                                (axes[1], "2_2", "2.2 Quentin: OLS, 8 variables as specified", "Quentin OLS (8 vars)")]:
        c = pd.read_csv(OUT / f"compare_{tag}.csv").set_index("model")
        c = c.drop(index=[i for i in c.index if "Baseline" in i or "Elastic" in i])
        c.index = ["Max: " + i.replace(" linear regression", "").replace(" (alpha CV)", "") for i in c.index]
        c.loc[label] = v.loc[mem]
        c = c.sort_values("cv_r2")
        cols = ["tab:orange" if i == label else "tab:blue" for i in c.index]
        ax.barh(c.index, c.cv_r2, xerr=c.cv_r2_sd / np.sqrt(100) * 1.96, color=cols)
        ax.axvline(0, color="k", lw=.8); ax.set_xlabel("Repeated 5-fold CV R² (mean, 95% CI)", fontsize=7)
        ax.set_title(f"Model {tag.replace('_', '.')}: {'goal difference' if tag == '2_1' else 'team goals'}", fontsize=8)
        ax.tick_params(labelsize=6.5)
    fig.tight_layout(); fig.savefig(OUT / "validate_cv_comparison.png", dpi=200); plt.close(fig)


if __name__ == "__main__":
    plot_comparison()
