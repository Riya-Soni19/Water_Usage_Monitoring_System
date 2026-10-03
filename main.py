"""Tkinter GUI for the Water Usage Monitoring and Analysis System."""

import tkinter as tk
from tkinter import messagebox, ttk

from analysis import (
    HIGH_DAILY_USAGE_LIMIT,
    HIGH_USAGE_LIMIT,
    activity_comparison,
    calculate_average,
    calculate_maximum,
    calculate_minimum,
    calculate_total,
    daily_consumption,
    get_high_consumption,
    high_consumption_days,
    highest_consumption_day,
)
from data_manager import add_record, read_data, search_records
from visualization import activity_usage_graph, daily_usage_graph


# -----------------------------
# COLORS / THEME
# -----------------------------
BG_COLOR = "#EAF6FF"
HEADER_COLOR = "#145A86"
SECTION_COLOR = "#D8EEF9"
CARD_COLOR = "#FFFFFF"
TEXT_COLOR = "#17324D"
BUTTON_COLOR = "#2E86AB"
BUTTON_TEXT = "#FFFFFF"
SUCCESS_COLOR = "#2E7D32"
WARNING_COLOR = "#B26A00"


root = tk.Tk()
root.title("Water Usage Monitoring and Analysis System")
root.geometry("1100x780")
root.minsize(1000, 700)
root.configure(bg=BG_COLOR)

style = ttk.Style()
try:
    style.theme_use("clam")
except tk.TclError:
    pass

style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
style.configure("TCombobox", padding=4)


def clear_fields():
    """Clear all input and search fields."""
    date_entry.delete(0, tk.END)
    activity_entry.delete(0, tk.END)
    litres_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    search_activity_entry.delete(0, tk.END)
    search_date_entry.delete(0, tk.END)
    date_entry.focus_set()


def refresh_table(data=None):
    """Display the supplied records or all records in the table."""
    for item in table.get_children():
        table.delete(item)

    if data is None:
        data = read_data()

    for _, row in data.iterrows():
        table.insert(
            "",
            tk.END,
            values=(
                row["Date"],
                row["Activity"],
                f"{float(row['Litres']):.2f}",
                row["Description"],
            ),
        )

    update_summary_cards()


def update_summary_cards():
    """Refresh dashboard statistics."""
    total_var.set(f"{calculate_total():.2f} L")
    average_var.set(f"{calculate_average():.2f} L")
    high_var.set(str(len(get_high_consumption())))
    day, litres = highest_consumption_day()
    highest_day_var.set(f"{day}\n{litres:.2f} L" if day else "No data")


def add_water_record():
    """Validate and save a new water-use record."""
    date = date_entry.get().strip()
    activity = activity_entry.get().strip()
    litres = litres_entry.get().strip()
    description = description_entry.get().strip()

    success, message = add_record(date, activity, litres, description)

    if success:
        messagebox.showinfo("Success", message)
        clear_fields()
        refresh_table()
    else:
        messagebox.showerror("Invalid Input", message)


def search_water_records():
    """Filter records by activity and/or exact date."""
    activity = search_activity_entry.get().strip()
    date = search_date_entry.get().strip()

    if date:
        from data_manager import validate_date
        if not validate_date(date):
            messagebox.showerror("Invalid Date", "Search date must be in YYYY-MM-DD format.")
            return

    result = search_records(activity, date)
    refresh_table(result)

    if result.empty:
        messagebox.showinfo("Search", "No records found for the selected filter.")


def show_all_records():
    """Display all stored records."""
    search_activity_entry.delete(0, tk.END)
    search_date_entry.delete(0, tk.END)
    refresh_table()


def show_total():
    messagebox.showinfo("Total Water Usage", f"Total Water Usage:\n\n{calculate_total():.2f} Litres")


def show_average():
    messagebox.showinfo("Average Water Usage", f"Average Water Usage:\n\n{calculate_average():.2f} Litres")


def show_maximum():
    messagebox.showinfo("Maximum Usage", f"Highest Individual Usage:\n\n{calculate_maximum():.2f} Litres")


def show_minimum():
    messagebox.showinfo("Minimum Usage", f"Lowest Individual Usage:\n\n{calculate_minimum():.2f} Litres")


def show_activity_comparison():
    """Display activity-wise totals."""
    data = activity_comparison()
    if data.empty:
        messagebox.showinfo("Activity Comparison", "No data available.")
        return

    result = "Activity-wise Water Usage\n\n"
    result += "\n".join(f"{activity}: {litres:.2f} Litres" for activity, litres in data.items())
    messagebox.showinfo("Activity Comparison", result)


def create_data_window(title, columns, rows, width=850, height=430):
    """Create a reusable table window for analysis results."""
    window = tk.Toplevel(root)
    window.title(title)
    window.geometry(f"{width}x{height}")
    window.configure(bg=BG_COLOR)

    tk.Label(
        window,
        text=title,
        font=("Segoe UI", 16, "bold"),
        bg=BG_COLOR,
        fg=HEADER_COLOR,
    ).pack(pady=12)

    frame = tk.Frame(window, bg=BG_COLOR)
    frame.pack(fill="both", expand=True, padx=15, pady=10)

    tree = ttk.Treeview(frame, columns=columns, show="headings")
    for column in columns:
        tree.heading(column, texlt=column)
        tree.column(column, width=180, anchor="center")

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for row in rows:
        tree.insert("", tk.END, values=row)

    return window


def show_high_usage():
    """Display individual high-consumption records."""
    data = get_high_consumption()
    if data.empty:
        messagebox.showinfo("High Consumption", f"No records at or above {HIGH_USAGE_LIMIT} litres.")
        return

    rows = [
        (row["Date"], row["Activity"], f"{float(row['Litres']):.2f}", row["Description"])
        for _, row in data.iterrows()
    ]
    create_data_window(
        f"High Consumption Records (≥ {HIGH_USAGE_LIMIT} L)",
        ("Date", "Activity", "Litres", "Description"),
        rows,
        width=900,
    )


def show_daily_comparison():
    """Display daily water consumption for period comparison."""
    data = daily_consumption()
    if data.empty:
        messagebox.showinfo("Daily Comparison", "No data available.")
        return

    rows = [(date, f"{float(litres):.2f}") for date, litres in data.items()]
    create_data_window(
        "Daily Water Consumption",
        ("Date", "Total Litres"),
        rows,
        width=600,
    )


def show_high_days():
    """Display days whose total consumption is above the daily threshold."""
    data = high_consumption_days()
    if data.empty:
        messagebox.showinfo(
            "High-Consumption Days",
            f"No days at or above {HIGH_DAILY_USAGE_LIMIT} litres.",
        )
        return

    rows = [(date, f"{float(litres):.2f}") for date, litres in data.items()]
    create_data_window(
        f"High-Consumption Days (≥ {HIGH_DAILY_USAGE_LIMIT} L)",
        ("Date", "Total Litres"),
        rows,
        width=600,
    )


def show_highest_day():
    """Display the highest-consumption day."""
    date, litres = highest_consumption_day()
    if not date:
        messagebox.showinfo("Highest Consumption Day", "No data available.")
        return

    messagebox.showinfo(
        "Highest Consumption Day",
        f"Date: {date}\n\nTotal Usage: {litres:.2f} Litres",
    )


# -----------------------------
# HEADER
# -----------------------------
header = tk.Frame(root, bg=HEADER_COLOR, height=78)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="💧 WATER USAGE MONITORING AND ANALYSIS SYSTEM",
    font=("Segoe UI", 19, "bold"),
    bg=HEADER_COLOR,
    fg="white",
).pack(pady=(12, 2))

tk.Label(
    header,
    text="Record • Analyze • Understand Water Consumption",
    font=("Segoe UI", 10),
    bg=HEADER_COLOR,
    fg="white",
).pack()

# -----------------------------
# DASHBOARD CARDS
# -----------------------------
dashboard = tk.Frame(root, bg=BG_COLOR)
dashboard.pack(fill="x", padx=18, pady=10)

total_var = tk.StringVar(value="0.00 L")
average_var = tk.StringVar(value="0.00 L")
high_var = tk.StringVar(value="0")
highest_day_var = tk.StringVar(value="No data")

cards = [
    ("TOTAL USAGE", total_var),
    ("AVERAGE / RECORD", average_var),
    ("HIGH-USAGE RECORDS", high_var),
    ("HIGHEST DAY", highest_day_var),
]

for index, (label, variable) in enumerate(cards):
    card = tk.Frame(dashboard, bg=CARD_COLOR, bd=1, relief="solid")
    card.grid(row=0, column=index, padx=5, sticky="nsew")
    dashboard.columnconfigure(index, weight=1)
    tk.Label(card, text=label, font=("Segoe UI", 9, "bold"), bg=CARD_COLOR, fg=TEXT_COLOR).pack(pady=(8, 2))
    tk.Label(card, textvariable=variable, font=("Segoe UI", 12, "bold"), bg=CARD_COLOR, fg=HEADER_COLOR).pack(pady=(0, 8))

# -----------------------------
# INPUT FRAME
# -----------------------------
input_frame = tk.LabelFrame(
    root,
    text="Add Water Usage Record",
    font=("Segoe UI", 11, "bold"),
    bg=SECTION_COLOR,
    fg=TEXT_COLOR,
    padx=8,
    pady=5,
)
input_frame.pack(fill="x", padx=18, pady=4)

for column in range(4):
    input_frame.columnconfigure(column, weight=1)

labels = ["Date (YYYY-MM-DD):", "Activity:", "Water Used (Litres):", "Description:"]
entries = []
for i, label in enumerate(labels):
    tk.Label(input_frame, text=label, bg=SECTION_COLOR, fg=TEXT_COLOR).grid(
        row=0 if i < 2 else 2,
        column=(i * 2) % 4,
        padx=6,
        pady=5,
        sticky="e",
    )


date_entry = tk.Entry(input_frame, width=24)
date_entry.grid(row=0, column=1, padx=6, pady=5, sticky="ew")
activity_entry = tk.Entry(input_frame, width=24)
activity_entry.grid(row=0, column=3, padx=6, pady=5, sticky="ew")
litres_entry = tk.Entry(input_frame, width=24)
litres_entry.grid(row=2, column=1, padx=6, pady=5, sticky="ew")
description_entry = tk.Entry(input_frame, width=24)
description_entry.grid(row=2, column=3, padx=6, pady=5, sticky="ew")

button_frame = tk.Frame(input_frame, bg=SECTION_COLOR)
button_frame.grid(row=4, column=0, columnspan=4, pady=5)

tk.Button(
    button_frame,
    text="ADD RECORD",
    command=add_water_record,
    width=16,
    bg=BUTTON_COLOR,
    fg=BUTTON_TEXT,
    relief="flat",
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="CLEAR",
    command=clear_fields,
    width=12,
    bg="#607D8B",
    fg=BUTTON_TEXT,
    relief="flat",
).pack(side="left", padx=5)

# -----------------------------
# SEARCH / FILTER
# -----------------------------
search_frame = tk.LabelFrame(
    root,
    text="Search / Filter Records",
    font=("Segoe UI", 11, "bold"),
    bg=SECTION_COLOR,
    fg=TEXT_COLOR,
    padx=8,
    pady=5,
)
search_frame.pack(fill="x", padx=18, pady=4)

search_activity_entry = tk.Entry(search_frame, width=22)
search_date_entry = tk.Entry(search_frame, width=18)

tk.Label(search_frame, text="Activity:", bg=SECTION_COLOR, fg=TEXT_COLOR).pack(side="left", padx=(5, 3))
search_activity_entry.pack(side="left", padx=3)
tk.Label(search_frame, text="Date:", bg=SECTION_COLOR, fg=TEXT_COLOR).pack(side="left", padx=(12, 3))
search_date_entry.pack(side="left", padx=3)

tk.Button(
    search_frame,
    text="SEARCH",
    command=search_water_records,
    width=12,
    bg=BUTTON_COLOR,
    fg=BUTTON_TEXT,
    relief="flat",
).pack(side="left", padx=5)

tk.Button(
    search_frame,
    text="SHOW ALL",
    command=show_all_records,
    width=12,
    bg="#607D8B",
    fg=BUTTON_TEXT,
    relief="flat",
).pack(side="left", padx=5)

tk.Button(
    search_frame,
    text="REFRESH",
    command=refresh_table,
    width=12,
    bg=SUCCESS_COLOR,
    fg=BUTTON_TEXT,
    relief="flat",
).pack(side="left", padx=5)

# -----------------------------
# RECORDS TABLE
# -----------------------------
table_frame = tk.LabelFrame(
    root,
    text="Water Usage Records",
    font=("Segoe UI", 11, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR,
)
table_frame.pack(fill="both", expand=True, padx=18, pady=4)

table_container = tk.Frame(table_frame, bg=BG_COLOR)
table_container.pack(fill="both", expand=True, padx=8, pady=6)

table = ttk.Treeview(
    table_container,
    columns=("Date", "Activity", "Litres", "Description"),
    show="headings",
    height=7,
)
for column, width in [("Date", 120), ("Activity", 150), ("Litres", 100), ("Description", 520)]:
    table.heading(column, text=column)
    table.column(column, width=width)

scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scrollbar.set)
table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# -----------------------------
# ANALYSIS BUTTONS
# -----------------------------
action_frame = tk.Frame(root, bg=BG_COLOR)
action_frame.pack(pady=6)

buttons = [
    ("TOTAL USAGE", show_total),
    ("AVERAGE", show_average),
    ("MAXIMUM", show_maximum),
    ("MINIMUM", show_minimum),
    ("HIGH USAGE", show_high_usage),
    ("ACTIVITY COMPARISON", show_activity_comparison),
    ("DAILY COMPARISON", show_daily_comparison),
    ("HIGH-USAGE DAYS", show_high_days),
    ("HIGHEST DAY", show_highest_day),
]

# First row: 5 buttons
first_row = tk.Frame(action_frame, bg=BG_COLOR)
first_row.pack()

for text, command in buttons[:5]:
    tk.Button(
        first_row,
        text=text,
        command=command,
        width=16 if len(text) < 17 else 19,
        bg=WARNING_COLOR if "HIGH" in text or "HIGHEST" in text else BUTTON_COLOR,
        fg=BUTTON_TEXT,
        relief="flat",
    ).pack(side="left", padx=3, pady=3)

# Second row: 4 buttons, centered
second_row = tk.Frame(action_frame, bg=BG_COLOR)
second_row.pack()

for text, command in buttons[5:]:
    tk.Button(
        second_row,
        text=text,
        command=command,
        width=16 if len(text) < 17 else 19,
        bg=WARNING_COLOR if "HIGH" in text or "HIGHEST" in text else BUTTON_COLOR,
        fg=BUTTON_TEXT,
        relief="flat",
    ).pack(side="left", padx=3, pady=3)

# -----------------------------
# GRAPH BUTTONS
# -----------------------------
graph_frame = tk.Frame(root, bg=BG_COLOR)
graph_frame.pack(pady=(1, 7))

tk.Button(
    graph_frame,
    text="ACTIVITY GRAPH",
    command=activity_usage_graph,
    width=22,
    bg=SUCCESS_COLOR,
    fg=BUTTON_TEXT,
    relief="flat",
).pack(side="left", padx=5)

tk.Button(
    graph_frame,
    text="DAILY USAGE GRAPH",
    command=daily_usage_graph,
    width=22,
    bg=SUCCESS_COLOR,
    fg=BUTTON_TEXT,
    relief="flat",
).pack(side="left", padx=5)

refresh_table()
date_entry.focus_set()
root.mainloop()