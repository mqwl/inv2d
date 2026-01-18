import tkinter as tk
import tkinter.font as tkfont
from ui.pages.base import BasePage
import queries

ORANGE = "#F47C2C"
WHITE = "#FFFFFF"


class ObjectDeletePage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        block = tk.Frame(self, bg=self.default_bg)
        block.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.6, relheight=0.35)

        tk.Label(block, text="Выберите объект для удаления", font=("Arial", 14, "bold"), fg="#000000", bg=self.default_bg).pack(pady=(10, 6))

        self.sel_var = tk.StringVar(value="Выбор объекта")
        self.selected_id = None
        self.option_menu = tk.OptionMenu(block, self.sel_var, 'Выбор объекта')
        self.option_menu.config(bg=WHITE, fg="#000000", width=40)
        self.option_menu.pack(pady=8)

        btns = tk.Frame(block, bg=self.default_bg)
        btns.pack(pady=12)

        back_btn = tk.Button(btns, text="Назад", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                             command=lambda: app.show('ObjectsPage'))
        back_btn.pack(side="left", padx=8)

        del_btn = tk.Button(btns, text="Удалить", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                            command=lambda: self._delete(app))
        del_btn.pack(side="left", padx=8)

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
            cur.close()
        except Exception:
            rows = []

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

    def _delete(self, app):
        oid = getattr(self, 'selected_id', None)
        if oid is None:
            try:
                oid = int(self.sel_var.get())
            except Exception:
                return
        try:
            queries.remove_object(app.con, oid)
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
