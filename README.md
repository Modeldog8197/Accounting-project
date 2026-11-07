# WellLedger — Accounting & Health

A consistent desktop workspace for expense tracking, wellbeing check-ins, and
calendar reminders. All main tools share one window, a sidebar, and Back/Home
navigation. Entries stay available when moving between pages.

## Start

Requires Python 3.10+ with Tkinter and a local MySQL 8 server. MySQL Workbench
is optional; the server itself must be installed and running.

1. Install the Python dependencies:

   ```sh
   python -m pip install -r requirements.txt
   ```

2. Open MySQL Workbench, connect to your local server, open `setup.sql`, and run
   the complete script. Alternatively, from the project folder run `mysql -u
   root -p`, then enter `SOURCE setup.sql;` at the MySQL prompt. This creates
   `wellledger` and its two tables without deleting existing rows.

3. Copy `db_config.example.py` to `db_config.py`. Enter your local MySQL username
   and password. Keep `database` as `wellledger`, and adjust the port if your
   server uses a port other than 3306. This password is for MySQL, not the account
   you will create inside WellLedger. `db_config.py` is ignored by Git.

4. Start the app:

   ```sh
   python app.py
   ```

If the database cannot open, the app shows a setup message. Check that MySQL is
running, that the credentials are correct, and that `setup.sql` has been run.
The configured MySQL user needs SELECT, INSERT and UPDATE access to both tables.
Use a local account suitable for your school environment; the example uses root
only as a common local setup. Do not expose this desktop database to the internet.

`PROJECTMODIFIED.py` and `project .py` also start the app. All entry points require
login before opening their corresponding pages.

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

MySQL stores accounts in `users` and each account's latest inputs in `workspaces`.
There is no tracking history. **View progress** reads the signed-in account's
profile, expenses, wellbeing inputs, notes and reminders, with the last save time
in UTC. It does not claim that health or finances have improved.

The SQL uses ordinary tables and parameterized INSERT, SELECT, UPDATE and WHERE
queries. Saving first checks whether a row exists, then inserts or updates it.
There are no upserts, triggers, stored procedures, ORMs or SQL JSON functions.
Python's `json` module keeps the existing workspace dictionary as text in the
`data` column; the MySQL queries do not interpret that text. `commit()` saves a
change and `rollback()` cancels a failed write. The test cleanup uses DELETE.

Passwords still use a unique random salt and PBKDF2-HMAC-SHA256 with 600,000
rounds in Python. SQL stores only the salt and hash as text. Personal inputs are
not encrypted in the database; anyone with database access can read them. There
is no cloud sync or password recovery. Keep your local configuration and database
backups private, outside the repository.

### Keeping data from the previous SQLite version

The old `~/.wellledger/wellledger.sqlite3` file is not changed or deleted. To copy
its accounts and saved inputs, run the following **after MySQL setup and before
creating any new app accounts**, with the app closed:

```sh
python import_sqlite.py
```

For a file in a different location, pass its path: `python import_sqlite.py
/path/to/wellledger.sqlite3`. The import requires an empty destination, keeps
existing passwords working and copies saved inputs and timestamps. It cancels
all new inserts if any row fails; it never overwrites existing MySQL accounts.
Keep the original file as a backup. SQLite is used only by this optional importer,
not by the application.

Calendar entries are notes, not operating-system notifications. Existing manual
check-ins remain; no new tracking, history charts or automated monitoring is
added. BMI categories are restricted to users aged 20 or older with an age in
their profile. BMI is a screening measure, not a diagnosis; cycle recording does
not predict fertility. Suggestions are general planning ideas, not treatment or
personalized diet/exercise prescriptions.

### Code map

- `app.py`: Tkinter screens, navigation and input collection/restoration
- `storage.py`: MySQL queries, password checks and saved workspaces
- `setup.sql`: the database and two table definitions
- `db_config.example.py`: a template for your private connection settings
- `import_sqlite.py`: optional copy of data from the previous version
- `guidance.py`: readable, editable suggestion text
- `test_app.py`, `test_storage.py`: GUI regression and database tests

### Check the changes

Tests use a real MySQL server and a **separate, disposable database**. In MySQL,
run `CREATE DATABASE wellledger_test CHARACTER SET utf8mb4;`. Copy your local
`db_config.py` to `db_config_test.py` and change `database` to `wellledger_test`.
The test account needs CREATE, SELECT, INSERT, UPDATE and DELETE permissions on
that database. Tests create their tables and clear their rows between cases.
They refuse to use any database name other than `wellledger_test`.

```sh
python -m unittest test_storage test_app -v
```

Database tests skip if `db_config_test.py` is missing; they do not silently fall
back to SQLite. GUI tests additionally need a desktop display. On Linux with
Xvfb installed, use:

```sh
xvfb-run -a python -m unittest test_storage test_app -v
```

Do not use broad test discovery: old prototype filenames beginning with `test`
can launch standalone windows. The focused tests cover login validation, SQL
injection inputs, account isolation, insert/update, reconnects, restart
persistence, optional import and the existing charts and navigation.

### Guidance references

- [CDC: sleep habits](https://www.cdc.gov/sleep/about/)
- [NIDDK: food choices and gradual activity](https://www.niddk.nih.gov/health-information/weight-management/healthy-eating-physical-activity-for-life/health-tips-for-adults)
- [CDC: adult BMI scope](https://www.cdc.gov/bmi/adult-calculator/)

Older numbered/duplicate prototype files remain in the repository for reference
and are not part of the main application.
