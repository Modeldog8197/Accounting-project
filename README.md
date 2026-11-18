# WellLedger

A Python desktop ledger for daily expenses, sleep and reminders. Follow [START_HERE.txt](START_HERE.txt) to install it. Existing users should run setup.sql again to add any missing history tables.

Enter your name and age (18–120) in Profile. Accounting opens on today’s date. Enter the daily total for each category and choose **Save day**. To correct a past date, open **Calendar → Edit expenses**. Saving replaces that date’s figures. An explicit zero counts as a recorded amount.

Sleep uses the date you woke up and a Monday–Sunday week. Save individual nights as you go. **Review sleep** becomes available when all seven dates have valid hours (0–24). Reviewing files the week and clears its input fields. Partial weeks stay available through Calendar. Future dates are unavailable for entry.

**Monthly reports** compares the selected months’ recorded everyday and healthcare totals and their average hours per recorded night. The counts show how much of each month has been entered. Dates use the computer’s local calendar. Old entries without dates stay in **View progress** for reference. You can enter them in Calendar if you know their dates.

### Health history

Choose a date in Calendar and open Body measurements, Activity, Cycle, Diet, Exercise plan or Care notes. Opening a health tool from the main menu starts on today’s date. Saving again updates the same day and section. Blank numeric fields are missing measurements. An entered zero is a recorded value. Clear a section’s fields and save to remove just that entry.

In Monthly reports, choose a metric below the two month selectors. Compare the selected months and see the six months ending with the later one. Numeric averages use recorded dates only. BMI requires both weight and height on the same date. Cycle intervals use consecutive recorded starts and belong to the month of the later start. Diet accepts optional meals eaten and free text. For written notes, the charts count dates with a note and list the text for the selected months.

Run setup.sql again when upgrading. Previously saved undated inputs can be read in View progress. Previously dated period starts written by the app are imported once. Profile and sign-in details are account settings.
