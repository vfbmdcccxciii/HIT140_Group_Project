"""Shared modelling helpers: OLS fit, K-fold CV metrics, predicted-vs-actual and diagnostics plots."""
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import RepeatedKFold, KFold, cross_val_predict
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from common import OUT, SEED

def cv_scores(model, X, y, n_splits=5, n_repeats=20):
    """Repeated K-fold CV: mean and SD of R2 / RMSE / MAE on held-out folds."""
    rows = []
    for tr, te in RepeatedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=SEED).split(X):
        model.fit(X.iloc[tr], y.iloc[tr]); p = model.predict(X.iloc[te])
        rows.append((r2_score(y.iloc[te], p), mean_squared_error(y.iloc[te], p) ** 0.5, mean_absolute_error(y.iloc[te], p)))
    a = np.array(rows)
    return dict(cv_r2=a[:, 0].mean(), cv_r2_sd=a[:, 0].std(), cv_rmse=a[:, 1].mean(), cv_rmse_sd=a[:, 1].std(), cv_mae=a[:, 2].mean(), cv_mae_sd=a[:, 2].std())

def ols_report(df, features, target, tag, title):
    X, y = df[features], df[target]
    ols = sm.OLS(y, sm.add_constant(X)).fit()
    coef = pd.DataFrame({"coef": ols.params, "std_err": ols.bse, "t": ols.tvalues, "p_value": ols.pvalues,
                         "ci_low": ols.conf_int()[0], "ci_high": ols.conf_int()[1]})
    # standardised coefficients (effect of +1 SD) for comparing importance
    coef["std_coef"] = [np.nan] + [ols.params[f] * X[f].std() / y.std() for f in features]
    coef["vif"] = [np.nan] + [variance_inflation_factor(sm.add_constant(X).values, i + 1) for i in range(len(features))]
    coef.round(4).to_csv(OUT / f"{tag}_ols_coefficients.csv")
    (OUT / f"{tag}_ols_summary.txt").write_text(str(ols.summary()))
    cv = cv_scores(LinearRegression(), X, y)
    oof = cross_val_predict(LinearRegression(), X, y, cv=KFold(5, shuffle=True, random_state=SEED))
    fit = dict(model=f"OLS {tag}", n=len(y), k=len(features), train_r2=ols.rsquared, adj_r2=ols.rsquared_adj,
               f_pvalue=ols.f_pvalue, train_rmse=np.sqrt(ols.mse_resid * ols.df_resid / len(y)),
               baseline_rmse_predict_mean=y.std(ddof=0), oof_r2=r2_score(y, oof),
               oof_rmse=mean_squared_error(y, oof) ** 0.5, oof_mae=mean_absolute_error(y, oof), **cv)
    pd.DataFrame([fit]).round(4).to_csv(OUT / f"{tag}_metrics.csv", index=False)
    # predicted vs actual (out-of-fold predictions, so they are honest)
    pred = df[[c for c in ["match_id", "team", "opponent", "team1", "team2", "round"] if c in df]].copy()
    pred["actual"] = y; pred["predicted_oof"] = oof.round(3); pred["residual"] = (y - oof).round(3)
    if target == "goal_diff":
        pred["actual_outcome"] = np.sign(y); pred["pred_outcome"] = np.where(oof > 0.5, 1, np.where(oof < -0.5, -1, 0))
    pred.to_csv(OUT / f"{tag}_predictions.csv", index=False)
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    jit = np.random.default_rng(SEED).uniform(-.15, .15, len(y))
    ax[0].scatter(oof, y + jit, alpha=.6); lo, hi = min(oof.min(), y.min()), max(oof.max(), y.max())
    ax[0].plot([lo, hi], [lo, hi], "r--", label="perfect prediction"); ax[0].set_xlabel("Predicted (5-fold out-of-fold)"); ax[0].set_ylabel("Actual (jittered)")
    ax[0].set_title(f"{title}: predicted vs actual\nOOF R²={fit['oof_r2']:.2f}, RMSE={fit['oof_rmse']:.2f}"); ax[0].legend()
    ax[1].scatter(ols.fittedvalues, ols.resid, alpha=.6); ax[1].axhline(0, color="r", ls="--")
    ax[1].set_xlabel("Fitted"); ax[1].set_ylabel("Residual"); ax[1].set_title("Residuals vs fitted (full-data OLS)")
    fig.tight_layout(); fig.savefig(OUT / f"{tag}_pred_vs_actual.png", dpi=150); plt.close(fig)
    fig = sm.qqplot(ols.resid, line="45", fit=True); fig.suptitle(f"{title}: residual Q-Q"); fig.savefig(OUT / f"{tag}_qq.png", dpi=120); plt.close(fig)
    # coefficient plot
    c = coef.drop("const")
    fig, ax = plt.subplots(figsize=(6, 3.5)); ax.barh(c.index, c.std_coef, xerr=None, color=["tab:green" if p < .05 else "tab:gray" for p in c.p_value])
    ax.axvline(0, color="k"); ax.set_xlabel("Standardised coefficient (green = p<0.05)"); ax.set_title(f"{title}: standardised coefficients")
    fig.tight_layout(); fig.savefig(OUT / f"{tag}_coefficients.png", dpi=150); plt.close(fig)
    print(f"[{tag}] train R2={ols.rsquared:.3f} adjR2={ols.rsquared_adj:.3f} | CV R2={cv['cv_r2']:.3f} RMSE={cv['cv_rmse']:.3f} MAE={cv['cv_mae']:.3f}")
    return ols, fit
