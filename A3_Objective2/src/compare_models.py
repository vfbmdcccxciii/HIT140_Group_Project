"""Systematic comparison of competing algorithms for both tasks using identical repeated 5-fold CV
(5 folds x 20 repeats, same seed): baseline mean, OLS, Ridge, Lasso, ElasticNet (alpha tuned by inner CV),
Random Forest, Gradient Boosting, plus a Poisson GLM for goals (count target) as an extension."""
import pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, RidgeCV, LassoCV, ElasticNetCV, PoissonRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from common import PROC, OUT, SEED
from modelling import cv_scores
from model_2_1 import FEATURES_2_1, TARGET_2_1
from model_2_2 import FEATURES_2_2, TARGET_2_2
import numpy as np

def models(count_target=False):
    a = np.logspace(-3, 3, 50)
    m = {"Baseline (predict mean)": DummyRegressor(),
         "OLS linear regression": make_pipeline(StandardScaler(), LinearRegression()),
         "Ridge (alpha CV)": make_pipeline(StandardScaler(), RidgeCV(alphas=a)),
         "Lasso (alpha CV)": make_pipeline(StandardScaler(), LassoCV(cv=5, random_state=SEED, max_iter=20000)),
         "ElasticNet (CV)": make_pipeline(StandardScaler(), ElasticNetCV(cv=5, l1_ratio=[.2, .5, .8], random_state=SEED, max_iter=20000)),
         "Random Forest": RandomForestRegressor(n_estimators=300, min_samples_leaf=5, random_state=SEED, n_jobs=-1),
         "Gradient Boosting": GradientBoostingRegressor(n_estimators=150, max_depth=2, learning_rate=0.05, subsample=0.8, random_state=SEED)}
    if count_target:
        m["Poisson GLM (extension)"] = make_pipeline(StandardScaler(), PoissonRegressor(alpha=0.01, max_iter=1000))
    return m

def compare(df, feats, target, tag, title, count_target=False):
    rows = []
    for name, mdl in models(count_target).items():
        rows.append(dict(model=name, **cv_scores(mdl, df[feats], df[target], n_repeats=10 if "Forest" in name or "Boost" in name else 20)))
        print(f"  {tag} {name}: R2={rows[-1]['cv_r2']:.3f} RMSE={rows[-1]['cv_rmse']:.3f}")
    res = pd.DataFrame(rows).round(4).sort_values("cv_rmse"); res.to_csv(OUT / f"compare_{tag}.csv", index=False)
    fig, ax = plt.subplots(figsize=(7, 3.5))
    r = res.sort_values("cv_rmse", ascending=False)
    ax.barh(r.model, r.cv_rmse, xerr=r.cv_rmse_sd, color="tab:blue", alpha=.8); ax.set_xlabel("Repeated 5-fold CV RMSE (lower is better, bars = ±1 SD)")
    ax.set_title(f"{title}: competing models"); fig.tight_layout(); fig.savefig(OUT / f"compare_{tag}.png", dpi=150); plt.close(fig)
    # importance view from RF (non-linear check)
    rf = RandomForestRegressor(n_estimators=500, min_samples_leaf=5, random_state=SEED).fit(df[feats], df[target])
    pd.Series(rf.feature_importances_, feats).sort_values(ascending=False).round(4).to_csv(OUT / f"compare_{tag}_rf_importance.csv", header=["importance"])
    lasso = models()["Lasso (alpha CV)"].fit(df[feats], df[target])
    pd.Series(lasso[-1].coef_, feats).round(4).to_csv(OUT / f"compare_{tag}_lasso_coefs.csv", header=["std_coef"])
    return res

def main():
    compare(pd.read_csv(PROC / "matches_104.csv"), FEATURES_2_1, TARGET_2_1, "2_1", "Model 2.1 (goal difference)")
    compare(pd.read_csv(PROC / "team_matches_208.csv"), FEATURES_2_2, TARGET_2_2, "2_2", "Model 2.2 (team goals)", count_target=True)

if __name__ == "__main__":
    main()
