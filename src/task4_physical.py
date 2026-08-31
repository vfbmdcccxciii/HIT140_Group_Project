"""Task 4: distance covered by playing position."""

from analysis_common import PROCESSED_FILE, run_two_sample_task
import pandas as pd


def main():
    data = pd.read_csv(PROCESSED_FILE)
    eligible = data[
        data["position"].isin(["MF", "FW"])
        & (data["minutes_played"] >= 180)
        & data["total_distance_km_per90"].notna()
    ].copy()
    eligible["position_group"] = eligible["position"].map(
        {"MF": "Midfielder", "FW": "Forward"}
    )

    run_two_sample_task(
        eligible=eligible,
        task_name="task4_physical",
        question=(
            "Do midfielders and forwards average different distance covered per 90?"
        ),
        group_column="position_group",
        groups=["Midfielder", "Forward"],
        metric="total_distance_km_per90",
        metric_label="Total distance (km per 90 minutes)",
        sample_size=30,
    )


if __name__ == "__main__":
    main()
