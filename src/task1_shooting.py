"""Task 1: shooting volume and team tournament progression."""

from analysis_common import PROCESSED_FILE, run_two_sample_task
import pandas as pd


def main():
    data = pd.read_csv(PROCESSED_FILE)
    eligible = data[
        (data["position"] != "GK")
        & (data["minutes_played"] >= 90)
        & data["attempts_at_goal_per90"].notna()
    ].copy()
    eligible["progression_group"] = eligible["reached_knockout"].map(
        {True: "Knockout team", False: "Group-stage exit"}
    )

    run_two_sample_task(
        eligible=eligible,
        task_name="task1_shooting",
        question=(
            "Do outfield players from knockout teams average a different number "
            "of attempts at goal per 90 than players from group-stage exits?"
        ),
        group_column="progression_group",
        groups=["Knockout team", "Group-stage exit"],
        metric="attempts_at_goal_per90",
        metric_label="Attempts at goal per 90 minutes",
        sample_size=60,
    )


if __name__ == "__main__":
    main()
