import tkinter as tk
import tkinter.font as tkfont
import tkinter.messagebox as messagebox
from ui.pages.base import BasePage
import queries

ORANGE = "#F47C2C"
WHITE = "#FFFFFF"


class ObjectCreatePage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        block = tk.Frame(self, bg=self.default_bg)
        block.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.6, relheight=0.35)

        tk.Label(block, text="Введите название", font=("Arial", 14, "bold"), fg="#000000", bg=self.default_bg).pack(pady=(10, 6))

        self.name_entry = tk.Entry(block, bg=WHITE, width=50)
        self.name_entry.pack(pady=6)

        
        tk.Label(block, text="Выберите коробку", bg=self.default_bg).pack(pady=(6, 0))
        self.box_var = tk.StringVar(value="Выбор коробки")
        self.box_menu = tk.OptionMenu(block, self.box_var, "Выбор коробки")
        self.box_menu.config(bg=WHITE, fg="#000000", width=40)
        self.box_menu.pack(pady=6)
        self.selected_box_id = None
        self._populate_boxes(app)

        btns = tk.Frame(block, bg=self.default_bg)
        btns.pack(pady=12)

        back_btn = tk.Button(btns, text="Назад", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                             command=lambda: app.show('ObjectsPage'))
        back_btn.pack(side="left", padx=8)

        create_btn = tk.Button(btns, text="Создать", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                       command=lambda: self._create(app))
        create_btn.pack(side="left", padx=8)

    def _create(self, app):
        name = self.name_entry.get().strip()

        if not name:
            messagebox.showwarning('Ошибка', 'Введите название объекта')
            return

        if not self.selected_box_id:
            messagebox.showwarning('Ошибка', 'Выберите коробку для объекта')
            return

        try:
            queries.add_object(app.con, name, self.selected_box_id, 1, None)
            app.con.commit()
        except Exception as e:
            print('add_object error:', e)
            messagebox.showerror('Ошибка', f'Не удалось создать объект: {e}')
            return

        objs_page = app.frames.get('ObjectsPage')
        if objs_page:
            try:
                objs_page.on_show()
            except Exception:
                pass
        app.show('ObjectsPage')

    def _populate_boxes(self, app):
        room_id = getattr(app, 'current_room_id', None)
        try:
            cur = app.con.cursor()
            if room_id is None:
                cur.execute("SELECT id, edge FROM box ORDER BY id ASC;")
            else:
                cur.execute("SELECT id, edge FROM box WHERE room_id = ? ORDER BY id ASC;", (room_id,))
            boxes = cur.fetchall()
            cur.close()
        except Exception:
            boxes = []

        menu = self.box_menu['menu']
        menu.delete(0, 'end')
        for b in boxes:
            bid = b[0]
            label = f"Коробка {bid} (edge={b[1]})"
            menu.add_command(label=label, command=lambda i=bid, l=label: self._set_box(i, l))
        if boxes:
            self.selected_box_id = boxes[0][0]
            self.box_var.set(f"Коробка {boxes[0][0]} (edge={boxes[0][1]})")

    def _set_box(self, bid, label):
        self.selected_box_id = bid
        self.box_var.set(label)

    def on_show(self):
        self._populate_boxes(self.app)
