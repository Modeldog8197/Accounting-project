"""Accounting and health app."""

import calendar
import math
import mysql.connector
import tkinter as tk
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
from tkinter import ttk, messagebox

from storage import Store
from reports import HEALTH_SECTIONS, METRICS, health_lines, metric_series, monthly_value, month_summary, week_start

BG, WHITE, INK, MUTED = '#F6F5F1', '#FFFFFF', '#20282E', '#52606B'
GREEN, SOFT, LINE, BLUE = '#244C66', '#E8EEF0', '#D4D8D7', '#BB793F'


def amount(text):
    """Read a finite, non-negative amount."""
    try:
        value = Decimal(text.strip().replace(',', '') or '0')
        if not value.is_finite() or value < 0:
            raise ValueError('Enter a non-negative amount.')
        return value
    except InvalidOperation as exc:
        raise ValueError('Enter a valid amount.') from exc


def number(text, label, minimum=0, maximum=None):
    try:
        value = float(text)
        if not math.isfinite(value) or value < minimum or (maximum is not None and value > maximum):
            raise ValueError
        return value
    except ValueError as exc:
        raise ValueError(f'Check {label.lower()} and enter a valid number.') from exc


def adult_age(text):
    if not text.strip().isdigit() or not 18 <= int(text.strip()) <= 120:
        raise ValueError('Enter your age in whole years (18–120).')
    return int(text.strip())


def label(parent, text, size=11, color=INK, bold=False, **kw):
    return tk.Label(parent, text=text, bg=parent.cget('bg'), fg=color,
                    font=('Segoe UI', size, 'bold' if bold else 'normal'), **kw)


def button(parent, text, command, primary=True):
    return tk.Button(parent, text=text, command=command, font=('Segoe UI', 10, 'bold'),
                     bg=GREEN if primary else SOFT, fg=WHITE if primary else GREEN,
                     activebackground='#125548' if primary else '#CDE7DD',
                     activeforeground=WHITE if primary else GREEN, bd=0,
                     padx=18, pady=11, cursor='hand2', takefocus=True)


def card(parent, title=None, subtitle=None):
    outer = tk.Frame(parent, bg=WHITE, highlightbackground=LINE, highlightthickness=1)
    inner = tk.Frame(outer, bg=WHITE)
    inner.pack(fill='both', expand=True, padx=24, pady=22)
    if title:
        label(inner, title, 15, bold=True).pack(anchor='w', pady=(0, 6))
    if subtitle:
        label(inner, subtitle, 10, MUTED, wraplength=450, justify='left').pack(anchor='w', pady=(0, 18))
    outer.content = inner
    return outer


def field(parent, caption, var):
    label(parent, caption, 10, bold=True).pack(anchor='w', pady=(12, 6))
    entry = ttk.Entry(parent, textvariable=var, style='Clean.TEntry', font=('Segoe UI', 11))
    entry.pack(fill='x')
    return entry


class App(tk.Tk):
    def __init__(self, initial='welcome', userdata=None, database=None):
        super().__init__()
        try:
            self.store = Store(database)
        except (mysql.connector.Error, ValueError) as exc:
            messagebox.showerror('MySQL setup',
                                 f'Could not open the database. Start MySQL, run setup.sql and check db_config.py.\n\n{exc}', parent=self)
            super().destroy()
            raise
        self.user_id, self.saved = None, {}
        self.initial = initial
        self.title('WellLedger | Accounting & Health')
        self.geometry('1120x800')
        self.minsize(880, 620)
        self.configure(bg=BG)
        self.history, self.pages, self.current = [], {}, None
        self.user = {key: tk.StringVar(self, value=(userdata or {}).get(key, ''))
                     for key in ('name', 'age', 'city', 'income')}
        self.reminders = {}
        self.clock_day = date.today()
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Clean.TEntry', padding=10, fieldbackground=WHITE,
                        foreground=INK, bordercolor=LINE, lightcolor=LINE, darkcolor=LINE)
        style.map('Clean.TEntry', bordercolor=[('focus', GREEN)])
        self.sidebar = tk.Frame(self, bg='#25313A', width=204)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)
        label(self.sidebar, 'WellLedger', 22, WHITE, True).pack(anchor='w', padx=24, pady=(34, 4))
        self.dateline = label(self.sidebar, date.today().strftime('%d %B %Y'), 10, '#CCD4D8')
        self.dateline.pack(anchor='w', padx=24, pady=(0, 24))
        self.nav = {}
        for key, caption in [('home', 'Overview'), ('accounting', 'Accounting'), ('health', 'Health & wellbeing'), ('calendar', 'Calendar'), ('reports', 'Monthly reports'), ('profile', 'Profile')]:
            btn = tk.Button(self.sidebar, text=caption, anchor='w', font=('Segoe UI', 11),
                            bg='#25313A', fg='#D7E8E1', activebackground='#3E5362',
                            activeforeground=WHITE, bd=0, padx=22, pady=14,
                            command=lambda k=key: self.navigate(k), cursor='hand2')
            btn.pack(fill='x', padx=12, pady=3)
            self.nav[key] = btn
        main = tk.Frame(self, bg=BG)
        main.pack(side='right', fill='both', expand=True)
        toolbar = tk.Frame(main, bg=WHITE, height=64)
        toolbar.pack(fill='x'); toolbar.pack_propagate(False)
        self.back_btn = button(toolbar, '← Back', self.back, False)
        self.back_btn.pack(side='left', padx=(24, 10), pady=10)
        button(toolbar, 'Home', self.home, False).pack(side='left', pady=10)
        self.logout_btn = button(toolbar, 'Log out', self.logout, False)
        self.logout_btn.pack(side='right', padx=(8, 24), pady=10)
        self.save_btn = button(toolbar, 'Save inputs', self.save_inputs, False)
        self.save_btn.pack(side='right', pady=10)
        self.canvas = tk.Canvas(main, bg=BG, bd=0, highlightthickness=0)
        scroll = ttk.Scrollbar(main, orient='vertical', command=self.canvas.yview)
        scroll.pack(side='right', fill='y'); self.canvas.pack(fill='both', expand=True)
        self.canvas.configure(yscrollcommand=scroll.set)
        self.host = tk.Frame(self.canvas, bg=BG)
        self.host_id = self.canvas.create_window((0, 0), window=self.host, anchor='nw')
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfigure(self.host_id, width=e.width))
        self.host.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.bind_all('<MouseWheel>', self.wheel)
        self.bind('<Alt-Left>', lambda e: self.back())
        self.bind('<Control-h>', lambda e: self.home())
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.show('login', remember=False)
        self.after(15000, self.check_day)

    def check_day(self):
        today = date.today()
        if today != self.clock_day:
            if self.save_workspace():
                old = self.clock_day
                self.clock_day = today
                self.dateline.configure(text=today.strftime('%d %B %Y'))
                if self.user_id is not None:
                    if self.expense_day == old:
                        self.expense_day = today
                    if self.sleep_week == week_start(old):
                        self.sleep_week = week_start(today)
                    for route, day in self.health_days.items():
                        if day == old:
                            self.health_days[route] = today
                    if self.current in HEALTH_SECTIONS or self.current in ('sleep', 'accounting', 'reports', 'calendar'):
                        self.pages[self.current].refresh()
        self.after(15000, self.check_day)

    def navigate(self, route):
        if self.user_id is not None and (route in HEALTH_SECTIONS or route in ('accounting', 'sleep')):
            self.open_day(route, date.today())
        else:
            self.show(route)

    def open_day(self, route, day):
        if self.current == route and not self.save_workspace():
            return
        if day > date.today():
            return
        if route in HEALTH_SECTIONS:
            self.health_days[route] = day
        elif route == 'accounting':
            self.expense_day = day
        else:
            self.sleep_week = week_start(day)
        if self.current == route:
            self.pages[route].refresh()
        else:
            self.show(route)

    def wheel(self, event):
        if self.host.winfo_height() > self.canvas.winfo_height():
            self.canvas.yview_scroll(-int(event.delta / 120), 'units')

    def show(self, route, remember=True):
        if self.user_id is None and route not in ('login', 'signup'):
            route = 'login'
        if self.user_id is not None and route not in ('profile', 'welcome'):
            try:
                adult_age(self.user['age'].get())
            except ValueError:
                route = 'welcome'
        if route == self.current:
            return
        if self.user_id is not None and not self.save_workspace():
            return
        if self.current:
            if self.current == 'calendar':
                self.pages[self.current].preserve_note()
            if remember: self.history.append(self.current)
            self.pages[self.current].pack_forget()
        if route not in self.pages:
            self.pages[route] = Page(self.host, self, route)
        self.current = route
        page = self.pages[route]
        page.pack(fill='both', expand=True)
        page.refresh()
        self.back_btn.configure(state='normal' if self.history else 'disabled')
        for btn in [self.save_btn, self.logout_btn, *self.nav.values()]:
            btn.configure(state='normal' if self.user_id is not None else 'disabled')
        section = 'health' if route in ('bmi', 'fitness', 'sleep', 'cycle', 'guides', 'nutrition', 'exercise', 'care') else route
        for key, btn in self.nav.items():
            btn.configure(bg='#3E5362' if key == section else '#25313A', fg=WHITE if key == section else '#D7E8E1')
        self.update_idletasks(); self.canvas.yview_moveto(0)
        self.title(f'WellLedger | {page.heading}')

    def back(self):
        if self.history: self.show(self.history.pop(), remember=False)

    def home(self):
        self.history.clear()
        if self.current == 'home': self.back_btn.configure(state='disabled')
        else: self.show('home', remember=False)

    def sign_in(self, user_id, destination='home'):
        # Load first to protect unreadable data.
        saved, _ = self.store.load(user_id)
        self.expense_log, self.nights = self.store.calendar_records(user_id)
        self.health_log = self.store.health_records(user_id)
        self.health_days = dict.fromkeys(HEALTH_SECTIONS, date.today())
        if not saved.get('cycle_dates_imported'):
            reminders = dict(saved.get('reminders', {}))
            for key, text in list(reminders.items()):
                prefix = 'Cycle: period start.'
                lines = text.splitlines()
                cycle_lines = [line for line in lines if line.startswith(prefix)]
                if not cycle_lines:
                    continue
                day = date.fromisoformat(key)
                if 'cycle' not in self.health_log.get(day, {}):
                    record = {'start': True}
                    notes = [line.removeprefix(prefix).strip() for line in cycle_lines]
                    if any(notes):
                        record['Notes'] = '\n'.join(dict.fromkeys(n for n in notes if n))
                    self.store.save_health(user_id, day, 'cycle', record)
                    self.health_log.setdefault(day, {})['cycle'] = record
                remaining = '\n'.join(line for line in lines if not line.startswith(prefix))
                if remaining.strip():
                    reminders[key] = remaining
                else:
                    reminders.pop(key)
            saved.update(reminders=reminders, cycle_dates_imported=True)
            self.store.save(user_id, saved)
        self.expense_day = date.today()
        self.sleep_week = week_start(date.today())
        self.reset_pages()
        self.user_id, self.saved = user_id, saved
        for key, var in self.user.items():
            var.set(saved.get('profile', {}).get(key, ''))
        self.reminders = dict(saved.get('reminders', {}))
        if destination == 'home' and not self.user['name'].get():
            destination = 'welcome'
        self.show(destination, remember=False)

    def save_workspace(self):
        if self.user_id is None:
            return True
        if self.current in ('accounting', 'sleep') and not self.pages[self.current].save_dated():
            return False
        if self.current == 'calendar':
            self.pages['calendar'].preserve_note()
        if self.current in HEALTH_SECTIONS and not self.pages[self.current].save_health_entry():
            return False
        data = dict(self.saved)
        data.update(profile={key: var.get() for key, var in self.user.items()}, reminders=dict(self.reminders))
        if data == self.saved:
            return True
        try:
            self.store.save(self.user_id, data)
        except mysql.connector.Error:
            messagebox.showerror('Could not save', 'Your inputs are still open. Check that MySQL is running and your account can save data, then try Save inputs again.', parent=self)
            return False
        self.saved = data
        return True

    def save_inputs(self):
        if self.current in ('welcome', 'profile'):
            self.pages[self.current].save_profile()
            return
        if self.save_workspace():
            messagebox.showinfo('Inputs saved', 'Your inputs are saved on this computer.', parent=self)

    def reset_pages(self):
        for widget in self.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
        for page in self.pages.values():
            page.destroy()
        self.pages, self.history, self.current = {}, [], None

    def logout(self):
        if not self.save_workspace():
            return
        self.reset_pages()
        self.user_id, self.saved, self.reminders = None, {}, {}
        for var in self.user.values():
            var.set('')
        self.show('login', remember=False)

    def close(self):
        if self.save_workspace():
            self.destroy()

    def destroy(self):
        if hasattr(self, 'store'):
            self.store.close()
        super().destroy()


class Page(tk.Frame):
    TITLES = {
        'login': 'WellLedger',
        'signup': 'Create an account',
        'progress': 'Your saved inputs',
        'welcome': 'Account details',
        'profile': 'Your profile',
        'home': 'Overview',
        'accounting': 'Expense overview',
        'health': 'Health & wellbeing',
        'bmi': 'Body measurements',
        'fitness': 'Activity check-in',
        'sleep': 'Your week of sleep',
        'cycle': 'Cycle tracking',
        'guides': 'Wellbeing notes',
        'nutrition': 'Diet & nutrition plan',
        'exercise': 'Exercise routine',
        'care': 'Care notes',
        'reports': 'Monthly reports',
        'calendar': 'Calendar',
    }

    def __init__(self, parent, app, route):
        super().__init__(parent, bg=BG, padx=30, pady=30)
        self.app, self.route = app, route
        self.heading = self.TITLES[route]
        label(self, self.heading, 25, bold=True).pack(anchor='w', pady=(0, 16))
        if route in HEALTH_SECTIONS:
            bar = tk.Frame(self, bg=BG)
            bar.pack(fill='x', pady=(0, 10))
            self.health_date_label = label(bar, '', 12, bold=True)
            self.health_date_label.pack(side='left')
            button(bar, 'Choose date', self.choose_health_date, False).pack(side='right')
        getattr(self, 'build_' + ('profile' if route == 'welcome' else route))()

    def refresh(self):
        if self.route in HEALTH_SECTIONS: self.load_health_entry()
        if self.route == 'progress': self.refresh_progress()
        if self.route == 'accounting': self.load_expenses()
        if self.route == 'sleep': self.load_week()
        if self.route == 'reports': self.refresh_reports()
        if self.route in ('welcome', 'profile'):
            for key, var in self.profile_vars.items():
                var.set(self.app.user[key].get())
        if self.route == 'home':
            self.greeting.configure(text=date.today().strftime('%B %Y'))
            totals = month_summary(self.app.expense_log, self.app.nights, date.today().strftime('%Y-%m'))
            everyday, healthcare, days, avg, nights = totals
            spending = f'₹{everyday+healthcare:,.2f} across {days} recorded days' if days else 'No expenses recorded'
            sleep = f'{avg:.1f} hours per night ({nights} recorded)' if nights else 'No nights recorded'
            self.month_status.configure(text=f'{spending}   ·   {sleep}')
        if self.route == 'calendar': self.render_month()
        if self.route == 'calendar': self.load_date()

    def build_login(self):
        self.build_auth(False)

    def build_signup(self):
        self.build_auth(True)

    def build_auth(self, signup):
        box = card(self, 'Sign up' if signup else 'Log in',
                   'Use a username and a password of at least 8 characters.' if signup else
                   'View progress also requires your username and password.')
        box.pack(fill='x')
        self.username, self.password, self.confirm = (tk.StringVar(self.app) for _ in range(3))
        field(box.content, 'Username', self.username).focus_set()
        field(box.content, 'Password', self.password).configure(show='•')
        if signup:
            field(box.content, 'Confirm password', self.confirm).configure(show='•')
        self.feedback = self.result(box.content)
        actions = tk.Frame(box.content, bg=WHITE); actions.pack(fill='x')
        button(actions, 'Create account' if signup else 'Log in', self.authenticate).pack(side='left')
        if not signup:
            button(actions, 'View progress', lambda: self.authenticate('progress'), False).pack(side='left', padx=10)
        button(box.content, 'Back to login' if signup else 'Create an account',
               lambda: self.switch_auth('login' if signup else 'signup'), False).pack(anchor='w', pady=(16, 0))

    def switch_auth(self, route):
        self.password.set(''); self.confirm.set('')
        self.app.show(route)

    def authenticate(self, destination=None):
        try:
            if self.route == 'signup':
                if self.password.get() != self.confirm.get():
                    raise ValueError('The passwords do not match.')
                user_id = self.app.store.sign_up(self.username.get(), self.password.get())
            else:
                user_id = self.app.store.log_in(self.username.get(), self.password.get())
            self.app.sign_in(user_id, destination or (self.app.initial if self.app.initial != 'welcome' else 'home'))
        except ValueError as exc:
            self.feedback.configure(text=str(exc), fg='#B42318')
        except mysql.connector.Error:
            self.feedback.configure(text='Could not open your account. Check MySQL and run setup.sql.', fg='#B42318')

    def build_progress(self):
        self.saved_time = label(self, '', 11, MUTED)
        self.saved_time.pack(anchor='w', pady=(0, 12))
        self.progress_body = tk.Frame(self, bg=BG); self.progress_body.pack(fill='x')
        button(self, 'Continue to overview', self.app.home).pack(anchor='e', pady=18)

    def refresh_progress(self):
        for widget in self.progress_body.winfo_children(): widget.destroy()
        try:
            data, saved_at = self.app.store.load(self.app.user_id)
        except (mysql.connector.Error, ValueError):
            self.saved_time.configure(text='Could not read saved inputs. Please try again.')
            return
        self.saved_time.configure(text=f'Last saved: {saved_at}' if saved_at else 'No saved inputs yet.')
        sections = [('Profile', data.get('profile', {}))]
        captions = {'name': 'Name', 'age': 'Age', 'city': 'City', 'income': 'Annual income (₹)',
                    'weight': 'Weight (kg)', 'height': 'Height (cm)', 'cycle_date': 'Period start date',
                    'cycle_note': 'Cycle note', 'plan': 'Notes'}
        for route, values in data.get('pages', {}).items():
            rows = {}
            for key, value in values.items():
                if isinstance(value, dict): rows.update(value)
                elif isinstance(value, list): rows.update({f'Night {i + 1} (hours)': v for i, v in enumerate(value)})
                else: rows[key] = value
            sections.append((('Undated inputs · ' if route in HEALTH_SECTIONS or route in ('accounting', 'sleep') else '') + self.TITLES[route], rows))
        sections.append(('Calendar reminders', data.get('reminders', {})))
        count = 0
        for title, rows in sections:
            lines = [f'{captions.get(key, key)}: {value}' for key, value in rows.items() if str(value).strip()]
            if not lines: continue
            count += 1
            box = card(self.progress_body, title); box.pack(fill='x', pady=(0, 12))
            label(box.content, '\n'.join(lines), 11, wraplength=500, justify='left').pack(anchor='w')
        if not count:
            label(self.progress_body, 'No inputs saved yet. Open a tool and enter your details.', wraplength=620).pack(anchor='w')
        label(self.progress_body, 'Values are shown as entered, including unfinished drafts.', 10, MUTED).pack(anchor='w')

    def result(self, parent):
        widget = label(parent, '', 11, GREEN, wraplength=500 if self.route in ('bmi', 'fitness', 'sleep') else 620, justify='left')
        widget.pack(anchor='w', pady=16)
        return widget

    def build_profile(self):
        box = card(self, 'Personal details', 'Enter your name and age (18 or older).')
        self.profile_vars = {k: tk.StringVar(self) for k in self.app.user}
        box.pack(fill='x')
        for key, caption in [('name', 'Full name'), ('age', 'Age'), ('city', 'City'), ('income', 'Annual income (₹)')]:
            field(box.content, caption, self.profile_vars[key])
        self.feedback = self.result(box.content)
        button(box.content, 'Continue to overview' if self.route == 'welcome' else 'Save profile', self.save_profile).pack(anchor='e')

    def save_profile(self):
        try:
            if not self.profile_vars['name'].get().strip():
                raise ValueError('Enter your name.')
            adult_age(self.profile_vars['age'].get())
            amount(self.profile_vars['income'].get())
        except ValueError as exc:
            self.feedback.configure(text=str(exc), fg='#B42318')
            return
        for key, var in self.profile_vars.items():
            self.app.user[key].set(var.get().strip())
        self.app.home()

    def tiles(self, items):
        grid = tk.Frame(self, bg=BG); grid.pack(fill='x')
        grid.columnconfigure((0, 1), weight=1, uniform='tile')
        for index, (title, route) in enumerate(items):
            row = tk.Frame(grid, bg=WHITE, padx=16, pady=11)
            row.grid(row=index, column=0, columnspan=2, sticky='ew', pady=(0, 2))
            button(row, title, lambda r=route: self.app.navigate(r), False).pack(side='left')

    def build_home(self):
        self.greeting = label(self, '', 16, GREEN, True); self.greeting.pack(anchor='w', pady=(0, 20))
        self.month_status = label(self, '', 11)
        self.month_status.pack(anchor='w', pady=(0, 16))
        self.tiles([('Monthly reports', 'reports'),
                    ('Accounting', 'accounting'),
                    ('Health', 'health'),
                    ('Calendar', 'calendar'),
                    ('Profile', 'profile')])
        button(self, 'View progress', lambda: self.app.show('progress'), False).pack(anchor='w')

    def build_accounting(self):
        self.expenses, self.metrics = {}, {}
        self.entry_heading = label(self, '', 15, bold=True)
        self.entry_heading.pack(anchor='w', pady=(0, 12))
        totals = tk.Frame(self, bg=BG); totals.pack(fill='x', pady=(0, 18))
        totals.columnconfigure((0, 1, 2), weight=1, uniform='total')
        for col, title in enumerate(('Everyday', 'Healthcare', 'Total')):
            box = card(totals, title)
            box.grid(row=0, column=col, sticky='ew', padx=4)
            self.metrics[title] = label(box.content, '₹0.00', 19, GREEN, True)
            self.metrics[title].pack(anchor='w')
        forms = tk.Frame(self, bg=BG); forms.pack(fill='x')
        forms.columnconfigure((0, 1), weight=1, uniform='form')
        groups = {'Everyday': ('Food & groceries', 'Transport', 'Entertainment', 'Other'),
                  'Healthcare': ('Medicines', 'Tests', 'Doctor visits', 'Other')}
        self.feedback = self.result(self)
        for col, (group, categories) in enumerate(groups.items()):
            box = card(forms, group); box.grid(row=0, column=col, sticky='nsew', padx=4)
            for category in categories:
                var = tk.StringVar(self.app)
                self.expenses[(group, category)] = var
                field(box.content, category + ' (₹)', var)
                var.trace_add('write', self.update_expenses)
        actions = tk.Frame(self, bg=BG); actions.pack(fill='x', pady=18)
        button(actions, 'View charts', self.charts).pack(side='right')
        button(actions, 'Save day', self.app.save_inputs, False).pack(side='right', padx=6)
        button(actions, 'Summary', self.summary, False).pack(side='right', padx=8)
        button(actions, 'Clear amounts', self.clear_expenses, False).pack(side='left')
        self.update_expenses()

    def expense_values(self):
        values = {key: amount(var.get()) for key, var in self.expenses.items()}
        for value in values.values():
            if value > Decimal('9999999999.99') or value != value.quantize(Decimal('.01')):
                raise ValueError('Use up to two decimal places and less than ₹10 billion per category.')
        return values

    def update_expenses(self, *_):
        try:
            values = self.expense_values()
            totals = {g: sum(v for (group, _), v in values.items() if group == g) for g in ('Everyday', 'Healthcare')}
            totals['Total'] = sum(totals.values())
            for key, value in totals.items(): self.metrics[key].configure(text=f'₹{value:,.2f}')
            self.feedback.configure(text='', fg=GREEN)
        except ValueError as exc:
            self.feedback.configure(text=str(exc), fg='#B42318')
            for widget in self.metrics.values(): widget.configure(text='—')

    def clear_expenses(self):
        if any(var.get() for var in self.expenses.values()) and not messagebox.askyesno('Clear amounts?', 'Clear all entered expense amounts?', parent=self.app): return
        for var in self.expenses.values(): var.set('')

    def summary(self):
        try: values = self.expense_values()
        except ValueError:
            self.update_expenses(); return
        total = sum(values.values())
        if not total:
            self.feedback.configure(text='Add an expense to create a summary.'); return
        largest, value = max(values.items(), key=lambda item: item[1])
        messagebox.showinfo('Spending summary', f'Total spending: ₹{total:,.2f}\nLargest category: {largest[0]} / {largest[1]}\n₹{value:,.2f} ({value / total:.0%} of your total)', parent=self.app)

    def charts(self):
        try: values = self.expense_values()
        except ValueError:
            self.update_expenses(); return
        items = [(f'{group} · {category}', float(v)) for (group, category), v in values.items() if v > 0]
        if not items:
            self.feedback.configure(text='Add an expense to view charts.'); return
        try:
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        except ImportError:
            self.feedback.configure(text='Charts need Matplotlib. Install the requirements to enable them.'); return
        win = tk.Toplevel(self.app); win.title('Spending insights'); win.geometry('950x580'); win.configure(bg=BG)
        button(win, 'Close charts', win.destroy, False).pack(anchor='e', padx=20, pady=12)
        fig = Figure(figsize=(9, 4.7), facecolor=BG)
        pie, bars = fig.subplots(1, 2)
        groups = [float(sum(v for (group, _), v in values.items() if group == g)) for g in ('Everyday', 'Healthcare')]
        pie.pie(groups, labels=['Everyday', 'Healthcare'], colors=[GREEN, BLUE], autopct='%1.0f%%', wedgeprops={'width': .4, 'edgecolor': BG})
        pie.set_title('Spending split')
        bars.barh([k for k, _ in items], [v for _, v in items], color=GREEN)
        bars.invert_yaxis(); bars.set_xlabel('Amount (INR)'); bars.set_title('By category')
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=win); canvas.draw(); canvas.get_tk_widget().pack(fill='both', expand=True)

    def build_health(self):
        self.tiles([('BMI', 'bmi'),
                    ('Activity', 'fitness'),
                    ('Sleep', 'sleep'),
                    ('Cycle tracking', 'cycle'),
                    ('Wellbeing notes', 'guides')])

    def build_bmi(self):
        box = card(self, 'Body measurements', 'BMI is a screening measure for adults, not a diagnosis. It is not suitable for children or pregnancy.')
        box.pack(fill='x')
        self.weight, self.height = tk.StringVar(self.app), tk.StringVar(self.app)
        field(box.content, 'Weight (kg)', self.weight); field(box.content, 'Height (cm)', self.height)
        self.feedback = self.result(box.content)
        button(box.content, 'Calculate BMI', self.calculate_bmi).pack(anchor='e')

    def calculate_bmi(self):
        try:
            age = self.app.user['age'].get().strip()
            age = adult_age(age)
            weight = number(self.weight.get(), 'weight', .1, 1000)
            height = number(self.height.get(), 'height', 30, 300)
            bmi = weight / (height / 100) ** 2
        except ValueError as exc:
            self.feedback.configure(text=str(exc), fg='#B42318'); return
        if age < 20:
            self.feedback.configure(text=f'BMI {bmi:.1f} kg/m². At ages 18–19, interpretation uses age-specific growth charts.', fg=GREEN)
            self.app.save_workspace()
            return
        category = 'Underweight' if bmi < 18.5 else 'Healthy weight range' if bmi < 25 else 'Overweight' if bmi < 30 else 'Obesity range'
        self.feedback.configure(text=f'BMI {bmi:.1f}  ·  {category}', fg=GREEN)
        self.app.save_workspace()

    def build_fitness(self):
        box = card(self, 'Activity check-in'); box.pack(fill='x')
        self.activity = {key: tk.StringVar(self.app) for key in ('Steps', 'Exercise (minutes)', 'Water (glasses)')}
        for key, var in self.activity.items(): field(box.content, key, var)
        self.feedback = self.result(box.content)
        button(box.content, 'Review check-in', self.review_activity).pack(anchor='e')

    def review_activity(self):
        try:
            values = {key: number(var.get(), key) for key, var in self.activity.items()}
            if not values['Steps'].is_integer(): raise ValueError('Steps must be a whole number.')
        except ValueError as exc:
            self.feedback.configure(text=str(exc), fg='#B42318'); return
        self.feedback.configure(text=f"Entered: {values['Steps']:,.0f} steps · {values['Exercise (minutes)']:g} minutes of exercise · {values['Water (glasses)']:g} glasses of water.", fg=GREEN)
        self.app.save_workspace()

    def load_expenses(self):
        day = self.app.expense_day
        self.entry_heading.configure(text=day.strftime('%A, %d %B %Y'))
        values = self.app.expense_log.get(day, {})
        for key, var in self.expenses.items():
            var.set(str(values.get(' / '.join(key), '')))

    def build_sleep(self):
        box = card(self, 'Sleep log', 'Use the date you woke up. Open an earlier week from Calendar.')
        box.pack(fill='x')
        self.week_heading = label(box.content, '', 13, bold=True)
        self.week_heading.pack(anchor='w')
        self.sleep_rows = []
        for i in range(7):
            row = tk.Frame(box.content, bg=WHITE)
            row.pack(fill='x', pady=3)
            caption = label(row, '', 11, width=24, anchor='w')
            caption.pack(side='left')
            var = tk.StringVar(self)
            entry = ttk.Entry(row, textvariable=var, width=8)
            entry.pack(side='left')
            label(row, 'hours', 10, MUTED).pack(side='left', padx=8)
            self.sleep_rows.append((caption, var, entry))
            var.trace_add('write', self.check_sleep)
        self.feedback = self.result(box.content)
        self.review_btn = button(box.content, 'Review sleep', self.review_sleep)
        self.review_btn.pack(side='right')
        button(box.content, 'Save nights', self.app.save_inputs, False).pack(side='left')

    def load_week(self):
        start = self.app.sleep_week
        self.week_heading.configure(text='Week of ' + start.strftime('%d %B %Y'))
        self.sleep_days = [start + timedelta(days=i) for i in range(7)]
        self.week_filed = all(self.app.nights.get(d, (None, False))[1] for d in self.sleep_days)
        self.loading_week = True
        for day, (caption, var, entry) in zip(self.sleep_days, self.sleep_rows):
            caption.configure(text=day.strftime('%a, %d %b %Y'))
            hours, reviewed = self.app.nights.get(day, (None, False))
            var.set('' if reviewed or hours is None else str(hours))
            entry.configure(state='disabled' if reviewed or day > date.today() else 'normal')
        self.loading_week = False
        self.check_sleep()

    def sleep_values(self):
        values = {}
        for day, (_, var, _) in zip(self.sleep_days, self.sleep_rows):
            if day > date.today() or self.app.nights.get(day, (None, False))[1]:
                continue
            value = var.get().strip()
            if value:
                number(value, 'sleep hours (0–24)', 0, 24)
                hours = Decimal(value)
                if hours != hours.quantize(Decimal('.01')):
                    raise ValueError('Use at most two decimal places for hours.')
                values[day] = hours
            else:
                values[day] = None
        return values

    def check_sleep(self, *_):
        if getattr(self, 'loading_week', True):
            return
        count = 0
        try:
            count = sum(v is not None for v in self.sleep_values().values())
            message = 'Week filed in Calendar.' if self.week_filed else f'{count} of 7 nights entered'
        except (ValueError, InvalidOperation) as exc:
            message = str(exc)
        self.review_btn.configure(state='normal' if count == 7 else 'disabled')
        self.feedback.configure(text=message)

    def save_dated(self, review=False):
        try:
            if self.route == 'accounting':
                day = self.app.expense_day
                values = {' / '.join(k): v for k, v in self.expense_values().items() if self.expenses[k].get().strip()}
                if values != self.app.expense_log.get(day, {}):
                    self.app.store.save_expenses(self.app.user_id, day, values)
                    if values:
                        self.app.expense_log[day] = values
                    else:
                        self.app.expense_log.pop(day, None)
            else:
                values = self.sleep_values()
                if review and (len(values) != 7 or None in values.values()):
                    raise ValueError('Enter all seven nights before reviewing.')
                changes = {d: v for d, v in values.items() if review or v != self.app.nights.get(d, (None, False))[0]}
                if changes:
                    self.app.store.save_nights(self.app.user_id, changes, review)
                    for day, hours in changes.items():
                        if hours is None:
                            self.app.nights.pop(day, None)
                        else:
                            self.app.nights[day] = (hours, review)
            return True
        except (ValueError, InvalidOperation, mysql.connector.Error) as exc:
            messagebox.showerror('Could not save entry', str(exc), parent=self.app)
            return False

    def review_sleep(self):
        if self.save_dated(review=True):
            hours = [self.app.nights[d][0] for d in self.sleep_days]
            self.load_week()
            self.feedback.configure(text=f'Filed in Calendar. Average {sum(hours)/7:.1f} h · Range {min(hours):g}–{max(hours):g} h.')

    def build_cycle(self):
        box = card(self, 'Record a cycle date'); box.pack(fill='x')
        self.period_start = tk.BooleanVar(self)
        tk.Checkbutton(box.content, text='Period started on this date', variable=self.period_start, bg=WHITE).pack(anchor='w')
        self.cycle_note = tk.StringVar(self)
        field(box.content, 'Notes', self.cycle_note)
        self.feedback = self.result(box.content)
        button(box.content, 'Save cycle entry', self.save_notes).pack(anchor='e')

    def build_guides(self):
        self.tiles([('Diet & nutrition', 'nutrition'),
                    ('Exercise routine', 'exercise'),
                    ('Care notes', 'care')])
        button(self, 'Plan a reminder', lambda: self.app.show('calendar'), False).pack(anchor='e', pady=18)

    def build_nutrition(self):
        self.build_notes('My meal plan')

    def build_exercise(self):
        self.build_notes('My activity plan')

    def build_care(self):
        self.build_notes('Appointment preparation')

    def build_notes(self, title):
        box = card(self, title); box.pack(fill='x')
        if self.route == 'nutrition':
            self.meals = tk.StringVar(self)
            field(box.content, 'Meals eaten (optional)', self.meals)
        self.plan = tk.Text(box.content, height=13, font=('Segoe UI', 11), wrap='word', bg=BG, fg=INK, relief='flat', padx=14, pady=14)
        self.plan.pack(fill='x')
        self.feedback = self.result(box.content)
        button(box.content, 'Save notes', self.save_notes).pack(anchor='e')
        button(self, 'Plan a reminder', lambda: self.app.show('calendar'), False).pack(anchor='e', pady=18)

    def save_notes(self):
        if self.app.save_workspace(): self.feedback.configure(text='Saved to calendar.', fg=GREEN)

    def choose_health_date(self):
        day = self.app.health_days[self.route]
        self.app.show('calendar')
        if self.app.current == 'calendar':
            cal = self.app.pages['calendar']
            cal.month = day.replace(day=1)
            cal.select_date(day)

    def load_health_entry(self):
        day = self.app.health_days[self.route]
        self.health_date_label.configure(text=day.strftime('%A, %d %B %Y'))
        data = self.app.health_log.get(day, {}).get(self.route, {})
        if self.route == 'bmi':
            self.weight.set(data.get('Weight (kg)', ''))
            self.height.set(data.get('Height (cm)', ''))
        elif self.route == 'fitness':
            for key, var in self.activity.items():
                var.set(data.get(key, ''))
        elif self.route == 'cycle':
            self.period_start.set(data.get('start', False))
            self.cycle_note.set(data.get('Notes', ''))
        else:
            if self.route == 'nutrition':
                self.meals.set(data.get('Meals', ''))
            self.plan.delete('1.0', 'end')
            self.plan.insert('1.0', data.get('Notes', ''))
        self.feedback.configure(text='')

    def save_health_entry(self):
        day = self.app.health_days[self.route]
        record = {}
        try:
            fields = []
            if self.route == 'bmi':
                fields = [('Weight (kg)', self.weight, .1, 1000), ('Height (cm)', self.height, 30, 300)]
            elif self.route == 'fitness':
                fields = [(key, var, 0, None) for key, var in self.activity.items()]
            elif self.route == 'nutrition':
                fields = [('Meals', self.meals, 0, None)]
            for key, var, low, high in fields:
                if var.get().strip():
                    value = number(var.get(), key, low, high)
                    if key in ('Steps', 'Meals') and not value.is_integer():
                        raise ValueError(f'{key} must be a whole number.')
                    record[key] = int(value) if value.is_integer() else value
            if self.route == 'cycle' and self.period_start.get():
                record['start'] = True
            note = self.cycle_note.get() if self.route == 'cycle' else ''
            if hasattr(self, 'plan'):
                note = self.plan.get('1.0', 'end-1c')
            if note.strip():
                record['Notes'] = note.strip()
            if record == self.app.health_log.get(day, {}).get(self.route, {}):
                return True
            self.app.store.save_health(self.app.user_id, day, self.route, record)
        except (ValueError, mysql.connector.Error) as exc:
            messagebox.showerror('Could not save health entry', str(exc), parent=self.app)
            return False
        if record:
            self.app.health_log.setdefault(day, {})[self.route] = record
        else:
            entries = self.app.health_log.get(day, {})
            entries.pop(self.route, None)
            if not entries:
                self.app.health_log.pop(day, None)
        return True

    def build_reports(self):
        controls = tk.Frame(self, bg=BG)
        controls.pack(fill='x')
        current = date.today().replace(day=1)
        self.month_picks = []
        for title, day in [('Month', current), ('Compare with', current - timedelta(days=1))]:
            label(controls, title, 10, bold=True).pack(side='left', padx=(0, 6))
            pick = ttk.Combobox(controls, width=10, state='readonly')
            pick.set(day.strftime('%Y-%m'))
            pick.pack(side='left', padx=(0, 18))
            pick.bind('<<ComboboxSelected>>', lambda _: self.refresh_reports())
            self.month_picks.append(pick)
        self.metric = ttk.Combobox(self, values=['Spending and sleep', *METRICS], state='readonly', width=24)
        self.metric.set('Spending and sleep')
        self.metric.pack(anchor='w')
        self.metric.bind('<<ComboboxSelected>>', lambda _: self.refresh_reports())
        self.report_text = label(self, '', 11, justify='left')
        self.report_text.pack(anchor='w', pady=16)
        self.plot_area = tk.Frame(self, bg=WHITE)
        self.plot_area.pack(fill='both', expand=True)

    def refresh_reports(self):
        months = [p.get() for p in self.month_picks]
        available = set(months)
        for day in [date.today(), *self.app.expense_log, *self.app.nights, *self.app.health_log]:
            available.add(day.strftime('%Y-%m'))
        for pick in self.month_picks:
            pick.configure(values=sorted(available, reverse=True))
        if self.metric.get() in METRICS:
            self.health_report(months)
            return
        stats = [month_summary(self.app.expense_log, self.app.nights, m) for m in months]
        lines = []
        for month, (everyday, health, days, avg, nights) in zip(months, stats):
            spending = f'₹{everyday+health:,.2f} on {days} recorded days' if days else 'No expenses recorded'
            sleep = f'{avg:.1f} h/night across {nights} nights' if nights else 'No sleep recorded'
            lines.append(f'{month}     {spending}     ·     {sleep}')
        self.report_text.configure(text='\n'.join(lines))
        for w in self.plot_area.winfo_children():
            w.destroy()
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        fig = Figure(figsize=(8, 3.8), facecolor=WHITE, constrained_layout=True)
        spending, sleep = fig.subplots(1, 2)
        for i, (everyday, health, days, avg, nights) in enumerate(stats):
            if days:
                spending.bar(i, float(everyday), .52, color=GREEN)
                spending.bar(i, float(health), .52, bottom=float(everyday), color=BLUE)
            if nights:
                sleep.bar(i, float(avg), .52, color=GREEN)
            for axis, count in [(spending, days), (sleep, nights)]:
                if not count:
                    axis.text(i, 0.04, 'No entries', ha='center', transform=axis.get_xaxis_transform(), color=MUTED)
        from matplotlib.patches import Patch
        spending.legend(handles=[Patch(color=GREEN, label='Everyday'), Patch(color=BLUE, label='Healthcare')], fontsize=8)
        for axis, title, unit in [(spending, 'Recorded spending', 'INR'), (sleep, 'Average sleep', 'Hours per night')]:
            axis.set_title(title, loc='left')
            axis.set_ylabel(unit)
            axis.set_xlim(-.6, 1.6)
            axis.set_ylim(bottom=0, top=max(1, axis.get_ylim()[1]))
            axis.set_xticks([0, 1], months)
            axis.spines[['top', 'right']].set_visible(False)
        canvas = FigureCanvasTkAgg(fig, master=self.plot_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def health_report(self, months):
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        metric = self.metric.get()
        section, field, unit = METRICS[metric]
        series = metric_series(self.app.health_log, metric)
        count = field in ('Notes', 'start')
        trend_months = []
        end = date.fromisoformat(max(months) + '-01')
        for _ in range(6):
            trend_months.insert(0, end.strftime('%Y-%m'))
            end = (end - timedelta(days=1)).replace(day=1)
        for w in self.plot_area.winfo_children():
            w.destroy()
        fig = Figure(figsize=(8, 3.8), facecolor=WHITE, constrained_layout=True)
        comparison, trend = fig.subplots(1, 2)
        lines = []
        for i, month in enumerate(months):
            value, n = monthly_value(series, month, count)
            if n:
                comparison.bar(i, value, .5, color=[GREEN, BLUE][i])
                lines.append(f'{month}   {value:.2f} {unit}   ({n} records)')
            else:
                lines.append(f'{month}   No records')
        self.report_text.configure(text='\n'.join(lines))
        comparison.set_xticks([0, 1], months)
        comparison.set_xlim(-.6, 1.6)
        comparison.set_title(metric if count else 'Average · ' + metric)
        points = [monthly_value(series, m, count)[0] for m in trend_months]
        trend.plot(range(6), [v if v is not None else float('nan') for v in points], 'o-', color=GREEN)
        trend.set_xticks(range(6), trend_months, rotation=35, ha='right')
        trend.set_title('Six months')
        for axis in (comparison, trend):
            axis.set_ylabel(unit)
            axis.set_ylim(bottom=0, top=max(1, axis.get_ylim()[1]))
        canvas = FigureCanvasTkAgg(fig, master=self.plot_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        if field == 'Notes':
            for month in dict.fromkeys(months):
                for day in sorted(series, reverse=True):
                    if day.strftime('%Y-%m') == month:
                        note = self.app.health_log[day][section]['Notes']
                        label(self.plot_area, f'{day}   {note}', 10, wraplength=650, justify='left').pack(anchor='w')

    def build_calendar(self):
        self.selected = date.today(); self.month = self.selected.replace(day=1)
        controls = tk.Frame(self, bg=BG); controls.pack(fill='x', pady=(0, 16))
        button(controls, '‹ Previous', lambda: self.change_month(-1), False).pack(side='left')
        self.month_title = label(controls, '', 16, bold=True); self.month_title.pack(side='left', padx=18)
        button(controls, 'Next ›', lambda: self.change_month(1), False).pack(side='left')
        button(controls, 'Today', self.today, False).pack(side='right')
        self.calendar_box = card(self); self.calendar_box.pack(fill='x')
        box = card(self, 'Day record', 'A dot marks a day with an entry.'); box.pack(fill='x', pady=18)
        self.date_title = label(box.content, '', 14, GREEN, True); self.date_title.pack(anchor='w', pady=(0, 12))
        self.day_record = label(box.content, '', 11, justify='left')
        self.day_record.pack(anchor='w', pady=8)
        links = tk.Frame(box.content, bg=WHITE)
        links.pack(anchor='w')
        self.day_links = []
        for title, route in [('Edit expenses', 'accounting'), ('Open sleep week', 'sleep')]:
            btn = button(links, title, lambda r=route: self.app.open_day(r, self.selected), False)
            btn.pack(side='left', padx=(0, 8))
            self.day_links.append(btn)
        health_links = tk.Frame(box.content, bg=WHITE)
        health_links.pack(anchor='w', pady=6)
        for i, (route, title) in enumerate(HEALTH_SECTIONS.items()):
            btn = button(health_links, title, lambda r=route: self.app.open_day(r, self.selected), False)
            btn.grid(row=i // 3, column=i % 3, sticky='ew', padx=2, pady=2)
            self.day_links.append(btn)
        label(box.content, 'Reminder', 10, bold=True).pack(anchor='w', pady=(10, 2))
        self.notes = tk.Text(box.content, height=5, font=('Segoe UI', 11), wrap='word', bg=BG, fg=INK, relief='flat', padx=12, pady=12)
        self.notes.pack(fill='x')
        self.notes.bind('<<Modified>>', self.note_changed)
        actions = tk.Frame(box.content, bg=WHITE); actions.pack(fill='x', pady=(14, 0))
        button(actions, 'Save reminder', self.save_reminder).pack(side='right')
        self.feedback = self.result(box.content)
        self.dirty = False; self.load_date()

    def note_changed(self, _=None):
        if self.notes.edit_modified():
            self.dirty = True
            self.notes.edit_modified(False)

    def preserve_note(self):
        # Keep drafts between pages.
        content = self.notes.get('1.0', 'end').strip()
        key = self.selected.isoformat()
        if content: self.app.reminders[key] = content
        else: self.app.reminders.pop(key, None)
        self.dirty = False

    def load_date(self):
        self.date_title.configure(text=self.selected.strftime('%A, %d %B %Y'))
        rows = []
        expenses = self.app.expense_log.get(self.selected, {})
        for key, value in expenses.items():
            rows.append(f'{key}: ₹{value:,.2f}')
        if expenses:
            rows.append(f'Total: ₹{sum(expenses.values()):,.2f}')
        if self.selected in self.app.nights:
            rows.append(f'Sleep: {self.app.nights[self.selected][0]:g} hours')
        for section, data in self.app.health_log.get(self.selected, {}).items():
            rows.append(HEALTH_SECTIONS[section] + ' · ' + ' · '.join(health_lines(section, data)))
        self.day_record.configure(text='\n'.join(rows) or 'No entries recorded.', wraplength=650)
        for btn in self.day_links:
            btn.configure(state='normal' if self.selected <= date.today() else 'disabled')
        self.notes.delete('1.0', 'end'); self.notes.insert('1.0', self.app.reminders.get(self.selected.isoformat(), ''))
        self.notes.edit_modified(False); self.dirty = False

    def render_month(self):
        if getattr(self, 'dirty', False): self.preserve_note()
        parent = self.calendar_box.content
        for widget in parent.winfo_children(): widget.destroy()
        self.month_title.configure(text=self.month.strftime('%B %Y'))
        for col, text in enumerate(('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN')):
            parent.columnconfigure(col, weight=1, uniform='day')
            label(parent, text, 9, MUTED, True).grid(row=0, column=col, pady=(0, 8))
        for row, week in enumerate(calendar.monthcalendar(self.month.year, self.month.month), 1):
            for col, day in enumerate(week):
                if not day: continue
                value = self.month.replace(day=day)
                text = f"{day}{' •' if value.isoformat() in self.app.reminders or value in self.app.nights or value in self.app.expense_log or value in self.app.health_log else ''}"
                btn = button(parent, text, lambda d=value: self.select_date(d), value == self.selected)
                btn.grid(row=row, column=col, sticky='ew', padx=3, pady=3)

    def select_date(self, value):
        self.preserve_note(); self.selected = value; self.load_date(); self.render_month()

    def change_month(self, direction):
        value = (self.month + timedelta(days=32)).replace(day=1) if direction > 0 else (self.month - timedelta(days=1)).replace(day=1)
        self.month = value; self.select_date(value)

    def today(self):
        self.month = date.today().replace(day=1); self.select_date(date.today())

    def save_reminder(self):
        self.preserve_note(); self.render_month()
        if self.app.save_workspace(): self.feedback.configure(text='Reminder saved.', fg=GREEN)


def launch(route='welcome', userdata=None):
    try:
        app = App(route, userdata)
    except (mysql.connector.Error, ValueError):
        return  # Setup error shown above.
    app.mainloop()


if __name__ == '__main__':
    launch()
