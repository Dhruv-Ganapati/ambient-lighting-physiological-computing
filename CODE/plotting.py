# =============================================================================
# Physiological Computing Project
# Visualization
#
# Project:
# Effect of Ambient Lighting on Cognitive Performance
# and Autonomic Activity
# =============================================================================

# %% import
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = "browser"

# %% [1] Loading dataset
master_df = pd.read_csv("master_dataset.csv")

print("="*60)
print("MASTER DATASET LOADED")
print("="*60)

print(master_df.shape)



# %% [2] Figure 
FIG_HEIGHT = 500
FIG_WIDTH = 700

TEMPLATE = "plotly_white"

FONT_SIZE = 16


# %% [3] Heart Rate BoxPlot
fig = go.Figure()

fig.add_trace(

    go.Box(

        y=master_df["HR_Bright"],

        name="Bright",

        boxpoints="all",

        jitter=0.30,

        pointpos=0,

        boxmean=True
    )

)

fig.add_trace(

    go.Box(

        y=master_df["HR_Dim"],

        name="Dim",

        boxpoints="all",

        jitter=0.30,

        pointpos=0,

        boxmean=True
    )

)

fig.update_layout(

    title="Heart Rate Under Bright and Dim Lighting",

    yaxis_title="Heart Rate (BPM)",

    template=TEMPLATE,

    width=FIG_WIDTH,

    height=FIG_HEIGHT,

    font=dict(size=FONT_SIZE),

    xaxis=dict(
        showline=True,
        linewidth=2,
        linecolor="black"
    ),

    yaxis=dict(
        title="Heart Rate (BPM)",
        showline=True,
        linewidth=2,
        linecolor="black"
    )

)
fig.show()

fig.write_image(
    "Figure1_HeartRate_Boxplot.png",
    scale=3
)



# %% [4] RMSSD Boxplot
fig = go.Figure()

fig.add_trace(

    go.Box(

        y=master_df["RMSSD_Bright"],

        name="Bright",

        boxpoints="all",

        jitter=0.30,

        pointpos=0,

    )

)

fig.add_trace(

    go.Box(

        y=master_df["RMSSD_Dim"],

        name="Dim",

        boxpoints="all",

        jitter=0.30,

        pointpos=0,

    )

)

fig.update_layout(

    title="RMSSD Under Bright and Dim Lighting",

    yaxis_title="RMSSD (ms)",

    template=TEMPLATE,

    width=FIG_WIDTH,

    height=FIG_HEIGHT,

    font=dict(size=FONT_SIZE)

)

fig.show()



# %% [5] Accuracy Plot
fig = go.Figure()

fig.add_trace(

    go.Box(

        y=master_df["Accuracy_Bright"],

        name="Bright",

        boxpoints="all",

        jitter=0.30,

        pointpos=0,

    )

)

fig.add_trace(

    go.Box(

        y=master_df["Accuracy_Dim"],

        name="Dim",

        boxpoints="all",

        jitter=0.30,

        pointpos=0,

    )

)

fig.update_layout(

    title="Task Accuracy Under Bright and Dim Lighting",

    yaxis_title="Accuracy (%)",

    template=TEMPLATE,

    width=FIG_WIDTH,

    height=FIG_HEIGHT,

    font=dict(size=FONT_SIZE)

)

fig.show()


# %% ==========================================================
# [6] Heart Rate - Paired Participant Plot
# ==========================================================

fig = go.Figure()

for _, row in master_df.iterrows():

    fig.add_trace(

        go.Scatter(

            x=["Bright", "Dim"],

            y=[row["HR_Bright"], row["HR_Dim"]],

            mode="lines+markers",

            line=dict(width=2),

            marker=dict(size=8),

            showlegend=False,

            hovertemplate=(
                f"Participant: {row['Participant']}<br>"
                "Condition: %{x}<br>"
                "Heart Rate: %{y:.2f} BPM"
                "<extra></extra>"
            )

        )

    )

fig.update_layout(

    title="Individual Changes in Heart Rate",

    xaxis_title="Lighting Condition",

    yaxis_title="Heart Rate (BPM)",

    template=TEMPLATE,

    width=FIG_WIDTH,

    height=FIG_HEIGHT,

    font=dict(size=FONT_SIZE)

)

fig.show()

# %% ==========================================================
# [7] RMSSD - Paired Participant Plot
# ==========================================================

fig = go.Figure()

for _, row in master_df.iterrows():

    fig.add_trace(

        go.Scatter(

            x=["Bright", "Dim"],

            y=[row["RMSSD_Bright"], row["RMSSD_Dim"]],

            mode="lines+markers",

            line=dict(width=2),

            marker=dict(size=8),

            showlegend=False,

            hovertemplate=(
                f"Participant: {row['Participant']}<br>"
                "Condition: %{x}<br>"
                "RMSSD: %{y:.2f} ms"
                "<extra></extra>"
            )

        )

    )

fig.update_layout(

    title="Individual Changes in RMSSD",

    xaxis_title="Lighting Condition",

    yaxis_title="RMSSD (ms)",

    template=TEMPLATE,

    width=FIG_WIDTH,

    height=FIG_HEIGHT,

    font=dict(size=FONT_SIZE)

)

fig.show()


# %% ==========================================================
# [8] Accuracy - Paired Participant Plot
# ==========================================================

fig = go.Figure()

for _, row in master_df.iterrows():

    fig.add_trace(

        go.Scatter(

            x=["Bright", "Dim"],

            y=[row["Accuracy_Bright"], row["Accuracy_Dim"]],

            mode="lines+markers",

            line=dict(width=2),

            marker=dict(size=8),

            showlegend=False,

            hovertemplate=(
                f"Participant: {row['Participant']}<br>"
                "Condition: %{x}<br>"
                "Accuracy: %{y:.2f}%"
                "<extra></extra>"
            )

        )

    )

fig.update_layout(

    title="Individual Changes in Task Accuracy",

    xaxis_title="Lighting Condition",

    yaxis_title="Accuracy (%)",

    template=TEMPLATE,

    width=FIG_WIDTH,

    height=FIG_HEIGHT,

    font=dict(size=FONT_SIZE)

)

fig.show()



