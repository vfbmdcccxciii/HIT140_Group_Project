import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats

# Load the dataset from the CSV file
df = pd.read_csv("player_age_stats.csv")

# FILTER DATASET FOR THE ANALYTICAL QUESTION
# What is the average age of rostered players who scored at least one goal during
# the FIFA World Cup 2026? Exclude players who did not score.

# Filter to keep only players who scored at least one goal (excluding those with 0 goals)
df_all_scorers = df[df["goals_score"] >= 1].dropna(subset=["players_age"])

# Randomly sample directly from the goalscorers population.
sample_size_target = 50

if len(df_all_scorers) >= sample_size_target:
    df_scorers = df_all_scorers.sample(n=sample_size_target, random_state=42)
else:
    df_scorers = df_all_scorers
    print(f"Warning: Sample size requested ({sample_size_target}) is larger than total scorers ({len(df_all_scorers)}). Using all scorers.")

print(f"--- Sampling Summary ---")
print(f"Total Goalscorers available in data: {len(df_all_scorers)}")
print(f"Randomly Sampled Goalscorers used for analysis (n): {len(df_scorers)}")
print("\n" + "=" * 45 + "\n")

# Calculate the statistics for goalscorers
n_samples = len(df_scorers)
mean_age = df_scorers["players_age"].mean()
median_age = df_scorers["players_age"].median()
mode_age = df_scorers["players_age"].mode()[0]
age_range = df_scorers["players_age"].max() - df_scorers["players_age"].min()
column_std = df_scorers["players_age"].std()

print("--- Player Age Statistics (Goalscorers Only) ---")
print(f"Mean (Average): {mean_age:.2f} years")
print(f"Median (Middle): {median_age} years")
print(f"Mode (Most Common): {mode_age} years")
print(f"Range (Spread): {age_range} years (Max: {df_scorers['players_age'].max()} - Min: {df_scorers['players_age'].min()})")
print(f"Sample Standard Deviation: {column_std:.2f}")

# Calculate 95% Confidence Interval for the Mean (Overall Sample)
sem = stats.sem(df_scorers["players_age"])
confidence_level = 0.95
degrees_freedom = n_samples - 1
confidence_interval = stats.t.interval(confidence_level, degrees_freedom, mean_age, sem)

print(f"95% Confidence Interval for Mean Age: ({confidence_interval[0]:.2f}, {confidence_interval[1]:.2f})")
print("\n" + "=" * 45 + "\n")


# TWO-SAMPLE T-TEST: YOUNGER VS OLDER PLAYERS GOALS
print("--- Two-Sample T-Test & Sub-Group Analytics (Scorers Only) ---")

age_threshold = mean_age

# Split groups directly from the sampled data (removed redundant filtering step)
younger_players = df_scorers[df_scorers["players_age"] <= age_threshold]["goals_score"]
older_players = df_scorers[df_scorers["players_age"] > age_threshold]["goals_score"]

# --- GROUP STATISTICAL CALCULATIONS ---
# Younger Group Calculations
younger_n = len(younger_players)
younger_mean = younger_players.mean()
younger_std = younger_players.std()
younger_sem = stats.sem(younger_players)
younger_ci = stats.t.interval(0.95, df=younger_n - 1, loc=younger_mean, scale=younger_sem)

# Older Group Calculations
older_n = len(older_players)
older_mean = older_players.mean()
older_std = older_players.std()
older_sem = stats.sem(older_players)
older_ci = stats.t.interval(0.95, df=older_n - 1, loc=older_mean, scale=older_sem)

# Print Detailed Sub-Group Metrics
print(f"Younger Scorers (Age <= {age_threshold} yrs): n = {younger_n}")
print(f"  Mean Goals: {younger_mean:.2f}")
print(f"  Standard Deviation: {younger_std:.2f}")
print(f"  SEM: {younger_sem:.2f}")
print(f"  95% Confidence Interval for Goals: ({younger_ci[0]:.2f}, {younger_ci[1]:.2f})")

print(f"\nOlder Scorers (Age > {age_threshold} yrs): n = {older_n}")
print(f"  Mean Goals: {older_mean:.2f}")
print(f"  Standard Deviation: {older_std:.2f}")
print(f"  SEM: {older_sem:.2f}")
print(f"  95% Confidence Interval for Goals: ({older_ci[0]:.2f}, {older_ci[1]:.2f})")
print("-" * 45)

# Perform independent two-sample t-test (Welch's t-test)
t_stat, p_value = stats.ttest_ind_from_stats(younger_mean, younger_std, younger_n, older_mean, older_std, older_n, equal_var=False, alternative='two-sided')

print(f"T-Statistic: {t_stat:.4f}")
print(f"P-Value: {p_value:.4f}")

alpha = 0.05
if p_value < alpha:
    conclusion = "Reject the null hypothesis H0:\nStatistically significant difference"
else:
    conclusion = "Fail to reject the null hypothesis H0:\nNo statistically significant difference"
print(f"Conclusion: {conclusion.replace('\n', ' ')}")


# CREATE SIDE-BY-SIDE HISTOGRAM VISUALIZATION COMPARING YOUNGER VS OLDER GOALSCORERS
plt.figure(figsize=(10, 6))

max_goals = int(max(df_scorers["goals_score"].max(), 5))
bins = np.arange(0.5, max_goals + 1.5, 1) 

# Pass both arrays as a list to plot bars side-by-side automatically
plt.hist([younger_players, older_players], bins=bins, color=["royalblue", "darkorange"], 
         edgecolor="black", alpha=0.85,
         label=[f"Younger (≤ {age_threshold} yrs) | n={younger_n}", 
                f"Older (> {age_threshold} yrs) | n={older_n}"])

# Add vertical dashed lines for the group means
plt.axvline(younger_mean, color="blue", linestyle="dashed", linewidth=1.5, 
            label=f"Younger Mean: {younger_mean:.2f}")
plt.axvline(older_mean, color="chocolate", linestyle="dashed", linewidth=1.5, 
            label=f"Older Mean: {older_mean:.2f}")

# Configure labels, titles, and layout
plt.title("Distribution of Goals Scored: Younger vs. Older Goalscorers", fontsize=14, fontweight="bold")
plt.xlabel("Number of Goals Scored", fontsize=12)
plt.ylabel("Player Count", fontsize=12)
plt.xticks(range(1, max_goals + 1))

# Statistical metrics text box placement
stats_text = (f"Welch's t-test Results:\n"
              f"t-stat: {t_stat:.3f}\n"
              f"p-value: {p_value:.4f}\n\n"
              f"{conclusion}")

plt.gca().text(0.95, 0.50, stats_text, transform=plt.gca().transAxes, fontsize=10,
            verticalalignment="center", horizontalalignment="right",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.9, edgecolor="gray"))

plt.legend(loc="upper right")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()

# Display the plot
plt.show()