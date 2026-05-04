import tkinter as tk
# import tkinter.font as tkfont
import queries
from ui.pages.base import BasePage
from PIL import ImageTk

ORANGE = "#F47C2C"
WHITE = "#FFFFFF"


class RoomFullViewPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        self.header = tk.Frame(self, bg=ORANGE)
        self.header.place(relx=0.5, rely=0.02, anchor='n',
                          relwidth=0.7, relheight=0.10)
        self.header_label = tk.Label(self.header,
                                     text="Расчёт расположения",
                                     bg=ORANGE, fg=WHITE,
                                     font=("Arial", 16, "bold"))
        self.header_label.pack(expand=True)
        self.tk_image = None

        back_btn = tk.Button(self, text="Назад", bg=ORANGE, fg=WHITE, bd=0,
                             padx=8, pady=4,
                             command=lambda: app.show('RoomDetailPage'))
        back_btn.place(relx=0.01, rely=0.02, anchor='nw')

        self.calc_btn = tk.Button(
            self, text="Сгенерировать 3D вид",
            bg=ORANGE, fg=WHITE, bd=0, padx=8, pady=4,
            command=self.run_3d_calculation
        )
        self.calc_btn.place(relx=0.01, rely=0.08, anchor='nw')
        self.canvas = tk.Canvas(self, bg="#ffffff", highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.14, anchor='n',
                          relwidth=0.9, relheight=0.78)

    def run_3d_calculation(self):
        room_id = getattr(self.app, 'current_room_id', None)
        if not room_id:
            return
        self.canvas.delete('all')
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            text="Идёт генерация, пожалуйста подождите",
            font=("Arial", 16, "bold")
        )
        self.update()
        try:
            img = queries.calculate_placement(self.app.con, room_id)
            cw = self.canvas.winfo_width()
            ch = self.canvas.winfo_height()
            img.thumbnail((cw, ch))
            self.tk_image = ImageTk.PhotoImage(img)
            self.canvas.delete('all')
            self.canvas.create_image(cw / 2, ch / 2,
                                     image=self.tk_image, anchor='center')

        except Exception as e:
            self.canvas.delete('all')
            self.canvas.create_text(100, 50, text=f"Ошибка: {e}",
                                    fill="red", anchor='nw')
            print(f"Error: {e}")

    def on_show(self):
        self.canvas.delete('all')
        self.tk_image = None
        # room_id = getattr(self.app, 'current_room_id', None)
        # if not room_id:
        #     self.canvas.create_text(200, 100, text='Помещение не выбрано',
        #                             font=("Arial", 14))
        #     return

        # try:
        #     room = queries.get_room_by_id(self.app.con, room_id)
        #     boxes = queries.get_boxes_by_room(self.app.con, room_id)
        # except Exception:
        #     room = None
        #     boxes = []

        # if not room:
        #     self.canvas.create_text(200, 100,
        #                             text='Информация о помещении недоступна',
        #                             font=("Arial", 14))
        #     return

        # length = room[2]
        # width = room[3]
        # if not length or not width:
        #     self.canvas.create_text(200, 100,
        #                             text='Некорректные размеры помещения',
        #                             font=("Arial", 14))
        #     return

        # cw = int(self.canvas.winfo_width() or 800)
        # ch = int(self.canvas.winfo_height() or 600)

        # scale = min((cw - 40) / length, (ch - 40) / width)
        # rw = length * scale
        # rh = width * scale
        # x0 = (cw - rw) / 2
        # y0 = (ch - rh) / 2
        # x1 = x0 + rw
        # y1 = y0 + rh
        # self.canvas.create_rectangle(x0, y0, x1, y1, fill="#f7f7f7",
        #                              outline=ORANGE, width=2)

        # for b in boxes:
        #     bid, edge, px, py, _ = b
        #     bx0 = x0 + px * scale
        #     by0 = y0 + py * scale
        #     bx1 = bx0 + edge * scale
        #     by1 = by0 + edge * scale
        #     self.canvas.create_rectangle(bx0, by0, bx1, by1, fill="#ffeecf",
        #                                  outline="#c77a3a")
        #     self.canvas.create_text((bx0+bx1)/2, (by0+by1)/2, text=str(bid))
