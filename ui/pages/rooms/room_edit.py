import tkinter as tk
import tkinter.font as tkfont
from ui.pages.base import BasePage
import queries

ORANGE = "#F47C2C"
WHITE = "#FFFFFF"


class RoomEditPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        block = tk.Frame(self, bg=self.default_bg)
        block.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.7, relheight=0.5)
        tk.Label(block, text="Введите данные помещения, которые вы хотите изменить", font=("Arial", 14, "bold"), fg="#000000", bg=self.default_bg).pack(pady=(10, 6))

        # список помещений
        rooms = []
        try:
            cur = app.con.cursor()
            cur.execute("SELECT id FROM room;")
            rooms = [str(r[0]) for r in cur.fetchall()]
            cur.close()
        except Exception:
            rooms = []

        self.sel_var = tk.StringVar(value="Выбор помещения")
        if rooms:
            self.sel_var.set(rooms[0])

        self.option_menu = tk.OptionMenu(block, self.sel_var, *rooms)
        self.option_menu.config(bg=WHITE, fg="#000000", width=25)
        self.option_menu.pack(pady=8)

        # Три поля в одну строку
        dims_frame = tk.Frame(block, bg=self.default_bg)
        dims_frame.pack(pady=8)

        labels = ["Длина помещения", "Ширина помещения", "Высота помещения"]
        self.dim_entries = []
        for i, lbl in enumerate(labels):
            col = tk.Frame(dims_frame, bg=self.default_bg)
            col.grid(row=0, column=i, padx=6, sticky="nsew")
            tk.Label(col, text=lbl, bg=self.default_bg).pack(anchor="w")
            bf = tk.Frame(col, bg=ORANGE)
            bf.pack(fill="x", pady=4)
            e = tk.Entry(bf, bd=0, bg=WHITE, fg="#000000")
            e.pack(fill="x", padx=2, pady=2)
            self.dim_entries.append(e)

        # Кнопки (внутри центрального блока)
        btns = tk.Frame(block, bg=self.default_bg)
        btns.pack(pady=12)

        back_btn = tk.Button(btns, text="Назад", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                             command=lambda: app.show('RoomsPage'))
        back_btn.pack(side="left", padx=8)

        save_btn = tk.Button(btns, text="Изменить", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                             command=lambda: self._edit_selected(app))
        save_btn.pack(side="left", padx=8)

    def on_show(self):
        # Обновляем список в выпадающем меню при показе страницы
        try:
            cur = self.app.con.cursor()
            cur.execute("SELECT id FROM room;")
            rooms = [str(r[0]) for r in cur.fetchall()]
            cur.close()
        except Exception:
            rooms = []

        menu = self.option_menu['menu']
        menu.delete(0, 'end')
        for r in rooms:
            menu.add_command(label=r, command=lambda v=r: self.sel_var.set(v))
        if rooms:
            self.sel_var.set(rooms[0])
        else:
            self.sel_var.set('Выбор помещения')

    def _edit_selected(self, app):
        val = self.sel_var.get()
        try:
            rid = int(val)
        except Exception:
            return

        try:
            length = int(self.dim_entries[0].get())
            width = int(self.dim_entries[1].get())
            height = int(self.dim_entries[2].get())
        except Exception:
            return

        try:
            queries.edit_room(app.con, rid, length, width, height)
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
