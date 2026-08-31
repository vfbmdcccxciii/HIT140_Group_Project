"""Task 3: forced turnovers by playing position."""

from analysis_common import PROCESSED_FILE, run_two_sample_task
import pandas as pd


def main():
    data = pd.read_csv(PROCESSED_FILE)
    eligible = data[
        data["position"].isin(["MF", "FW"])
        & (data["minutes_played"] >= 90)
        & data["forced_turnovers_per90"].notna()
    ].copy()
    eligible["position_group"] = eligible["position"].map(
        {"MF": "Midfielder", "FW": "Forward"}
    )

    run_two_sample_task(
        eligible=eligible,
        task_name="task3_defending",
        question=(
            "Do midfielders and forwards average different forced turnovers per 90?"
        ),
        group_column="position_group",
        groups=["Midfielder", "Forward"],
        metric="forced_turnovers_per90",
        metric_label="Forced turnovers per 90 minutes",
        sample_size=40,
    )


if __name__ == "__main__":
    main()
