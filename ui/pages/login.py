import tkinter as tk
import tkinter.font as tkfont
from ui.pages.base import BasePage
from PIL import Image, ImageTk

ORANGE = "#F47C2C"
WHITE = "#FFFFFF"

class LoginPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        self.configure(bg="black")

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)


        self.bg_orig = Image.open("assets/background.png")
        self.bg_image = ImageTk.PhotoImage(self.bg_orig)
        self.bg_image_id = self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        title_frame = tk.Frame(self.canvas, bg=ORANGE)


        self.title_font = tkfont.Font(family="Arial", size=32, weight="bold")
        self.btn_font = tkfont.Font(family="Arial", size=16, weight="bold")

        self.title_label = tk.Label(
            title_frame,
            text="Инвентаризация!",
            font=self.title_font,
            fg=WHITE,
            bg=ORANGE
        )
        self.title_label.pack(padx=40, pady=20)

        self.title_win = self.canvas.create_window(600, 200, window=title_frame)

        self.enter_btn = tk.Button(
            self.canvas,
            text="Войти",
            font=self.btn_font,
            bg=ORANGE,
            fg=WHITE,
            activebackground=ORANGE,
            bd=0,
            padx=30,
            pady=12,
            command=lambda: app.show("RoomsPage")
        )

        self.btn_win = self.canvas.create_window(600, 500, window=self.enter_btn)

        self.title_rel = (0.5, 0.25)
        self.btn_rel = (0.5, 0.6)
        
        self.canvas.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        w = max(1, event.width)
        h = max(1, event.height)

        try:
            resized = self.bg_orig.resize((w, h), Image.LANCZOS)
        except Exception:
            resized = self.bg_orig.resize((w, h), Image.ANTIALIAS)
        self.bg_image = ImageTk.PhotoImage(resized)
        self.canvas.itemconfig(self.bg_image_id, image=self.bg_image)

        tx = int(w * self.title_rel[0])
        ty = int(h * self.title_rel[1])
        bx = int(w * self.btn_rel[0])
        by = int(h * self.btn_rel[1])
        self.canvas.coords(self.title_win, tx, ty)
        self.canvas.coords(self.btn_win, bx, by)

        base_height = 800.0
        scale = max(0.4, h / base_height)
        new_title_size = max(12, int(32 * scale))
        new_btn_size = max(10, int(16 * scale))
        self.title_font.configure(size=new_title_size)
        self.btn_font.configure(size=new_btn_size)
