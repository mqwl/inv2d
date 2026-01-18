import tkinter as tk
import tkinter.font as tkfont
from ui.pages.base import BasePage
import queries

ORANGE = "#F47C2C"
WHITE = "#FFFFFF"


class BoxEditPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        block = tk.Frame(self, bg=self.default_bg)
        block.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.7, relheight=0.5)

        tk.Label(block, text="Выберите коробку для изменения", font=("Arial", 14, "bold"), fg="#000000", bg=self.default_bg).pack(pady=(6, 4))

        self.sel_var = tk.StringVar(value="Выбор коробки")
        self.name_to_id = {}
        self.selected_id = None
        self.option_menu = tk.OptionMenu(block, self.sel_var, 'Выбор коробки')
        self.option_menu.config(bg=WHITE, fg="#000000", width=40)
        self.option_menu.pack(pady=8)

        tk.Label(block, text="Изменить данные коробки", bg=self.default_bg).pack(pady=(8, 4))

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

        save_btn = tk.Button(btns, text="Подтвердить", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                             command=lambda: self._edit_box(app))
        save_btn.pack(side="left", padx=8)

        self._populate_menu(app)

    def _populate_menu(self, app):
        try:
            cur = app.con.cursor()
            cur.execute("SELECT id, edge FROM box ORDER BY id ASC;")
            rows = cur.fetchall()
            cur.close()
        except Exception:
            rows = []
        menu = self.option_menu['menu']
        menu.delete(0, 'end')
        self.name_to_id = {}
        for r in rows:
            bid = r[0]
            edge = r[1]
            label = f"Коробка {bid} (edge={edge})"
            self.name_to_id[label] = bid
            menu.add_command(label=label, command=lambda v=label, i=bid: self._set_selection(v, i))
        if rows:
            first_label = f"Коробка {rows[0][0]} (edge={rows[0][1]})"
            self.sel_var.set(first_label)
            self.selected_id = rows[0][0]

    def on_show(self):
        self._populate_menu(self.app)

    def _set_selection(self, label, bid):
        self.sel_var.set(label)
        self.selected_id = bid

    def _edit_box(self, app):
        bid = getattr(self, 'selected_id', None)
        if bid is None:
            try:
                bid = int(self.sel_var.get())
            except Exception:
                return
        try:
            edge = int(self.e_edge.get())
            x = int(self.e_x.get())
            y = int(self.e_y.get())
        except Exception:
            return
        try:
            queries.edit_box(app.con, bid, edge=edge, pivot_x=x, pivot_y=y)
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
