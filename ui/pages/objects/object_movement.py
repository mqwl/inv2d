import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from ui.pages.base import BasePage
import queries

ORANGE = "#F47C2C"
WHITE = "#FFFFFF"


class ObjectMovementPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.selected_id = None
        self.small_font = tkfont.Font(family="Arial", size=10)
        block = tk.Frame(self, bg=self.default_bg)
        block.place(relx=0.5, rely=0.02, anchor="n", relwidth=0.9, relheight=0.45)

        tk.Label(block, text="Перемещения объектов", font=("Arial", 16, "bold"),
                 fg="#000000", bg=self.default_bg).pack(pady=(10, 5))

        fields = tk.Frame(block, bg=self.default_bg)
        fields.pack(pady=10)
        back_btn = tk.Button(self, text="Назад", bg=ORANGE, fg=WHITE, font=self.small_font, bd=0,
                                        padx=8, pady=4, command=lambda: app.show('ObjectsPage'))
        back_btn.place(relx=0.01, rely=0.02, anchor='nw')

        history_frame = tk.Frame(self, bg=WHITE, bd=1, relief="flat")
        history_frame.place(relx=0.5, rely=0.1, anchor="n", relwidth=0.9, relheight=0.8)

        columns = ("id", "object_id", "phone", "date_rent", "date_return", "finished")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("object_id", text="ID Объекта")
        self.tree.heading("phone", text="Номер телефона")
        self.tree.heading("date_rent", text="Начало аренды")
        self.tree.heading("date_return", text="Конец аренды")
        self.tree.heading("finished", text="Завершенность")

        self.tree.column("id", width=30, anchor="center")
        self.tree.column("object_id", width=70, anchor="center")
        self.tree.column("phone", width=100)
        self.tree.column("date_rent", width=150)
        self.tree.column("date_return", width=100)
        self.tree.column("finished", width=100)
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _fill_history(self, app):
        for i in self.tree.get_children():
            self.tree.delete(i)

        try:
            cur = app.con.cursor()
            cur.execute("""
                SELECT *
                FROM movement
                ORDER BY id DESC
                LIMIT 50
            """)
            rows = cur.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
            cur.close()
        except Exception as e:
            print(f"Ошибка загрузки: {e}")

    def on_show(self):
        self._fill_history(self.app)
