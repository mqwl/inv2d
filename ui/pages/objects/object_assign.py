import tkinter as tk
import tkinter.font as tkfont
from ui.pages.base import BasePage
import queries

ORANGE = "#F47C2C"
WHITE = "#FFFFFF"


class ObjectAssignPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        block = tk.Frame(self, bg=self.default_bg)
        block.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.7, relheight=0.5)

        tk.Label(block, text="Выберите коробку и объект для добавления", font=("Arial", 14, "bold"), fg="#000000", bg=self.default_bg).pack(pady=(10, 6))

        
        self.box_var = tk.StringVar(value="Выбор коробки")
        self.box_id = None
        self.box_menu = tk.OptionMenu(block, self.box_var, "Выбор коробки")
        self.box_menu.config(bg=WHITE, fg="#000000", width=40)
        self.box_menu.pack(pady=8)

        
        self.obj_var = tk.StringVar(value="Выбор объекта")
        self.obj_id = None
        self.obj_menu = tk.OptionMenu(block, self.obj_var, "Выбор объекта")
        self.obj_menu.config(bg=WHITE, fg="#000000", width=40)
        self.obj_menu.pack(pady=8)

        btns = tk.Frame(block, bg=self.default_bg)
        btns.pack(pady=12)

        back_btn = tk.Button(btns, text="Назад", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                             command=lambda: app.show('BoxesPage'))
        back_btn.pack(side="left", padx=8)

        add_btn = tk.Button(btns, text="Добавить", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                            command=lambda: self._assign(app))
        add_btn.pack(side="left", padx=8)

        self._populate_menus(app)

    def _populate_menus(self, app):
        room_id = getattr(app, 'current_room_id', None)
        try:
            cur = app.con.cursor()
            if room_id is None:
                cur.execute("SELECT id, edge FROM box ORDER BY id ASC;")
            else:
                cur.execute("SELECT id, edge FROM box WHERE room_id = ? ORDER BY id ASC;", (room_id,))
            boxes = cur.fetchall()
            cur.execute("SELECT id, name FROM object ORDER BY id ASC;")
            objects = cur.fetchall()
            cur.close()
        except Exception:
            boxes = []
            objects = []

        bmenu = self.box_menu['menu']
        bmenu.delete(0, 'end')
        for b in boxes:
            bid = b[0]
            label = f"Коробка {bid} (edge={b[1]})"
            bmenu.add_command(label=label, command=lambda i=bid, l=label: self._set_box(i, l))
        if boxes:
            self.box_id = boxes[0][0]
            self.box_var.set(f"Коробка {boxes[0][0]} (edge={boxes[0][1]})")

        omenu = self.obj_menu['menu']
        omenu.delete(0, 'end')
        for o in objects:
            oid = o[0]
            name = o[1]
            label = f"{name} (id={oid})"
            omenu.add_command(label=label, command=lambda i=oid, l=label: self._set_obj(i, l))
        if objects:
            self.obj_id = objects[0][0]
            self.obj_var.set(f"{objects[0][1]} (id={objects[0][0]})")

    def on_show(self):
        self._populate_menus(self.app)

    def _set_box(self, bid, label):
        self.box_id = bid
        self.box_var.set(label)

    def _set_obj(self, oid, label):
        self.obj_id = oid
        self.obj_var.set(label)

    def _assign(self, app):
        if self.box_id is None or self.obj_id is None:
            return
        try:
            queries.edit_object(app.con, self.obj_id, box_id=self.box_id)
            app.con.commit()
        except Exception:
            return

        boxes_page = app.frames.get('BoxesPage')
        if boxes_page:
            try:
                boxes_page.on_show()
            except Exception:
                pass
        app.show('BoxesPage')
