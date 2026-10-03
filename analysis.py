"""Water-use calculations and analysis functions."""

import numpy as np
import pandas as pd

from data_manager import read_data

# Demonstration thresholds used by this project.
HIGH_USAGE_LIMIT = 100       # litres for one activity record
HIGH_DAILY_USAGE_LIMIT = 320 # litres for one day


def calculate_total():
    """Calculate total water consumption."""
    df = read_data()
    return float(df["Litres"].sum()) if not df.empty else 0.0


def calculate_average():
    """Calculate average water consumption per recorded observation."""
    df = read_data()
    return float(df["Litres"].mean()) if not df.empty else 0.0


def calculate_maximum():
    """Find the highest water consumption in one record."""
    df = read_data()
    return float(df["Litres"].max()) if not df.empty else 0.0


def calculate_minimum():
    """Find the lowest water consumption in one record."""
    df = read_data()
    return float(df["Litres"].min()) if not df.empty else 0.0


def get_high_consumption():
    """Return individual records at or above the high-use limit."""
    df = read_data()
    if df.empty:
        return df
    return df[df["Litres"] >= HIGH_USAGE_LIMIT].copy()


def activity_comparison():
    """Calculate total water usage for each activity."""
    df = read_data()
    if df.empty:
        return pd.Series(dtype=float)
    return df.groupby("Activity")["Litres"].sum().sort_values(ascending=False)


def daily_consumption():
    """Calculate total water usage for each day."""
    df = read_data()
    if df.empty:
        return pd.Series(dtype=float)
    return df.groupby("Date")["Litres"].sum().sort_index()


def high_consumption_days():
    """Return days whose total consumption reaches the daily high-use limit."""
    daily = daily_consumption()
    if daily.empty:
        return daily
    return daily[daily >= HIGH_DAILY_USAGE_LIMIT]


def highest_consumption_day():
    """Return the date and total usage for the highest-consumption day."""
    daily = daily_consumption()
    if daily.empty:
        return None, 0.0

    date = daily.idxmax()
    litres = float(daily.max())
    return date, litres


def calculate_statistics():
    """Calculate basic statistics using NumPy."""
    df = read_data()

    if df.empty:
        return {"total": 0.0, "average": 0.0, "maximum": 0.0, "minimum": 0.0}

    values = df["Litres"].to_numpy()

    return {
        "total": float(np.sum(values)),
        "average": float(np.mean(values)),
        "maximum": float(np.max(values)),
        "minimum": float(np.min(values)),
    }