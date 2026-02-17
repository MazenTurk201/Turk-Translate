from customtkinter import *
import tkinter as tk
import pystray
from PIL import Image
from keyboard import add_hotkey
from pyperclip import paste
from deep_translator import GoogleTranslator
from win10toast import ToastNotifier
from time import sleep
import threading
import webbrowser

# ================== Global State ==================
target_lang = "ar"
root = None
icon = None

# ================== GUI ==================
class GuiWindow(CTk):
    def __init__(self):
        super().__init__()
        self.title("Turk Translator")
        self.geometry("300x220")
        set_appearance_mode("dark")
        self.iconbitmap("MT.ico")

        self.listbox = tk.Listbox(
            self, 
            height=5, 
            exportselection=False, 
            font=("Arial", 14), 
            selectbackground="#8a0000", 
            selectforeground="white", 
            background="#333333", 
            foreground="white", 
            highlightthickness=0, 
            bd=0,
            activestyle="none",
            selectborderwidth=0,
            borderwidth=0,
            highlightcolor="#8a0000",
            highlightbackground="#333333",
        )
        self.listbox.pack(padx=20, pady=20)

        for item in ["AR", "EN", "FR", "DE"]:
            self.listbox.insert(tk.END, item)

        CTkButton(
            self,
            text="Save Language",
            command=self.get_selection,
            fg_color="#8a0000",
            hover_color="#a00000",
            font=("Arial", 14),
            border_width=0,
            corner_radius=10,
            width=150,
            height=50
        ).pack(pady=10)

    def get_selection(self):
        global target_lang
        selection = self.listbox.get(tk.ACTIVE)
        target_lang = selection.lower()
        self.withdraw()

# ================== Translator ==================
def translate_clipboard():
    sleep(0.3)
    text = paste().strip()
    if not text:
        return

    toaster = ToastNotifier()
    result = GoogleTranslator(
        source="auto",
        target=target_lang
    ).translate(text)

    toaster.show_toast(
        "Turk Say",
        result,
        icon_path="MT.ico",
        duration=10,
        threaded=True
    )

# ================== Tray ==================
def show_app(icon, item):
    root.after(0, root.deiconify)

def quit_app(icon, item):
    icon.stop()
    root.quit()

def contact_app(icon, item):
    webbrowser.open("https://mazenturk201.github.io")

def tray():
    global icon
    icon = pystray.Icon(
        "TurkTranslator",
        Image.open("MT.ico"),
        "Turk Translator",
        pystray.Menu(
            pystray.MenuItem("Edit Language", show_app),
            pystray.MenuItem("Contact", contact_app),
            pystray.MenuItem("Quit", quit_app)
        )
    )
    icon.run()

# ================== Main ==================
if __name__ == "__main__":
    root = GuiWindow()
    root.withdraw()

    add_hotkey("ctrl+c", translate_clipboard)

    threading.Thread(target=tray, daemon=True).start()
    root.mainloop()
