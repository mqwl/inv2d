import tkinter as tk
import tkinter.font as tkfont
from ui.pages.base import BasePage
import queries

ORANGE = "#F47C2C"
WHITE = "#FFFFFF"


class RestrictedCreatePage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        block = tk.Frame(self, bg=self.default_bg)
        block.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.6, relheight=0.45)

        tk.Label(block, text="Введите данные запретной зоны", font=("Arial", 14, "bold"), fg="#000000", bg=self.default_bg).pack(pady=(10, 6))

        fields = tk.Frame(block, bg=self.default_bg)
        fields.pack(pady=8)

        tk.Label(fields, text="Длина", bg=self.default_bg).grid(row=0, column=0, padx=6, sticky='w')
        self.e_length = tk.Entry(fields, bg=WHITE)
        self.e_length.grid(row=1, column=0, padx=6, pady=4)

        tk.Label(fields, text="Ширина", bg=self.default_bg).grid(row=0, column=1, padx=6, sticky='w')
        self.e_width = tk.Entry(fields, bg=WHITE)
        self.e_width.grid(row=1, column=1, padx=6, pady=4)

        tk.Label(fields, text="Координата X", bg=self.default_bg).grid(row=2, column=0, padx=6, sticky='w')
        self.e_x = tk.Entry(fields, bg=WHITE)
        self.e_x.grid(row=3, column=0, padx=6, pady=4)

        tk.Label(fields, text="Координата Y", bg=self.default_bg).grid(row=2, column=1, padx=6, sticky='w')
        self.e_y = tk.Entry(fields, bg=WHITE)
        self.e_y.grid(row=3, column=1, padx=6, pady=4)

        btns = tk.Frame(block, bg=self.default_bg)
        btns.pack(pady=12)

        back_btn = tk.Button(btns, text="Назад", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                             command=lambda: app.show('RestrictedPage'))
        back_btn.pack(side="left", padx=8)

        create_btn = tk.Button(btns, text="Создать", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                               command=lambda: self._create(app))
        create_btn.pack(side="left", padx=8)

    def _create(self, app):
        try:
            length = int(self.e_length.get())
            width = int(self.e_width.get())
            px = int(self.e_x.get())
            py = int(self.e_y.get())
        except Exception:
            return

        room_id = getattr(app, 'current_room_id', None)
        try:
            queries.add_restricted(app.con, room_id, px, py, length, width)
            app.con.commit()
        except Exception:
            return
        rpage = app.frames.get('RestrictedPage')
        if rpage:
            try:
                rpage.on_show()
            except Exception:
                pass
        app.show('RestrictedPage')
