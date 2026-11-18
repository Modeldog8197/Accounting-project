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


HEALTH_SECTIONS = {'bmi': 'Body measurements', 'fitness': 'Activity', 'cycle': 'Cycle',
                   'nutrition': 'Diet', 'exercise': 'Exercise plan', 'care': 'Care notes'}

# Each numeric average uses only dates that have that measurement.
METRICS = {
    'BMI': ('bmi', 'BMI', 'kg/m²'), 'Weight': ('bmi', 'Weight (kg)', 'kg'),
    'Height': ('bmi', 'Height (cm)', 'cm'), 'Steps': ('fitness', 'Steps', 'steps'),
    'Exercise minutes': ('fitness', 'Exercise (minutes)', 'min'),
    'Water': ('fitness', 'Water (glasses)', 'glasses'), 'Meals': ('nutrition', 'Meals', 'meals'),
    'Period starts': ('cycle', 'start', 'starts'), 'Days between starts': ('cycle', 'interval', 'days'),
    'Diet notes': ('nutrition', 'Notes', 'days logged'), 'Exercise plans': ('exercise', 'Notes', 'days logged'),
    'Care notes': ('care', 'Notes', 'days logged'), 'Cycle notes': ('cycle', 'Notes', 'days logged')
}


def metric_series(records, metric):
    section, field, _ = METRICS[metric]
    previous = None
    result = {}
    for day, entries in sorted(records.items()):
        data = entries.get(section, {})
        if field == 'BMI' and 'Weight (kg)' in data and 'Height (cm)' in data:
            result[day] = float(data['Weight (kg)']) / (float(data['Height (cm)']) / 100) ** 2
        elif field == 'interval' and data.get('start'):
            if previous is not None:
                result[day] = (day - previous).days
            previous = day
        elif field in data:
            result[day] = 1 if field in ('Notes', 'start') else float(data[field])
    return result


def monthly_value(series, month, count):
    values = [v for d, v in series.items() if d.strftime('%Y-%m') == month]
    if not values:
        return None, 0
    return (len(values) if count else sum(values) / len(values)), len(values)


def health_lines(section, data):
    lines = []
    for key, value in data.items():
        lines.append('Period start' if key == 'start' else f'{key}: {value}')
    if section == 'bmi' and 'Weight (kg)' in data and 'Height (cm)' in data:
        bmi = float(data['Weight (kg)']) / (float(data['Height (cm)']) / 100) ** 2
        lines.append(f'BMI: {bmi:.1f}')
    return lines
