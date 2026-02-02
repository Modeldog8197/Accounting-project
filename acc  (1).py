import tkinter as tk
from PIL import Image, ImageTk
import pirgraph1

def load_acc_page():
    window = tk.Tk()
    window.title("Accounting Home Page")
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    win_w = int(screen_w * 0.75)
    win_h = int(screen_h * 0.75)
    window.geometry(f"{win_w}x{win_h}")
    bg_image = Image.open("aacoutingbg.jpg.jpg")  
    bg_image = bg_image.resize((win_w, win_h))
    bg_photo = ImageTk.PhotoImage(bg_image)
     
    bg_label = tk.Label(window, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    numg = tk.IntVar()
    numf = tk.IntVar()
    numc = tk.IntVar()
    nums = tk.IntVar()
    num1 = tk.IntVar()
    num2 = tk.IntVar()
    num3 = tk.IntVar()

    def info():
        btn.config(state="disabled")

        row = tk.Frame(window, bg="lightblue")
        row.pack()

        tk.Label(row, text="luxuries(clothing shopping etc").pack()
        tk.Entry(row, textvariable=numg).pack()

        tk.Label(row, text="Food").pack()
        tk.Entry(row, textvariable=numf).pack()

        tk.Label(row, text="entertainment").pack()
        tk.Entry(row, textvariable=numc).pack()

        tk.Label(row, text="Monthly Savings").pack()
        tk.Entry(row, textvariable=nums).pack()

    def med():
        btm.config(state="disabled")
        
        row1 = tk.Frame(window, bg="lightblue")
        row1.pack()

        tk.Label(row1, text="Tests in General").pack()
        tk.Entry(row1, textvariable=num1).pack()

        tk.Label(row1, text="Medicines").pack()
        tk.Entry(row1, textvariable=num2).pack()

        tk.Label(row1, text="General Visits").pack()
        tk.Entry(row1, textvariable=num3).pack()
    def openpiegraph():
        data =[
            numg.get(),
            numf.get(),
            numc.get(),
            nums.get(),
            num1.get(),
            num2.get(),
            num3.get()
        ]
        labels = ['Luxuries', 'Food', 'Entertainment', 'Savings', 'Tests', 'Meds', 'Visits']
        pirgraph1.load_pirgraph1_page(data, labels)

    label = tk.Label(window, text="Accounting Home Page", font=("Rockwell", 20))
    label.pack(pady=10)

    btn = tk.Button(window, text="General Expenditure", command=info,bg="Lightblue",font=("Lucida Fax",10),width=15,height=3)
    btn.pack(pady=10)
    btm = tk.Button(window, text="medical expenses",command=med,bg="Lightblue",font=("Lucida Fax",10),width=15,height=3)
    btm.pack(pady=10)
    btg=tk.Button(window,text="graph",command=info,bg="Lightblue",font=("Lucida Fax",10),width=15,height=3)
    btg.pack(side="left",padx=10,pady=10)
    btp=tk.Button(window,text="piegraph",command=openpiegraph,bg="Lightblue",font=("Lucida Fax",10),width=15,height=3)
    btp.pack(side="left",padx=10,pady=10)
    btb=tk.Button(window,text="bargraph",command=info,bg="Lightblue",font=("Lucida Fax",10),width=15,height=3)
    btb.pack(side="left",padx=10,pady=10)

    tk.mainloop()

load_acc_page()
