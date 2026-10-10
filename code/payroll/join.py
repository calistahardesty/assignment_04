"""
join.py — Step 2 of the pipeline: bring the roster onto the timesheet.

The timesheet knows *who worked and how long*. The roster knows *what each
person is paid*. Neither file can produce a paycheck on its own, so the pipeline
has to combine them — and the two files have different **grains**: one row per
week-of-work versus one row per person. That is exactly what `pd.merge` is for.

The decision in this step is not *how* to merge but *which kind*. A left merge
keeps every timesheet row and only matches from the roster.
"""

import pandas as pd


def merge_employees(timesheet: pd.DataFrame, employees: pd.DataFrame) -> pd.DataFrame:
    """Return the timesheet with every roster column added to each row.

    Given the (already cleaned) timesheet and the (already cleaned) roster,
    return one row **per timesheet row** with that employee's roster columns —
    `first_name`, `last_name`, `department`, `hourly_rate`, `hourly_rate_usd` —
    filled in beside the timesheet columns.

    Two rules decide the join type:

    1. **Every timesheet row survives.** An `employee_id` that is not on the
       roster still worked those hours, so its roster columns come back as
       `NaN` instead of the row vanishing.
    2. **Rostered people who did not work do not appear.** No timesheet row,
       no paycheck.

    Keeping all of the left frame (the timesheet) and only matches from the
    right frame (the roster) is a left merge.
    """
    return pd.merge(timesheet, employees, on="employee_id", how="left")