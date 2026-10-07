"""Accounting and health tools in one navigable desktop window."""

import calendar
import math
import tkinter as tk
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
from tkinter import ttk, messagebox

BG, WHITE, INK, MUTED = '#F4F7FA', '#FFFFFF', '#172B35', '#627580'
GREEN, SOFT, LINE, BLUE = '#176B5B', '#E4F3ED', '#DDE5E8', '#5667C8'


def amount(text):
    """Parse currency without accepting infinity, NaN or negatives."""
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
    def __init__(self, initial='welcome', userdata=None):
        super().__init__()
        self.title('WellLedger | Accounting & Health')
        self.geometry('1120x800')
        self.minsize(880, 620)
        self.configure(bg=BG)
        self.history, self.pages, self.current = [], {}, None
        self.user = {key: tk.StringVar(self, value=(userdata or {}).get(key, ''))
                     for key in ('name', 'age', 'city', 'income')}
        self.reminders = {}
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Clean.TEntry', padding=10, fieldbackground=WHITE,
                        foreground=INK, bordercolor=LINE, lightcolor=LINE, darkcolor=LINE)
        style.map('Clean.TEntry', bordercolor=[('focus', GREEN)])
        self.sidebar = tk.Frame(self, bg='#143C35', width=204)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)
        label(self.sidebar, 'WellLedger', 22, WHITE, True).pack(anchor='w', padx=24, pady=(34, 4))
        label(self.sidebar, 'MONEY & WELLBEING', 8, '#AFCCC3').pack(anchor='w', padx=24, pady=(0, 36))
        self.nav = {}
        for key, caption in [('home', 'Overview'), ('accounting', 'Accounting'), ('health', 'Health & wellbeing'), ('calendar', 'Calendar'), ('profile', 'Your profile')]:
            btn = tk.Button(self.sidebar, text=caption, anchor='w', font=('Segoe UI', 11),
                            bg='#143C35', fg='#D7E8E1', activebackground='#27574B',
                            activeforeground=WHITE, bd=0, padx=22, pady=14,
                            command=lambda k=key: self.show(k), cursor='hand2')
            btn.pack(fill='x', padx=12, pady=3)
            self.nav[key] = btn
        label(self.sidebar, 'Private by default\nData stays in this session.', 9, '#AFCCC3', justify='left').pack(side='bottom', anchor='w', padx=24, pady=28)
        main = tk.Frame(self, bg=BG)
        main.pack(side='right', fill='both', expand=True)
        toolbar = tk.Frame(main, bg=WHITE, height=64)
        toolbar.pack(fill='x'); toolbar.pack_propagate(False)
        self.back_btn = button(toolbar, '← Back', self.back, False)
        self.back_btn.pack(side='left', padx=(24, 10), pady=10)
        button(toolbar, 'Home', self.home, False).pack(side='left', pady=10)
        label(toolbar, 'Accounting & Health', 10, MUTED).pack(side='right', padx=24)
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
        self.show(initial, remember=False)

    def wheel(self, event):
        if self.host.winfo_height() > self.canvas.winfo_height():
            self.canvas.yview_scroll(-int(event.delta / 120), 'units')

    def show(self, route, remember=True):
        if route == self.current:
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
        section = 'health' if route in ('bmi', 'fitness', 'sleep', 'cycle', 'guides', 'nutrition', 'exercise', 'care') else route
        for key, btn in self.nav.items():
            btn.configure(bg='#27574B' if key == section else '#143C35', fg=WHITE if key == section else '#D7E8E1')
        self.update_idletasks(); self.canvas.yview_moveto(0)
        self.title(f'WellLedger | {page.heading}')

    def back(self):
        if self.history: self.show(self.history.pop(), remember=False)

    def home(self):
        self.history.clear()
        if self.current == 'home': self.back_btn.configure(state='disabled')
        else: self.show('home', remember=False)


class Page(tk.Frame):
    TITLES = {
        'welcome': ('A little more balance.', 'One place for your expenses, wellbeing, and everyday plans.'),
        'profile': ('Your profile', 'Update your details without losing your progress.'),
        'home': ('Your everyday overview', 'Small steps toward a clearer picture of your money and wellbeing.'),
        'accounting': ('Expense overview', 'Track your spending with a simple, live breakdown.'),
        'health': ('Health & wellbeing', 'Choose a tool for your next check-in.'),
        'bmi': ('Body measurements', 'Calculate adult BMI from your height and weight.'),
        'fitness': ('Activity check-in', 'Keep a record of movement, exercise, and hydration.'),
        'sleep': ('Your week of sleep', 'Record seven nights and see your average.'),
        'cycle': ('Cycle tracking', 'Record dates and notes in your personal calendar.'),
        'guides': ('Wellbeing notes', 'A space for your diet, exercise, and care plans.'),
        'nutrition': ('Diet & nutrition plan', 'Keep your meal plans and dietary notes together.'),
        'exercise': ('Exercise routine', 'Organize your activity plan for the week.'),
        'care': ('Care notes', 'Prepare questions and notes for your next appointment.'),
        'calendar': ('Calendar & reminders', 'Plan your next appointment, payment, or personal reminder.')}

    def __init__(self, parent, app, route):
        super().__init__(parent, bg=BG, padx=30, pady=30)
        self.app, self.route = app, route
        self.heading, subtitle = self.TITLES[route]
        label(self, self.heading, 25, bold=True).pack(anchor='w')
        label(self, subtitle, 11, MUTED, wraplength=690, justify='left').pack(anchor='w', pady=(7, 24))
        getattr(self, 'build_' + ('profile' if route == 'welcome' else route))()

    def refresh(self):
        if self.route == 'home':
            name = self.app.user['name'].get().strip().split()
            self.greeting.configure(text=f"Welcome back, {name[0]}" if name else 'Welcome to WellLedger')
        if self.route == 'calendar': self.render_month()
        if self.route == 'calendar': self.load_date()

    def result(self, parent):
        widget = label(parent, '', 11, GREEN, wraplength=620, justify='left')
        widget.pack(anchor='w', pady=16)
        return widget

    def build_profile(self):
        box = card(self, 'Let’s get to know you' if self.route == 'welcome' else 'Personal details', 'Your name is required. Other details are optional.')
        box.pack(fill='x')
        for key, caption in [('name', 'Full name'), ('age', 'Age'), ('city', 'City'), ('income', 'Annual income (₹)')]:
            field(box.content, caption, self.app.user[key])
        self.feedback = self.result(box.content)
        button(box.content, 'Continue to overview' if self.route == 'welcome' else 'Save profile', self.save_profile).pack(anchor='e')

    def save_profile(self):
        try:
            if not self.app.user['name'].get().strip(): raise ValueError('Please add your name.')
            age = self.app.user['age'].get().strip()
            if age:
                value = number(age, 'age', 1, 120)
                if not value.is_integer(): raise ValueError('Age must be a whole number.')
            amount(self.app.user['income'].get())
        except ValueError as exc:
            self.feedback.configure(text=str(exc), fg='#B42318'); return
        self.app.home()

    def tiles(self, items):
        grid = tk.Frame(self, bg=BG); grid.pack(fill='x')
        grid.columnconfigure((0, 1), weight=1, uniform='tile')
        for index, (title, text, route) in enumerate(items):
            box = card(grid, title, text)
            box.grid(row=index // 2, column=index % 2, sticky='nsew', padx=(0, 8) if index % 2 == 0 else (8, 0), pady=(0, 16))
            button(box.content, 'Open ' + title.lower(), lambda r=route: self.app.show(r), False).pack(anchor='w', pady=(5, 0))

    def build_home(self):
        self.greeting = label(self, '', 16, GREEN, True); self.greeting.pack(anchor='w', pady=(0, 20))
        self.tiles([('Accounting', 'Everyday costs, healthcare spending, charts and summaries.', 'accounting'),
                    ('Health', 'Body metrics, activity, sleep, and cycle tracking.', 'health'),
                    ('Calendar', 'Keep important dates and reminders close at hand.', 'calendar'),
                    ('Profile', 'Review or edit your personal details.', 'profile')])
        label(self, 'Your entries are retained as you move between pages. Closing the app clears this session.', 10, MUTED, wraplength=680, justify='left').pack(anchor='w', pady=8)

    def build_accounting(self):
        self.expenses, self.metrics = {}, {}
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
        button(actions, 'Summary', self.summary, False).pack(side='right', padx=8)
        button(actions, 'Clear amounts', self.clear_expenses, False).pack(side='left')
        self.update_expenses()

    def expense_values(self):
        return {key: amount(var.get()) for key, var in self.expenses.items()}

    def update_expenses(self, *_):
        try:
            values = self.expense_values()
            totals = {g: sum(v for (group, _), v in values.items() if group == g) for g in ('Everyday', 'Healthcare')}
            totals['Total'] = sum(totals.values())
            for key, value in totals.items(): self.metrics[key].configure(text=f'₹{value:,.2f}')
            self.feedback.configure(text='Totals update automatically. Amounts stay here as you navigate.', fg=GREEN)
        except ValueError:
            self.feedback.configure(text='Check your amounts. Use non-negative numbers only.', fg='#B42318')
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
        self.tiles([('BMI', 'Calculate your adult body mass index.', 'bmi'),
                    ('Activity', 'Log steps, exercise minutes, and water intake.', 'fitness'),
                    ('Sleep', 'Record seven nights and compare your sleep.', 'sleep'),
                    ('Cycle tracking', 'Record period dates and personal notes.', 'cycle'),
                    ('Wellbeing notes', 'Keep your diet, exercise, and care plans.', 'guides')])

    def build_bmi(self):
        box = card(self, 'Body measurements', 'BMI is a screening measure for adults, not a diagnosis. It is not suitable for children or pregnancy.')
        box.pack(fill='x')
        self.weight, self.height = tk.StringVar(self.app), tk.StringVar(self.app)
        field(box.content, 'Weight (kg)', self.weight); field(box.content, 'Height (cm)', self.height)
        self.feedback = self.result(box.content)
        button(box.content, 'Calculate BMI', self.calculate_bmi).pack(anchor='e')

    def calculate_bmi(self):
        try:
            weight = number(self.weight.get(), 'weight', .1, 1000)
            height = number(self.height.get(), 'height', 30, 300)
            bmi = weight / (height / 100) ** 2
        except ValueError as exc:
            self.feedback.configure(text=str(exc), fg='#B42318'); return
        category = 'Underweight' if bmi < 18.5 else 'Healthy weight range' if bmi < 25 else 'Overweight' if bmi < 30 else 'Obesity range'
        self.feedback.configure(text=f'BMI {bmi:.1f}  ·  {category}\nDiscuss questions about your measurements with a healthcare professional.', fg=GREEN)

    def build_fitness(self):
        box = card(self, 'Today’s activity', 'Keep a simple record of your daily habits.'); box.pack(fill='x')
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
        self.feedback.configure(text=f"Today: {values['Steps']:,.0f} steps · {values['Exercise (minutes)']:g} minutes of exercise · {values['Water (glasses)']:g} glasses of water.\nYour check-in stays available throughout this session.", fg=GREEN)

    def build_sleep(self):
        box = card(self, 'Seven-night sleep log', 'Enter hours slept for each night, from oldest to most recent.'); box.pack(fill='x')
        self.sleep_vars = [tk.StringVar(self.app) for _ in range(7)]
        for i, var in enumerate(self.sleep_vars): field(box.content, f'Night {i + 1} (hours)', var)
        self.feedback = self.result(box.content)
        button(box.content, 'Review sleep', self.review_sleep).pack(anchor='e')

    def review_sleep(self):
        try: values = [number(v.get(), 'sleep hours', 0, 24) for v in self.sleep_vars]
        except ValueError as exc:
            self.feedback.configure(text=str(exc), fg='#B42318'); return
        self.feedback.configure(text=f'Average: {sum(values) / 7:.1f} hours per night\nShortest: {min(values):g} hours · Longest: {max(values):g} hours', fg=GREEN)

    def build_cycle(self):
        box = card(self, 'Record a cycle date', 'Keep a personal record. This tool does not predict fertility or provide contraceptive guidance.'); box.pack(fill='x')
        self.cycle_date = tk.StringVar(self.app, date.today().isoformat())
        self.cycle_note = tk.StringVar(self.app)
        field(box.content, 'Period start date (YYYY-MM-DD)', self.cycle_date)
        field(box.content, 'Notes (optional)', self.cycle_note)
        self.feedback = self.result(box.content)
        button(box.content, 'Add to calendar', self.save_cycle).pack(anchor='e')

    def save_cycle(self):
        try: value = date.fromisoformat(self.cycle_date.get().strip())
        except ValueError:
            self.feedback.configure(text='Use a date like 2026-10-07.', fg='#B42318'); return
        key = value.isoformat()
        existing = self.app.reminders.get(key, '')
        self.app.reminders[key] = (existing + '\nCycle: period start. ' + self.cycle_note.get().strip()).strip()
        self.feedback.configure(text='Added to your calendar for this session.', fg=GREEN)

    def build_guides(self):
        self.tiles([('Diet & nutrition', 'Plan meals and keep personal dietary notes.', 'nutrition'),
                    ('Exercise routine', 'Organize movement and activities for your week.', 'exercise'),
                    ('Care notes', 'Record questions for a healthcare appointment.', 'care')])
        button(self, 'Plan a reminder', lambda: self.app.show('calendar'), False).pack(anchor='e', pady=18)

    def build_nutrition(self):
        self.build_notes('My meal plan', 'Breakfast:\n\nLunch:\n\nDinner:\n\nDietary preferences / notes:\n')

    def build_exercise(self):
        self.build_notes('My activity plan', 'Monday:\nTuesday:\nWednesday:\nThursday:\nFriday:\nSaturday:\nSunday:\n\nPersonal goals / notes:\n')

    def build_care(self):
        self.build_notes('Appointment preparation', 'Questions to ask:\n\nSymptoms or changes to discuss:\n\nNotes from my healthcare professional:\n\nNext appointment:\n')

    def build_notes(self, title, template):
        box = card(self, title, 'These notes stay available while the application is open.'); box.pack(fill='x')
        self.plan = tk.Text(box.content, height=13, font=('Segoe UI', 11), wrap='word', bg=BG, fg=INK, relief='flat', padx=14, pady=14)
        self.plan.pack(fill='x')
        self.plan.insert('1.0', template)
        self.feedback = self.result(box.content)
        button(box.content, 'Keep notes', lambda: self.feedback.configure(text='Notes kept for this session.')).pack(anchor='e')
        button(self, 'Plan a reminder', lambda: self.app.show('calendar'), False).pack(anchor='e', pady=18)

    def build_calendar(self):
        self.selected = date.today(); self.month = self.selected.replace(day=1)
        controls = tk.Frame(self, bg=BG); controls.pack(fill='x', pady=(0, 16))
        button(controls, '‹ Previous', lambda: self.change_month(-1), False).pack(side='left')
        self.month_title = label(controls, '', 16, bold=True); self.month_title.pack(side='left', padx=18)
        button(controls, 'Next ›', lambda: self.change_month(1), False).pack(side='left')
        button(controls, 'Today', self.today, False).pack(side='right')
        self.calendar_box = card(self); self.calendar_box.pack(fill='x')
        box = card(self, 'Selected date', 'A dot marks a date with a reminder.'); box.pack(fill='x', pady=18)
        self.date_title = label(box.content, '', 14, GREEN, True); self.date_title.pack(anchor='w', pady=(0, 12))
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
        # Drafts are kept in memory when dates or pages change.
        content = self.notes.get('1.0', 'end').strip()
        key = self.selected.isoformat()
        if content: self.app.reminders[key] = content
        else: self.app.reminders.pop(key, None)
        self.dirty = False

    def load_date(self):
        self.date_title.configure(text=self.selected.strftime('%A, %d %B %Y'))
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
                text = f"{day}{' •' if value.isoformat() in self.app.reminders else ''}"
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
        self.feedback.configure(text='Reminder updated for this session.', fg=GREEN)


def launch(route='welcome', userdata=None):
    App(route, userdata).mainloop()


if __name__ == '__main__':
    launch()
