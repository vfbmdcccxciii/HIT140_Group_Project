import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats

#Load the dataset from the CSV file
df = pd.read_csv("player_details.csv")

#FILTER DATASET FOR THE ANALYTICAL QUESTION

#What is the average age of rostered players who scored at least one goal during
# the FIFA World Cup 2026? Exclude players who did not score.

#Filter to keep only players who scored at least one goal (excluding those with 0 goals)
df_scorers = df[df["goals_score"] >= 1].dropna(subset=["players_age"])

df_all_scorers = df[df["goals_score"] >= 1].dropna(subset=["players_age"])

#Sample directly from the goalscorers population.
sample_size_target = 61

if len(df_all_scorers) >= sample_size_target:
    df_scorers = df_all_scorers.sample(n=sample_size_target, random_state=42)
else:
    # Fallback to using the entire population if the requested sample is too large
    df_scorers = df_all_scorers
    print(f"Warning: Sample size requested ({sample_size_target}) is larger than total scorers ({len(df_all_scorers)}). Using all scorers.")

print(f"--- Optimized Sampling Summary ---")
print(f"Total Goalscorers available in data: {len(df_all_scorers)}")
print(f"Randomly Sampled Goalscorers used for analysis (n): {len(df_scorers)}")

print("\n" + "=" * 45 + "\n")

#Calculate the statistics for goalscorers
mean_age = df_scorers["players_age"].mean()
median_age = df_scorers["players_age"].median()
mode_age = df_scorers["players_age"].mode()[0]
age_range = df_scorers["players_age"].max() - df_scorers["players_age"].min()
column_std = df_scorers["players_age"].std()

# Print the statistical results
print("--- Player Age Statistics (Goalscorers Only) ---")
print(f"Mean (Average): {mean_age:.2f} years")
print(f"Median (Middle): {median_age} years")
print(f"Mode (Most Common): {mode_age} years")
print(f"Range (Spread): {age_range} years (Max: {df_scorers['players_age'].max()} - Min: {df_scorers['players_age'].min()})")
print(f"Sample Standard Deviation: {column_std:.2f}")

print("\n" + "=" * 45 + "\n")

# Calculate the 95% confidence interval using T-Distribution method
players_ages = df_scorers["players_age"]
sample_mean = np.mean(players_ages)
sample_size = len(players_ages)
sample_std = players_ages.std(ddof=1)

# Standard error of mean
sem = stats.sem(players_ages)

confidence_level = 0.95
ci_lower, ci_upper = stats.t.interval(
    confidence_level, df=sample_size - 1, loc=sample_mean, scale=sem
)

print(f"--- 95% Confidence Interval Summary (T-Distribution) ---")
print(f"Sample Size (n): {sample_size}")
print(f"Sample Mean (x̄): {sample_mean:.2f}")
print(f"Sample Std Dev (s): {sample_std:.2f}")
print(f"Standard Error of mean (SEM): {sem:.2f}")
print(f"95% Confidence Interval: ({ci_lower:.2f}, {ci_upper:.2f})")

print("\n" + "=" * 45 + "\n")

# Execute ONE-SAMPLE T-TEST
# Null Hypothesis (H0): The mean age of 2026 FIFA goalscorers is equal to the historical benchmark (μ = 26.5 years).
# Alternative Hypothesis (H1): The mean age of 2026 FIFA goalscorers is not equal to the historical benchmark (μ ≠ 26.5 years).

historical_benchmark = 26.5
t_stat, p_value = stats.ttest_1samp(players_ages, popmean=historical_benchmark)

print(f"--- One-Sample T-Test Results ---")
print(f"Hypothesised Mean (μ₀): {historical_benchmark} years")
print(f"T-Statistic: {t_stat:.4f}")
print(f"P-Value: {p_value:.4f}")

print("\n" + "=" * 45 + "\n")

alpha = 0.05
print(f"--- Hypothesis Testing Conclusion ---")
if p_value < alpha:
    print(f"Reject the Null Hypothesis (H₀).")
    # Dynamically determine the direction of the difference
    direction = "less" if sample_mean < historical_benchmark else "greater"
    print(f"Conclusion: There is statistically significant evidence that the average age ")
    print(f"of 2026 FIFA WC goalscorers ({sample_mean:.2f} years) is {direction} than ")
    print(f"the historical benchmark ({historical_benchmark:.2f} years).")
else:
    print(f"Fail to reject the Null Hypothesis (H₀).")
    print(f"Conclusion: There is not enough evidence to prove that the average age of ")
    print(f"2026 World Cup goalscorers ({sample_mean:.2f} years) differs significantly from ")
    print(f"the historical benchmark ({historical_benchmark:.2f} years).")



# Create and display the histogram
plt.figure(figsize=(8, 5))
plt.hist(df_scorers["players_age"], bins=10, edgecolor="black", color="purple")

plt.axvline(
    x=sample_mean,
    color="skyblue",
    linestyle="--",
    linewidth=2,
    label=f"Sample Mean (x̄): {sample_mean:.1f}",
)


plt.axvline(
    x=historical_benchmark,
    color="red",
    linestyle=":",
    linewidth=2.5,
    label=f"Historical Mean (μ): {historical_benchmark}",
)

plt.axvspan(
    ci_lower,
    ci_upper,
    color="Orange",
    alpha=0.3,
    label=f"95% T-CI [{ci_lower:.2f}, {ci_upper:.2f}]",
)

plt.title(
    "Distribution of Age Among 2026 World Cup Goalscorers",
    fontsize=14,
    fontweight="bold",
    pad=15
)
plt.xlabel("Age", fontsize=12)
plt.ylabel("Number of Scorers", fontsize=12)
plt.grid(axis="y", alpha=0.75)
plt.legend(loc="upper right")

plt.tight_layout()
plt.show()