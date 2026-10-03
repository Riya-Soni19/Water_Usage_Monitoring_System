"""Tests for data storage, searching and input validation."""

from data_manager import add_record, read_data, search_records, validate_date


def run_tests():
    data = read_data()
    assert {"Date", "Activity", "Litres", "Description"}.issubset(data.columns)
    assert not data.empty

    assert validate_date("2026-09-27") is True
    assert validate_date("2026-02-30") is False
    assert validate_date("27-09-2026") is False

    success, _ = add_record("", "Bathing", "80", "Invalid test")
    assert success is False

    success, _ = add_record("2026-09-27", "Bathing", "-10", "Invalid test")
    assert success is False

    success, _ = add_record("2026-09-27", "Bathing", "abc", "Invalid test")
    assert success is False

    result = search_records("Bathing")
    assert not result.empty
    assert result["Activity"].str.contains("Bathing", case=False).all()

    date_result = search_records(date="2026-09-01")
    assert not date_result.empty
    assert date_result["Date"].eq("2026-09-01").all()

    print("All data and validation tests passed.")


if __name__ == "__main__":
    run_tests()