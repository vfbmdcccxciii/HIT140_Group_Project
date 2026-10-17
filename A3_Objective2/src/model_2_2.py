"""Linear Regression 2.2: predict goals scored by a team in a match (208 team-match rows).
Eight pre-match explanatory variables mixing the team's own strength/form with the opponent's defence."""
import pandas as pd
from common import PROC
from modelling import ols_report

FEATURES_2_2 = ["elo_pre", "opp_elo_pre", "gf10", "opp_ga10", "log_avg_value", "opp_log_avg_value", "host", "knockout"]
TARGET_2_2 = "goals"

def load():
    return pd.read_csv(PROC / "team_matches_208.csv")

def main():
    df = load(); assert len(df) == 208 and len(FEATURES_2_2) == 8
    df[["match_id", "team", "opponent", TARGET_2_2] + FEATURES_2_2].to_csv(PROC / "model_2_2_dataset.csv", index=False)
    return ols_report(df, FEATURES_2_2, TARGET_2_2, "model_2_2", "Model 2.2 (team goals)")

if __name__ == "__main__":
    main()
