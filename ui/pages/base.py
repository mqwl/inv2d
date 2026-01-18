# ui/pages/base.py
import tkinter as tk

DEFAULT_BG = "#F5F5F5"


class BasePage(tk.Frame):

    def __init__(self, parent, app, bg: str = None):
        use_bg = bg if bg is not None else DEFAULT_BG
        super().__init__(parent, bg=use_bg)
        self.app = app
        self.default_bg = DEFAULT_BG
