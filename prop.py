
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk, ImageDraw



def load_prop_page(userdata):
    import hel
    profile = tk.Tk()
    profile.title("Profile Page")
    profile.geometry("600x750")
    profile.configure(bg="#222222") 

    def openhealthpage():
        
        profile.destroy() 
        
        hel.load_hel_page()

    style = ttk.Style()
    style.theme_use('clam') 
    style.configure("TFrame", background="#222222")
    style.configure("TLabel", background="#222222", foreground="white")

    top_frame = ttk.Frame(profile, padding=40)
    top_frame.pack(fill="x")

    size = (80, 80)
    try:
        pfp_image = Image.open("pfp.jpg").resize(size, Image.Resampling.LANCZOS)
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        pfp_image.putalpha(mask)
        profile.pfp_photo = ImageTk.PhotoImage(pfp_image)
    except:
        profile.pfp_photo = None

    logo_canvas = tk.Canvas(top_frame, width=100, height=100, highlightthickness=0, bg="#222222")
    logo_canvas.pack(side="left")
    if profile.pfp_photo:
        logo_canvas.create_image(50, 50, image=profile.pfp_photo)

    heading = tk.Label(top_frame, text="Your Profile", font=("Helvetica", 32, "bold"), fg="white", bg="#222222")
    heading.pack(side="left", expand=True)

    grid_frame = ttk.Frame(profile, padding=(60, 20, 60, 40))
    grid_frame.pack(fill="both", expand=True)

    def create_row(row_idx, label_text, value_text):
        tk.Label(grid_frame, text=label_text, font=("Helvetica", 16),
                 fg="#bbbbbb", bg="#222222").grid(row=row_idx, column=0, sticky="w", pady=12, padx=(0, 20))
        
        tk.Label(grid_frame, text=value_text, font=("Helvetica", 18, "bold"),
                 fg="#1abc9c", bg="#222222").grid(row=row_idx, column=1, sticky="e", pady=12)

    create_row(0, "Name", userdata.get('name', 'N/A'))
    create_row(1, "Age", userdata.get('age', 'N/A'))
    create_row(2, "City", userdata.get('city', 'N/A'))
    create_row(3, "Income", userdata.get('income', 'N/A'))

    grid_frame.grid_columnconfigure(0, weight=1)
    grid_frame.grid_columnconfigure(1, weight=1)
    
    buttons_frame = ttk.Frame(profile, padding=(60, 0, 60, 30))
    buttons_frame.pack(fill="x")

    tk.Button(buttons_frame, text="Health", bg="#2ecc71", fg="black", 
              font=("Helvetica", 12, "bold"), width=15, pady=10,command=openhealthpage).pack(side="left", padx=15, expand=True)

    tk.Button(buttons_frame, text="Accounting",bg="#3498db", fg="black", 
              font=("Helvetica", 12, "bold"), width=15, pady=10).pack(side="right", padx=15, expand=True)

    logout_frame = ttk.Frame(profile, padding=40)
    logout_frame.pack(fill="x", side="bottom")

    logout_btn = tk.Button(logout_frame, text="Logout", fg="black", bg="#222222",
                           command=profile.destroy, 
                           activeforeground="white", activebackground="#e74c3c",
                           font=("Helvetica", 12, "bold"), width=25, pady=8, 
                           highlightbackground="#e74c3c", relief="flat", bd=1)
    logout_btn.pack(anchor="center")

    profile.mainloop()
