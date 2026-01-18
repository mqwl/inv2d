import tkinter as tk
import tkinter.font as tkfont
from ui.pages.base import BasePage
import queries

ORANGE = "#F47C2C"
WHITE = "#FFFFFF"


class BoxesPage(BasePage):
	def __init__(self, parent, app):
		super().__init__(parent, app)

		self.small_font = tkfont.Font(family="Arial", size=10)

		back_btn = tk.Button(self, text="Назад", bg=ORANGE, fg=WHITE, font=self.small_font, bd=0,
				     padx=8, pady=4, command=lambda: app.show('RoomDetailPage'))
		back_btn.place(relx=0.01, rely=0.02, anchor='nw')

		self.header = tk.Frame(self, bg=ORANGE)
		self.header.place(relx=0.5, rely=0.02, anchor='n', relwidth=0.7, relheight=0.10)
		self.header_label = tk.Label(self.header, text="Коробки", bg=ORANGE, fg=WHITE, font=("Arial", 16, "bold"))
		self.header_label.pack(expand=True)

		self.left_frame = tk.Frame(self, bg=self.default_bg)
		self.left_frame.place(relx=0.02, rely=0.14, relwidth=0.28, relheight=0.82)

		self.right_frame = tk.Frame(self, bg=self.default_bg)
		self.right_frame.place(relx=0.32, rely=0.14, relwidth=0.66, relheight=0.82)

		buttons = [
			"Добавить коробку",
			"Изменить коробку",
			"Удалить коробку",
			"Добавить объект в коробку",
		]

		self.left_buttons = []
		for i, t in enumerate(buttons):
			b = tk.Button(self.left_frame, text=t, bg=ORANGE, fg=WHITE, bd=0)
			b.pack(fill='x', pady=(6 if i == 0 else 4, 4), padx=6)
			self.left_buttons.append(b)

		
		try:
			if len(self.left_buttons) > 0:
				self.left_buttons[0].config(command=lambda a=app: a.show('BoxCreatePage'))
			if len(self.left_buttons) > 1:
				self.left_buttons[1].config(command=lambda a=app: a.show('BoxEditPage'))
			if len(self.left_buttons) > 2:
				self.left_buttons[2].config(command=lambda a=app: a.show('BoxDeletePage'))
			if len(self.left_buttons) > 3:
				self.left_buttons[3].config(command=lambda a=app: a.show('ObjectAssignPage'))
		except Exception:
			pass

		
		self.box_canvas = tk.Canvas(self.right_frame, bg=self.default_bg, highlightthickness=0)
		self.box_scroll = tk.Scrollbar(self.right_frame, orient='vertical', command=self.box_canvas.yview)
		self.box_inner = tk.Frame(self.box_canvas, bg=self.default_bg)

		self.box_inner.bind("<Configure>", lambda e: self.box_canvas.configure(scrollregion=self.box_canvas.bbox("all")))
		self.box_canvas.create_window((0, 0), window=self.box_inner, anchor='nw')
		self.box_canvas.configure(yscrollcommand=self.box_scroll.set)

		self.box_canvas.pack(side='left', fill='both', expand=True, padx=6, pady=6)
		self.box_scroll.pack(side='right', fill='y')

	def on_show(self):
		
		for child in self.box_inner.winfo_children():
			child.destroy()

		
		room_id = getattr(self.app, 'current_room_id', None)
		try:
			cur = self.app.con.cursor()
			if room_id is None:
				cur.execute("SELECT id, edge FROM box ORDER BY id ASC;")
			else:
				cur.execute("SELECT id, edge FROM box WHERE room_id = ? ORDER BY id ASC;", (room_id,))
			rows = cur.fetchall()
			cur.close()
		except Exception:
			rows = []

		for i, row in enumerate(rows):
			bid = row[0]
			edge = row[1]
			frame = tk.Frame(self.box_inner, bg=WHITE, bd=1, relief='solid')
			frame.pack(fill='x', pady=6, padx=6)
			title = tk.Label(frame, text=f"Коробка {bid}", bg=WHITE, fg="#000000", font=("Arial", 12, "bold"))
			title.pack(anchor='w', padx=6, pady=(6, 2))
			info = tk.Label(frame, text=f"Грань коробки: {edge}", bg=WHITE, fg="#000000")
			info.pack(anchor='w', padx=6, pady=(0, 6))
