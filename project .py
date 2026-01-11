import tkinter as tk
import prop
from tkinter.ttk import Label
from PIL import Image, ImageTk
window=tk.Tk()

window.title("Start Page")
window.geometry("1000x1000")

name = tk.StringVar()
age = tk.StringVar()
city = tk.StringVar()
income = tk.StringVar()

original_image = Image.open("home.jpg")
o = original_image.resize((1000, 1000), Image.Resampling.LANCZOS)
bg_img = ImageTk.PhotoImage(o)

def openprofilepage():
    userdata= {
        'name': name.get(),
        'age': age.get(),
        'city': city.get(),
        'income': income.get()
    }
           
    window.destroy()
    prop.load_prop_page(userdata)
def info():
    row=tk.Frame(window,bg="lightblue")
    row.pack(fill='x',padx=325,pady=10)
    l1=tk.Label(row,text="Enter Name:",font=("Lucida Fax",15),bg="lightblue").pack()
    t1=tk.Entry(row,textvariable=name).pack()
    l2=tk.Label(row,text="Enter Age:",font=("Lucida Fax",15),bg="lightblue").pack()
    t2=tk.Entry(row,textvariable=age).pack()
            
    row1=tk.Frame(window,height=30,width=60,bg="lightblue")
    row1.pack(fill='x',padx=325)
    l3=tk.Label(row1,text="Enter city:",font=("Lucida Fax",15),bg="lightblue").pack()
    t3=tk.Entry(row1,textvariable=city).pack()
    l4=tk.Label(row1,text="Enter annual income:",font=("Lucida Fax",15),bg="lightblue").pack()
    t4=tk.Entry(row1,textvariable=income,).pack()
            
    row2= tk.Frame(window,bg="lightblue")
    row2.pack(fill='x',padx=10,pady=10 )
    l5=tk.Label(window,text="please proceed",font=("Lucida Fax",15),bg="lightblue").pack()
    b3=tk.Button(window, text="Continue", bg="lightblue",command=openprofilepage)
    b3.pack()

background_label = tk.Label(window, image=bg_img)
background_label.place(x=0, y=0)

label=tk.Label(text="Accounting and Health Project",font=("Rockwell",20),bg="lightblue").pack(pady=20)
b2=tk.Button(window,text="Get Started",font=("Lucida Fax",15),bg="lightblue",command=info).pack()
window.title("Start Page")
window.mainloop()


