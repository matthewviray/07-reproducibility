import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import altair as alt
    return alt, mo, pd


@app.cell
def _(pd):
    df = pd.read_csv("data/features/events.csv")
    return (df,)


@app.cell
def _(alt, df, mo):
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            alt.X(
                "duration_minutes:Q",
                bin=alt.Bin(maxbins=40),
                title="Duration (minutes)",
            ),
            alt.Y("count()", title="Number of Events"),
            tooltip=["count()"],
        )
        .properties(
            title="Distribution of Event Durations",
            width=600,
            height=400,
        )
    )
    mo.ui.altair_chart(chart)
    return (chart,)