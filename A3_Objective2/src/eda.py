"""Exploratory data analysis for both modelling datasets: target distributions, descriptive stats,
correlation heatmaps and feature-vs-target scatter plots."""
import pandas as pd, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, seaborn as sns
from common import PROC, OUT
from model_2_1 import FEATURES_2_1, TARGET_2_1
from model_2_2 import FEATURES_2_2, TARGET_2_2

def eda(df, feats, target, tag, title):
    df[[target] + feats].describe().T.round(3).to_csv(OUT / f"eda_{tag}_descriptives.csv")
    corr = df[[target] + feats].corr()
    corr.round(3).to_csv(OUT / f"eda_{tag}_correlations.csv")
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=ax, annot_kws={"size": 7})
    ax.set_title(f"{title}: correlation matrix"); fig.tight_layout(); fig.savefig(OUT / f"eda_{tag}_heatmap.png", dpi=150); plt.close(fig)
    fig, ax = plt.subplots(figsize=(5, 3))
    vc = df[target].value_counts().sort_index(); ax.bar(vc.index, vc.values)
    ax.set_xlabel(target); ax.set_ylabel("count"); ax.set_title(f"{title}: target distribution (mean {df[target].mean():.2f}, sd {df[target].std():.2f})")
    fig.tight_layout(); fig.savefig(OUT / f"eda_{tag}_target_hist.png", dpi=150); plt.close(fig)
    fig, axes = plt.subplots(2, 4, figsize=(14, 6))
    for a, f in zip(axes.ravel(), feats):
        sns.regplot(x=df[f], y=df[target] + np.random.default_rng(0).uniform(-.15, .15, len(df)), ax=a, scatter_kws={"s": 10, "alpha": .5}, line_kws={"color": "r"})
        a.set_title(f"r = {df[f].corr(df[target]):.2f}"); a.set_ylabel(target)
    fig.suptitle(f"{title}: each explanatory variable vs target"); fig.tight_layout(); fig.savefig(OUT / f"eda_{tag}_scatter.png", dpi=150); plt.close(fig)

def main():
    m = pd.read_csv(PROC / "matches_104.csv"); t = pd.read_csv(PROC / "team_matches_208.csv")
    eda(m, FEATURES_2_1, TARGET_2_1, "2_1", "Model 2.1")
    eda(t, FEATURES_2_2, TARGET_2_2, "2_2", "Model 2.2")
    # context tables
    m.groupby("knockout")[["goals1", "goals2"]].sum().assign(matches=m.groupby("knockout").size()).to_csv(OUT / "eda_goals_by_stage.csv")
    t.groupby("confederation").goals.agg(["count", "mean", "std"]).round(3).sort_values("mean").to_csv(OUT / "eda_goals_by_confederation.csv")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=t, x="confederation", y="goals", ax=ax); ax.set_title("Goals per team-match by confederation")
    fig.tight_layout(); fig.savefig(OUT / "eda_goals_by_confederation.png", dpi=150); plt.close(fig)
    print("EDA done")

if __name__ == "__main__":
    main()
