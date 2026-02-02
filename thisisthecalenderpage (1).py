import tkinter as tk
from tkcalendar import Calendar

def load_Cal():

    reminders = {}


    root = tk.Tk()
    root.title("Calendar & Reminders")
    root.geometry("900x900")
    root.configure(bg="#1e1e1e")
    root.resizable(False, False)

    header = tk.Frame(root, bg="#1e1e1e")
    header.pack(fill="x", pady=20)

    tk.Label(
        header,
        text="Calendar",
        font=("Segoe UI", 22, "bold"),
        fg="white",
        bg="#1e1e1e"
    ).pack()

    tk.Label(
        header,
        text="Select a date and manage reminders",
        font=("Segoe UI", 11),
        fg="#aaaaaa",
        bg="#1e1e1e"
    ).pack()


    card = tk.Frame(root, bg="#2a2a2a")
    card.pack(padx=60, pady=30, fill="both", expand=True)

    cal = Calendar(
        card,
        selectmode="day",
        year=2025,
        month=12,
        day=21,
        showweeknumbers=False,

        font=("Segoe UI", 18),
        headersfont=("Segoe UI", 16),

        background="#2a2a2a",
        foreground="white",
        headersbackground="#2a2a2a",
        headersforeground="#bbbbbb",

        normalbackground="#f5f5f5",
        weekendbackground="#eeeeee",

        calendarborderwidth=0,
        borderwidth=0
    )
    cal.pack(padx=40, pady=30, fill="both", expand=True)


    cal.tag_config(
        "reminder",
        background="#fca5a5",
        foreground="#111111"
    )


    def open_reminder():
        date_key = cal.get_date()

        win = tk.Toplevel(root)
        win.title(f"Reminders — {date_key}")
        win.geometry("700x700")
        win.configure(bg="#1e1e1e")


        tk.Label(
            win,
            text=f"Reminders for {date_key}",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#1e1e1e"
        ).pack(pady=20)

        editor = tk.Frame(win, bg="#2a2a2a")
        editor.pack(padx=40, pady=20, fill="both", expand=True)

        text = tk.Text(
            editor,
            font=("Segoe UI", 12),
            wrap="word",
            bg="#f5f5f5",
            fg="#111111",
            padx=12,
            pady=12,
            bd=0
        )
        text.pack(padx=20, pady=20, fill="both", expand=True)


        if date_key in reminders:
            text.insert("1.0", reminders[date_key])

        tags = tk.Frame(editor, bg="#2a2a2a")
        tags.pack(pady=10)

        def add_tag(tag):
            text.insert(tk.END, f"\n• {tag}: ")

        for label, color in [
            ("Medical", "#ef4444"),
            ("Accounting", "#3b82f6"),
            ("Personal", "#22c55e"),
            ("Work", "#eab308")
        ]:
            tk.Button(
                tags,
                text=label,
                bg=color,
                fg="white",
                bd=0,
                padx=14,
                pady=6,
                command=lambda l=label: add_tag(l)
            ).pack(side="left", padx=6)

        def save():
            content = text.get("1.0", tk.END).strip()

            if content:
                reminders[date_key] = content

                cal.calevent_remove("all")
                for d in reminders:
                    cal.calevent_create(d, "", "reminder")

            win.destroy()

        tk.Button(
            win,
            text="Save Reminder",
            font=("Segoe UI", 12, "bold"),
            bg="#3b82f6",
            fg="white",
            bd=0,
            width=18,
            pady=8,
            command=save
        ).pack(pady=20)

    tk.Button(
        card,
        text="Open Selected Date",
        font=("Segoe UI", 13, "bold"),
        bg="#3b82f6",
        fg="white",
        bd=0,
        width=22,
        pady=10,
        command=open_reminder
    ).pack(pady=20)

    root.mainloop()
