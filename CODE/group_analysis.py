# %% ==========================================================
# STEP 3 — GROUP DATA PREPARATION
# Ambient Lighting Project
# ==========================================================

# %% Imports

import pandas as pd
import glob


# %% Load All Participant Result Files

print("=" * 60)
print("LOADING PARTICIPANT RESULT FILES")
print("=" * 60)

files = sorted(glob.glob("*_results.csv"))

print(f"Files Found: {len(files)}")

for file in files:
    print(file)


# %% Combine All Files

master_df = pd.concat(
    [pd.read_csv(file) for file in files],
    ignore_index=True
)

master_df = master_df.sort_values(
    by="Participant"
).reset_index(drop=True)

print()
print("=" * 60)
print("MASTER DATASET CREATED")
print("=" * 60)

print("Rows   :", len(master_df))
print("Columns:", len(master_df.columns))


# %% Dataset Structure

print()
print("=" * 60)
print("DATASET COLUMNS")
print("=" * 60)

for col in master_df.columns:
    print(col)


# %% Missing Values Check

print()
print("=" * 60)
print("MISSING VALUES CHECK")
print("=" * 60)

print(master_df.isnull().sum())


# %% Participant Check

print()
print("=" * 60)
print("PARTICIPANT CHECK")
print("=" * 60)

print(master_df["Participant"].value_counts())


# %% Counterbalancing Check

print()
print("=" * 60)
print("CONDITION ORDER CHECK")
print("=" * 60)

print(master_df["Order"].value_counts())


# %% Descriptive Statistics

print()
print("=" * 60)
print("DESCRIPTIVE STATISTICS")
print("=" * 60)

metrics = [

    "HR_Bright",
    "HR_Dim",

    "RMSSD_Bright",
    "RMSSD_Dim",

    "Accuracy_Bright",
    "Accuracy_Dim"

]

print(master_df[metrics].describe())


# %% Difference Scores

master_df["HR_Diff"] = (
    master_df["HR_Bright"]
    - master_df["HR_Dim"]
)

master_df["RMSSD_Diff"] = (
    master_df["RMSSD_Bright"]
    - master_df["RMSSD_Dim"]
)

master_df["Accuracy_Diff"] = (
    master_df["Accuracy_Bright"]
    - master_df["Accuracy_Dim"]
)

print()
print("=" * 60)
print("DIFFERENCE SCORES")
print("=" * 60)

print(
    master_df[
        [
            "Participant",
            "HR_Diff",
            "RMSSD_Diff",
            "Accuracy_Diff"
        ]
    ]
)


# %% Duplicate Physiological Profiles

print()
print("=" * 60)
print("DUPLICATE PROFILE CHECK")
print("=" * 60)

duplicate_rows = master_df[
    master_df[
        [
            "HR_Bright",
            "HR_Dim",
            "RMSSD_Bright",
            "RMSSD_Dim"
        ]
    ].duplicated(keep=False)
]

if len(duplicate_rows) == 0:
    print("No duplicate physiological profiles found.")
else:
    print(duplicate_rows[
        [
            "Participant",
            "HR_Bright",
            "HR_Dim",
            "RMSSD_Bright",
            "RMSSD_Dim"
        ]
    ])


# %% Range Check

print()
print("=" * 60)
print("PHYSIOLOGICAL RANGE CHECK")
print("=" * 60)

print()

print("Minimum HR")
print(
    master_df[
        ["HR_Bright", "HR_Dim"]
    ].min()
)

print()

print("Maximum HR")
print(
    master_df[
        ["HR_Bright", "HR_Dim"]
    ].max()
)

print()

print("Minimum RMSSD")
print(
    master_df[
        ["RMSSD_Bright", "RMSSD_Dim"]
    ].min()
)

print()

print("Maximum RMSSD")
print(
    master_df[
        ["RMSSD_Bright", "RMSSD_Dim"]
    ].max()
)


# %% Save Clean Master Dataset

master_df.to_csv(
    "master_dataset.csv",
    index=False
)

print()
print("=" * 60)
print("MASTER DATASET SAVED")
print("=" * 60)
print("File: master_dataset.csv")


# %%
print()
print("=" * 60)
print("STATISTICAL ANALYSIS")
print("1. Assumption check (Shapiro–Wilk)")
print("2. Paired t-tests")
print("3. Effect size (Cohen's d)")
print("4. Confidence intervals- 95% ")

print("5. Graphs")
print("Interpret the results")
print("=" * 60) 




