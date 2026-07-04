# ==========================================================
# Physiological Computing Project
# Ambient Lighting vs HRV & Arithmetic Performance
# ============================================================
import os

print(os.getcwd())


# %% [1] Imports

import numpy as np
import pandas as pd
import neurokit2 as nk


# %% [2] Participant Information

participant_id = "P0033"

# Choose ONE:

#condition_order = "Bright-Dim"

condition_order = "Dim-Bright"


# %% [3] Load ECG

df = pd.read_csv("AshleyP0016/ECG_P0016_20260625_134424.csv")

print(df.head())
t = df["polar_timestamp_s"].values
ecg = df["ecg_voltage_uv"].values

fs = 1.0 / np.median(np.diff(t))

print("="*50)
print("[3] ECG FILE INFORMATION")
print("="*50)
print(f"Participant : {participant_id}")
print(f"Condition   : {condition_order}")
print(f"Sample Rate : {fs:.2f} Hz")
print(f"Duration    : {(t[-1]-t[0])/60:.2f} min")
print()


# %% [4] Normalize Time

t = t - t[0]

print("Recording starts at 0 sec")
print("Recording ends at", round(t[-1],2), "sec")


# %% [5] Segment Experiment

baseline = df[(t >= 0) & (t < 120)]

first_task = df[(t >= 120) & (t < 420)]

recovery = df[(t >= 420) & (t < 540)]

second_task = df[(t >= 540) & (t < 840)]

print()
print("="*50)
print("SEGMENTS")
print("="*50)
print("Baseline :", len(baseline))
print("Task 1   :", len(first_task))
print("Recovery :", len(recovery))
print("Task 2   :", len(second_task))


# %% [6] Assign Bright / Dim Based on Order
if condition_order == "Bright-Dim":

    bright = first_task
    dim = second_task

elif condition_order == "Dim-Bright":

    dim = first_task
    bright = second_task

else:

    raise ValueError(
        "condition_order must be either "
        "'Bright-Dim' or 'Dim-Bright'"
    )

print()
print("="*50)
print("CONDITION ASSIGNMENT")
print("="*50)
print("Bright samples :", len(bright))
print("Dim samples    :", len(dim))


# %% [7] HR + RMSSD Function
print(50*"=")
print("COMPUTING HR + RMSSD")
print(50*"=")

def compute_hr_rmssd(segment):

    signal = segment["ecg_voltage_uv"].values

    _, peaks_info = nk.ecg_peaks(
        signal,
        sampling_rate=int(round(fs)),
        method="pantompkins"
    )

    r_peaks = peaks_info["ECG_R_Peaks"]

    if len(r_peaks) < 5:
        return np.nan, np.nan

    rr_ms = np.diff(r_peaks) / fs * 1000

    mean_hr = 60000 / np.mean(rr_ms)

    rmssd = np.sqrt(
        np.mean(
            np.diff(rr_ms) ** 2
        )
    )

    return mean_hr, rmssd


# %% [8] Compute Metrics

baseline_hr, baseline_rmssd = compute_hr_rmssd(
    baseline
)

bright_hr, bright_rmssd = compute_hr_rmssd(
    bright
)

recovery_hr, recovery_rmssd = compute_hr_rmssd(
    recovery
)

dim_hr, dim_rmssd = compute_hr_rmssd(
    dim
)


# %% [9] Arithmetic Performance


attempts_bright = 29
correct_bright = 29

attempts_dim = 35
correct_dim = 33

accuracy_bright = (
    correct_bright /
    attempts_bright
) * 100

accuracy_dim = (
    correct_dim /
    attempts_dim
) * 100

accuracy_prop_bright = (
    correct_bright /
    attempts_bright
)

accuracy_prop_dim = (
    correct_dim /
    attempts_dim
)

print()
print("="*50)
print("[9] TASK PERFORMANCE")
print("="*50)

print("Bright Accuracy:",
      round(accuracy_bright,2))

print("Dim Accuracy:",
      round(accuracy_dim,2))


# %% [10] Print Physiological Results

print()
print("="*50)
print("[10] PHYSIOLOGICAL RESULTS")
print("="*50)

print()
print("BASELINE")
print("HR    :", round(baseline_hr,2))
print("RMSSD :", round(baseline_rmssd,2))

print()
print("BRIGHT")
print("HR    :", round(bright_hr,2))
print("RMSSD :", round(bright_rmssd,2))

print()
print("RECOVERY")
print("HR    :", round(recovery_hr,2))
print("RMSSD :", round(recovery_rmssd,2))

print()
print("DIM")
print("HR    :", round(dim_hr,2))
print("RMSSD :", round(dim_rmssd,2))


# %% [11] Save Results

results = pd.DataFrame({

    "Participant":[participant_id],

    "Order":[condition_order],

    "HR_Baseline":[baseline_hr],
    "RMSSD_Baseline":[baseline_rmssd],

    "HR_Bright":[bright_hr],
    "RMSSD_Bright":[bright_rmssd],

    "HR_Dim":[dim_hr],
    "RMSSD_Dim":[dim_rmssd],

    "HR_Recovery":[recovery_hr],
    "RMSSD_Recovery":[recovery_rmssd],

    "Attempts_Bright":[attempts_bright],
    "Correct_Bright":[correct_bright],
    "Accuracy_Bright":[accuracy_bright],
    "AccuracyProp_Bright":[accuracy_prop_bright],

    "Attempts_Dim":[attempts_dim],
    "Correct_Dim":[correct_dim],
    "Accuracy_Dim":[accuracy_dim],
    "AccuracyProp_Dim":[accuracy_prop_dim]
})

results.to_csv(
    f"{participant_id}_results.csv",
    index=False
)

print()
print("="*50)
print("[11] RESULTS SAVED")
print("="*50)

print(results)
# %%
