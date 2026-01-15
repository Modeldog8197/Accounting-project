import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

def load_acc_page():

    window = tk.Tk()
    window.title("Accounting Page")
    window.geometry("820x860")
    window.configure(bg="#111827")   


    generallab = ["Food", "Transport", "Entertainment", "Other"]
    medicallab = ["Medicines", "Tests", "Doctor Visits", "Other"]

    generalvar = [tk.DoubleVar() for _ in generallab]
    medicalvar = [tk.DoubleVar() for _ in medicallab]


    def total(varslist):
        return sum(v.get() for v in varslist)

    def show_graph():
        g, m = total(generalvar), total(medicalvar)
        if g <= 0 and m <= 0:
            messagebox.showerror("Error", "Enter valid expenses")
            return

        plt.figure()
        plt.pie([g, m],
                labels=["General", "Medical"],
                autopct="%1.1f%%",
                startangle=90)
        plt.title("Expense Distribution")
        plt.show()

        labels = generallab + medicallab
        values = [v.get() for v in generalvar + medicalvar]

        labels = [l for l, v in zip(labels, values) if v > 0]
        values = [v for v in values if v > 0]

        plt.figure()
        plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
        plt.title("Individual Categories")
        plt.show()


    def show_summary():
        g, m = total(generalvar), total(medicalvar)
        t = g + m
        if t <= 0:
            messagebox.showerror("Error", "Enter valid expenses")
            return

        if g > m:
            s = "General spending is high.\nReduce discretionary costs."
        elif m > g:
            s = "Medical spending is high.\nPlan insurance and prevention."
        else:
            s = "Spending is balanced.\nGood control."

        messagebox.showinfo(
            "Accounting Summary",
            f"General: ₹{g}\nMedical: ₹{m}\nTotal: ₹{t}\n\n{s}"
        )


    tk.Label(
        window,
        text="Accounting Page",
        font=("Segoe UI", 26, "bold"),
        fg="white",
        bg="#111827"
    ).pack(pady=(30, 8))

    tk.Label(
        window,
        text="Track and analyze your expenses",
        font=("Segoe UI", 11),
        fg="#9ca3af",
        bg="#111827"
    ).pack(pady=(0, 30))

    container = tk.Frame(window, bg="#111827")
    container.pack(fill="both", expand=True, padx=40)


    def card(title, labels, vars_list, column):
        frame = tk.Frame(container, bg="#1f2933")
        frame.grid(row=0, column=column, padx=20, sticky="n")

        tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 15, "bold"),
            fg="#e5e7eb",
            bg="#1f2933"
        ).pack(anchor="w", padx=20, pady=(20, 10))

        for lab, var in zip(labels, vars_list):
            row = tk.Frame(frame, bg="#1f2933")
            row.pack(fill="x", padx=20, pady=6)

            tk.Label(
                row,
                text=lab,
                font=("Segoe UI", 11),
                fg="#d1d5db",
                bg="#1f2933",
                width=14,
                anchor="w"
            ).pack(side="left")

            tk.Entry(
                row,
                textvariable=var,
                font=("Segoe UI", 11),
                width=16,
                bg="#111827",
                fg="white",
                insertbackground="white",
                bd=0
            ).pack(side="right")


    card("General Expenses (₹)", generallab, generalvar, 0)
    card("Medical Expenses (₹)", medicallab, medicalvar, 1)


    actions = tk.Frame(window, bg="#111827")
    actions.pack(pady=40)

    tk.Button(
        actions,
        text="View Charts",
        font=("Segoe UI", 13, "bold"),
        bg="#22c55e",   
        fg="#052e16",
        width=18,
        bd=0,
        pady=10,
        command=show_graph
    ).grid(row=0, column=0, padx=15)

    tk.Button(
        actions,
        text="View Summary",
        font=("Segoe UI", 13, "bold"),
        bg="#4b5563",   
        fg="white",
        width=18,
        bd=0,
        pady=10,
        command=show_summary
    ).grid(row=0, column=1, padx=15)

    window.mainloop()
