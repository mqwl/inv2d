import tkinter as tk
import tkinter.font as tkfont
from ui.pages.base import BasePage
import queries

ORANGE = "#F47C2C"
WHITE = "#FFFFFF"


class ObjectReturnPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        block = tk.Frame(self, bg=self.default_bg)
        block.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.7, relheight=0.55)

        tk.Label(block, text="Выберите объект для возвращения", font=("Arial", 14, "bold"), fg="#000000", bg=self.default_bg).pack(pady=(6, 4))

        self.sel_var = tk.StringVar(value="Выбор объекта")
        self.selected_id = None
        self.option_menu = tk.OptionMenu(block, self.sel_var, 'Выбор объекта')
        self.option_menu.config(bg=WHITE, fg="#000000", width=50)
        self.option_menu.pack(pady=8)

        fields = tk.Frame(block, bg=self.default_bg)
        fields.pack(pady=8)


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
                cur.execute("SELECT id, name FROM object WHERE available = 0 ORDER BY id ASC;")
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
        query = '''
            SELECT id FROM movement
            WHERE object_id = ? AND finished = 0
        '''
        values = (oid, )
        cur = app.con.cursor()
        cur.execute(query, values)
        res = cur.fetchone()[0]
        print(res)
        cur.close()
        try:
            queries.return_object(app.con, oid, res)
        except Exception:
            pass
        app.con.commit()

        objs_page = app.frames.get('ObjectsPage')
        if objs_page:
            try:
                objs_page.on_show()
            except Exception:
                pass
        app.show('ObjectsPage')
