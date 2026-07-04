# =============================================================================
# Physiological Computing Project
# Statistical Analysis

# Effect of Ambient Lighting on Cognitive Performance
# and Autonomic Activity

# Load master_dataset.csv.
# Perform assumption checks (Shapiro–Wilk).
# Run paired t-tests.
# Compute effect sizes (Cohen's d for paired samples).
# Calculate 95% confidence intervals.
# Save a statistical summary (CSV or printed table).
# =============================================================================

# %%
print()
print("=" * 60)
print("INFERENTIAL STATISTICS (NEW)")
print("=" * 60)

# %% ==========================================================
# [1] Imports
# ==========================================================

import numpy as np
import pandas as pd

from scipy.stats import (
    shapiro,
    ttest_rel,
    wilcoxon
)

from scipy import stats


# %% ==========================================================
# [2] Load Dataset
# ==========================================================

master_df = pd.read_csv("master_dataset.csv")

print("="*60)
print("MASTER DATASET")
print("="*60)

print(master_df.shape)
print()
print(master_df.head())


# %% ==========================================================
# [3] Create Difference Scores
# ==========================================================

master_df["HR_Diff"] = (
    master_df["HR_Bright"]
    -
    master_df["HR_Dim"]
)

master_df["RMSSD_Diff"] = (
    master_df["RMSSD_Bright"]
    -
    master_df["RMSSD_Dim"]
)

master_df["Accuracy_Diff"] = (
    master_df["Accuracy_Bright"]
    -
    master_df["Accuracy_Dim"]
)

print()
print("="*60)
print("Difference Scores Created")
print("="*60)


# %% [4] SHAPIRO-WILK TEST
print("="*60)
print("SHAPIRO-WILK NORMALITY TEST")
print("="*60)

variables = [
    "HR_Diff",
    "RMSSD_Diff",
    "Accuracy_Diff"
]

for var in variables:

    stat, p = shapiro(master_df[var])

    print(f"\n{var}")
    print(f"W = {stat:.4f}")
    print(f"p = {p:.4f}")

    if p > 0.05:
        print("Result : Normally Distributed ✓")
    else:
        print("Result : Not Normally Distributed ✗")

# %% [4.1] Wilcoxon Signed-Rank Test (Accuracy)

wilcox_stat, wilcox_p = wilcoxon(
    master_df["Accuracy_Bright"],
    master_df["Accuracy_Dim"]
)

print()
print("="*60)
print("WILCOXON SIGNED-RANK TEST")
print("="*60)

print(f"Statistic : {wilcox_stat:.3f}")
print(f"p-value   : {wilcox_p:.4f}")

# %% [5] Paired t-test

print()
print("="*60)
print("PAIRED T-TESTS")
print("="*60)

# Heart Rate
hr_test = ttest_rel(
    master_df["HR_Bright"],
    master_df["HR_Dim"]
)

# RMSSD
rmssd_test = ttest_rel(
    master_df["RMSSD_Bright"],
    master_df["RMSSD_Dim"]
)

# Accuracy
acc_test = ttest_rel(
    master_df["Accuracy_Bright"],
    master_df["Accuracy_Dim"]
)

print("\nHeart Rate")
print(hr_test)

print("\nRMSSD")
print(rmssd_test)

print("\nAccuracy")
print(acc_test)


# %% [6] Effect Size- Cohen's D

print()
print("="*60)
print("COHEN'S d")
print("="*60)

def cohens_d_paired(diff):

    return np.mean(diff) / np.std(diff, ddof=1)


hr_d = cohens_d_paired(master_df["HR_Diff"])

rmssd_d = cohens_d_paired(master_df["RMSSD_Diff"])

acc_d = cohens_d_paired(master_df["Accuracy_Diff"])


print(f"HR       : {hr_d:.3f}")
print(f"RMSSD    : {rmssd_d:.3f}")
print(f"Accuracy : {acc_d:.3f}")


# %% [7] Confidence Interval

print()
print("="*60)
print("95% CONFIDENCE INTERVALS")
print("="*60)

def confidence_interval(diff):

    n = len(diff)

    mean = np.mean(diff)

    sd = np.std(diff, ddof=1)

    se = sd / np.sqrt(n)

    t_value = stats.t.ppf(
        0.975,
        df=n-1
    )

    lower = mean - t_value * se
    upper = mean + t_value * se

    return mean, lower, upper


metrics = {

    "HR": master_df["HR_Diff"],

    "RMSSD": master_df["RMSSD_Diff"],

    "Accuracy": master_df["Accuracy_Diff"]

}


for name, values in metrics.items():

    mean, low, high = confidence_interval(values)

    print(f"\n{name}")

    print(f"Mean Difference : {mean:.3f}")

    print(f"95% CI : [{low:.3f}, {high:.3f}]")



# %% [8] Statistical Summary Table

# Confidence Intervals
hr_mean_diff, hr_ci_low, hr_ci_high = confidence_interval(master_df["HR_Diff"])

rmssd_mean_diff, rmssd_ci_low, rmssd_ci_high = confidence_interval(master_df["RMSSD_Diff"])

acc_mean_diff, acc_ci_low, acc_ci_high = confidence_interval(master_df["Accuracy_Diff"])


summary = pd.DataFrame({

    "Metric":[
        "Heart Rate",
        "RMSSD",
        "Accuracy"
    ],

    "Mean Bright":[

        master_df["HR_Bright"].mean(),

        master_df["RMSSD_Bright"].mean(),

        master_df["Accuracy_Bright"].mean()

    ],

    "Mean Dim":[

        master_df["HR_Dim"].mean(),

        master_df["RMSSD_Dim"].mean(),

        master_df["Accuracy_Dim"].mean()

    ],

    "Mean Difference":[

        hr_mean_diff,

        rmssd_mean_diff,

        acc_mean_diff

    ],

    "95% CI Lower":[

        hr_ci_low,

        rmssd_ci_low,

        acc_ci_low

    ],

    "95% CI Upper":[

        hr_ci_high,

        rmssd_ci_high,

        acc_ci_high

    ],

    "Statistical Test":[

        "Paired t-test",

        "Paired t-test",

        "Wilcoxon Signed-Rank"

    ],

    "Statistic":[

        hr_test.statistic,

        rmssd_test.statistic,

        wilcox_stat

    ],

    "p-value":[

        hr_test.pvalue,

        rmssd_test.pvalue,

        wilcox_p

    ],

    "Effect Size (Cohen's d)":[

        hr_d,

        rmssd_d,

        acc_d

    ]

})

print()
print("="*60)
print("FINAL STATISTICAL SUMMARY")
print("="*60)

print(summary.round(4))


# %% [8.1] round off
summary = summary.round({
    "Mean Bright":3,
    "Mean Dim":3,
    "Mean Difference":3,
    "95% CI Lower":3,
    "95% CI Upper":3,
    "Statistic":4,
    "p-value":4,
    "Effect Size (Cohen's d)":3
})

# %% [9] Save Results

summary.to_csv(
    "master_statistics.csv",
    index=False
)

print()
print("="*60)
print("STATISTICAL RESULTS SAVED")
print("="*60)
print("Saved as: master_statistics.csv")
# %%
