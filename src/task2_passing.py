"""Task 2: passing accuracy by playing position."""

from analysis_common import PROCESSED_FILE, run_two_sample_task
import pandas as pd


def main():
    data = pd.read_csv(PROCESSED_FILE)
    eligible = data[
        data["position"].isin(["MF", "DF"])
        & (data["minutes_played"] >= 180)
        & data["passing_accuracy_pct"].notna()
    ].copy()
    eligible["position_group"] = eligible["position"].map(
        {"MF": "Midfielder", "DF": "Defender"}
    )

    run_two_sample_task(
        eligible=eligible,
        task_name="task2_passing",
        question=(
            "Is average passing accuracy different for midfielders and defenders?"
        ),
        group_column="position_group",
        groups=["Midfielder", "Defender"],
        metric="passing_accuracy_pct",
        metric_label="Passing accuracy (%)",
        sample_size=50,
    )


if __name__ == "__main__":
    main()
