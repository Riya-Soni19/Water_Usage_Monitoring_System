"""Data storage and validation functions for the Water Usage project."""

from datetime import datetime
from pathlib import Path

import re
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
FILE_NAME = BASE_DIR / "water_usage.csv"
REQUIRED_COLUMNS = ["Date", "Activity", "Litres", "Description"]
DATE_FORMAT = "%Y-%m-%d"


def create_file():
    """Create the CSV file with the required columns if it does not exist."""
    if not FILE_NAME.exists():
        pd.DataFrame(columns=REQUIRED_COLUMNS).to_csv(FILE_NAME, index=False)

def read_data():
    """Read all water-use records from the CSV file safely."""
    create_file()

    try:
        df = pd.read_csv(FILE_NAME)

        missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
        if missing_columns:
            raise ValueError(
                "Invalid CSV file format. Missing columns: " + ", ".join(missing_columns)
            )

        # Keep only the expected columns and clean numeric values.
        df = df[REQUIRED_COLUMNS].copy()
        df["Litres"] = pd.to_numeric(df["Litres"], errors="coerce")
        df = df.dropna(subset=["Litres"])
        df["Date"] = df["Date"].astype(str)
        df["Activity"] = df["Activity"].astype(str)
        df["Description"] = df["Description"].fillna("").astype(str)

        return df

    except FileNotFoundError:
        create_file()
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    except (pd.errors.EmptyDataError, pd.errors.ParserError, ValueError) as error:
        print("Error reading file:", error)
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    except OSError as error:
        print("File access error:", error)
        return pd.DataFrame(columns=REQUIRED_COLUMNS)


def validate_date(date):
    """Validate a date strictly in YYYY-MM-DD format."""
    date = str(date).strip()

    # Check exact format: YYYY-MM-DD
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        return False

    try:
        # Check whether it is a real calendar date
        datetime.strptime(date, DATE_FORMAT)
        return True
    except ValueError:
        return False


def add_record(date, activity, litres, description):
    """Validate and add a new water-use record to the CSV file."""
    try:
        date = str(date).strip()
        activity = str(activity).strip()
        description = str(description).strip()

        if not date:
            return False, "Date cannot be empty."

        if not validate_date(date):
            return False, "Date must be a valid date in YYYY-MM-DD format."

        if not activity:
            return False, "Activity cannot be empty."

        if str(litres).strip() == "":
            return False, "Water usage cannot be empty."

        litres = float(litres)

        if litres <= 0:
            return False, "Water usage must be greater than 0."

        if litres > 100000:
            return False, "Water usage is too large. Please enter a realistic value."

        df = read_data()

        new_record = pd.DataFrame(
            {
                "Date": [date],
                "Activity": [activity],
                "Litres": [litres],
                "Description": [description],
            }
        )

        df = pd.concat([df, new_record], ignore_index=True)
        df.to_csv(FILE_NAME, index=False)

        return True, "Record added successfully."

    except ValueError:
        return False, "Litres must be a valid number."
    except OSError as error:
        return False, f"File error: {error}"
    except Exception as error:
        return False, f"Error: {error}"


def search_records(activity="", date=""):
    """Search records by activity and/or exact date."""
    try:
        df = read_data()

        activity = str(activity).strip()
        date = str(date).strip()

        if activity:
            df = df[df["Activity"].str.contains(activity, case=False, na=False, regex=False)]

        if date:
            if not validate_date(date):
                return pd.DataFrame(columns=REQUIRED_COLUMNS)
            df = df[df["Date"] == date]

        return df

    except Exception as error:
        print("Search error:", error)
        return pd.DataFrame(columns=REQUIRED_COLUMNS)


def get_all_activities():
    """Return a sorted list of all unique activities."""
    df = read_data()

    if df.empty:
        return []

    return sorted(df["Activity"].dropna().unique().tolist())