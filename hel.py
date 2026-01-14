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
    weight=tk.IntVar()
    height=tk.IntVar()
    age=tk.IntVar()
    num1=tk.StringVar()
    num2=tk.IntVar()
    num3=tk.StringVar()
    num4=tk.IntVar()
    def load_Calendar():
        
        
        window.destroy() 
        
        cal.load_Cal()



    l1=tk.Label(window,text="User Health Details",font=("Georgia",50,"bold","underline")).pack()
    l1=tk.Label(window,text="General health:",font=("Calibri",25,"bold"),fg="Blue").pack(pady=0)
    n = 0
    def gsm():
        yes()
        """frame2 = tk.Frame(window)
        l1=tk.Label(window,text="would you like to proceed",font=("Rockwell",20)).pack(pady=20)
        frame2 = tk.Frame(window)
        frame2.pack()

        b1 = tk.Button(frame2, text="Yes",font=("Arial",20), command=yes, bg="Green",width=12, height=1)
        b1.pack(side="left", padx=10, pady=10)


        b2 = tk.Button(frame2, text="No",font=("Arial",20), command=no, bg="Red",width=12, height=1)
        b2.pack(side="left", padx=10, pady=10)"""
    def gsf():
        global n
        n=1
        print(n)
        yes()
        """frame2 = tk.Frame(window)
        l1=tk.Label(window,text="would u like to proceed?",font=("Rockwell",20)).pack(pady=20)
        frame2 = tk.Frame(window)
        frame2.pack()

        b1 = tk.Button(frame2, text="Yes",font=("Arial",20), command=yes, bg="Green",width=12, height=1)
        b1.pack(side="left", padx=10, pady=10)


        b2 = tk.Button(frame2, text="No",font=("Arial",20), command=no, bg="Red",width=12, height=1)
        b2.pack(side="left", padx=10, pady=10)"""
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
            command=window2.destroy
        )
        exit.place(x=win_w-80, y=win_h-40)

        def bmi(window2):
            l11 = tk.Label(window2, text="Enter age:", font=("Rockwell",20)).pack()
            e11 = tk.Entry(window2, textvariable=age, width=40).pack(pady=10)
            l1 = tk.Label(window2, text="Enter weight:", font=("Rockwell",20)).pack()
            e1 = tk.Entry(window2, textvariable=weight, width=40).pack(pady=10)
            l2 = tk.Label(window2, text="Enter height in cm:", font=("Rockwell",20)).pack()
            e2 = tk.Entry(window2, textvariable=height, width=40).pack(pady=10)
            b4 = tk.Button(window2, text="Calculate BMI", font=("Arial",20), command=calculatebmi).pack()

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

            
            """text_frame = tk.Frame(content_frame, bg="")
            text_frame.pack(side="left", fill="both", expand=True, padx=30, pady=30)"""

            
            """text_bg_image = Image.open("bg4.jpg")

            
            desired_width = int(win_w * 0.4)   
            desired_height = int(win_h * 0.8)
            text_bg_image = text_bg_image.resize((desired_width, desired_height))
            text_bg_photo = ImageTk.PhotoImage(text_bg_image)
            text_bg_label = tk.Label(text_frame, image=text_bg_photo)
            text_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            text_bg_label.image = text_bg_photo"""
            graph_container = tk.Frame(content_frame, bg="")
            graph_container.pack(side="right", fill="both", expand=True, padx=60, pady=30)

            chart_frame = tk.Frame(graph_container, bg="", highlightthickness=0)
            chart_frame.pack(padx=30,fill="both", expand=True)
            a = int(age.get())
            w = float(weight.get())
            h = float(height.get())/100
            bmi_value = w / (h*h)
            text_frame2=tk.Frame(window3)
            root = tk.Tk()
            root.withdraw()

            
            
            if bmi_value < 18.5:
                messagebox.showinfo("You are Underweight!", "You should increase your calorie intake and consult a dietician, would you like us to show our reccomendation?")
                root.destroy()
                
            elif 18.5 <= bmi_value < 24.9:
                messagebox.showinfo("You have the ideal height and weight!", "Maintain your weight with a balanced diet and regular exercise, would you like us to show our reccomendation?")
                root.destroy()
            elif 25 <= bmi_value < 29.9:
                messagebox.showinfo("You are slightly overweight!", "Incorporate more physical activity into your routine and monitor your diet, would you like us to show our reccomendation?")
                root.destroy()
            else:
                messagebox.showinfo("You overweight!", "Seek guidance from a healthcare professional for a personalized weight loss plan, would you like us to show our reccomendation?")
                root.destroy()

            
            if a > 18:
                if bmi_value < 18.5:
                    advice = "You should increase your calorie intake and consult a dietician, would you like us to show our reccomendation"
                elif 18.5 <= bmi_value < 24.9:
                    advice = "Maintain your weight with a balanced diet and regular exercise, would you like us to show our reccomendation"
                elif 25 <= bmi_value < 29.9:
                    advice = "Incorporate more physical activity into your routine and monitor your diet, would you like us to show our reccomendation?"
                else:
                    advice = "Seek guidance from a healthcare professional for a personalized weight loss plan, would you like us to show our reccomendation"
                l5 = tk.Label(chart_frame,text=advice, font=("Rockwell",20), justify="center", wraplength=400).pack(fill="x", pady=10)

            if a > 18:
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

        result_label = tk.Label(window2, text="", font=("Rockwell", 20))
        result_label.pack()

        

        l1 = tk.Label(window2, text="Choose an Option:", font=("Calibri",25,"bold"), fg="Blue").pack(pady=0)
        frame = tk.Frame(window2, bg="", highlightthickness=0)
        frame.pack(pady=20)
        b3 = tk.Button(frame, text="Calculate BMI", font=("Arial",20), command=lambda: bmi(window2), bg="Grey", width=12, height=1)
        b3.pack(side="left", padx=10, pady=10)

        b4 = tk.Button(frame, text="Track fitness", font=("Arial",20), command=lambda: bmi(window2), bg="Grey", width=12, height=1)
        b4.pack(side="left", padx=10, pady=10)
        print(n)
        b5 = tk.Button(frame, text="Menstrual Cycle", font=("Arial",20), command=lambda: bmi(window2), bg="Grey", width=12, height=1)


        if n == 1:
            b5 = tk.Button(frame, text="Menstrual Cycle", font=("Arial",20), command=lambda: bmi(window2), bg="Grey", width=12, height=1)
            b5.pack(side="left", padx=10, pady=10)
        frame2 = tk.Frame(window2, bg="", highlightthickness=0)
        frame2.pack(pady=20)

        b5 = tk.Button(frame2, text="Calendar", font=("Arial",20), command=lambda:load_Calendar(), bg="Grey", width=12, height=1)
        b5.pack(side="left", padx=10, pady=10)

        b6 = tk.Button(frame2, text="Accounting", font=("Arial",20), command=lambda: bmi(window2), bg="Grey", width=15, height=1)
        b6.pack(side="left", padx=10, pady=10)
        b9 = tk.Button(frame2, text="Sleep Tracker",font=("Arial",20), bg="Grey",width=12, height=1)
        b9.pack(side="left", padx=10, pady=10)

    def no():
        window2 = tk.Toplevel(window)
        screen_w = window2.winfo_screenwidth()
        screen_h = window2.winfo_screenheight()
        win_w = int(screen_w * 0.75)
        win_h = int(screen_h * 0.75)
        window2.geometry(f"{win_w}x{win_h}")
        bg_image = Image.open("bg3.jpg")
        bg_image = bg_image.resize((win_w, win_h))
        bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(window2, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        exit_button = tk.Button(window2, text="Exit", font=("Arial",10),
                            bg="light grey", width=5, height=1,
                            command=window2.destroy)
        exit_button.place(x=win_w-80, y=10)  

        def calculatebmi():
            w=weight.get()
            h=height.get()/100
            bmi_value=w/(h*h)
            l3=tk.Label(window2,text=f"Your BMI is:{bmi_value:.2f}",font=("Rockwell",20)).pack()
        def bmi(window2):
            l11 = tk.Label(window2, text="Enter age:", font=("Rockwell",20)).pack()
            e11 = tk.Entry(window2, textvariable=age, width=40).pack(pady=10)
            l1 = tk.Label(window2, text="Enter weight:", font=("Rockwell",20)).pack()
            e1 = tk.Entry(window2, textvariable=weight, width=40).pack(pady=10)
            l2 = tk.Label(window2, text="Enter height in cm:", font=("Rockwell",20)).pack()
            e2 = tk.Entry(window2, textvariable=height, width=40).pack(pady=10)
            b4 = tk.Button(window2, text="Calculate BMI", font=("Arial",20), command=calculatebmi).pack()   

        
        bg_label.image = bg_photo
        frame = tk.Frame(window2, bg="", highlightthickness=0)
        frame.pack(pady=0)
        window2.title("Finance")
        
        
        GRAPH_WIDTH = 600
        GRAPH_HEIGHT = 300

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

            fig, ax = plt.subplots(figsize=(GRAPH_WIDTH/100, GRAPH_HEIGHT/100), dpi=100)

            
            wedges_info = [
                (180, 120, "orange", "Underweight"),
                (120, 60, "green", "Normal"),
                (60, 0, "red", "Overweight")
            ]

            for start, end, color, label in wedges_info:
                wedge = Wedge(center=(0,0), r=1, theta1=end, theta2=start, width=0.35,
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
            ax.plot([0, 0.85 * math.cos(angle_rad)], [0, 0.85 * math.sin(angle_rad)], lw=3, color="black")
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
            content_frame.pack(fill="both", expand=True)

            
            text_frame = tk.Frame(content_frame, bg="")
            text_frame.pack(side="left", fill="both", expand=True, padx=30, pady=30)
            text_bg_image = Image.open("bg4.jpg")

            
            desired_width = int(win_w * 0.4)   
            desired_height = int(win_h * 0.8)  
            text_bg_image = text_bg_image.resize((desired_width, desired_height))

            text_bg_photo = ImageTk.PhotoImage(text_bg_image)
            text_bg_label = tk.Label(text_frame, image=text_bg_photo)
            text_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            text_bg_label.image = text_bg_photo

            graph_container = tk.Frame(content_frame, bg="")
            graph_container.pack(side="right", fill="both", expand=True, padx=30, pady=30)

            chart_frame = tk.Frame(graph_container, bg="", highlightthickness=0)
            chart_frame.pack(fill="both", expand=True)

            a = int(age.get())
            w = float(weight.get())
            h = float(height.get())/100
            bmi_value = w / (h*h)
            if bmi_value < 18.5:
                l4 = tk.Label(text_frame, anchor="w", text="\n\n\n\n\n\n      You are underweight", font=("Rockwell",20), bg="Red",
                            justify="center", wraplength=400).pack(fill="x", pady=10)
            elif 18.5 <= bmi_value < 24.9:
                l4 = tk.Label(text_frame, anchor="w", text="\n\n\n\n\n\n   You have a normal weight", font=("Rockwell",20), bg="Green",
                            justify="center", wraplength=400).pack(fill="x", pady=10)
            elif 25 <= bmi_value < 29.9:
                l4 = tk.Label(text_frame, anchor="w", text="\n\n\n\n\n\nYou are slighty over normal weight requirements", font=("Rockwell",20), bg="Orange",
                            justify="center", wraplength=400).pack(fill="x", pady=10)
            else:
                l4 = tk.Label(text_frame, anchor="w", text="\n\n\n\n\n\n       You are obese", font=("Rockwell",20), bg="Red",
                            justify="center", wraplength=400).pack(fill="x", pady=10)

            
            if a > 18:
                if bmi_value < 18.5:
                    l5 = tk.Label(text_frame, anchor="w", text="You should increase your calorie intake and consult a dietician.", font=("Rockwell",20),
                                justify="left", wraplength=400).pack(fill="x", pady=10)
                elif 18.5 <= bmi_value < 24.9:
                    l5 = tk.Label(text_frame, anchor="w", text="Maintain your weight with a balanced diet and regular exercise.", font=("Rockwell",20),
                                justify="left", wraplength=400).pack(fill="x", pady=10)
                elif 25 <= bmi_value < 29.9:
                    l5 = tk.Label(text_frame, anchor="w", text="Incorporate more physical activity into your routine and monitor your diet.", font=("Rockwell",20),
                                justify="left", wraplength=400).pack(fill="x", pady=10)
                else:
                    l5 = tk.Label(text_frame, anchor="w", text="Seek guidance from a healthcare professional for a personalized weight loss plan.", font=("Rockwell",20),
                                justify="left", wraplength=400).pack(fill="x", pady=10)

            if a > 18:
                status, color, highlight = bmi_status(bmi_value)
                try:
                    result_label.config(text=f"BMI: {bmi_value:.2f} ({status})", bg=color)
                    draw_bmi_chart(chart_frame, bmi_value)
                except:
                    messagebox.showerror("Error", "Enter valid numbers")

        
            close_button = tk.Button(window3, text="Close", font=("Arial", 24, "bold"),
                                    bg="red", fg="white", width=20, height=2,
                                    command=window3.destroy)
            close_button.pack(side="bottom", pady=30)

        result_label = tk.Label(window2, text="", font=("Rockwell", 20))
        result_label.pack()

        frame = tk.Frame(window2, bg="", highlightthickness=0)
        frame.pack(pady=0)

        l1 = tk.Label(window2, text="Choose an Option:", font=("Calibri",25,"bold"), fg="Blue").pack(pady=0)
        b3 = tk.Button(frame, text="Calculate BMI", font=("Arial",20), command=lambda: bmi(window2), bg="Grey", width=12, height=1)
        b3.pack(side="left", padx=10, pady=10)

        b4 = tk.Button(frame, text="Accounting page",font=("Arial",20), command=lambda: bmi(window2), bg="Grey",width=12, height=1)
        b4.pack(side="left", padx=10, pady=10)
       
        frame2 = tk.Frame(window2, bg="", highlightthickness=0)
        frame2.pack(pady=0)
        
        
        b8 = tk.Button(frame2, text="Calender",font=("Arial",20), command=lambda: bmi(window2), bg="Grey",width=12, height=1)
        b8.pack(side="left", padx=10, pady=10)
        b9 = tk.Button(frame2, text="Graph",font=("Arial",20), command=lambda: bmi(window2), bg="Grey",width=12, height=1)
        b9.pack(side="left", padx=10, pady=10)
        


    start_btn=tk.Button(window,text="Get Started",font=("Arial", 20),bg="light grey",width=18,height=1,command=gender)
    start_btn.pack(pady=30)




    tk.mainloop()