import tkinter as tk
def ExeciseRoutine():
    window5 = tk.Tk()
    window5.title("Exercise Routine")
    window5.geometry("600x520")
    window5.configure(bg="#f5f5f5")

    def open_plan(title, tips):
        win = tk.Toplevel(window5)
        win.title(title)
        win.geometry("600x420")
        win.configure(bg="#f5f5f5")

        tk.Label(
            win,
            text=title,
            font=("Arial", 16, "bold"),
            bg="#f5f5f5"
        ).pack(pady=15)

        for t in tips:
            tk.Label(
                win,
                text="• " + t,
                anchor="w",
                justify="left",
                wraplength=520,
                bg="#f5f5f5",
                font=("Arial", 11)
            ).pack(padx=30, pady=6, anchor="w")

        tk.Button(
            win,
            text="Close",
            font=("Arial", 11),
            bg="#d32f2f",
            fg="white",
            width=15,
            command=win.destroy
        ).pack(pady=15)

    # ---------------- Data ----------------
    BULK = [
        "Strength training with compound movements",
        "Use progressive overload",
        "Protein intake: 1.2–2.2 g/kg bodyweight",
        "Maintain a caloric surplus"
    ]

    CUT = [
        "Regular cardio for fat loss",
        "Continue strength training",
        "Maintain a caloric deficit",
        "High protein to preserve muscle"
    ]

    MAINTAIN = [
        "Mix strength and cardio",
        "Match calories to expenditure",
        "Monitor weight and measurements",
        "Stay physically active daily"
    ]

    HEALTHY = [
        "150 min moderate exercise per week",
        "Eat a balanced, nutrient-rich diet",
        "Stay well hydrated",
        "Sleep 7–9 hours daily"
    ]

    # ---------------- UI ----------------
    tk.Label(
        window5,
        text="Exercise Routine",
        font=("Arial", 18, "bold"),
        bg="#f5f5f5"
    ).pack(pady=15)

    tk.Label(
        window5,
        text="Choose your fitness goal:",
        font=("Arial", 14),
        bg="#f5f5f5"
    ).pack(pady=10)

    def goal_btn(text, tips):
        tk.Button(
            window5,
            text=text,
            font=("Arial", 13),
            bg="#333333",
            fg="white",
            width=20,
            command=lambda: open_plan(text, tips)
        ).pack(pady=6)

    goal_btn("Bulking", BULK)
    goal_btn("Cutting", CUT)
    goal_btn("Maintain Weight", MAINTAIN)
    goal_btn("Staying Healthy", HEALTHY)


    tk.Button(
        window5,
        text="Close",
        font=("Arial", 11),
        bg="#d32f2f",
        fg="white",
        width=15,
        command=window5.destroy
    ).pack(pady=6)
