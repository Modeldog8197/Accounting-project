'''import tkinter as tk
from matplotlib import pyplot as plt
import numpy as np 

def load_pirgraph1_page():
    graph_window = tk.Toplevel()
    graph_window.title(f"Income Distribution")
    graph_window.geometry("800x600")
        
    datavalues = [34, 20, 55]
    names = ['Income', 'Expenses', 'Savings']
    fig=plt.figure(figsize=(10,7))
    plt.pie(datavalues,labels=names)
    plt.show()
    graph_window.mainloop()'''

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def load_pirgraph1_page(datavalues, names):
    graph_window = tk.Toplevel() 
    graph_window.title("Expense Distribution")
    graph_window.geometry("800x600")
        
    fig = Figure(figsize=(7, 6), dpi=100)
    ax = fig.add_subplot(111)

    ax.pie(datavalues, labels=names, autopct='%1.1f%%', startangle=140)
    ax.set_title("Financial Summary")

    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

