# Water Usage Monitoring and Analysis System

## 1. Project Title

**Water Usage Monitoring and Analysis System**

## 2. Problem Statement

A household or institution records daily water usage but wants to identify high-consumption periods and understand how water usage changes across different activities or days.

## 3. Domain

**Environment**

## 4. Objective

Develop a Python-based application that maintains water-use records and helps users analyze consumption patterns.

The system allows users to:

- Record water usage.
- View saved records.
- Search/filter water-use records.
- Refresh the records table with the latest data from the CSV file.
- Calculate total and average water consumption.
- Find minimum and maximum usage.
- Identify high-consumption records.
- Identify high-consumption days and the highest-consumption day.
- Compare water usage between activities and days.
- Generate two meaningful visual reports.

## 5. Technologies Used

- **Python** – Main programming language
- **Tkinter** – Graphical User Interface
- **Pandas** – Data handling and analysis
- **NumPy** – Numerical calculations and statistics
- **Matplotlib** – Data visualization
- **CSV** – Persistent data storage

## 6. Project Structure

```text
Water_Usage_Project/
│
├── main.py
├── data_manager.py
├── analysis.py
├── visualization.py
│
├── water_usage.csv
├── requirements.txt
├── README.md
│
├── test_data.py
├── test_analysis.py
└── test_visualization.py
```

### `main.py`

Contains the Tkinter GUI and connects the project modules. It provides:

- Water-use input form
- Search/filter controls
- Show All and Refresh controls
- Records table with scrollbar
- Summary statistics cards
- Analysis buttons
- Graph buttons
- Input and error messages

### `data_manager.py`

Handles data storage and validation.

Main functions include:

- Creating the CSV file
- Reading records
- Validating dates and water usage
- Adding records
- Searching/filtering records
- Getting activities

### `analysis.py`

Performs calculations and data analysis.

It calculates:

- Total water usage
- Average water usage
- Maximum usage
- Minimum usage
- High-consumption records
- Activity-wise consumption
- Daily consumption
- High-consumption days
- Highest-consumption day
- NumPy statistics

### `visualization.py`

Creates graphs using Matplotlib:

1. Activity-wise water usage bar chart
2. Daily water consumption line chart

The graph functions read the current data from the CSV file whenever a graph is generated.

### `water_usage.csv`

Stores water-use records persistently. Each record contains:

- Date
- Activity
- Litres
- Description

### Test files

- `test_data.py` – tests file handling, searching and input validation.
- `test_analysis.py` – tests calculations, high-usage analysis and NumPy statistics.
- `test_visualization.py` – tests creation of both Matplotlib graphs without opening graph windows.

## 7. Data Format

The CSV file uses:

```text
Date,Activity,Litres,Description
```

Example:

```text
2026-09-01,Bathing,80.0,Morning bath
2026-09-01,Kitchen,45.0,Cooking and cleaning
2026-09-01,Laundry,120.0,Clothes washing
2026-09-01,Gardening,60.0,Plant watering
```

## 8. Main Features

### 8.1 Add Water Usage Record

Users can enter:

- Date in `YYYY-MM-DD` format
- Activity
- Water usage in litres
- Description

The record is validated and saved to the CSV file.

### 8.2 View Records

All stored water-use records are displayed in the main table.

### 8.3 Search / Filter Records

Users can search by activity and/or exact date.

Example:

```text
Activity: Bathing
Date: 2026-09-05
```

### 8.4 Refresh Records

The **REFRESH** button reloads the latest data from the CSV file and updates the records table and dashboard without restarting the application.

### 8.5 Total and Average Water Usage

The application calculates total water consumption and average consumption per recorded observation.

### 8.6 Minimum and Maximum Usage

The application displays the lowest and highest individual water-use values.

### 8.7 High Consumption Detection

Two levels are used for this project:

- **High-consumption record:** 100 litres or more for one activity record.
- **High-consumption day:** 320 litres or more in total for one day.

These thresholds are demonstration values selected for the project dataset and can be changed in `analysis.py`.

### 8.8 Activity Comparison

The application groups records by activity and calculates total water usage for each activity.

### 8.9 Daily Comparison

The application groups records by date to show how total water consumption changes from day to day.

### 8.10 Highest Consumption Day

The application identifies the date with the highest total water consumption.

### 8.11 Data Visualization

Two meaningful graphs are provided:

**Activity Usage Bar Chart**

Shows total water consumption for each activity.

**Daily Usage Line Chart**

Shows how total water consumption changes across different days.

## 9. Input Validation

The application validates user input before saving a record.

It checks for:

- Empty date
- Invalid date format
- Invalid calendar dates
- Empty activity
- Empty water usage
- Non-numeric water usage
- Zero or negative water usage
- Unrealistically large water usage values

The search date is also checked for valid `YYYY-MM-DD` format.

## 10. Exception Handling

Python `try-except` blocks are used to handle common errors such as:

- Invalid numerical input
- Missing CSV file
- Empty or malformed CSV data
- Incorrect CSV columns
- File access errors
- Search errors

Error messages are displayed or handled without unnecessarily stopping the application.

## 11. Python Functions and Data Structures

The project uses user-defined Python functions and data structures such as:

- Lists
- Dictionaries
- Pandas DataFrames
- Pandas Series

The project is divided into reusable modules so that data management, analysis and visualization are kept separate.

## 12. Use of NumPy

NumPy is used for numerical statistics:

```python
np.sum(values)
np.mean(values)
np.max(values)
np.min(values)
```

## 13. Use of Pandas

Pandas is used for CSV reading, data processing, grouping and analysis.

Example:

```python
data = pd.read_csv("water_usage.csv")
data.groupby("Activity")["Litres"].sum()
```

## 14. Use of Matplotlib

Matplotlib is used to create two visual reports:

1. **Bar chart** – compares total water usage by activity.
2. **Line chart** – shows daily water consumption over time.

## 15. Testing

The project contains three test files.

### `test_data.py`

Tests:

- Reading stored records
- Date validation
- Invalid input handling
- Activity search
- Date filtering

### `test_analysis.py`

Tests:

- Total usage
- Average usage
- Maximum and minimum usage
- High-consumption records
- Daily consumption
- High-consumption days
- Highest-consumption day
- NumPy statistics

### `test_visualization.py`

Tests:

- Activity bar chart creation
- Daily line chart creation

The visualization tests use a non-interactive Matplotlib backend so that test execution does not require graph windows.

Run all tests separately from the project folder:

```bash
python test_data.py
python test_analysis.py
python test_visualization.py
```

## 16. How to Run the Project

### Step 1: Install Python

Check Python installation:

```bash
python --version
```

### Step 2: Install Required Libraries

From the project folder, run:

```bash
pip install -r requirements.txt
```

Tkinter is normally included with the standard Python installation on Windows.

### Step 3: Open the Project Folder

Open a terminal in:

```text
Water_Usage_Project
```

### Step 4: Run the Application

```bash
python main.py
```

The Water Usage Monitoring and Analysis System GUI will open.

## 17. Example Activities

The application can record activities such as:

- Bathing
- Kitchen
- Laundry
- Gardening
- Cleaning

Example:

```text
Date: 2026-09-01
Activity: Bathing
Water Used: 80 Litres
Description: Morning bath
```

## 18. System Workflow

```text
Start
  ↓
Open Application
  ↓
Enter Water Usage Record
  ↓
Validate Input
  ↓
Save Record to CSV
  ↓
View / Search / Filter Records
  ↓
Refresh Records if CSV data is changed externally
  ↓
Analyze Water Usage
  ↓
Calculate Total and Average
  ↓
Identify High-Consumption Records and Days
  ↓
Compare Activities and Days
  ↓
Generate Graphs
  ↓
End
```

## 19. Advantages

- Simple and easy-to-use GUI
- Persistent CSV storage
- Search and filtering support
- Manual refresh of latest CSV data
- Useful water-consumption statistics
- High-consumption detection
- Daily and activity comparisons
- Two graphical reports
- Uses Python, NumPy and Pandas concepts 

## 20. Limitations

- Designed for a single computer
- Data is stored in a CSV file instead of a database
- Water usage is entered manually
- It does not automatically measure real-time water consumption
- CSV changes made outside the application require the **REFRESH** button to update the displayed records
- High-consumption thresholds are demonstration values

## 21. Future Scope

The project can be extended with:

- Database support
- Monthly and yearly reports
- Automatic water-meter integration
- User login system
- PDF or Excel report export
- More advanced statistical analysis
- Water-saving recommendations
- Cloud-based storage
- Mobile application support

## 22. Conclusion

The **Water Usage Monitoring and Analysis System** provides a simple way to record, analyze and visualize water consumption. It uses Python, Tkinter, Pandas, NumPy, Matplotlib and CSV file handling to provide persistent storage, data analysis and visual reporting.

The project helps users understand water consumption patterns, identify high-consumption activities and days and observe changes in usage over time. It demonstrates practical use of Python functions, data structures, modules, file handling, GUI development, NumPy, Pandas, exception handling, testing and data visualization.