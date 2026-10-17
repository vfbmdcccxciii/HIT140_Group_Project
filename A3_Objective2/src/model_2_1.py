"""Linear Regression 2.1: predict goal difference (team1 goals - team2 goals) for all 104 WC 2026 matches.
Eight pre-match explanatory variables, all expressed as team1-minus-team2 differences (feature engineering)."""
import pandas as pd
from common import PROC
from modelling import ols_report

FEATURES_2_1 = ["elo_diff", "log_rank_diff", "log_value_diff", "gf10_diff", "ga10_diff", "age_diff", "wc_exp_diff", "host_diff"]
TARGET_2_1 = "goal_diff"

def load():
    return pd.read_csv(PROC / "matches_104.csv")

def main():
    df = load(); assert len(df) == 104 and len(FEATURES_2_1) == 8
    df[["match_id", "team1", "team2", TARGET_2_1] + FEATURES_2_1].to_csv(PROC / "model_2_1_dataset.csv", index=False)
    return ols_report(df, FEATURES_2_1, TARGET_2_1, "model_2_1", "Model 2.1 (goal difference)")

if __name__ == "__main__":
    main()
