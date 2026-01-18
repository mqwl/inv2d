import tkinter as tk
import tkinter.font as tkfont
from ui.pages.base import BasePage
import queries

ORANGE = "#F47C2C"
WHITE = "#FFFFFF"


class ObjectsPage(BasePage):
	def __init__(self, parent, app):
		super().__init__(parent, app)

		self.small_font = tkfont.Font(family="Arial", size=10)

		back_btn = tk.Button(self, text="Назад", bg=ORANGE, fg=WHITE, font=self.small_font, bd=0,
				     padx=8, pady=4, command=lambda: app.show('RoomDetailPage'))
		back_btn.place(relx=0.01, rely=0.02, anchor='nw')

		self.header = tk.Frame(self, bg=ORANGE)
		self.header.place(relx=0.5, rely=0.02, anchor='n', relwidth=0.7, relheight=0.10)
		self.header_label = tk.Label(self.header, text="Объекты", bg=ORANGE, fg=WHITE, font=("Arial", 16, "bold"))
		self.header_label.pack(expand=True)

		self.left_frame = tk.Frame(self, bg=self.default_bg)
		self.left_frame.place(relx=0.02, rely=0.14, relwidth=0.28, relheight=0.82)

		self.right_frame = tk.Frame(self, bg=self.default_bg)
		self.right_frame.place(relx=0.32, rely=0.14, relwidth=0.66, relheight=0.82)

		buttons = [
			"Добавить объект",
			"Изменить объект",
			"Удалить объект",
		]

		self.left_buttons = []
		for i, t in enumerate(buttons):
			b = tk.Button(self.left_frame, text=t, bg=ORANGE, fg=WHITE, bd=0)
			b.pack(fill='x', pady=(6 if i == 0 else 4, 4), padx=6)
			self.left_buttons.append(b)

		try:
			if len(self.left_buttons) > 0:
				self.left_buttons[0].config(command=lambda a=app: a.show('ObjectCreatePage'))
			if len(self.left_buttons) > 1:
				self.left_buttons[1].config(command=lambda a=app: a.show('ObjectEditPage'))
			if len(self.left_buttons) > 2:
				self.left_buttons[2].config(command=lambda a=app: a.show('ObjectDeletePage'))
		except Exception:
			pass

		
		self.obj_canvas = tk.Canvas(self.right_frame, bg=self.default_bg, highlightthickness=0)
		self.obj_scroll = tk.Scrollbar(self.right_frame, orient='vertical', command=self.obj_canvas.yview)
		self.obj_inner = tk.Frame(self.obj_canvas, bg=self.default_bg)

		self.obj_inner.bind("<Configure>", lambda e: self.obj_canvas.configure(scrollregion=self.obj_canvas.bbox("all")))
		self.obj_canvas.create_window((0, 0), window=self.obj_inner, anchor='nw')
		self.obj_canvas.configure(yscrollcommand=self.obj_scroll.set)

		self.obj_canvas.pack(side='left', fill='both', expand=True, padx=6, pady=6)
		self.obj_scroll.pack(side='right', fill='y')

	def on_show(self):
		for child in self.obj_inner.winfo_children():
			child.destroy()

		
		room_id = getattr(self.app, 'current_room_id', None)
		try:
			cur = self.app.con.cursor()
			cur.execute("PRAGMA table_info('object');")
			cols = [c[1] for c in cur.fetchall()]
			has_phone = 'phone' in cols
			if room_id is None:
				cur.execute("SELECT id, name, available, date, box_id FROM object ORDER BY id ASC;")
			else:
				cur.execute(
					"SELECT o.id, o.name, o.available, o.date, o.box_id FROM object o JOIN box b ON o.box_id = b.id WHERE b.room_id = ? ORDER BY o.id ASC;",
					(room_id,)
				)
			rows = cur.fetchall()
			cur.close()
		except Exception:
			rows = []
			has_phone = False

		for row in rows:
			oid = row[0]
			name = row[1]
			available = row[2]
			date = row[3]
			box_id = row[4]

			frame = tk.Frame(self.obj_inner, bg=WHITE, bd=1, relief='solid')
			frame.pack(fill='x', pady=6, padx=6)
			title = tk.Label(frame, text=f"{name}", bg=WHITE, fg="#000000", font=("Arial", 12, "bold"))
			title.pack(anchor='w', padx=6, pady=(6, 2))

			box_text = f"Коробка {box_id}" if box_id else "Без коробки"
			if date and date != 'NULL':
				avail_text = "Арендуется"
			else:
				avail_text = "В наличии" if available == 1 else "Занят"
			parts = [box_text, avail_text]
			if date and date != 'NULL':
				parts.append(f"Дата конца аренды: {date}")
			# phone is shown only if present in schema; actual value not available otherwise
			if has_phone:
				try:
					cur = self.app.con.cursor()
					cur.execute("SELECT phone FROM object WHERE id = ?", (oid,))
					phone_row = cur.fetchone()
					cur.close()
					if phone_row and phone_row[0]:
						parts.append(f"Телефон арендующего: {phone_row[0]}")
				except Exception:
					pass

			info = tk.Label(frame, text=" | ".join(parts), bg=WHITE, fg="#000000", wraplength=600, justify='left')
			info.pack(anchor='w', padx=6, pady=(0, 6))
