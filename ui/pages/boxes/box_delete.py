import tkinter as tk
import tkinter.font as tkfont
from ui.pages.base import BasePage
import queries

ORANGE = "#F47C2C"
WHITE = "#FFFFFF"


class BoxDeletePage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        block = tk.Frame(self, bg=self.default_bg)
        block.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.6, relheight=0.35)

        tk.Label(block, text="Выберите коробку для удаления", font=("Arial", 14, "bold"), fg="#000000", bg=self.default_bg).pack(pady=(10, 6))

        self.sel_var = tk.StringVar(value="Выбор коробки")
        self.selected_id = None
        self.option_menu = tk.OptionMenu(block, self.sel_var, 'Выбор коробки')
        self.option_menu.config(bg=WHITE, fg="#000000", width=40)
        self.option_menu.pack(pady=8)

        btns = tk.Frame(block, bg=self.default_bg)
        btns.pack(pady=12)

        back_btn = tk.Button(btns, text="Назад", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                             command=lambda: app.show('BoxesPage'))
        back_btn.pack(side="left", padx=8)

        del_btn = tk.Button(btns, text="Удалить", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                            command=lambda: self._delete_selected(app))
        del_btn.pack(side="left", padx=8)

        self._populate_menu(app)

    def _populate_menu(self, app):
        room_id = getattr(app, 'current_room_id', None)
        try:
            cur = app.con.cursor()
            if room_id is None:
                cur.execute("SELECT id, edge FROM box ORDER BY id ASC;")
            else:
                cur.execute("SELECT id, edge FROM box WHERE room_id = ? ORDER BY id ASC;", (room_id,))
            rows = cur.fetchall()
            cur.close()
        except Exception:
            rows = []

        menu = self.option_menu['menu']
        menu.delete(0, 'end')
        for r in rows:
            bid = r[0]
            label = f"Коробка {bid} (edge={r[1]})"
            menu.add_command(label=label, command=lambda v=bid: self._set_sel(v))
        if rows:
            self.selected_id = rows[0][0]
            self.sel_var.set(f"Коробка {rows[0][0]} (edge={rows[0][1]})")

    def on_show(self):
        self._populate_menu(self.app)

    def _set_sel(self, bid):
        self.selected_id = bid
        self.sel_var.set(f"Коробка {bid}")

    def _delete_selected(self, app):
        bid = getattr(self, 'selected_id', None)
        if bid is None:
            try:
                bid = int(self.sel_var.get())
            except Exception:
                return
        try:
            queries.remove_box(app.con, bid)
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
