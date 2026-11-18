"""Monthly totals from dated entries."""

from datetime import timedelta
from decimal import Decimal


def week_start(day):
    return day - timedelta(days=day.weekday())


def month_summary(expenses, nights, month):
    everyday = healthcare = Decimal(0)
    days = 0
    for day, categories in expenses.items():
        if day.strftime('%Y-%m') == month:
            days += 1
            for key, value in categories.items():
                if key.startswith('Everyday / '):
                    everyday += value
                else:
                    healthcare += value
    hours = [value for day, (value, _) in nights.items() if day.strftime('%Y-%m') == month]
    return everyday, healthcare, days, sum(hours) / len(hours) if hours else None, len(hours)
