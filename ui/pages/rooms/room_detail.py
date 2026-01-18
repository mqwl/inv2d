import tkinter as tk
import tkinter.font as tkfont
from ui.pages.base import BasePage

ORANGE = "#F47C2C"
WHITE = "#FFFFFF"


class RoomDetailPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        self.small_font = tkfont.Font(family="Arial", size=10)

        
        back_btn = tk.Button(self, text="Назад", bg=ORANGE, fg=WHITE, font=self.small_font, bd=0,
                             padx=8, pady=4, command=lambda: app.show('RoomsPage'))
        back_btn.place(relx=0.01, rely=0.02, anchor='nw')

        self.header = tk.Frame(self, bg=ORANGE)
        
        self.header.place(relx=0.5, rely=0.02, anchor='n', relwidth=0.7, relheight=0.10)
        self.header_label = tk.Label(self.header, text="Помещение", bg=ORANGE, fg=WHITE, font=("Arial", 16, "bold"))
        self.header_label.pack(expand=True)

        
        self.left_frame = tk.Frame(self, bg=self.default_bg)
        self.left_frame.place(relx=0.02, rely=0.14, relwidth=0.28, relheight=0.82)

        self.right_frame = tk.Frame(self, bg=self.default_bg)
        self.right_frame.place(relx=0.32, rely=0.14, relwidth=0.66, relheight=0.82)

        
        buttons = [
            "Список коробок",
            "Список объектов",
            "Список запретных зон",
            "Эффективно занять пространство",
            "Просмотр помещения полностью",
        ]

        self.left_buttons = []
        for i, t in enumerate(buttons):
            b = tk.Button(self.left_frame, text=t, bg=ORANGE, fg=WHITE, bd=0)
            b.pack(fill='x', pady=(6 if i==0 else 4, 4), padx=6)
            self.left_buttons.append(b)

        
        self.canvas = tk.Canvas(self.right_frame, bg="#ffffff", highlightthickness=1, highlightbackground="#000000")
        self.canvas.pack(fill='both', expand=True, padx=6, pady=6)

    def on_show(self):
        
        room_id = getattr(self.app, 'current_room_id', None)
        if room_id is None:
            self.header_label.config(text="Помещение")
            self.canvas.delete('all')
            return

        
        try:
            cur = self.app.con.cursor()
            cur.execute("SELECT id, length, width, height FROM room WHERE id = ?", (room_id,))
            row = cur.fetchone()
            cur.close()
        except Exception:
            row = None

        if not row:
            self.header_label.config(text=f"Помещение {room_id} (не найдено)")
            self.canvas.delete('all')
            return

        rid, length, width, height = row
        self.header_label.config(text=f"Помещение {rid}")

        
        self.canvas.delete('all')
        cw = self.canvas.winfo_width() or 400
        ch = self.canvas.winfo_height() or 300

        # Scale room to fit canvas with margin
        margin = 20
        available_w = max(10, cw - 2 * margin)
        available_h = max(10, ch - 2 * margin)

        # room length and width are in cm; scale preserving aspect ratio
        if width == 0 or length == 0:
            return
        scale = min(available_w / width, available_h / length)

        rw = width * scale
        rh = length * scale

        x0 = (cw - rw) / 2
        y0 = (ch - rh) / 2
        x1 = x0 + rw
        y1 = y0 + rh

        # Draw room rectangle
        self.canvas.create_rectangle(x0, y0, x1, y1, fill="#f0f0f0", outline=ORANGE, width=3)
        # Label dimensions inside
        self.canvas.create_text((cw/2, y0+10), text=f"{int(length)} x {int(width)} (cm)", anchor='n')
