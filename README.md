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

- Local sign-up/login, editable profile, and separate saved inputs for each account
- Overview dashboard and persistent sidebar
- Expense totals, spending summary, and category charts
- Adult BMI, activity check-ins, seven-night sleep log, and cycle date recording
- Wellbeing notes and a calendar with reminders and Today/month controls
- Scrollable pages for smaller screens
- Alt+Left to go Back; Ctrl+H to return Home
- View progress on the login page (enter your credentials first) or overview
- Practical meal, activity, sleep and appointment-planning suggestions

## Data and scope

Create an account when the app opens. Usernames are case-insensitive; passwords
must contain 8–128 characters. Use **Save inputs** at any time. Inputs also save
when changing pages, logging out or closing the window normally. Review actions,
Save notes and Save reminder save their inputs too. A crash or forced termination
can lose edits made since the last save. Unfinished inputs are saved as drafts;
the existing calculators still validate before calculating.

SQLite creates `~/.wellledger/wellledger.sqlite3` automatically (`~` is your home
folder). No database server, API key or additional dependency is required. Each
account has one latest workspace, not a historical tracking system. **View
progress** reads that account's saved profile, expenses, wellbeing inputs, notes
and reminders from the database, with the last save time in UTC. It does not
claim that health or finances have improved.

Passwords use a unique random salt and PBKDF2-HMAC-SHA256 with 600,000 rounds;
plaintext passwords are never saved. The database itself is **not encrypted**:
anyone with access to the file can read personal entries. Accounts separate data
inside this local app, not from someone who controls your computer. There is no
cloud sync or password recovery. To back up your data, close the app and copy the
database to a private location. Do not commit it to GitHub.

Calendar entries are notes, not operating-system notifications. Existing manual
check-ins remain; no new tracking, history charts or automated monitoring is
added. BMI categories are restricted to users aged 20 or older with an age in
their profile. BMI is a screening measure, not a diagnosis; cycle recording does
not predict fertility. Suggestions are general planning ideas, not treatment or
personalized diet/exercise prescriptions.

### Code map

- `app.py`: Tkinter screens, navigation and input collection/restoration
- `storage.py`: SQLite tables, password checks and saved workspaces
- `guidance.py`: readable, editable suggestion text
- `test_app.py`, `test_storage.py`: GUI regression and database tests

### Check the changes

```sh
python -m unittest test_storage test_app -v
```

GUI tests need a desktop display; they are skipped without one. On a Linux
machine with Xvfb installed, use `xvfb-run -a python -m unittest test_storage
test_app -v`. Do not use broad test discovery: some old prototype filenames
start with `test` but launch standalone windows.

### Guidance references

- [CDC: sleep habits](https://www.cdc.gov/sleep/about/)
- [NIDDK: food choices and gradual activity](https://www.niddk.nih.gov/health-information/weight-management/healthy-eating-physical-activity-for-life/health-tips-for-adults)
- [CDC: adult BMI scope](https://www.cdc.gov/bmi/adult-calculator/)

Older numbered/duplicate prototype files remain in the repository for reference
and are not part of the main application.
