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

        btns = tk.Frame(block, bg=self.default_bg)
        btns.pack(pady=12)

        back_btn = tk.Button(btns, text="Назад", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                             command=lambda: app.show('RoomsPage'))
        back_btn.pack(side="left", padx=8)

        del_btn = tk.Button(btns, text="Удалить", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                            command=lambda: self._delete_selected(app))
        del_btn.pack(side="left", padx=8)

    def _delete_selected(self, app):
        val = self.sel_var.get()
        try:
            rid = int(val)
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
