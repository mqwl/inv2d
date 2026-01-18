import tkinter as tk
import tkinter.font as tkfont
import tkinter.messagebox as messagebox
from ui.pages.base import BasePage

ORANGE = "#F47C2C"
WHITE = "#FFFFFF"


class AutoLayoutPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        self.small_font = tkfont.Font(family="Arial", size=10)

        back_btn = tk.Button(self, text="Назад", bg=ORANGE, fg=WHITE, font=self.small_font, bd=0,
                             padx=8, pady=4, command=lambda: app.show('RoomDetailPage'))
        back_btn.place(relx=0.01, rely=0.02, anchor='nw')

        self.header = tk.Frame(self, bg=ORANGE)
        self.header.place(relx=0.5, rely=0.02, anchor='n', relwidth=0.7, relheight=0.10)
        self.header_label = tk.Label(self.header, text="Генерация расположения объектов", bg=ORANGE, fg=WHITE, font=("Arial", 16, "bold"))
        self.header_label.pack(expand=True)

        self.generate_btn = tk.Button(self, text="Сгенерировать расположение", bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=10,
                                      command=self._generate)
        self.generate_btn.place(relx=0.5, rely=0.16, anchor='n')

        self.images_frame = tk.Frame(self, bg=self.default_bg)
        self.images_frame.place(relx=0.5, rely=0.26, anchor='n', relwidth=0.9, relheight=0.56)

        self.confirm_frame = tk.Frame(self, bg=self.default_bg)
        self.confirm_frame.place(relx=0.5, rely=0.84, anchor='n')

        self.confirm_btn = tk.Button(self.confirm_frame, text='Подтвердить', bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                                     command=self._confirm)
        self.back_btn2 = tk.Button(self.confirm_frame, text='Назад', bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                                   command=lambda: app.show('RoomDetailPage'))

    def _generate(self):
        for c in self.images_frame.winfo_children():
            c.destroy()

        for i in range(3):
            cv = tk.Canvas(self.images_frame, bg="#ffffff", highlightthickness=1, highlightbackground="#000000")
            cv.pack(side='left', expand=True, fill='both', padx=6, pady=6)
            w = cv.winfo_reqwidth()
            h = cv.winfo_reqheight()
            cv.create_rectangle(10, 10, 190, 140, fill="#f0f0f0", outline=ORANGE, width=2)
            cv.create_text(100, 75, text=f"Вид {i+1}", font=("Arial", 12, "bold"))

        for widget in self.confirm_frame.winfo_children():
            widget.destroy()
        self.confirm_btn = tk.Button(self.confirm_frame, text='Подтвердить', bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                                     command=self._confirm)
        self.back_btn2 = tk.Button(self.confirm_frame, text='Назад', bg=ORANGE, fg=WHITE, bd=0, padx=12, pady=8,
                                   command=lambda: self.app.show('RoomDetailPage'))
        self.confirm_btn.pack(side='left', padx=8)
        self.back_btn2.pack(side='left', padx=8)

    def _confirm(self):
        self.app.temp_layout = 'generated'
        messagebox.showinfo('Сгенерировано', 'Расположение объектов сгенерировано и сохранено во временном состоянии')
        self.app.show('RoomDetailPage')
