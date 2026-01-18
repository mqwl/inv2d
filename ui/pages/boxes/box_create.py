import tkinter as tk
import tkinter.font as tkfont
from ui.pages.base import BasePage
import queries

ORANGE = "#F47C2C"
WHITE = "#FFFFFF"


class BoxCreatePage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        block = tk.Frame(self, bg=self.default_bg)
        block.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.6, relheight=0.4)

        tk.Label(block, text="Введите данные коробки", font=("Arial", 14, "bold"), fg="#000000", bg=self.default_bg).pack(pady=(10, 6))

        fields = tk.Frame(block, bg=self.default_bg)
        fields.pack(pady=8)

        tk.Label(fields, text="Размер грани", bg=self.default_bg).grid(row=0, column=0, padx=6, sticky='w')
        self.e_edge = tk.Entry(fields, bg=WHITE)
        self.e_edge.grid(row=1, column=0, padx=6, pady=4)

        tk.Label(fields, text="Координата X", bg=self.default_bg).grid(row=0, column=1, padx=6, sticky='w')
        self.e_x = tk.Entry(fields, bg=WHITE)
        self.e_x.grid(row=1, column=1, padx=6, pady=4)

        tk.Label(fields, text="Координата Y", bg=self.default_bg).grid(row=0, column=2, padx=6, sticky='w')
        self.e_y = tk.Entry(fields, bg=WHITE)
        self.e_y.grid(row=1, column=2, padx=6, pady=4)

        btns = tk.Frame(block, bg=self.default_bg)
        btns.pack(pady=12)

        back_btn = tk.Button(btns, text="Назад", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                             command=lambda: app.show('BoxesPage'))
        back_btn.pack(side="left", padx=8)

        create_btn = tk.Button(btns, text="Создать", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                               command=lambda: self._create_box(app))
        create_btn.pack(side="left", padx=8)

    def _create_box(self, app):
        try:
            edge = int(self.e_edge.get())
            x = int(self.e_x.get())
            y = int(self.e_y.get())
        except Exception:
            return

        room_id = getattr(app, 'current_room_id', None)
        try:
            queries.add_box(app.con, edge, x, y, room_id)
            app.con.commit()
        except Exception:
            return
        boxes_page = app.frames.get('BoxesPage')
        if boxes_page:
            try:
                boxes_page.on_show()
            except Exception:
                pass

        obj_create = app.frames.get('ObjectCreatePage')
        if obj_create:
            try:
                obj_create.on_show()
            except Exception:
                pass
        obj_assign = app.frames.get('ObjectAssignPage')
        if obj_assign:
            try:
                obj_assign.on_show()
            except Exception:
                pass

        app.show('BoxesPage')
