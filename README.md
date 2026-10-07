# WellLedger — Accounting & Health

A consistent desktop workspace for expense tracking, wellbeing check-ins, and
calendar reminders. All main tools share one window, a sidebar, and Back/Home
navigation. Entries stay available when moving between pages.

## Start

Requires Python 3.10+ with Tkinter. For expense charts, install the dependency:

```sh
python -m pip install -r requirements.txt
python app.py
```

`PROJECTMODIFIED.py` and `project .py` also launch the welcome page. The original
module entry points open their corresponding redesigned pages.

## Features

- Welcome form and editable profile with input validation
- Overview dashboard and persistent sidebar
- Expense totals, spending summary, and category charts
- Adult BMI, activity check-ins, seven-night sleep log, and cycle date recording
- Wellbeing notes and a calendar with reminders and Today/month controls
- Scrollable pages for smaller screens
- Alt+Left to go Back; Ctrl+H to return Home

## Data and scope

Entries are stored in memory for the current session, not written to disk or
sent to a server. Closing the application clears them. Calendar entries are
notes, not operating-system notifications. BMI is an adult screening measure,
not a diagnosis; cycle recording does not predict fertility.

Older numbered/duplicate prototype files remain in the repository for reference
and are not part of the main application.
