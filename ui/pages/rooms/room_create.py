import tkinter as tk
import tkinter.font as tkfont
from ui.pages.base import BasePage
import queries

ORANGE = "#F47C2C"
WHITE = "#FFFFFF"


class RoomCreatePage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        self.title_font = tkfont.Font(family="Arial", size=16, weight="bold")

        block = tk.Frame(self, bg=self.default_bg)
        block.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.6, relheight=0.5)

        tk.Label(block, text="Введите данные помещения", font=("Arial", 14, "bold"), fg="#000000", bg=self.default_bg).pack(pady=(10, 8))

        name_frame = tk.Frame(block, bg=self.default_bg)
        name_frame.pack(fill="x", pady=6)
        tk.Label(name_frame, text="Название помещения", bg=self.default_bg).pack(anchor="w", padx=6)
        nf = tk.Frame(name_frame, bg=ORANGE)
        nf.pack(fill="x", padx=6, pady=4)
        self.name_entry = tk.Entry(nf, bd=0, bg=WHITE, fg="#000000")
        self.name_entry.pack(fill="x", padx=2, pady=2)

        dims_frame = tk.Frame(block, bg=self.default_bg)
        dims_frame.pack(fill="x", pady=8, padx=6)

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

        buttons = tk.Frame(block, bg=self.default_bg)
        buttons.pack(pady=12)

        back_btn = tk.Button(buttons, text="Назад", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                             command=lambda: app.show("RoomsPage"))
        back_btn.pack(side="left", padx=8)

        create_btn = tk.Button(buttons, text="Создать", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                               command=lambda: self._create_room(app))
        create_btn.pack(side="left", padx=8)

    def _create_room(self, app):
        try:
            length = int(self.dim_entries[0].get())
            width = int(self.dim_entries[1].get())
            height = int(self.dim_entries[2].get())
        except Exception:
            
            return

        try:
            name = self.name_entry.get().strip()
            if not name:
                name = "Помещение"
            queries.add_room(app.con, name, length, width, height)
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
