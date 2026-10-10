"""
clean.py — Step 1 of the pipeline: turn text into numbers, one value at a time.

Two element functions that each read one messy string and return one number, and
two DataFrame functions that use `Series.apply` to run them down a whole column
and store the result in a **new** column.

The lineage rule, which every step of this pipeline follows:

    A pipeline function takes a DataFrame and returns a WIDER copy of it.
    It never changes a value it was given, never removes a column, never renames
    one, and never modifies the frame the caller passed in.

So `"38h 30m"` stays in `hours`, and `38.5` goes in `hours_worked` beside it. An
auditor reading the payroll table can see both — which is the point.

This step is walked through line by line in each docstring. The next two steps
give you less.
"""

import pandas as pd


def parse_hours(value) -> float:
    """Read a weekly-hours string the way a shift lead typed it; return a float.

    Examples:

        parse_hours("38h 30m")   ->  38.5
        parse_hours("42h")       ->  42.0
        parse_hours("45m")       ->  0.75
        parse_hours("24.5")      ->  24.5
        parse_hours("")          ->  0.0      # unreadable -> zero, never a crash
        parse_hours(None)        ->  0.0
    """
    if not isinstance(value, str):
        if pd.isna(value):
            return 0.0
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    text = value.strip()
    if not text:
        return 0.0

    if "h" not in text and "m" not in text:
        try:
            return float(text)
        except ValueError:
            return 0.0

    hours = 0.0
    try:
        for word in text.split():
            if word.endswith("h"):
                hours += float(word[:-1])
            elif word.endswith("m"):
                hours += float(word[:-1]) / 60
    except ValueError:
        return 0.0
    return hours


def clean_currency(value) -> float:
    """Read a dollar amount as HR typed it; return it as a float.

    Examples:

        clean_currency("$18.50")     ->  18.5
        clean_currency("17.75")      ->  17.75
        clean_currency(" $1,020.00") ->  1020.0
        clean_currency("")           ->  0.0      # unreadable -> zero
        clean_currency(None)         ->  0.0
    """
    if not isinstance(value, str):
        if pd.isna(value):
            return 0.0
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    text = value.replace("$", "").replace(",", "").strip()
    try:
        return float(text)
    except ValueError:
        return 0.0


def add_hours_worked(timesheet: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of the timesheet with one new column, `hours_worked` (float).

    `hours_worked` is `parse_hours` applied to every value in `hours`. The `hours`
    column itself is untouched — the text the shift lead typed stays in the table.
    """
    out = timesheet.copy()
    out["hours_worked"] = out["hours"].apply(parse_hours)
    return out


def add_hourly_rate(employees: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of the roster with one new column, `hourly_rate_usd` (float).

    `hourly_rate_usd` is `clean_currency` applied to every value in
    `hourly_rate`. `hourly_rate` stays exactly as HR typed it.
    """
    out = employees.copy()
    out["hourly_rate_usd"] = out["hourly_rate"].apply(clean_currency)
    return out


if __name__ == "__main__":
    # Try the parser here with the debugger — the tests will not stop at breakpoints.
    for sample in ("38h 30m", "42h", "45m", "24.5", "", "forty"):
        print(repr(sample), "->", parse_hours(sample))
    print(clean_currency("$1,020.00"))