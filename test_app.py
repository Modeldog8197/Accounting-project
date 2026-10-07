"""Integration checks for routes, retained state, and input handling."""

import unittest
from datetime import date
from decimal import Decimal

from app import App, amount


class CurrencyTests(unittest.TestCase):
    def test_currency_precision_and_invalid_values(self):
        self.assertEqual(amount('1,234.50') + amount('0.10'), Decimal('1234.60'))
        for value in ('NaN', 'Infinity', '-1', 'hello'):
            with self.assertRaises(ValueError):
                amount(value)


class NavigationTests(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.app.withdraw()

    def tearDown(self):
        self.app.destroy()

    def test_all_pages_back_home_and_retained_expenses(self):
        self.app.user['name'].set('Preview')
        self.app.pages['welcome'].save_profile()
        self.assertEqual(self.app.current, 'home')
        self.app.show('accounting')
        page = self.app.pages['accounting']
        page.expenses[('Everyday', 'Food & groceries')].set('100.10')
        page.expenses[('Healthcare', 'Medicines')].set('25.20')
        self.assertEqual(page.metrics['Total'].cget('text'), '₹125.30')
        self.app.show('health'); self.app.back()
        self.assertEqual(self.app.current, 'accounting')
        self.assertEqual(page.metrics['Total'].cget('text'), '₹125.30')
        for route in ('profile', 'health', 'bmi', 'fitness', 'sleep', 'cycle', 'guides', 'nutrition', 'exercise', 'care', 'calendar'):
            self.app.show(route)
            self.app.update_idletasks()
            self.assertEqual(self.app.current, route)
        self.app.home()
        self.assertEqual(self.app.history, [])
        self.assertEqual(self.app.current, 'home')

    def test_calendar_drafts_month_rollover_and_cycle(self):
        self.app.show('calendar')
        page = self.app.pages['calendar']
        page.select_date(date(2026, 12, 31))
        page.notes.insert('1.0', 'Appointment')
        self.app.show('home')
        self.app.show('calendar')
        self.assertEqual(page.notes.get('1.0', 'end').strip(), 'Appointment')
        page.month = date(2026, 12, 1)
        page.change_month(1)
        self.assertEqual(page.month, date(2027, 1, 1))
        page.change_month(-1)
        self.assertEqual(page.month, date(2026, 12, 1))
        self.app.show('cycle')
        cycle = self.app.pages['cycle']
        cycle.cycle_date.set('2026-12-31'); cycle.save_cycle()
        self.assertIn('Appointment', self.app.reminders['2026-12-31'])
        self.assertIn('Cycle:', self.app.reminders['2026-12-31'])

    def test_health_and_invalid_amounts(self):
        self.app.show('bmi'); page = self.app.pages['bmi']
        page.weight.set('70'); page.height.set('175'); page.calculate_bmi()
        self.assertIn('22.9', page.feedback.cget('text'))
        page.height.set('0'); page.calculate_bmi()
        self.assertEqual(page.feedback.cget('fg'), '#B42318')
        self.app.show('sleep'); page = self.app.pages['sleep']
        for var in page.sleep_vars: var.set('8')
        page.review_sleep()
        self.assertIn('8.0', page.feedback.cget('text'))
        self.app.show('accounting'); page = self.app.pages['accounting']
        page.expenses[('Everyday', 'Transport')].set('NaN')
        self.assertEqual(page.metrics['Total'].cget('text'), '—')

    def test_chart_rendering_and_unchanged_inputs(self):
        self.app.show('accounting')
        page = self.app.pages['accounting']
        page.expenses[('Everyday', 'Other')].set('20')
        page.expenses[('Healthcare', 'Other')].set('30')
        page.charts()
        self.app.update_idletasks()
        charts = [widget for widget in self.app.winfo_children()
                  if widget.winfo_class() == 'Toplevel']
        self.assertEqual(len(charts), 1)
        self.assertEqual(charts[0].title(), 'Spending insights')
        charts[0].destroy()
        self.assertEqual(page.metrics['Total'].cget('text'), '₹50.00')


if __name__ == '__main__':
    unittest.main()
