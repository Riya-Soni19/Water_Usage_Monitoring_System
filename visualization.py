"""Matplotlib visualizations for water-use analysis."""

import matplotlib.pyplot as plt

from data_manager import read_data

def activity_usage_graph(show=True):
    """Create a bar chart of total water usage by activity."""
    df = read_data()
    if df.empty:
        print("No data available for graph.")
        return None

    activity_data = df.groupby("Activity")["Litres"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    activity_data.plot(kind="bar", ax=ax)
    ax.set_title("Water Usage by Activity")
    ax.set_xlabel("Activity")
    ax.set_ylabel("Water Usage (Litres)")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()

    if show:
        plt.show()
    return fig


def daily_usage_graph(show=True):
    """Create a line chart of daily water consumption."""
    df = read_data()

    if df.empty:
        print("No data available for graph.")
        return None

    daily_data = df.groupby("Date")["Litres"].sum().sort_index()

    fig, ax = plt.subplots(figsize=(9, 5))

    x = range(len(daily_data))

    ax.plot(
        x,
        daily_data.values,
        marker="o"
    )

    ax.set_title("Daily Water Consumption")
    ax.set_xlabel("Date")
    ax.set_ylabel("Water Usage (Litres)")

    # Show every date on the X-axis
    ax.set_xticks(list(x))
    ax.set_xticklabels(
        daily_data.index,
        rotation=45,
        ha="right"
    )

    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    if show:
        plt.show()

    return fig