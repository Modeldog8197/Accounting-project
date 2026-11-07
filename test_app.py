"""Integration checks for routes, retained state, and input handling."""

import unittest
import os
import mysql.connector
from unittest.mock import patch
from datetime import date
from decimal import Decimal

from app import App, amount
from test_support import prepare_database


class CurrencyTests(unittest.TestCase):
    def test_currency_precision_and_invalid_values(self):
        self.assertEqual(amount('1,234.50') + amount('0.10'), Decimal('1234.60'))
        for value in ('NaN', 'Infinity', '-1', 'hello'):
            with self.assertRaises(ValueError):
                amount(value)


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name == 'nt' or __import__('sys').platform == 'darwin', 'Needs a desktop display')
class NavigationTests(unittest.TestCase):
    def setUp(self):
        self.database = prepare_database()
        self.app = App(database=self.database)
        self.app.withdraw()
        user_id = self.app.store.sign_up('preview', 'test-password')
        self.app.sign_in(user_id)
        self.app.user['age'].set('25')

    def tearDown(self):
        self.app.destroy()

    def test_login_gate_and_wrong_password(self):
        self.app.logout()
        self.app.show('progress')
        self.assertEqual(self.app.current, 'login')
        self.app.home()
        self.assertEqual(self.app.current, 'login')
        page = self.app.pages['login']
        page.username.set('preview'); page.password.set('wrong')
        page.authenticate('progress')
        self.assertIsNone(self.app.user_id)
        self.assertIn('Incorrect', page.feedback.cget('text'))
        page.password.set('test-password'); page.authenticate('progress')
        self.assertEqual(self.app.current, 'progress')

    def test_restart_restores_all_inputs_and_accounts_are_isolated(self):
        self.app.user['name'].set('Preview')
        self.app.show('bmi')
        self.app.pages['bmi'].weight.set('70')
        self.app.pages['bmi'].height.set('175')
        self.app.show('fitness')
        for var in self.app.pages['fitness'].activity.values(): var.set('12')
        self.app.show('sleep')
        for var in self.app.pages['sleep'].sleep_vars: var.set('8')
        self.app.show('cycle')
        self.app.pages['cycle'].cycle_date.set('2026-11-01')
        self.app.pages['cycle'].cycle_note.set('Example')
        self.app.pages['cycle'].save_cycle()
        for route in ('nutrition', 'exercise', 'care'):
            self.app.show(route)
            self.app.pages[route].plan.insert('end', 'Saved note')
        self.app.show('accounting')
        self.app.pages['accounting'].expenses[('Everyday', 'Food & groceries')].set('123.45')
        self.app.show('calendar')
        self.app.pages['calendar'].select_date(date(2026, 11, 2))
        self.app.pages['calendar'].notes.insert('1.0', 'Saved reminder')
        self.app.close()
        self.app = App(database=self.database); self.app.withdraw()
        page = self.app.pages['login']
        page.username.set('preview'); page.password.set('test-password'); page.authenticate('progress')
        self.assertEqual(self.app.current, 'progress')
        self.assertEqual(self.app.user['name'].get(), 'Preview')
        self.assertEqual(self.app.reminders['2026-11-02'], 'Saved reminder')
        self.app.show('accounting')
        self.assertEqual(self.app.pages['accounting'].metrics['Total'].cget('text'), '₹123.45')
        for route in ('bmi', 'fitness', 'sleep', 'cycle', 'nutrition', 'exercise', 'care'):
            self.app.show(route)
            self.assertEqual(self.app.pages[route].snapshot(), self.app.saved['pages'][route])
        self.assertEqual(self.app.pages['bmi'].weight.get(), '70')
        self.app.logout()
        second = self.app.store.sign_up('another', 'another-password')
        self.app.sign_in(second, 'progress')
        self.assertEqual(self.app.reminders, {})
        self.assertEqual(self.app.saved.get('pages'), {})
        self.app.show('accounting')
        self.assertEqual(self.app.pages['accounting'].metrics['Total'].cget('text'), '₹0.00')
        self.assertEqual(self.app.user['name'].get(), '')

    def test_failed_save_does_not_logout_or_close(self):
        self.app.user['name'].set('Keep my draft')
        with patch.object(self.app.store, 'save', side_effect=mysql.connector.OperationalError('server unavailable')), patch('app.messagebox.showerror'):
            self.app.logout()
            self.app.close()
            self.assertIsNotNone(self.app.user_id)
            self.assertEqual(self.app.user['name'].get(), 'Keep my draft')
            self.assertTrue(self.app.winfo_exists())

    def test_startup_database_error_is_explained(self):
        with patch('app.Store', side_effect=mysql.connector.DatabaseError('server unavailable')), patch('app.messagebox.showerror') as dialog:
            with self.assertRaises(mysql.connector.DatabaseError): App(database=self.database)
            self.assertIn('setup.sql', dialog.call_args.args[1])

    def test_edit_and_delete_reminder_after_login(self):
        self.app.reminders['2026-11-02'] = 'Original reminder'
        self.app.save_workspace(); self.app.logout()
        self.app.sign_in(self.app.store.log_in('preview', 'test-password'))
        self.app.show('calendar'); page = self.app.pages['calendar']
        page.select_date(date(2026, 11, 2))
        page.notes.delete('1.0', 'end'); page.notes.insert('1.0', 'Changed reminder')
        page.save_reminder()
        data, _ = self.app.store.load(self.app.user_id)
        self.assertEqual(data['reminders']['2026-11-02'], 'Changed reminder')
        page.notes.delete('1.0', 'end'); page.save_reminder()
        data, _ = self.app.store.load(self.app.user_id)
        self.assertNotIn('2026-11-02', data['reminders'])

    def test_signup_confirmation_and_empty_progress(self):
        self.app.logout(); self.app.show('signup')
        page = self.app.pages['signup']
        page.username.set('new-account'); page.password.set('new-password'); page.confirm.set('different')
        page.authenticate()
        self.assertIn('do not match', page.feedback.cget('text'))
        self.assertIsNone(self.app.user_id)
        page.confirm.set('new-password'); page.authenticate()
        self.assertEqual(self.app.current, 'welcome')
        self.app.show('progress')
        texts = [widget.cget('text') for widget in self.app.pages['progress'].progress_body.winfo_children() if widget.winfo_class() == 'Label']
        self.assertTrue(any('No inputs saved' in text for text in texts))

    def test_bmi_does_not_classify_teenagers(self):
        self.app.user['age'].set('17')
        self.app.show('bmi'); page = self.app.pages['bmi']
        page.weight.set('70'); page.height.set('175'); page.calculate_bmi()
        self.assertIn('20 and above', page.feedback.cget('text'))
        self.assertNotIn('Healthy weight range', page.feedback.cget('text'))

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
