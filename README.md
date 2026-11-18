# WellLedger

A Python desktop ledger for daily expenses, sleep and reminders. Follow [START_HERE.txt](START_HERE.txt) to install it. Existing users should run setup.sql again to add the dated tables.

Enter your name and age (18–120) in Profile. Accounting opens on today’s date. Enter the daily total for each category and choose **Save day**. To correct a past date, open **Calendar → Edit expenses**. Saving replaces that date’s figures. An explicit zero counts as a recorded amount.

Sleep uses the date you woke up and a Monday–Sunday week. Save individual nights as you go. **Review sleep** becomes available when all seven dates have valid hours (0–24). Reviewing files the week and clears its input fields. Partial weeks stay available through Calendar. Future dates are unavailable for entry.

**Monthly reports** compares the selected months’ recorded everyday and healthcare totals and their average hours per recorded night. The counts show how much of each month has been entered. Dates use the computer’s local calendar. Old entries without dates stay in **View progress** for reference. You can enter them in Calendar if you know their dates.
