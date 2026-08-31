"""Shared functions for the four Objective 1 analytic tasks."""

from pathlib import Path
import math

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_FILE = PROJECT_ROOT / "data" / "processed" / "fifa_player_analysis.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
RANDOM_SEED = 2026
ALPHA = 0.05


def random_sample_by_group(data, group_column, groups, sample_size):
    """Take the same-size reproducible random sample from each group."""
    samples = []
    for number, group in enumerate(groups):
        group_data = data[data[group_column] == group]
        if len(group_data) < sample_size:
            raise ValueError(
                f"{group} has {len(group_data)} eligible rows; "
                f"{sample_size} are required"
            )
        samples.append(
            group_data.sample(
                n=sample_size,
                replace=False,
                random_state=RANDOM_SEED + number,
            )
        )
    return pd.concat(samples, ignore_index=True)


def mean_confidence_interval(values, confidence=0.95):
    """Return a two-sided t confidence interval for a population mean."""
    clean = pd.Series(values).dropna()
    n = len(clean)
    mean = clean.mean()
    standard_error = clean.std(ddof=1) / math.sqrt(n)
    critical_value = stats.t.ppf((1 + confidence) / 2, df=n - 1)
    margin = critical_value * standard_error
    return mean - margin, mean + margin


def run_two_sample_task(
    eligible,
    task_name,
    question,
    group_column,
    groups,
    metric,
    metric_label,
    sample_size,
):
    """Sample, describe, infer, visualise, save, and print one task."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sample = random_sample_by_group(
        eligible,
        group_column=group_column,
        groups=groups,
        sample_size=sample_size,
    )

    descriptive_rows = []
    for group in groups:
        values = sample.loc[sample[group_column] == group, metric]
        lower, upper = mean_confidence_interval(values)
        descriptive_rows.append(
            {
                "group": group,
                "n": values.count(),
                "mean": values.mean(),
                "median": values.median(),
                "standard_deviation": values.std(ddof=1),
                "minimum": values.min(),
                "maximum": values.max(),
                "ci_95_lower": lower,
                "ci_95_upper": upper,
            }
        )
    descriptive = pd.DataFrame(descriptive_rows)

    first = sample.loc[sample[group_column] == groups[0], metric]
    second = sample.loc[sample[group_column] == groups[1], metric]
    test = stats.ttest_ind(first, second, equal_var=False)
    mean_difference = first.mean() - second.mean()
    conclusion = (
        "Reject H0: evidence of a difference in population means."
        if test.pvalue < ALPHA
        else "Fail to reject H0: insufficient evidence of a difference."
    )
    test_results = pd.DataFrame(
        [
            {
                "group_1": groups[0],
                "group_2": groups[1],
                "mean_difference_group_1_minus_group_2": mean_difference,
                "t_statistic": test.statistic,
                "degrees_of_freedom": getattr(test, "df", float("nan")),
                "p_value_two_sided": test.pvalue,
                "alpha": ALPHA,
                "conclusion": conclusion,
            }
        ]
    )

    sample.to_csv(OUTPUT_DIR / f"{task_name}_sample.csv", index=False)
    descriptive.to_csv(
        OUTPUT_DIR / f"{task_name}_descriptive_and_ci.csv", index=False
    )
    test_results.to_csv(OUTPUT_DIR / f"{task_name}_welch_t_test.csv", index=False)

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=sample, x=group_column, y=metric, color="#d9e8fb")
    sns.swarmplot(
        data=sample,
        x=group_column,
        y=metric,
        color="#17365d",
        size=4,
    )
    plt.title(question, wrap=True)
    plt.xlabel("")
    plt.ylabel(metric_label)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f"{task_name}_plot.png", dpi=200)
    plt.close()

    print(f"\n{question}")
    print(f"Eligible population rows: {len(eligible)}")
    print(f"Random sample: {sample_size} per group; seed={RANDOM_SEED}")
    print("\nDescriptive statistics and 95% confidence intervals:")
    print(descriptive.to_string(index=False))
    print("\nWelch independent two-sample t-test:")
    print(test_results.to_string(index=False))

    return descriptive, test_results
