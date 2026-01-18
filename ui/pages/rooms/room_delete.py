import tkinter as tk
import tkinter.font as tkfont
from ui.pages.base import BasePage
import queries

ORANGE = "#F47C2C"
WHITE = "#FFFFFF"


class RoomDeletePage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        block = tk.Frame(self, bg=self.default_bg)
        block.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.6, relheight=0.4)

        tk.Label(block, text="Выберите помещение для удаления", font=("Arial", 14, "bold"), fg="#000000", bg=self.default_bg).pack(pady=(10, 6))

        rooms = []
        try:
            cur = app.con.cursor()
            cur.execute("SELECT id, name FROM room;")
            rows = cur.fetchall()
            cur.close()
            rooms = rows
        except Exception:
            rooms = []

        self.sel_var = tk.StringVar(value="Выбор помещения")
        self.name_to_id = {}
        self.selected_id = None
        self.option_menu = tk.OptionMenu(block, self.sel_var, 'Выбор помещения')
        self.option_menu.config(bg=WHITE, fg="#000000", width=40)
        self.option_menu.pack(pady=8)
        menu = self.option_menu['menu']
        menu.delete(0, 'end')
        for r in rooms:
            rid = r[0]
            name = r[1] if r[1] else f"Помещение {rid}"
            self.name_to_id[name] = rid
            menu.add_command(label=name, command=lambda v=name, i=rid: self._set_selection(v, i))
        if rooms:
            first_name = rooms[0][1] if rooms[0][1] else f"Помещение {rooms[0][0]}"
            self.sel_var.set(first_name)
            self.selected_id = rooms[0][0]

        btns = tk.Frame(block, bg=self.default_bg)
        btns.pack(pady=12)

        back_btn = tk.Button(btns, text="Назад", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                     command=lambda: app.show('RoomsPage'))
        back_btn.pack(side="left", padx=8)

        del_btn = tk.Button(btns, text="Удалить", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                            command=lambda: self._delete_selected(app))
        del_btn.pack(side="left", padx=8)

    def _delete_selected(self, app):
        rid = getattr(self, 'selected_id', None)
        if rid is None:
            try:
                rid = int(self.sel_var.get())
            except Exception:
                return

        try:
            queries.remove_room(app.con, rid)
            app.con.commit()
        except Exception:
            return

        rooms_page = app.frames.get('RoomsPage')
        if rooms_page:
            try:
                rooms_page.refresh(app)
            except Exception:
                pass
        app.show('RoomsPage')

    def on_show(self):
        try:
            cur = self.app.con.cursor()
            cur.execute("SELECT id, name FROM room;")
            rows = cur.fetchall()
            cur.close()
        except Exception:
            rows = []
        menu = self.option_menu['menu']
        menu.delete(0, 'end')
        self.name_to_id = {}
        for r in rows:
            rid = r[0]
            name = r[1] if r[1] else f"Помещение {rid}"
            self.name_to_id[name] = rid
            menu.add_command(label=name, command=lambda v=name, i=rid: self._set_selection(v, i))
        if rows:
            first_name = rows[0][1] if rows[0][1] else f"Помещение {rows[0][0]}"
            self.sel_var.set(first_name)
            self.selected_id = rows[0][0]
        else:
            self.sel_var.set('Выбор помещения')

    def _set_selection(self, label, rid):
        self.sel_var.set(label)
        self.selected_id = rid
