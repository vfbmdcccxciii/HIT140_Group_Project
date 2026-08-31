"""Merge the preserved FIFA tables and create analysis-ready variables."""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
KEY = ["player", "team", "position"]


def read_metric(filename):
    """Read one metric table and retain only its analysis columns."""
    data = pd.read_csv(RAW_DIR / filename)
    if data.duplicated(KEY).any():
        raise ValueError(f"Duplicate player/team/position keys in {filename}")
    return data.drop(columns=["rank", "source_url", "retrieved_date"])


def main():
    minutes = pd.read_csv(RAW_DIR / "fifa_player_minutes_2026-08-31.csv")
    if minutes.duplicated(KEY).any():
        raise ValueError("Duplicate player/team/position keys in minutes table")

    attacking = read_metric("fifa_player_attacking_2026-08-31.csv")
    distribution = read_metric("fifa_player_distribution_2026-08-31.csv")
    defending = read_metric("fifa_player_defending_2026-08-31.csv")
    physical = read_metric("fifa_player_physical_2026-08-31.csv")

    progression = pd.read_csv(
        RAW_DIR / "fifa_team_progression_2026-08-31.csv"
    ).drop(columns=["source_url", "retrieved_date"])
    if progression["team"].duplicated().any():
        raise ValueError("Duplicate team keys in progression table")

    data = minutes.copy()
    for metric_table in [attacking, distribution, defending, physical]:
        data = data.merge(
            metric_table,
            on=KEY,
            how="left",
            validate="one_to_one",
        )
    data = data.merge(
        progression,
        on="team",
        how="left",
        validate="many_to_one",
    )

    if data["reached_knockout"].isna().any():
        missing = sorted(data.loc[data["reached_knockout"].isna(), "team"].unique())
        raise ValueError(f"Missing tournament progression for: {missing}")
    if (data["minutes_played"] <= 0).any():
        raise ValueError("The minutes table must contain only players who appeared")

    data["attempts_at_goal_per90"] = (
        data["attempts_at_goal"] / data["minutes_played"] * 90
    )
    data["forced_turnovers_per90"] = (
        data["forced_turnovers"] / data["minutes_played"] * 90
    )
    data["total_distance_km_per90"] = (
        data["total_distance_metres"] / 1000 / data["minutes_played"] * 90
    )

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output = PROCESSED_DIR / "fifa_player_analysis.csv"
    data.to_csv(output, index=False)

    print(f"Saved {len(data)} player records to {output}")
    print("Players with each focal statistic:")
    print(
        data[
            [
                "attempts_at_goal_per90",
                "passing_accuracy_pct",
                "forced_turnovers_per90",
                "total_distance_km_per90",
            ]
        ].count()
    )


if __name__ == "__main__":
    main()
