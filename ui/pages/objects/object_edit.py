import tkinter as tk
import tkinter.font as tkfont
from ui.pages.base import BasePage
import queries

ORANGE = "#F47C2C"
WHITE = "#FFFFFF"


class ObjectEditPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        block = tk.Frame(self, bg=self.default_bg)
        block.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.7, relheight=0.55)

        tk.Label(block, text="Выберите объект для изменения", font=("Arial", 14, "bold"), fg="#000000", bg=self.default_bg).pack(pady=(6, 4))

        self.sel_var = tk.StringVar(value="Выбор объекта")
        self.selected_id = None
        self.option_menu = tk.OptionMenu(block, self.sel_var, 'Выбор объекта')
        self.option_menu.config(bg=WHITE, fg="#000000", width=50)
        self.option_menu.pack(pady=8)

        tk.Label(block, text="Введите новые данные объекта", bg=self.default_bg).pack(pady=(8, 4))

        fields = tk.Frame(block, bg=self.default_bg)
        fields.pack(pady=8)

        tk.Label(fields, text="Дата конца аренды (YYYY-MM-DD)", bg=self.default_bg).grid(row=0, column=0, sticky='w', padx=6)
        self.e_date = tk.Entry(fields, bg=WHITE)
        self.e_date.grid(row=1, column=0, padx=6, pady=4)

        tk.Label(fields, text="Название", bg=self.default_bg).grid(row=0, column=1, sticky='w', padx=6)
        self.e_name = tk.Entry(fields, bg=WHITE)
        self.e_name.grid(row=1, column=1, padx=6, pady=4)

        tk.Label(fields, text="Телефон заемщика", bg=self.default_bg).grid(row=0, column=2, sticky='w', padx=6)
        self.e_phone = tk.Entry(fields, bg=WHITE)
        self.e_phone.grid(row=1, column=2, padx=6, pady=4)

        btns = tk.Frame(block, bg=self.default_bg)
        btns.pack(pady=12)

        back_btn = tk.Button(btns, text="Назад", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                             command=lambda: app.show('ObjectsPage'))
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
                cur.execute("SELECT id, name FROM object ORDER BY id ASC;")
            else:
                cur.execute(
                    "SELECT o.id, o.name FROM object o JOIN box b ON o.box_id = b.id WHERE b.room_id = ? ORDER BY o.id ASC;",
                    (room_id,)
                )
            rows = cur.fetchall()
            cur.execute("PRAGMA table_info('object');")
            cols = [c[1] for c in cur.fetchall()]
            self.has_phone = 'phone' in cols
            cur.close()
        except Exception:
            rows = []
            self.has_phone = False

        menu = self.option_menu['menu']
        menu.delete(0, 'end')
        for r in rows:
            oid = r[0]
            name = r[1] if r[1] else f"Объект {oid}"
            menu.add_command(label=name, command=lambda i=oid, l=name: self._set_sel(i, l))
        if rows:
            self.selected_id = rows[0][0]
            first_name = rows[0][1] if rows[0][1] else f"Объект {rows[0][0]}"
            self.sel_var.set(first_name)

    def on_show(self):
        self._populate_menu(self.app)

    def _set_sel(self, oid, label):
        self.selected_id = oid
        self.sel_var.set(label)

    def _save(self, app):
        oid = getattr(self, 'selected_id', None)
        if oid is None:
            try:
                oid = int(self.sel_var.get())
            except Exception:
                return

        date = self.e_date.get().strip()
        name = self.e_name.get().strip()
        phone = self.e_phone.get().strip()

        try:
            if name:
                try:
                    queries.edit_object(app.con, oid, name=name)
                except Exception:
                    pass

            if date:
                try:
                    queries.rent_object(app.con, oid, date)
                except Exception:
                    pass
            else:
                try:
                    queries.return_object(app.con, oid)
                except Exception:
                    pass

            if hasattr(self, 'has_phone') and self.has_phone:
                try:
                    cur = app.con.cursor()
                    cur.execute("UPDATE object SET phone = ? WHERE id = ?", (phone if phone else None, oid))
                    cur.close()
                except Exception:
                    pass

            app.con.commit()
        except Exception:
            return

        objs_page = app.frames.get('ObjectsPage')
        if objs_page:
            try:
                objs_page.on_show()
            except Exception:
                pass
        app.show('ObjectsPage')
