import tkinter as tk
import tkinter.font as tkfont
from ui.pages.base import BasePage
import queries

ORANGE = "#F47C2C"
WHITE = "#FFFFFF"


class RestrictedEditPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        block = tk.Frame(self, bg=self.default_bg)
        block.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.7, relheight=0.55)

        tk.Label(block, text="Выберите зону для изменения", font=("Arial", 14, "bold"), fg="#000000", bg=self.default_bg).pack(pady=(6, 4))

        self.sel_var = tk.StringVar(value="Выбор зоны")
        self.selected_id = None
        self.option_menu = tk.OptionMenu(block, self.sel_var, 'Выбор зоны')
        self.option_menu.config(bg=WHITE, fg="#000000", width=50)
        self.option_menu.pack(pady=8)

        tk.Label(block, text="Изменить данные зоны", bg=self.default_bg).pack(pady=(8, 4))

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

        save_btn = tk.Button(btns, text="Подтвердить", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                             command=lambda: self._save(app))
        save_btn.pack(side="left", padx=8)

        self._populate_menu(app)

    def _populate_menu(self, app):
        room_id = getattr(app, 'current_room_id', None)
        try:
            cur = app.con.cursor()
            if room_id is None:
                cur.execute("SELECT id, length, width FROM restricted ORDER BY id ASC;")
            else:
                cur.execute("SELECT id, length, width FROM restricted WHERE room_id = ? ORDER BY id ASC;", (room_id,))
            rows = cur.fetchall()
            cur.close()
        except Exception:
            rows = []

        menu = self.option_menu['menu']
        menu.delete(0, 'end')
        for r in rows:
            rid = r[0]
            label = f"Зона {rid} ( {r[1]}x{r[2]} )"
            menu.add_command(label=label, command=lambda i=rid, l=label: self._set_sel(i, l))
        if rows:
            self.selected_id = rows[0][0]
            self.sel_var.set(f"Зона {rows[0][0]} ( {rows[0][1]}x{rows[0][2]} )")

    def on_show(self):
        self._populate_menu(self.app)

    def _set_sel(self, rid, label):
        self.selected_id = rid
        self.sel_var.set(label)

    def _save(self, app):
        rid = getattr(self, 'selected_id', None)
        if rid is None:
            try:
                rid = int(self.sel_var.get())
            except Exception:
                return
        try:
            length = int(self.e_length.get())
            width = int(self.e_width.get())
            px = int(self.e_x.get())
            py = int(self.e_y.get())
        except Exception:
            return
        try:
            queries.edit_restricted(app.con, rid, pivot_x=px, pivot_y=py, length=length, width=width)
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
