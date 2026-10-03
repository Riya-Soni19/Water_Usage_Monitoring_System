"""Tests for Matplotlib visualization functions without opening GUI windows."""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from visualization import activity_usage_graph, daily_usage_graph


def run_tests():
    activity_fig = activity_usage_graph(show=False)
    daily_fig = daily_usage_graph(show=False)

    assert activity_fig is not None
    assert daily_fig is not None
    assert len(activity_fig.axes) == 1
    assert len(daily_fig.axes) == 1

    plt.close(activity_fig)
    plt.close(daily_fig)

    print("All Matplotlib visualization tests passed.")


if __name__ == "__main__":
    run_tests()