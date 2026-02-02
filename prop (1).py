import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFilter

def load_prop_page(userdata):
    import hel
    import accountingpage as acc 

    profile = tk.Tk()
    profile.title("Profile Page")
    profile.geometry("1000x1000")
    profile.resizable(False, False)


    bg_original = Image.open("home.jpg").resize((1000, 1000))
    bg_img = ImageTk.PhotoImage(bg_original)
    tk.Label(profile, image=bg_img).place(x=0, y=0, relwidth=1, relheight=1)


    CARD_W, CARD_H = 600, 620
    CARD_X, CARD_Y = 200, 190

    blur_crop = bg_original.crop((
        CARD_X, CARD_Y,
        CARD_X + CARD_W, CARD_Y + CARD_H
    )).filter(ImageFilter.GaussianBlur(20))

    glass = Image.new("RGBA", blur_crop.size, (255, 255, 255, 130))
    blur_crop = blur_crop.convert("RGBA")
    frosted = Image.alpha_composite(blur_crop, glass)

    frosted_img = ImageTk.PhotoImage(frosted)
    tk.Label(profile, image=frosted_img).place(x=CARD_X, y=CARD_Y)

    card = tk.Frame(profile, bg="#ffffff")
    card.place(x=CARD_X, y=CARD_Y, width=CARD_W, height=CARD_H)


    header = tk.Frame(card, bg="#ffffff")
    header.pack(pady=30)


    size = (90, 90)
    try:
        pfp = Image.open("pfp.jpg").resize(size, Image.Resampling.LANCZOS)
        mask = Image.new("L", size, 0)
        ImageDraw.Draw(mask).ellipse((0, 0) + size, fill=255)
        pfp.putalpha(mask)
        pfp_img = ImageTk.PhotoImage(pfp)
        tk.Label(header, image=pfp_img, bg="#ffffff").pack(side="left")
    except:
        pfp_img = None

    tk.Label(
        header,
        text="Your Profile",
        font=("Segoe UI", 22, "bold"),
        bg="#ffffff"
    ).pack(side="left")


    info = tk.Frame(card, bg="#ffffff")
    info.pack(pady=30)

    def row(label, value):
        r = tk.Frame(info, bg="#ffffff")
        r.pack(fill="x", pady=10, padx=60)

        tk.Label(
            r,
            text=label,
            font=("Segoe UI", 12),
            fg="#666",
            bg="#ffffff"
        ).pack(side="left",padx=10)

        tk.Label(
            r,
            text=value,
            font=("Segoe UI", 14, "bold"),
            fg="#2563eb",
            bg="#ffffff"
        ).pack(side="right",padx=10)

    row("Name", userdata.get("name", "N/A"))
    row("Age", userdata.get("age", "N/A"))
    row("City", userdata.get("city", "N/A"))
    row("Annual Income", userdata.get("income", "N/A"))\
    
    def openaccpage():
        profile.destroy()
        acc.load_acc_page()

    def openhealthpage():
        profile.destroy()
        hel.load_hel_page()

    actions = tk.Frame(card, bg="#ffffff")
    actions.pack(pady=30)

    tk.Button(
        actions,
        text="Health",
        font=("Segoe UI", 12, "bold"),
        bg="#22c55e",
        fg="white",
        width=16,
        bd=0,
        pady=10,
        command=openhealthpage
    ).pack(side="left", padx=20)

    tk.Button(
        actions,
        text="Accounting",
        font=("Segoe UI", 12, "bold"),
        bg="#3b82f6",
        fg="white",
        width=16,
        bd=0,
        pady=10,
        command=openaccpage
    ).pack(side="right", padx=20)


    tk.Button(
        card,
        text="Logout",
        font=("Segoe UI", 11, "bold"),
        fg="#ef4444",
        bg="#ffffff",
        bd=1,
        relief="solid",
        width=20,
        pady=8,
        command=profile.destroy
    ).pack(side="bottom", pady=30)

    profile.mainloop()
