import tkinter as tk
import prop
from PIL import Image, ImageTk, ImageFilter


window = tk.Tk()
window.title("Start Page")
window.geometry("1000x1000")



name = tk.StringVar()
age = tk.StringVar()
city = tk.StringVar()
income = tk.StringVar()


bg_original = Image.open("home.jpg").resize((1000, 1000))
bg_img = ImageTk.PhotoImage(bg_original)
tk.Label(window, image=bg_img).place(x=0, y=0, relwidth=1, relheight=1)


CARD_W, CARD_H = 520, 420
CARD_X, CARD_Y = 240, 290  


blur_crop = bg_original.crop((
    CARD_X, CARD_Y,
    CARD_X + CARD_W, CARD_Y + CARD_H
)).filter(ImageFilter.GaussianBlur(18))

glass = Image.new("RGBA", blur_crop.size, (255, 255, 255, 120))
blur_crop = blur_crop.convert("RGBA")
frosted = Image.alpha_composite(blur_crop, glass)

frosted_img = ImageTk.PhotoImage(frosted)
tk.Label(window, image=frosted_img, bd=0).place(x=CARD_X, y=CARD_Y)


card = tk.Frame(window, bg="#ffffff", bd=0)
card.place(x=CARD_X, y=CARD_Y, width=CARD_W, height=CARD_H)


tk.Label(
    card,
    text="Accounting & Health Project",
    font=("Segoe UI", 20, "bold"),
    bg="#ffffff"
).pack(pady=(25, 5))

tk.Label(
    card,
    text="Enter your personal details",
    font=("Segoe UI", 11),
    fg="#555",
    bg="#ffffff"
).pack(pady=(0, 25))

def field(label, var):
    frame = tk.Frame(card, bg="#ffffff")
    frame.pack(pady=8)

    tk.Label(
        frame,
        text=label,
        font=("Segoe UI", 11),
        bg="#ffffff",
        width=15,
        anchor="w"
    ).pack(side="left", padx=10)

    tk.Entry(
        frame,
        textvariable=var,
        font=("Segoe UI", 11),
        width=25,
        relief="solid",
        bd=1
    ).pack(side="right", padx=10)

field("Full Name", name)
field("Age", age)
field("City", city)
field("Annual Income", income)


def openprofilepage():
    window.destroy()
    prop.load_prop_page({
        "name": name.get(),
        "age": age.get(),
        "city": city.get(),
        "income": income.get()
    })

btn = tk.Button(
    card,
    text="Continue",
    font=("Segoe UI", 12, "bold"),
    bg="#3b82f6",
    fg="white",
    bd=0,
    width=16,
    command=openprofilepage
)
btn.pack(pady=25)

window.mainloop()
