"""Tests for water-use calculations and analysis."""

from analysis import (
    calculate_average,
    calculate_maximum,
    calculate_minimum,
    calculate_statistics,
    calculate_total,
    daily_consumption,
    get_high_consumption,
    high_consumption_days,
    highest_consumption_day,
)


def run_tests():
    total = calculate_total()
    average = calculate_average()
    maximum = calculate_maximum()
    minimum = calculate_minimum()

    assert total > 0
    assert average > 0
    assert maximum >= minimum > 0

    high_records = get_high_consumption()
    assert not high_records.empty
    assert (high_records["Litres"] >= 100).all()

    daily = daily_consumption()
    assert not daily.empty
    assert daily.max() >= daily.min()

    high_days = high_consumption_days()
    assert (high_days >= 320).all()

    highest_date, highest_litres = highest_consumption_day()
    assert highest_date is not None
    assert highest_litres == daily.max()

    stats = calculate_statistics()
    assert stats["total"] == total
    assert stats["average"] == average
    assert stats["maximum"] == maximum
    assert stats["minimum"] == minimum

    print("All analysis and NumPy tests passed.")


if __name__ == "__main__":
    run_tests()