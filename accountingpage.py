"""Clean, friendly accounting dashboard for the desktop application."""

import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib.pyplot as plt

COLORS = {"page": "#F4F7FB", "surface": "#FFFFFF", "ink": "#172033", "muted": "#667085", "border": "#DDE3EC", "primary": "#176B5B", "primary_hover": "#125548", "accent": "#DDF4EC", "medical": "#5B67D8", "danger": "#B42318"}


def load_acc_page():
    """Open the accounting dashboard from the main application."""
    parent = tk._default_root
    window = tk.Toplevel(parent) if parent else tk.Tk()
    window.title("Expense overview")
    window.geometry("980x720")
    window.minsize(820, 640)
    window.configure(bg=COLORS["page"])

    style = ttk.Style(window)
    style.theme_use("clam")
    style.configure("Clean.TEntry", fieldbackground=COLORS["surface"], foreground=COLORS["ink"], bordercolor=COLORS["border"], lightcolor=COLORS["border"], darkcolor=COLORS["border"], padding=(10, 9))
    style.map("Clean.TEntry", bordercolor=[("focus", COLORS["primary"])])

    categories = {
        "Everyday": ["Food & groceries", "Transport", "Entertainment", "Other"],
        "Healthcare": ["Medicines", "Tests", "Doctor visits", "Other"],
    }
    values = {group: [tk.StringVar() for _ in labels] for group, labels in categories.items()}
    total_vars = {name: tk.StringVar(value="₹0.00") for name in ("Everyday", "Healthcare", "Total")}
    status_var = tk.StringVar(value="Add an amount to begin tracking your spending.")

    def parse_amount(raw):
        raw = raw.strip().replace(",", "")
        if not raw:
            return 0.0
        amount = float(raw)
        if amount < 0:
            raise ValueError
        return amount

    def collect(show_error=False):
        result, invalid = {}, False
        for group, labels in categories.items():
            result[group] = []
            for label, variable in zip(labels, values[group]):
                try:
                    amount = parse_amount(variable.get())
                except ValueError:
                    invalid, amount = True, 0.0
                result[group].append((label, amount))
        everyday = sum(amount for _, amount in result["Everyday"])
        healthcare = sum(amount for _, amount in result["Healthcare"])
        overall = everyday + healthcare
        for name, amount in (("Everyday", everyday), ("Healthcare", healthcare), ("Total", overall)):
            total_vars[name].set(f"₹{amount:,.2f}")
        if invalid:
            status_var.set("Use positive numbers only. Invalid entries are excluded.")
            status_label.configure(fg=COLORS["danger"])
            if show_error:
                messagebox.showerror("Check your amounts", "Please use positive numbers only. You can leave unused fields blank.", parent=window)
        elif overall:
            status_var.set("Your totals are up to date.")
            status_label.configure(fg=COLORS["primary"])
        else:
            status_var.set("Add an amount to begin tracking your spending.")
            status_label.configure(fg=COLORS["muted"])
        return None if invalid else (result, everyday, healthcare, overall)

    def show_charts():
        snapshot = collect(show_error=True)
        if not snapshot:
            return
        result, everyday, healthcare, overall = snapshot
        if overall <= 0:
            messagebox.showinfo("Nothing to chart", "Add at least one expense before opening the charts.", parent=window)
            return
        detail = [(label, amount) for group in categories for label, amount in result[group] if amount > 0]
        figure, axes = plt.subplots(1, 2, figsize=(11, 5.4))
        figure.canvas.manager.set_window_title("Expense insights")
        figure.patch.set_facecolor(COLORS["page"])
        axes[0].pie([everyday, healthcare], labels=["Everyday", "Healthcare"], colors=[COLORS["primary"], COLORS["medical"]], autopct="%1.0f%%", startangle=90, wedgeprops={"width": 0.42, "edgecolor": "white"})
        axes[0].set_title("Spending split", fontweight="bold", color=COLORS["ink"])
        labels, amounts = zip(*detail)
        axes[1].barh(labels, amounts, color=COLORS["primary"])
        axes[1].invert_yaxis()
        axes[1].set_title("By category", fontweight="bold", color=COLORS["ink"])
        axes[1].set_xlabel("Amount (₹)")
        axes[1].spines[["top", "right", "left"]].set_visible(False)
        axes[1].grid(axis="x", alpha=0.2)
        axes[1].set_axisbelow(True)
        figure.tight_layout(pad=2.5)
        plt.show()

    def show_summary():
        snapshot = collect(show_error=True)
        if not snapshot:
            return
        _, everyday, healthcare, overall = snapshot
        if overall <= 0:
            messagebox.showinfo("No expenses yet", "Add at least one expense to create a summary.", parent=window)
            return
        dominant = "Everyday" if everyday >= healthcare else "Healthcare"
        share = max(everyday, healthcare) / overall * 100
        messagebox.showinfo("Expense summary", f"Total spending: ₹{overall:,.2f}\n\nEveryday: ₹{everyday:,.2f}\nHealthcare: ₹{healthcare:,.2f}\n\n{dominant} expenses make up {share:.0f}% of your total.", parent=window)

    def clear_all():
        for group_values in values.values():
            for variable in group_values:
                variable.set("")
        collect()

    shell = tk.Frame(window, bg=COLORS["page"])
    shell.pack(fill="both", expand=True, padx=38, pady=30)
    header = tk.Frame(shell, bg=COLORS["page"])
    header.pack(fill="x", pady=(0, 22))
    tk.Label(header, text="Expense overview", font=("Segoe UI", 25, "bold"), fg=COLORS["ink"], bg=COLORS["page"]).pack(anchor="w")
    tk.Label(header, text="A simple view of where your money is going.", font=("Segoe UI", 11), fg=COLORS["muted"], bg=COLORS["page"]).pack(anchor="w", pady=(5, 0))

    metrics = tk.Frame(shell, bg=COLORS["page"])
    metrics.pack(fill="x", pady=(0, 18))
    metrics.columnconfigure((0, 1, 2), weight=1, uniform="metric")
    for column, (label, key) in enumerate((("EVERYDAY", "Everyday"), ("HEALTHCARE", "Healthcare"), ("TOTAL SPEND", "Total"))):
        card = tk.Frame(metrics, bg=COLORS["surface"], highlightthickness=1, highlightbackground=COLORS["border"])
        card.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 6, 0 if column == 2 else 6))
        tk.Label(card, text=label, font=("Segoe UI", 9, "bold"), fg=COLORS["muted"], bg=COLORS["surface"]).pack(anchor="w", padx=18, pady=(15, 4))
        tk.Label(card, textvariable=total_vars[key], font=("Segoe UI", 19, "bold"), fg=COLORS["primary"] if key == "Total" else COLORS["ink"], bg=COLORS["surface"]).pack(anchor="w", padx=18, pady=(0, 15))

    content = tk.Frame(shell, bg=COLORS["page"])
    content.pack(fill="both", expand=True)
    content.columnconfigure((0, 1), weight=1, uniform="group")

    def expense_card(group, column, description):
        card = tk.Frame(content, bg=COLORS["surface"], highlightthickness=1, highlightbackground=COLORS["border"])
        card.grid(row=0, column=column, sticky="nsew", padx=(0, 8) if column == 0 else (8, 0))
        tk.Label(card, text=group, font=("Segoe UI", 15, "bold"), fg=COLORS["ink"], bg=COLORS["surface"]).pack(anchor="w", padx=22, pady=(20, 2))
        tk.Label(card, text=description, font=("Segoe UI", 9), fg=COLORS["muted"], bg=COLORS["surface"]).pack(anchor="w", padx=22, pady=(0, 13))
        for label, variable in zip(categories[group], values[group]):
            row = tk.Frame(card, bg=COLORS["surface"])
            row.pack(fill="x", padx=22, pady=5)
            tk.Label(row, text=label, font=("Segoe UI", 10), fg=COLORS["ink"], bg=COLORS["surface"], width=17, anchor="w").pack(side="left")
            ttk.Entry(row, textvariable=variable, style="Clean.TEntry", justify="right").pack(side="right", fill="x", expand=True)
            variable.trace_add("write", lambda *_: collect())

    expense_card("Everyday", 0, "Regular living and lifestyle costs")
    expense_card("Healthcare", 1, "Medical care and wellbeing costs")

    footer = tk.Frame(shell, bg=COLORS["page"])
    footer.pack(fill="x", pady=(18, 0))
    status_label = tk.Label(footer, textvariable=status_var, font=("Segoe UI", 9), fg=COLORS["muted"], bg=COLORS["page"])
    status_label.pack(side="left")
    tk.Button(footer, text="View charts", command=show_charts, font=("Segoe UI", 10, "bold"), bg=COLORS["primary"], activebackground=COLORS["primary_hover"], fg="white", activeforeground="white", bd=0, padx=19, pady=9, cursor="hand2").pack(side="right", padx=(8, 0))
    tk.Button(footer, text="Summary", command=show_summary, font=("Segoe UI", 10, "bold"), bg=COLORS["surface"], activebackground=COLORS["accent"], fg=COLORS["primary"], bd=1, relief="solid", padx=19, pady=8, cursor="hand2").pack(side="right", padx=(8, 0))
    tk.Button(footer, text="Clear", command=clear_all, font=("Segoe UI", 10), bg=COLORS["page"], activebackground=COLORS["page"], fg=COLORS["muted"], bd=0, padx=12, pady=9, cursor="hand2").pack(side="right")
    window.bind("<Control-r>", lambda _event: clear_all())
    window.bind("<Control-Return>", lambda _event: show_summary())
    if parent is None:
        window.mainloop()


if __name__ == "__main__":
    load_acc_page()
