import io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler

# Set seaborn style for clean visuals
sns.set_theme(style="whitegrid")

# 1. Load the dataset from the CSV file
file_name = "FIFA_2026_predictive_pre_match_world_cup_Datastats.csv"
try:
    df = pd.read_csv(file_name)
except FileNotFoundError:
    print(
        f"Error: The file '{file_name}' was not found. Please ensure it is in your current working directory."
    )
    exit()

for col in ["Team_1_Name", "Team_2_Name", "Pre_Match_Elo_Advantage_Holder"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# ==========================================
# STAGE-AWARE FEATURE 
# ==========================================
df["Directional_Elo_Difference"] = np.where(
    df["Pre_Match_Elo_Advantage_Holder"] == df["Team_1_Name"],
    df["Pre_Match_Elo_Difference_Value"],
    -df["Pre_Match_Elo_Difference_Value"],
)

# Map categorical stages to a binary Knockout flag (1 = Knockout, 0 = Group Stage)
df["Is_Knockout"] = np.where(
    df["Tournament_Stage"].astype(str).str.strip() == "Group stage", 0, 1
)

df["Elo_x_IsKnockout"] = df["Directional_Elo_Difference"] * df["Is_Knockout"]
df["Big5_Roster_x_IsKnockout"] = (
    df["Elite_Big5_League_Player_Count_Diff"] * df["Is_Knockout"]
)


features = [
    "Directional_Elo_Difference",
    "Historical_H2H_Win_Diff",
    "Scored_First_Percentage_Diff",
    "Fouls_Committed_Per90_Fewer_Diff",
    "Rest_Days_Advantage",
    "Average_Squad_Travel_Distance_KM_Diff",
    "Elite_Big5_League_Player_Count_Diff",
    "Historical_Squad_Distance_Covered_Km_Per90_Diff",
    "Is_Knockout",
    "Elo_x_IsKnockout",
    "Big5_Roster_x_IsKnockout",
]
target = "Final_Goal_Difference"

X = df[features]
y = df[target]

# 3. Split the data into training (60%) and testing (40%) sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.40, random_state=42
)

# 4. Standardize Data (Critical for fair coefficient penalization)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
X_all_scaled = scaler.fit_transform(X)  # Scale full matrix for cross-validation

# 5. Initialize and Fit Ridge Model 
model = RidgeCV(alphas=np.logspace(-3, 3, 100))
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)

# ==========================================
# K-FOLD CROSS-VALIDATION PIPELINE
# ==========================================
kf = KFold(n_splits=5, shuffle=True, random_state=42)

cv_r2_scores = cross_val_score(model, X_all_scaled, y, cv=kf, scoring="r2")
cv_mse_scores = -cross_val_score(
    model, X_all_scaled, y, cv=kf, scoring="neg_mean_squared_error"
)
cv_mae_scores = -cross_val_score(
    model, X_all_scaled, y, cv=kf, scoring="neg_mean_absolute_error"
)

# ==========================================
# METRICS & EVALUATION 
# ==========================================
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
rmse_norm = rmse / (y_test.max() - y_test.min()) if (y_test.max() - y_test.min()) != 0 else rmse
r2 = r2_score(y_test, y_pred)

# Baseline dummy evaluation metrics using the training baseline mean value
y_mean_baseline = np.full_like(y_test, y_train.mean())
mae_dummy = mean_absolute_error(y_test, y_mean_baseline)
r2_dummy = r2_score(y_test, y_mean_baseline)


print("======================================================================")
print("                    LEARNED REGRESSION PARAMETERS                     ")
print("======================================================================")
print(f"Model Intercept (Baseline Expectation): {model.intercept_:.4f}\n")
print(f"{'Explanatory Variable Name':<47} | {'Coefficient Weight'}")
print("----------------------------------------------------------------------")
for feature_name, coef_weight in zip(features, model.coef_):
    print(f"{feature_name:<47} |             {coef_weight:7.4f}")
print("======================================================================")
print("\nPredicted Score Sample Overview (Top 10 Rows Preview):")
print("   Actual  Predicted")
for idx, (actual_val, pred_val) in enumerate(zip(y_test[:10], y_pred[:10])):
    print(f"{idx:<5} {float(actual_val):<7.1f} {pred_val:<.6f}")

print("\nMultiple Linear Regression performance (Static 60/40 Split):")
print(f"Mean Absolute Error: {mae:.4f}")
print(f"Mean Squared Error: {mse:.4f}")
print(f"Root Mean Square Error: {rmse:.4f}")
print(f"Root Mean Square Error (Normalised): {rmse_norm:.4f}")
print(f"R-Squared: {r2:.4f}")

print("\n5-Fold Cross-Validation Performance:")
print(f"Mean Cross-Validated MAE: {cv_mae_scores.mean():.4f}")
print(f"Mean Cross-Validated MSE: {cv_mse_scores.mean():.4f}")
print(f"Mean Cross-Validated R2:  {cv_r2_scores.mean():.4f} (+/- {cv_r2_scores.std() * 2:.4f})")
print(f"R2 Scores per Individual Fold: {np.array2string(cv_r2_scores, precision=4)}")

print("\nDummy Baseline Performance (Using Mean):")
print(f"Mean Absolute Error: {mae_dummy:.4f}")
print(f"R-Squared: {r2_dummy:.4f}")

# ==========================================
# VISUALIZATION
# ==========================================
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

test_results = pd.DataFrame({"Actual": y_test, "Predicted": y_pred})
test_results["Stage"] = df.loc[X_test.index, "Tournament_Stage"].astype(str).str.strip()
test_results["Stage_Type"] = np.where(test_results["Stage"] == "Group stage", "Group Stage", "Knockout Rounds")

# Plot 1: Actual vs Predicted Scatter Plot
sns.scatterplot(data=test_results, x="Actual", y="Predicted", hue="Stage_Type", palette="Set1", s=140, alpha=0.8, ax=axes[0])
max_val = max(max(y_test), max(y_pred))
min_val = min(min(y_test), min(y_pred))
axes[0].plot([min_val, max_val], [min_val, max_val], color="crimson", linestyle="--", lw=2)
axes[0].set_title("Actual vs. Predicted Margins (Stage-Aware Pipeline)", fontsize=12)
axes[0].set_xlabel("Actual Goal Difference")
axes[0].set_ylabel("Predicted Goal Difference")
axes[0].legend(title="Tournament Format")

# Plot 2: K-Fold R2 Stability Trend Line
fold_indices = [f"Fold {i+1}" for i in range(len(cv_r2_scores))]
sns.lineplot(x=fold_indices, y=cv_r2_scores, marker="o", color="teal", linewidth=2.5, markersize=8, ax=axes[1])
axes[1].axhline(y=cv_r2_scores.mean(), color="orange", linestyle="-.", label=f"Mean R2 ({cv_r2_scores.mean():.2f})")
axes[1].set_title("R2 Stability Performance Across Folds", fontsize=12)
axes[1].set_ylabel("R-squared Score")
axes[1].set_ylim(-0.2, 1.0)
axes[1].legend()

plt.tight_layout()
plt.show()
