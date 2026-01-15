 #THINGS NEED TO BE DONE : BALENCED DIET, EXERSIZE ROUTINE... 
#create a new window in a function and give suggetions like bmi format
#merge accounting page
#menstrual cycle
#GO TO LINE 239
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib
matplotlib.use("TkAgg")
from tkinter import messagebox
import matplotlib.pyplot as plt 
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
def load_hel_page():
    import thisisthecalenderpage as cal
    import accountingpage as acc
    
    window=tk.Tk()
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    win_w = int(screen_w * 0.75)
    win_h = int(screen_h * 0.75)
    window.geometry(f"{win_w}x{win_h}")
    bg_image = Image.open("sharan.jpg")  
    bg_image = bg_image.resize((win_w, win_h))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(window, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    window.title("Health input")
    weight=tk.StringVar()
    height=tk.StringVar()
    age=tk.StringVar()
    num1=tk.StringVar()
    num2=tk.IntVar()
    num3=tk.StringVar()
    num4=tk.IntVar()
    def load_Calendar():   
        cal.load_Cal()
    l1=tk.Label(window,text="User Health Details",font=("Georgia",50,"bold","underline")).pack()
    l1=tk.Label(window,text="General health:",font=("Calibri",25,"bold"),fg="Blue").pack(pady=0)
    def load_acc_page():
        window.destroy()
        acc.load_acc_page()
    n = 0
    def gsm():
        yes() 
    def gsf():
        nonlocal n
        n=1
        print(n)
        yes()
    def gender():
        gender = tk.Label(window,text="Select your Gender:",font=("Rockwell", 20)).pack(pady=20)
        gender_frame=tk.Frame(window)
        gender_frame.pack()
        male = tk.Button(gender_frame,text="Male",font=("Arial", 20),bg="Blue",fg="White",width=12,height=1,command=gsm).pack(side="left", padx=10, pady=10)
        female = tk.Button(gender_frame,text="Female",font=("Arial", 20),bg="Pink",width=12,height=1,command=gsf).pack(side="left", padx=10, pady=10)
    def yes():  
        window2 = tk.Toplevel(window)   
        screen_w = window2.winfo_screenwidth()
        screen_h = window2.winfo_screenheight()
        win_w = int(screen_w * 0.75)
        win_h = int(screen_h * 0.75)
        window2.geometry(f"{win_w}x{win_h}")
        window2.title("Medical Condition")
        bg_image = Image.open("158887167_10558814.jpg")
        bg_image = bg_image.resize((win_w, win_h))
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(window2, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_photo    
        exit = tk.Button(
            window2, text="Exit", font=("Arial",10),
            bg="light grey", width=5, height=1,
            command=window2.destroy )
        def trackfitness():
            steps_var = tk.StringVar()
            exersize_var = tk.StringVar()
            water_var = tk.StringVar()
            sleep = []
            intsleep = tk.StringVar()
            num1 = tk.StringVar()
            num2 = tk.StringVar()

            window6 = tk.Toplevel(window2)
            window6.title("Fitness Tracker")
            window6.geometry(f"{win_w}x{win_h}")

            bg_image6 = Image.open("fitness-concept-with-equipment-frame.jpg")
            bg_image6 = bg_image6.resize((win_w, win_h))
            bg_photo6 = ImageTk.PhotoImage(bg_image6)
            bg_label6 = tk.Label(window6, image=bg_photo6)
            bg_label6.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label6.image = bg_photo6

            Title = tk.Label(window6, text="Basic Lifestyle Tracker", font=("Georgia", 30, "bold", "underline"))
            Title.pack(pady=20)

            steps = tk.Label(window6, text="Enter steps walked:", font=("Arial", 16))
            steps.pack(pady=10)
            steps_e = tk.Entry(window6, textvariable=steps_var, font=("Arial", 16))
            steps_e.pack(pady=10)

            exersize = tk.Label(window6, text="Enter exercise done (in minutes):", font=("Arial", 16))
            exersize.pack(pady=10)
            exersize_e = tk.Entry(window6, textvariable=exersize_var, font=("Arial", 16))
            exersize_e.pack(pady=10)

            water = tk.Label(window6, text="Enter water intake (in number of glasses):", font=("Arial", 16))
            water.pack(pady=10)
            water_e = tk.Entry(window6, textvariable=water_var, font=("Arial", 16))
            water_e.pack(pady=10)

            def ok():
                ok_btn.pack_forget()

                steps.pack_forget()
                steps_e.pack_forget()
                exersize.pack_forget()
                exersize_e.pack_forget()
                water.pack_forget()
                water_e.pack_forget()

                sleepo = tk.Label(window6, text="Enter sleep duration (in hours) for the last 7 days:", font=("Arial", 16))
                sleepo.pack(pady=10)

                def reset_view():
                    sleepo.pack_forget()
                    back.pack_forget()
                    for i in sleep:
                        i.pack_forget()
                    generate.pack_forget()
                    ok_btn.pack(pady=10)
                    steps.pack(pady=10)
                    steps_e.pack(pady=10)
                    exersize.pack(pady=10)
                    exersize_e.pack(pady=10)
                    water.pack(pady=10)
                    water_e.pack(pady=10)

                for i in range(7):
                    e = tk.Entry(window6, textvariable=tk.StringVar(), font=("Arial", 16))
                    e.pack(pady=5)
                    sleep.append(e)

                generate.pack(pady=20)
                back = tk.Button(window6, text="Back", font=("Arial", 16), command=reset_view)
                back.pack(pady=10)

            ok_btn = tk.Button(window6, text="Next", font=("Arial", 16), command=ok)
            ok_btn.pack(pady=10)

            def generate_summary():
                try:
                    steps_val = int(steps_e.get())
                    exersize_val = int(exersize_e.get())
                    water_val = int(water_e.get())
                    sleep_vals = [float(e.get()) for e in sleep]
                    avg = sum(sleep_vals) / 7
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid numbers")
                    return

                if steps_val >= 10000:
                    feedback1 = "Great job on meeting your daily step goal!"
                elif steps_val >= 5000:
                    feedback1 = "Good effort! Try to increase your steps a bit more."
                else:
                    feedback1 = "Let's aim to walk more for better health."

                if exersize_val >= 30:
                    feedback2 = "Excellent work on your exercise!"
                elif exersize_val >= 15:
                    feedback2 = "Good job! Try to exercise a bit more."
                else:
                    feedback2 = "Incorporating more exercise will benefit your health."

                if water_val >= 8:
                    feedback3 = "You're staying well-hydrated!"
                elif water_val >= 4:
                    feedback3 = "Not bad! Aim to drink more water."
                else:
                    feedback3 = "Drinking more water is necessary."

                if avg >= 7:
                    feedback4 = "You're getting enough sleep!"
                elif avg >= 5:
                    feedback4 = "Your sleep is just sufficient, try to improve a bit more!"
                else:
                    feedback4 = "Your sleep is insufficient for good health."

                window7 = tk.Toplevel(window6)
                window7.title("Fitness Summary")
                window7.geometry(f"{win_w}x{win_h}")
                bg_image7 = Image.open("board-background-1li7fr7rrtu1q0n1.jpg")
                bg_image7 = bg_image7.resize((win_w, win_h))
                bg_photo7 = ImageTk.PhotoImage(bg_image7)
                bg_label7 = tk.Label(window7, image=bg_photo7)
                bg_label7.place(x=0, y=0, relwidth=1, relheight=1)
                bg_label7.image = bg_photo7
                def BalancedDiet():
                    window5 = tk.Toplevel(window7)
                    window5.title("Balanced Diet")
                    window5.geometry("620x520")
                    window5.configure(bg="#f5f5f5")

                    tk.Label(
                        window5,
                        text="Balanced Diet",
                        font=("Arial", 18, "bold"),
                        bg="#f5f5f5"
                    ).pack(pady=15)

                    tips = [
                        "Carbohydrates – 45–60% of daily intake\n  Main energy source (rice, wheat, fruits)",
                        "Proteins – 15–25% of daily intake\n  Muscle growth & repair (pulses, eggs, milk, nuts)",
                        "Fats – 20–30% of daily intake\n  Brain health & stored energy (nuts, seeds, olive oil)",
                        "Vitamins – Small amounts daily\n  Immunity support (fruits & vegetables)",
                        "Minerals – Small amounts daily\n  Bones & body functions (calcium, iron)",
                        "Fiber – 25–30 g per day\n  Aids digestion (whole grains, vegetables)",
                        "Water – 6–8 glasses per day\n  Hydration & temperature control"
                    ]

                    for t in tips:
                        tk.Label(
                            window5,
                            text="• " + t,
                            anchor="w",
                            justify="left",
                            wraplength=540,
                            bg="#f5f5f5",
                            font=("Arial", 11)
                        ).pack(padx=30, pady=6, anchor="w")

                    tk.Label(
                        window5,
                        text="Be Consistent and Monitor Progress!",
                        font=("Arial", 18, "bold"),
                        bg="#f5f5f5"
                    ).pack(pady=15)

                   

                    tk.Button(
                        window5,
                        text="Calendar",
                        font=("Arial", 11),
                        bg="black",
                        fg="white",
                        width=15,
                        command=cal.load_Cal
                    ).pack(pady=5)

                    tk.Button(
                        window5,
                        text="Close",
                        font=("Arial", 11),
                        bg="#d32f2f",
                        fg="white",
                        width=15,
                        command=window5.destroy
                    ).pack(pady=8)

                '''def ExeciseRoutine():
                    window5 = tk.Toplevel(window7)
                    window5.title("Exercise Routine")
                    window5.geometry("620x520")
                    window5.configure(bg="#f5f5f5")
                    def Bulk():
                        window8= tk.Toplevel(window5)
                        tips = [
                            "Strength Training: Focus on compound movements like squats, deadlifts, bench presses, and overhead presses to build muscle mass.",
                            "Progressive Overload: Gradually increase the weight and intensity of your workouts to continuously challenge your muscles.",
                            "Adequate Protein Intake: Consume 1.2 to 2.2 grams of protein per kilogram of body weight daily to support muscle growth.",
                            "Caloric Surplus: Eat more calories than you burn to provide your body with the energy needed for muscle gain."
                        ]
                        
                    

                    

                        
                    

                        for t in tips:
                            tk.Label(
                                window8,
                                text="• " + t,
                                anchor="w",
                                justify="left",
                                wraplength=540,
                                bg="#f5f5f5",
                                font=("Arial", 11)
                            ).pack(padx=30, pady=6, anchor="w")
                    def Cut():
                        window8= tk.Toplevel(window5)
                        tips = [
                            "Cardiovascular Exercise: Incorporate regular cardio sessions such as running, cycling, or swimming to help burn calories and fat.",
                            "Strength Training: Maintain muscle mass while cutting by continuing to lift weights, focusing on compound movements.",
                            "Caloric Deficit: Consume fewer calories than you burn to promote fat loss while preserving muscle.",
                            "High Protein Diet: Increase protein intake to support muscle retention and promote satiety during a caloric deficit."
                           
                        ]
                        
                    

                    

                        
                    

                        for t in tips:
                            tk.Label(
                                window8,
                                text="• " + t,
                                anchor="w",
                                justify="left",
                                wraplength=540,
                                bg="#f5f5f5",
                                font=("Arial", 11)
                            ).pack(padx=30, pady=6, anchor="w")

                    def Maintain():
                        window8= tk.Toplevel(window5)
                        tips = [
                            "Balanced Exercise Routine: Combine both strength training and cardiovascular exercises to maintain overall fitness and muscle mass.",
                            "Consistent Caloric Intake: Eat a balanced diet that matches your energy expenditure to maintain your current weight.",
                            "Regular Monitoring: Keep track of your weight, body measurements, and fitness levels to ensure you stay on track with your maintenance goals.",
                            "Stay Active: Incorporate daily physical activity, such as walking or recreational sports, to support overall health and well-being."
                        ]
                        
                    

                    

                        
                    

                        for t in tips:
                            tk.Label(
                                window8,
                                text="• " + t,
                                anchor="w",
                                justify="left",
                                wraplength=540,
                                bg="#f5f5f5",
                                font=("Arial", 11)
                            ).pack(padx=30, pady=6, anchor="w")
                    def Healthy():
                        window8= tk.Toplevel(window5)
                        tips = [
                            "Regular Physical Activity: Aim for at least 150 minutes of moderate aerobic exercise or 75 minutes of vigorous exercise each week, along with muscle-strengthening activities on two or more days.",
                            "Balanced Diet: Consume a variety of nutrient-dense foods, including fruits, vegetables, whole grains, lean proteins, and healthy fats to support overall health.",
                            "Adequate Hydration: Drink plenty of water throughout the day to maintain hydration and support bodily functions.",
                            "Sufficient Sleep: Aim for 7-9 hours of quality sleep per night to promote recovery and overall well-being."
                        ]
                        for t in tips:
                            tk.Label(
                                window8,
                                text="• " + t,
                                anchor="w",
                                justify="left",
                                wraplength=540,
                                bg="#f5f5f5",
                                font=("Arial", 11)
                            ).pack(padx=30, pady=6, anchor="w")

                        
                    

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
                 


                    tk.Button(
                        window5,
                        text="Bulking",
                        font=("Arial", 14),
                        bg="#1976d2",
                        fg="white",
                        command=Bulk
                    ).pack(pady=10)

                    tk.Button(
                        window5,
                        text="Cutting",
                        font=("Arial", 14),
                        bg="#1976d2",
                        fg="white",
                        command=Cut
                    ).pack(pady=10)

                    tk.Button(
                        window5,
                        text="Maintain Weight",
                        font=("Arial", 14),
                        bg="#1976d2",
                        fg="white",
                        command=Maintain
                    ).pack(pady=10)

                    tk.Button(
                        window5,
                        text="Staying healthy",
                        font=("Arial", 14),
                        bg="#1976d2",
                        fg="white",
                        command=Healthy
                    ).pack(pady=10)

                    

                    

                        
                    

                    


           
                   

                    tk.Button(
                        window5,
                        text="Calendar",
                        font=("Arial", 11),
                        bg="black",
                        fg="white",
                        width=15,
                        command=cal.load_Cal
                    ).pack(pady=5)

                    tk.Button(
                        window5,
                        text="Close",
                        font=("Arial", 11),
                        bg="#d32f2f",
                        fg="white",
                        width=15,
                        command=window5.destroy
                    ).pack(pady=8)'''
                def ExeciseRoutine():
                    window5 = tk.Toplevel(window7)
                    window5.title("Exercise Routine")
                    window5.geometry("620x520")
                    window5.resizable(False, False)

                    # ---------- Gradient Background ----------
                    canvas = tk.Canvas(window5, width=620, height=520, highlightthickness=0)
                    canvas.pack(fill="both", expand=True)

                    for i in range(520):
                        color = f"#{240-i//6:02x}{240-i//6:02x}{240-i//6:02x}"
                        canvas.create_line(0, i, 620, i, fill=color)

                    # ---------- Card ----------
                    card = tk.Frame(window5, bg="#ffffff")
                    card.place(relx=0.5, rely=0.5, anchor="center", width=520, height=440)

                    def open_plan(title, tips):
                        win = tk.Toplevel(window5)
                        win.title(title)
                        win.geometry("560x420")
                        win.configure(bg="#f5f5f5")

                        tk.Label(win, text=title, font=("Arial", 16, "bold"),
                                bg="#f5f5f5").pack(pady=15)

                        for t in tips:
                            tk.Label(
                                win,
                                text="• " + t,
                                anchor="w",
                                justify="left",
                                wraplength=500,
                                bg="#f5f5f5",
                                font=("Arial", 11)
                            ).pack(padx=30, pady=6, anchor="w")

                        tk.Button(win, text="Close", font=("Arial", 11),
                                bg="#333", fg="white",
                                width=15, command=win.destroy).pack(pady=15)

                    # ---------- Data ----------
                    BULK = [
                        "Strength training with compound movements",
                        "Progressive overload",
                        "Protein: 1.2–2.2 g/kg bodyweight",
                        "Maintain a caloric surplus"
                    ]

                    CUT = [
                        "Regular cardio for fat loss",
                        "Continue strength training",
                        "Maintain a caloric deficit",
                        "High protein intake"
                    ]

                    MAINTAIN = [
                        "Balanced strength and cardio",
                        "Calories match expenditure",
                        "Monitor weight regularly",
                        "Stay active daily"
                    ]

                    HEALTHY = [
                        "150 min exercise per week",
                        "Balanced diet",
                        "Proper hydration",
                        "7–9 hours sleep"
                    ]

                    # ---------- UI ----------
                    tk.Label(card, text="Exercise Routine",
                            font=("Arial", 18, "bold"),
                            bg="white").pack(pady=15)

                    tk.Label(card, text="Choose your fitness goal:",
                            font=("Arial", 13),
                            bg="white").pack(pady=8)

                    def goal_btn(text, tips):
                        tk.Button(
                            card,
                            text=text,
                            font=("Arial", 12),
                            bg="#2f2f2f",
                            fg="white",
                            width=22,
                            bd=0,
                            command=lambda: open_plan(text, tips)
                        ).pack(pady=6)

                    goal_btn("Bulking", BULK)
                    goal_btn("Cutting", CUT)
                    goal_btn("Maintain Weight", MAINTAIN)
                    goal_btn("Staying Healthy", HEALTHY)

                    tk.Button(card, text="Calendar",
                            font=("Arial", 11),
                            bg="black", fg="white",
                            width=16,
                            command=cal.load_Cal).pack(pady=10)

                    tk.Button(card, text="Close",
                            font=("Arial", 11),
                            bg="#b91c1c", fg="white",
                            width=16,
                            command=window5.destroy).pack(pady=4)


                def graph():
                    window6 = tk.Toplevel(window7)

                    def plot_graph():
                        try:
                            weeks = list(range(1, 9))
                            weights = [float(num1.get()) - i*float(num2.get()) for i in range(8)]
                        except ValueError:
                            messagebox.showerror("Error", "Please enter valid numbers for weight and weekly loss")
                            return
                        fig, ax = plt.subplots(figsize=(6, 4))
                        ax.plot(weeks, weights, marker='o')
                        ax.set_title('Weight Loss Over 8 Weeks')
                        ax.set_xlabel('Weeks')
                        ax.set_ylabel('Weight (kg)')
                        ax.grid(True)
                        canvas = FigureCanvasTkAgg(fig, master=window6)
                        canvas.draw()
                        canvas.get_tk_widget().pack(pady=20)
                        exit_btn = tk.Button(window6, text="Close", font=("Arial", 14), command=window6.destroy)

                    frame = tk.Frame(window6, bg="")
                    frame.pack(pady=10)
                    l_weight = tk.Label(frame, text="Current Weight (kg):", font=("Arial", 14))
                    l_weight.pack(side="left", padx=5)
                    e_weight = tk.Entry(frame, textvariable=num1, font=("Arial", 14))
                    e_weight.pack(side="left", padx=5)
                    l_loss = tk.Label(frame, text="Weekly Weight Loss (kg):", font=("Arial", 14))
                    l_loss.pack(side="left", padx=5)
                    e_loss = tk.Entry(frame, textvariable=num2, font=("Arial", 14))
                    e_loss.pack(side="left", padx=5)
                    plot_button = tk.Button(window6, text="Plot Weight Loss Graph", font=("Arial", 14), command=plot_graph)
                    plot_button.pack(pady=10)

                tk.Label(window7, text="Your Fitness Summary", font=("Georgia", 30, "bold", "underline")).pack(pady=20)
                tk.Label(window7, text=f"Steps Walked: {steps_val}\n{feedback1}", font=("Arial", 16)).pack(pady=10)
                tk.Label(window7, text=f"Exercise Done: {exersize_val} minutes\n{feedback2}", font=("Arial", 16)).pack(pady=10)
                tk.Label(window7, text=f"Water Intake: {water_val} glasses\n{feedback3}", font=("Arial", 16)).pack(pady=10)
                tk.Label(window7, text=f"Average Sleep Duration: {avg:.2f} hours\n{feedback4}", font=("Arial", 16)).pack(pady=10)
                frame22 = tk.Frame(window7, bg="")
                frame22.pack(pady=10)
                #THINGS NEED TO BE DONE : BALENCED DIET, EXERSIZE ROUTINE... 


                #create a new window in a function and give suggetions like bmi format
                tk.Button(frame22, text="Balanced Diet", font=("Arial", 16), bg="Black", fg="white", command=BalancedDiet).pack(side="left",padx=10)
                tk.Button(frame22, text="Exercise routine", font=("Arial", 16), bg="Black", fg="white", command=ExeciseRoutine).pack(side="left",padx=10)
                tk.Button(frame22, text="Weight loss plan", font=("Arial", 16), bg="Black", fg="white", command=graph).pack(side="left",padx=10)
                tk.Button(window7, text="Close", font=("Arial", 16), command=window7.destroy).pack(pady=20)

            generate = tk.Button(window6, text="Generate Summary", font=("Arial", 16), command=generate_summary)


            


        def calculatebmi():
            window3 = tk.Toplevel(window2)
            window3.title("BMI Result")
            window3.geometry(f"{win_w}x{win_h}")
            bg_image3 = Image.open("158887167_10558814.jpg")
            bg_image3 = bg_image3.resize((win_w, win_h))
            bg_photo3 = ImageTk.PhotoImage(bg_image3)
            bg_label3 = tk.Label(window3, image=bg_photo3)
            bg_label3.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label3.image = bg_photo3
            content_frame = tk.Frame(window3, bg="")
            content_frame.pack( padx="10",fill="both",expand=True)
            graph_container = tk.Frame(content_frame, bg="")
            graph_container.pack(side="right", fill="both", expand=True, padx=60, pady=30)
            chart_frame = tk.Frame(graph_container, bg="", highlightthickness=0)
            chart_frame.pack(padx=30,fill="both", expand=True)
            try:
                a = int(age.get())
                w = float(weight.get())
                h = float(height.get()) / 100
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
                return
            bmi_value = w / (h*h)
            text_frame2=tk.Frame(window3)           
            def Diet():
                window5 = tk.Toplevel(window4)  
                window5.title("Nutrition Tips")
                window5.geometry("700x500")  
                
                
                points = [
                    "Eat More Often: Aim for 5-6 smaller meals or snacks throughout the day, rather than three large ones, to increase calorie intake.",
                    "Add Healthy Calories: Mix in extra calories with nuts, seeds, avocado, cheese, olive oil, and nut butters in your meals.",
                    "Choose Nutrient-Dense Foods: Focus on whole grains, lean proteins (fish, eggs, chicken), fruits, vegetables, and dairy.",
                    "Boost Drinks: Drink milk, milkshakes, or smoothies with added protein powder or fruit instead of low-calorie drinks."

                ]
                
                
                for tip in points:
                    lll = tk.Label(window5, text="• " + tip, anchor="w", justify="left", wraplength=550, font=("Arial", 12))
                    lll.pack(pady=5, padx=10, anchor="w") 
                t5=tk.Label(window5,text="Stay consistent with these tips and monitor your progress regularly!",font=("Arial",14,"bold")).pack(pady=10)
                t5=tk.Label(window5,text="Save reminders in calendar:",font=("Arial",14,"bold")).pack(pady=10)
                calendar = tk.Button(window5, text="Calendar",command=cal.load_Cal, font=("Arial", 14), bg="Black", fg="white")
                calendar.pack(pady=10)
                close= tk.Button(window5, text="Close", font=("Arial", 14), bg="red", fg="white", command=window5.destroy)
                close.pack(pady=10)
            def lifestyle():
                window5 = tk.Toplevel(window4)  
                window5.title("Lifestyle Tips")
                window5.geometry("700x500")  
                
                
                points = [
                    "Time Fluids: Drink water between meals, not right before, to avoid feeling full too quickly.",
                    "Strength Training: Incorporate weight lifting or resistance exercises to build muscle mass.",
                    "Get Enough Sleep: Aim for 7-9 hours of quality sleep per night to support overall health and weight gain.",
                    "Manage Stress: Practice relaxation techniques like meditation or yoga to reduce stress, which can affect appetite."

                ]
                
                
                for tip in points:
                    lll = tk.Label(window5, text="• " + tip, anchor="w", justify="left", wraplength=550, font=("Arial", 12))
                    lll.pack(pady=5, padx=10, anchor="w") 
                t5=tk.Label(window5,text="Stay consistent with these tips and monitor your progress regularly!",font=("Arial",14,"bold")).pack(pady=10)
                t5=tk.Label(window5,text="Save reminders in calendar:",font=("Arial",14,"bold")).pack(pady=10)
                calendar = tk.Button(window5, text="Calendar",command=cal.load_Cal, font=("Arial", 14), bg="Black", fg="white")
                calendar.pack(pady=10)
                close= tk.Button(window5, text="Close", font=("Arial", 14), bg="red", fg="white", command=window5.destroy)
                close.pack(pady=10)
            def medical_help():
                
                window5 = tk.Toplevel(window4)  
                window5.title("Medical Help Tips")
                window5.geometry("700x500")  
                
                
                points = [
                    "Consult a Healthcare Professional: Seek advice from a doctor or dietitian to rule out any underlying health issues affecting weight.",
                    "Regular Check-ups: Schedule regular health check-ups to monitor your overall health and nutritional status.",
                    "Consider Supplements: Discuss with your healthcare provider about the possibility of using nutritional supplements if needed.",
                    "Therapy and Support: If emotional or psychological factors are impacting your weight, consider counseling or support groups."

                ]
                
                
                for tip in points:
                    lll = tk.Label(window5, text="• " + tip, anchor="w", justify="left", wraplength=550, font=("Arial", 12))
                    lll.pack(pady=5, padx=10, anchor="w") 
                t5=tk.Label(window5,text="Stay consistent with these tips and monitor your progress regularly!",font=("Arial",14,"bold")).pack(pady=10)
                t5=tk.Label(window5,text="Save reminders in calendar:",font=("Arial",14,"bold")).pack(pady=10)
                calendar = tk.Button(window5, text="Calendar",command=cal.load_Cal, font=("Arial", 14), bg="Black", fg="white")
                calendar.pack(pady=10)
                close= tk.Button(window5, text="Close", font=("Arial", 14), bg="red", fg="white", command=window5.destroy)
                close.pack(pady=10)
            def Dietforideal():
                window5 = tk.Toplevel(window4)  
                window5.title("Nutrition Tips")
                window5.geometry("700x500")  
                
                
                points = [
                    "Eat a Balanced Diet: Include a variety of foods from all food groups - fruits, vegetables, whole grains, lean proteins, and healthy fats.",
                    "Portion Control: Be mindful of portion sizes to avoid overeating while ensuring you get enough nutrients.",
                    "Stay Hydrated: Drink plenty of water throughout the day to support overall health.",
                    "Limit Processed Foods: Reduce intake of sugary snacks, sodas, and fast food that can lead to weight gain."

                ]
                
                
                for tip in points:
                    lll = tk.Label(window5, text="• " + tip, anchor="w", justify="left", wraplength=550, font=("Arial", 12))
                    lll.pack(pady=5, padx=10, anchor="w") 
                t5=tk.Label(window5,text="Stay consistent with these tips and monitor your progress regularly!",font=("Arial",14,"bold")).pack(pady=10)
                t5=tk.Label(window5,text="Save reminders in calendar:",font=("Arial",14,"bold")).pack(pady=10)
                calendar = tk.Button(window5, text="Calendar",command=cal.load_Cal, font=("Arial", 14), bg="Black", fg="white")
                calendar.pack(pady=10)
                close= tk.Button(window5, text="Close", font=("Arial", 14), bg="red", fg="white", command=window5.destroy)
                close.pack(pady=10)
            def lifestyleforideal():
                window5 = tk.Toplevel(window4)  
                window5.title("Lifestyle Tips")
                window5.geometry("700x500")  
                
                
                points = [
                    "Regular Exercise: Engage in at least 150 minutes of moderate aerobic activity or 75 minutes of vigorous activity each week, along with muscle-strengthening exercises.",
                    "Maintain a Routine: Keep a consistent eating and exercise schedule to help regulate your metabolism.",
                    "Get Enough Sleep: Aim for 7-9 hours of quality sleep per night to support overall health and weight management.",
                    "Manage Stress: Practice relaxation techniques like meditation or yoga to reduce stress, which can impact weight."

                ]
                
                
                for tip in points:
                    lll = tk.Label(window5, text="• " + tip, anchor="w", justify="left", wraplength=550, font=("Arial", 12))
                    lll.pack(pady=5, padx=10, anchor="w") 
                t5=tk.Label(window5,text="Stay consistent with these tips and monitor your progress regularly!",font=("Arial",14,"bold")).pack(pady=10)
                t5=tk.Label(window5,text="Save reminders in calendar:",font=("Arial",14,"bold")).pack(pady=10)
                calendar = tk.Button(window5, text="Calendar",command=cal.load_Cal, font=("Arial", 14), bg="Black", fg="white")
                calendar.pack(pady=10)
                close= tk.Button(window5, text="Close", font=("Arial", 14), bg="red", fg="white", command=window5.destroy)
                close.pack(pady=10)
            def medical_helpforideal():
                
                window5 = tk.Toplevel(window4)  
                window5.title("Medical Help Tips")
                window5.geometry("700x500")  
                
                
                points = [
                    "Regular Health Check-ups: Schedule routine visits with your healthcare provider to monitor your overall health and catch any potential issues early.",
                    "Stay Informed: Keep up-to-date with health screenings and vaccinations as recommended for your age and health status.",
                    "Mental Health: Pay attention to your mental well-being and seek support if you experience stress, anxiety, or depression.",
                    "Healthy Habits: Avoid smoking, limit alcohol consumption, and practice safe behaviors to maintain long-term health."

                ]
                
                
                for tip in points:
                    lll = tk.Label(window5, text="• " + tip, anchor="w", justify="left", wraplength=550, font=("Arial", 12))
                    lll.pack(pady=5, padx=10, anchor="w") 
                t5=tk.Label(window5,text="Stay consistent with these tips and monitor your progress regularly!",font=("Arial",14,"bold")).pack(pady=10)
                t5=tk.Label(window5,text="Save reminders in calendar:",font=("Arial",14,"bold")).pack(pady=10)
                calendar = tk.Button(window5, text="Calendar",command=cal.load_Cal, font=("Arial", 14), bg="Black", fg="white")
                calendar.pack(pady=10)
                close= tk.Button(window5, text="Close", font=("Arial", 14), bg="red", fg="white", command=window5.destroy)
                close.pack(pady=10)
            def Dietforslightobese():
                window5 = tk.Toplevel(window4)  
                window5.title("Nutrition Tips")
                window5.geometry("700x500")  
                
                
                points = [
                    "Eat a Balanced Diet: Include a variety of foods from all food groups - fruits, vegetables, whole grains, lean proteins, and healthy fats.",
                    "Portion Control: Be mindful of portion sizes to avoid overeating while ensuring you get enough nutrients.",
                    "Stay Hydrated: Drink plenty of water throughout the day to support overall health.",
                    "Limit Processed Foods: Reduce intake of sugary snacks, sodas, and fast food that can lead to weight gain."

                ]
                
                
                for tip in points:
                    lll = tk.Label(window5, text="• " + tip, anchor="w", justify="left", wraplength=550, font=("Arial", 12))
                    lll.pack(pady=5, padx=10, anchor="w") 
                t5=tk.Label(window5,text="Stay consistent with these tips and monitor your progress regularly!",font=("Arial",14,"bold")).pack(pady=10)
                t5=tk.Label(window5,text="Save reminders in calendar:",font=("Arial",14,"bold")).pack(pady=10)
                calendar = tk.Button(window5, text="Calendar",command=cal.load_Cal, font=("Arial", 14), bg="Black", fg="white")
                calendar.pack(pady=10)
                close= tk.Button(window5, text="Close", font=("Arial", 14), bg="red", fg="white", command=window5.destroy)
                close.pack(pady=10)
            def lifestyleformildobese():
                window5 = tk.Toplevel(window4)  
                window5.title("Lifestyle Tips")
                window5.geometry("700x500")  
                
                
                points = [
                    "Regular Exercise: Engage in at least 150 minutes of moderate aerobic activity or 75 minutes of vigorous activity each week, along with muscle-strengthening exercises.",
                    "Maintain a Routine: Keep a consistent eating and exercise schedule to help regulate your metabolism.",
                    "Get Enough Sleep: Aim for 7-9 hours of quality sleep per night to support overall health and weight management.",
                    "Manage Stress: Practice relaxation techniques like meditation or yoga to reduce stress, which can impact weight."

                ]
                
                
                for tip in points:
                    lll = tk.Label(window5, text="• " + tip, anchor="w", justify="left", wraplength=550, font=("Arial", 12))
                    lll.pack(pady=5, padx=10, anchor="w") 
                t5=tk.Label(window5,text="Stay consistent with these tips and monitor your progress regularly!",font=("Arial",14,"bold")).pack(pady=10)
                t5=tk.Label(window5,text="Save reminders in calendar:",font=("Arial",14,"bold")).pack(pady=10)
                calendar = tk.Button(window5, text="Calendar",command=cal.load_Cal, font=("Arial", 14), bg="Black", fg="white")
                calendar.pack(pady=10)
                close= tk.Button(window5, text="Close", font=("Arial", 14), bg="red", fg="white", command=window5.destroy)
                close.pack(pady=10)
            def medical_helpformildobese():
                
                window5 = tk.Toplevel(window4)  
                window5.title("Medical Help Tips")
                window5.geometry("700x500")  
                
                
                points = [
                    "Regular Health Check-ups: Schedule routine visits with your healthcare provider to monitor your overall health and catch any potential issues early.",
                    "Stay Informed: Keep up-to-date with health screenings and vaccinations as recommended for your age and health status.",
                    "Mental Health: Pay attention to your mental well-being and seek support if you experience stress, anxiety, or depression.",
                    "Healthy Habits: Avoid smoking, limit alcohol consumption, and practice safe behaviors to maintain long-term health."

                ]
                
                
                for tip in points:
                    lll = tk.Label(window5, text="• " + tip, anchor="w", justify="left", wraplength=550, font=("Arial", 12))
                    lll.pack(pady=5, padx=10, anchor="w") 
                t5=tk.Label(window5,text="Stay consistent with these tips and monitor your progress regularly!",font=("Arial",14,"bold")).pack(pady=10)
                t5=tk.Label(window5,text="Save reminders in calendar:",font=("Arial",14,"bold")).pack(pady=10)
                calendar = tk.Button(window5, text="Calendar",command=cal.load_Cal, font=("Arial", 14), bg="Black", fg="white")
                calendar.pack(pady=10)
                close= tk.Button(window5, text="Close", font=("Arial", 14), bg="red", fg="white", command=window5.destroy)
                close.pack(pady=10)
            def Dietforveryobese():
                window5 = tk.Toplevel(window4)  
                window5.title("Nutrition Tips")
                window5.geometry("700x500")  
                
                
                points = [
                    "Eat a Balanced Diet: Include a variety of foods from all food groups - fruits, vegetables, whole grains, lean proteins, and healthy fats.",
                    "Portion Control: Be mindful of portion sizes to avoid overeating while ensuring you get enough nutrients.",
                    "Stay Hydrated: Drink plenty of water throughout the day to support overall health.",
                    "Limit Processed Foods: Reduce intake of sugary snacks, sodas, and fast food that can lead to weight gain."

                ]
                
                
                for tip in points:
                    lll = tk.Label(window5, text="• " + tip, anchor="w", justify="left", wraplength=550, font=("Arial", 12))
                    lll.pack(pady=5, padx=10, anchor="w") 
                t5=tk.Label(window5,text="Stay consistent with these tips and monitor your progress regularly!",font=("Arial",14,"bold")).pack(pady=10)
                t5=tk.Label(window5,text="Save reminders in calendar:",font=("Arial",14,"bold")).pack(pady=10)
                calendar = tk.Button(window5, text="Calendar",command=cal.load_Cal, font=("Arial", 14), bg="Black", fg="white")
                calendar.pack(pady=10)
                close= tk.Button(window5, text="Close", font=("Arial", 14), bg="red", fg="white", command=window5.destroy)
                close.pack(pady=10)
            def lifestyleforveryobese():
                window5 = tk.Toplevel(window4)  
                window5.title("Lifestyle Tips")
                window5.geometry("700x500")  
                
                
                points = [
                    "Regular Exercise: Engage in at least 150 minutes of moderate aerobic activity or 75 minutes of vigorous activity each week, along with muscle-strengthening exercises.",
                    "Maintain a Routine: Keep a consistent eating and exercise schedule to help regulate your metabolism.",
                    "Get Enough Sleep: Aim for 7-9 hours of quality sleep per night to support overall health and weight management.",
                    "Manage Stress: Practice relaxation techniques like meditation or yoga to reduce stress, which can impact weight."

                ]
                
                
                for tip in points:
                    lll = tk.Label(window5, text="• " + tip, anchor="w", justify="left", wraplength=550, font=("Arial", 12))
                    lll.pack(pady=5, padx=10, anchor="w") 
                t5=tk.Label(window5,text="Stay consistent with these tips and monitor your progress regularly!",font=("Arial",14,"bold")).pack(pady=10)
                t5=tk.Label(window5,text="Save reminders in calendar:",font=("Arial",14,"bold")).pack(pady=10)
                calendar = tk.Button(window5, text="Calendar",command=cal.load_Cal, font=("Arial", 14), bg="Black", fg="white")
                calendar.pack(pady=10)
                close= tk.Button(window5, text="Close", font=("Arial", 14), bg="red", fg="white", command=window5.destroy)
                close.pack(pady=10)
            def medical_helpforveryobese():
                
                window5 = tk.Toplevel(window4)  
                window5.title("Medical Help Tips")
                window5.geometry("700x500")  
                
                
                points = [
                    "Regular Health Check-ups: Schedule routine visits with your healthcare provider to monitor your overall health and catch any potential issues early.",
                    "Stay Informed: Keep up-to-date with health screenings and vaccinations as recommended for your age and health status.",
                    "Mental Health: Pay attention to your mental well-being and seek support if you experience stress, anxiety, or depression.",
                    "Healthy Habits: Avoid smoking, limit alcohol consumption, and practice safe behaviors to maintain long-term health."

                ]
                
                
                for tip in points:
                    lll = tk.Label(window5, text="• " + tip, anchor="w", justify="left", wraplength=550, font=("Arial", 12))
                    lll.pack(pady=5, padx=10, anchor="w") 
                t5=tk.Label(window5,text="Stay consistent with these tips and monitor your progress regularly!",font=("Arial",14,"bold")).pack(pady=10)
                t5=tk.Label(window5,text="Save reminders in calendar:",font=("Arial",14,"bold")).pack(pady=10)
                calendar = tk.Button(window5, text="Calendar",command=cal.load_Cal, font=("Arial", 14), bg="Black", fg="white")
                calendar.pack(pady=10)
                close= tk.Button(window5, text="Close", font=("Arial", 14), bg="red", fg="white", command=window5.destroy)
                close.pack(pady=10)
                
            if bmi_value < 18.5:
                messagebox.showinfo("You are Underweight!", "You should increase your calorie intake and consult a dietician, would you like us to show our reccomendation?")
                window2.withdraw()
                window4 = tk.Toplevel(window2)

                window4.title("Underweight Recommendations")
                window4.geometry(f"{win_w}x{win_h}")
                bg_image4 = Image.open("health-still-life-with-copy-space.jpg")
                bg_image4 = bg_image4.resize((win_w, win_h))
                bg_photo4 = ImageTk.PhotoImage(bg_image4)
                bg_label4 = tk.Label(window4, image=bg_photo4)
                bg_label4.place(x=0, y=0, relwidth=1, relheight=1)
                bg_label4.image = bg_photo4
                label=tk.Label(window4,text="Underweight Recommendations",font=("Georgia",30,"bold","underline")).pack(pady=20)
                b11=tk.Button(window4,text="Dietry changes",font=("Arial",20),command=Diet,bg="light grey",width=30,height=2).pack(pady=10)
                b12=tk.Button(window4,text="Lifestyle changes",font=("Arial",20),command=lifestyle,bg="light grey",width=30,height=2).pack(pady=10)
                b13=tk.Button(window4,text="Medical help",font=("Arial",20),command=medical_help,bg="light grey",width=30,height=2).pack(pady=10)
                b14=tk.Button(window4,text="Close",font=("Arial",20),bg="Red",width=30,height=2,command=window4.destroy).pack(pady=10)
                def back_to_menu():
                    window4.destroy()
                    window2.deiconify()

                b15 = tk.Button(window4,text="Back to Menu",font=("Arial", 15),bg="light grey",command=back_to_menu)
                b15.pack(pady=10)
                


            elif 18.5 <= bmi_value < 24.9:
                messagebox.showinfo("You have the ideal height and weight!", "Maintain your weight with a balanced diet and regular exercise, would you like us to show our reccomendation?")
                window2.withdraw()
                window4 = tk.Toplevel(window2)

                window4.title("Suggestions to maintain ideal weight")
                window4.geometry(f"{win_w}x{win_h}")
                bg_image4 = Image.open("health-still-life-with-copy-space.jpg")
                bg_image4 = bg_image4.resize((win_w, win_h))
                bg_photo4 = ImageTk.PhotoImage(bg_image4)
                bg_label4 = tk.Label(window4, image=bg_photo4)
                bg_label4.place(x=0, y=0, relwidth=1, relheight=1)
                bg_label4.image = bg_photo4
                label=tk.Label(window4,text="Tips to maintain bmi:",font=("Georgia",30,"bold","underline")).pack(pady=20)
                b11=tk.Button(window4,text="Dietry tips",font=("Arial",20),command=Dietforideal,bg="light grey",width=30,height=2).pack(pady=10)
                b12=tk.Button(window4,text="Lifestyle tips",font=("Arial",20),command=lifestyleforideal,bg="light grey",width=30,height=2).pack(pady=10)
                b13=tk.Button(window4,text="Medical tips",font=("Arial",20),command=medical_helpforideal,bg="light grey",width=30,height=2).pack(pady=10)
                b14=tk.Button(window4,text="Close",font=("Arial",20),bg="Red",width=30,height=2,command=window4.destroy).pack(pady=10)
                def back_to_menu():
                    window4.destroy()
                    window2.deiconify()

                b15 = tk.Button(window4,text="Back to Menu",font=("Arial", 15),bg="light grey",command=back_to_menu)
                b15.pack(pady=10)    
            
            elif 25 <= bmi_value < 29.9:
                messagebox.showinfo("You are slightly overweight!", "Incorporate more physical activity into your routine and monitor your diet, would you like us to show our reccomendation?")
                window2.withdraw()
                window4 = tk.Toplevel(window2)

                window4.title("Tips to reduce slight obesity")
                window4.geometry(f"{win_w}x{win_h}")
                bg_image4 = Image.open("health-still-life-with-copy-space.jpg")
                bg_image4 = bg_image4.resize((win_w, win_h))
                bg_photo4 = ImageTk.PhotoImage(bg_image4)
                bg_label4 = tk.Label(window4, image=bg_photo4)
                bg_label4.place(x=0, y=0, relwidth=1, relheight=1)
                bg_label4.image = bg_photo4
                label=tk.Label(window4,text="Obesity reccomendations:",font=("Georgia",30,"bold","underline")).pack(pady=20)
                b11=tk.Button(window4,text="Dietry tips",font=("Arial",20),command=Dietforslightobese,bg="light grey",width=30,height=2).pack(pady=10)
                b12=tk.Button(window4,text="Lifestyle tips",font=("Arial",20),command=lifestyleformildobese,bg="light grey",width=30,height=2).pack(pady=10)
                b13=tk.Button(window4,text="Medical tips",font=("Arial",20),command=medical_helpformildobese,bg="light grey",width=30,height=2).pack(pady=10)
                b14=tk.Button(window4,text="Close",font=("Arial",20),bg="Red",width=30,height=2,command=window4.destroy).pack(pady=10)
                def back_to_menu():
                    window4.destroy()
                    window2.deiconify()

                b15 = tk.Button(window4,text="Back to Menu",font=("Arial", 15),bg="light grey",command=back_to_menu)
                b15.pack(pady=10)
            else:
                messagebox.showinfo("You overweight!", "Seek guidance from a healthcare professional for a personalized weight loss plan, would you like us to show our reccomendation?")
                window2.withdraw()
                window4 = tk.Toplevel(window2)

                window4.title("Tips to reduce obesity")
                window4.geometry(f"{win_w}x{win_h}")
                bg_image4 = Image.open("health-still-life-with-copy-space.jpg")
                bg_image4 = bg_image4.resize((win_w, win_h))
                bg_photo4 = ImageTk.PhotoImage(bg_image4)
                bg_label4 = tk.Label(window4, image=bg_photo4)
                bg_label4.place(x=0, y=0, relwidth=1, relheight=1)
                bg_label4.image = bg_photo4
                label=tk.Label(window4,text="IMMEDIATE ATTENTION REQUIRED!",font=("Georgia",30,"bold","underline")).pack(pady=20)
                b11=tk.Button(window4,text="Diet",font=("Arial",20),command=Dietforveryobese,bg="light grey",width=30,height=2).pack(pady=10)
                b12=tk.Button(window4,text="Lifestyle",font=("Arial",20),command=lifestyleforveryobese,bg="light grey",width=30,height=2).pack(pady=10)
                b13=tk.Button(window4,text="Medical (RECOMMENDED)",font=("Arial",20),command=medical_helpforveryobese,bg="Maroon",width=30,height=2).pack(pady=10)
                b14=tk.Button(window4,text="Close",font=("Arial",20),bg="Red",width=30,height=2,command=window4.destroy).pack(pady=10)
                def back_to_menu():
                    window4.destroy()
                    window2.deiconify()

                b15 = tk.Button(window4,text="Back to Menu",font=("Arial", 15),bg="light grey",command=back_to_menu)
                b15.pack(pady=10)

            
            

            if a >= 0:
                status, color, highlight = bmi_status(bmi_value)
                try:
                    result_label.config(text=f"BMI: {bmi_value:.2f} ({status})", bg=color)
                    draw_bmi_chart(chart_frame, bmi_value)
                except:
                    messagebox.showerror("Error", "Enter valid numbers")

            close_button = tk.Button(window3, text="Close", font=("Arial", 24, "bold"),
                                    bg="red", fg="white", width=10, height=1,
                                    command=window3.destroy)
            close_button.pack(side="bottom", pady=30)
        exit.place(x=win_w-80, y=win_h-40)
        l11 = tk.Label(window2, text="Choose an Option:", font=("Calibri",25,"bold"), fg="Blue")
        l11.pack(side="top", pady=20)

        frame = tk.Frame(window2, bg="", highlightthickness=0)
        frame.pack(pady=20)
        b3 = tk.Button(frame, text="Calculate BMI", font=("Arial",20), command=lambda: bmi(window2), bg="Grey", width=12, height=1)
        b3.pack(side="left", padx=10, pady=10)

        b4 = tk.Button(frame, text="Track fitness", font=("Arial",20), command=trackfitness, bg="Grey", width=12, height=1)
        b4.pack(side="left", padx=10, pady=10)
       
        b5 = tk.Button(frame, text="Menstrual Cycle", font=("Arial",20), command=lambda: bmi(window2), bg="Grey", width=12, height=1)

        if n == 1:
            b5 = tk.Button(frame, text="Menstrual Cycle", font=("Arial",20), command=lambda: bmi(window2), bg="Grey", width=12, height=1)
            b5.pack(side="left", padx=10, pady=10)
        frame2 = tk.Frame(window2, bg="", highlightthickness=0)
        frame2.pack(pady=20)

        b5 = tk.Button(frame2, text="Calendar", font=("Arial",20), command=lambda:load_Calendar(), bg="Grey", width=12, height=1)
        b5.pack(side="left", padx=10, pady=10)

        b6 = tk.Button(frame2, text="Accounting", font=("Arial",20), command=lambda:load_acc_page(), bg="Grey", width=15, height=1)
        b6.pack(side="left", padx=10, pady=10)
        b9 = tk.Button(frame2, text="Sleep Tracker",font=("Arial",20), bg="Grey",width=12, height=1)
        b9.pack(side="left", padx=10, pady=10)
        bmi_frame = tk.Frame(window2, bg="")
        l12 = tk.Label(bmi_frame, text="Enter age:", font=("Rockwell",20))
        e11 = tk.Entry(bmi_frame, textvariable=age, width=40)

        l1 = tk.Label(bmi_frame, text="Enter weight:", font=("Rockwell",20))
        e1 = tk.Entry(bmi_frame, textvariable=weight, width=40)
        l2 = tk.Label(bmi_frame, text="Enter height in cm:", font=("Rockwell",20))
        e2 = tk.Entry(bmi_frame, textvariable=height, width=40)

        b4 = tk.Button(bmi_frame, text="Calculate BMI",
                        font=("Arial",20), command=calculatebmi)

        l12.pack()
        e11.pack(pady=10)
        l1.pack()
        e1.pack(pady=10)
        l2.pack()
        e2.pack(pady=10)
        b4.pack()
        

        GRAPH_WIDTH = 480
        GRAPH_HEIGHT = 240

        def bmi_status(bmi):
            if bmi < 18.5:
                return "Underweight", "red", [0, 0, 1]
            elif bmi < 25:
                return "Normal", "green", [1, 0, 0]
            elif bmi < 30:
                return "Overweight", "orange", [0, 1, 0]
            else:
                return "Obese", "red", [0, 1, 0]

        import math
        from matplotlib.patches import Wedge

        def draw_bmi_chart(chart_frame, bmi_value):
            for widget in chart_frame.winfo_children():
                widget.destroy()

            fig, ax = plt.subplots(figsize=(GRAPH_WIDTH/120, GRAPH_HEIGHT/120), dpi=100)

            wedges_info = [
                (180, 120, "orange", "Underweight"),
                (120, 60, "green", "Normal"),
                (60, 0, "red", "Overweight")
            ]

            for start, end, color, label in wedges_info:
                wedge = Wedge(center=(0,0), r=0.75, theta1=end, theta2=start, width=0.35,
                            facecolor=color, edgecolor='white')
                ax.add_patch(wedge)
                mid_angle = (start + end) / 2
                x = 0.9 * math.cos(math.radians(mid_angle))
                y = 0.9 * math.sin(math.radians(mid_angle))
                ax.text(x, y, label, ha='center', va='center', fontsize=10, fontweight='bold', color='black')

            bmi_min, bmi_max = 15, 35
            bmi_value_clamped = max(min(bmi_value, bmi_max), bmi_min)
            angle = 180 - (bmi_value_clamped - bmi_min) / (bmi_max - bmi_min) * 180
            angle_rad = math.radians(angle)
            ax.plot([0, 0.75 * math.cos(angle_rad)], [0, 0.75 * math.sin(angle_rad)], lw=3, color="black")
            ax.scatter(0, 0, s=60, color="black")

            ax.text(0, 1.15, f"Your BMI is: {bmi_value:.2f}", ha='center', va='center',
                    fontsize=16, fontweight='bold', color='black')

            ax.set_aspect("equal")
            ax.set_xlim(-1.2, 1.2)
            ax.set_ylim(0, 1.2)  
            ax.axis("off")

            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        bmi_value_label = tk.Label(window2, font=("Rockwell", 20))
        bmi_value_label.pack()

        bmi_status_label = tk.Label(window2, font=("Rockwell", 20))
        bmi_status_label.pack()

        advice_label = tk.Label(window2, font=("Rockwell", 18), wraplength=700, justify="center")
        advice_label.pack()

        def show_menu():
            bmi_frame.pack_forget()
            l11.pack(side="top", pady=20)
            frame.pack(pady=20)
            frame2.pack(pady=20)

        
        def bmi(window2):
            
            l11.pack_forget()
            
            
            frame.pack_forget()
            frame2.pack_forget()

            
            bmi_value_label.pack_forget()
            bmi_status_label.pack_forget()
            advice_label.pack_forget()
            result_label.pack_forget()

            
            bmi_frame.pack(pady=20)
            b15= tk.Button(window2, text="Back", font=("Arial", 15), bg="light grey", command=show_menu)
            b15.pack(pady=10)
            


        result_label = tk.Label(window2, text="", font=("Rockwell", 20))
        result_label.pack()

        
        


    start_btn=tk.Button(window,text="Get Started",font=("Arial", 20),bg="light grey",width=18,height=1,command=gender)
    start_btn.pack(pady=30)




    tk.mainloop()