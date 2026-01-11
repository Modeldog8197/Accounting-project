import tkinter as tk
from PIL import Image, ImageTk
#this is ai generated

window = tk.Tk()
window.title("Health Input")

screen_w = window.winfo_screenwidth()
screen_h = window.winfo_screenheight()
win_w = int(screen_w * 0.75)
win_h = int(screen_h * 0.75)
window.geometry(f"{win_w}x{win_h}")


bg_image = Image.open("158887222_10554240.jpg")
bg_image = bg_image.resize((win_w, win_h))
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(window, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.image = bg_photo


weight = tk.IntVar()
height = tk.IntVar()
gender_val = tk.IntVar(value=-1)   


def calculate_bmi(parent):
    w = weight.get()
    h = height.get() / 100
    if w > 0 and h > 0:
        bmi = w / (h * h)
        tk.Label(parent, text=f"Your BMI is: {bmi:.2f}", font=("Rockwell", 20)).pack(pady=10)

def bmi_page(parent):
    tk.Label(parent, text="Enter weight (kg):", font=("Rockwell", 20)).pack()
    tk.Entry(parent, textvariable=weight, width=30).pack(pady=10)

    tk.Label(parent, text="Enter height (cm):", font=("Rockwell", 20)).pack()
    tk.Entry(parent, textvariable=height, width=30).pack(pady=10)

    tk.Button(
        parent,
        text="Calculate BMI",
        font=("Arial", 20),
        bg="Grey",
        command=lambda: calculate_bmi(parent)
    ).pack(pady=15)

# ---------------- MEDICAL WINDOW ----------------
def open_medical_window():
    window2 = tk.Toplevel(window)
    window2.title("Medical Options")
    window2.geometry(f"{win_w}x{win_h}")

    bg2 = Image.open("158887167_10558814.jpg")
    bg2 = bg2.resize((win_w, win_h))
    bg2_photo = ImageTk.PhotoImage(bg2)

    bg2_label = tk.Label(window2, image=bg2_photo)
    bg2_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg2_label.image = bg2_photo

    tk.Label(window2, text="Choose an Option:", font=("Calibri", 25, "bold"), fg="Blue").pack(pady=20)

    frame = tk.Frame(window2)
    frame.pack(pady=20)

    def disable_after_click(btn):
        btn.config(state="disabled")

    b1 = tk.Button(frame, text="Calculate BMI", font=("Arial", 20), bg="Grey",
                   command=lambda: (bmi_page(window2), disable_after_click(b1)))
    b1.pack(side="left", padx=10)

    b2 = tk.Button(frame, text="Track Fitness", font=("Arial", 20), bg="Grey",
                   command=lambda: disable_after_click(b2))
    b2.pack(side="left", padx=10)

    if gender_val.get() == 1:
        b3 = tk.Button(frame, text="Menstrual Cycle", font=("Arial", 20), bg="Grey",
                       command=lambda: disable_after_click(b3))
        b3.pack(side="left", padx=10)

# ---------------- YES / NO ----------------
def medical_question():
    tk.Label(window, text="Do you face any Medical condition?", font=("Rockwell", 20)).pack(pady=20)

    frame = tk.Frame(window)
    frame.pack()

    def yes_clicked():
        yes_btn.config(state="disabled")
        no_btn.config(state="disabled")
        open_medical_window()

    def no_clicked():
        yes_btn.config(state="disabled")
        no_btn.config(state="disabled")
        open_medical_window()

    yes_btn = tk.Button(frame, text="Yes", font=("Arial", 20), bg="Green", width=12, command=yes_clicked)
    yes_btn.pack(side="left", padx=10)

    no_btn = tk.Button(frame, text="No", font=("Arial", 20), bg="Red", width=12, command=no_clicked)
    no_btn.pack(side="left", padx=10)

# ---------------- GENDER ----------------
def gender_selection():
    start_btn.config(state="disabled")

    tk.Label(window, text="Select your Gender:", font=("Rockwell", 20)).pack(pady=20)
    frame = tk.Frame(window)
    frame.pack()

    def male():
        gender_val.set(0)
        male_btn.config(state="disabled")
        female_btn.config(state="disabled")
        medical_question()

    def female():
        gender_val.set(1)
        male_btn.config(state="disabled")
        female_btn.config(state="disabled")
        medical_question()

    male_btn = tk.Button(frame, text="Male", font=("Arial", 20), bg="Blue", fg="White", width=12, command=male)
    male_btn.pack(side="left", padx=10)

    female_btn = tk.Button(frame, text="Female", font=("Arial", 20), bg="Pink", width=12, command=female)
    female_btn.pack(side="left", padx=10)

# ---------------- TITLE ----------------
tk.Label(window, text="User Health Details", font=("Georgia", 50, "bold", "underline")).pack(pady=20)
tk.Label(window, text="General Health", font=("Calibri", 25, "bold"), fg="Blue").pack()

# ---------------- START ----------------
start_btn = tk.Button(window, text="Get Started", font=("Arial", 20),
                      bg="light grey", width=18, command=gender_selection)
start_btn.pack(pady=30)

window.mainloop()
