import tkinter as tk
import tkinter.font as tkfont
from ui.pages.base import BasePage

ORANGE = "#F47C2C"
WHITE = "#FFFFFF"


class RoomsPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        
        self.small_font = tkfont.Font(family="Arial", size=10)
        self.btn_font = tkfont.Font(family="Arial", size=12, weight="bold")
        
        back_btn = tk.Button(
            self,
            text="Назад",
            command=lambda: app.show("LoginPage"),
            bg=ORANGE,
            fg=WHITE,
            font=self.small_font,
            bd=0,
            padx=8,
            pady=6,
        )
        back_btn.place(relx=0.01, rely=0.01, anchor="nw")

        menu_relheight = 0.16
        menu_frame = tk.Frame(self, bg=self.default_bg)
        menu_frame.place(relx=0, rely=0.06, relwidth=1.0, relheight=menu_relheight)

        menu_inner = tk.Frame(menu_frame, bg=self.default_bg)
        menu_inner.place(relx=0.5, rely=0.5, anchor="center")

        btn_names = [
            ("Добавить помещение", "RoomCreatePage"),
            ("Удалить помещение", "RoomDeletePage"),
            ("Редактировать помещение", "RoomEditPage"),
        ]


        left_margin = 0.04
        gap = 0.03
        btn_relwidth = (1.0 - 2 * left_margin - 2 * gap) / 3.0

        for i, (text, page_name) in enumerate(btn_names):
            relx = left_margin + i * (btn_relwidth + gap)
            b = tk.Button(
                menu_frame,
                text=text,
                bg=ORANGE,
                fg=WHITE,
                font=self.btn_font,
                bd=0,
                command=lambda p=page_name: app.show(p)
            )
            b.place(relx=relx, rely=0.0, relwidth=btn_relwidth, relheight=1.0)

        
        self.grid_top_rel = 0.06 + menu_relheight + 0.05
        self.grid_frame = None
        
        self.render_grid(app)

    def render_grid(self, app):
        
        if self.grid_frame is not None:
            try:
                self.grid_frame.destroy()
            except Exception:
                pass
        
        rooms = []
        try:
            con = app.con
            cur = con.cursor()
            cur.execute("SELECT id, length, width, height FROM room;")
            rooms = cur.fetchall()
            cur.close()
        except Exception:
            rooms = []

        if not rooms:
            self.grid_frame = None
            return
        
        self.grid_frame = tk.Frame(self, bg=self.default_bg)
        self.grid_frame.place(relx=0, rely=self.grid_top_rel, relwidth=1.0, relheight=1.0 - self.grid_top_rel)
        
        item_relwidth = 0.22
        item_step = 0.24
        item_relheight = 0.18
        
        vertical_gap = 0.05

        for idx, row in enumerate(rooms):
            col = idx % 4
            r = idx // 4
            relx = 0.02 + col * item_step
            rely = r * (item_relheight + vertical_gap)
            text = f"Помещение {row[0]}"
            item = tk.Button(
                self.grid_frame,
                text=text,
                bg="#FFFFFF",
                fg="#000000",
                bd=1,
                relief="solid",
                wraplength=200,
                command=(lambda r=row[0], a=app: (a.__setattr__('current_room_id', r), a.show('RoomDetailPage')))
            )
            item.place(relx=relx, rely=rely, relwidth=item_relwidth, relheight=item_relheight)

    def refresh(self, app):
        """Перерисовать список помещений (вызывать после изменений в БД)."""
        self.render_grid(app)
