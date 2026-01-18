import tkinter as tk
import pkgutil
import importlib
import inspect
from ui.pages.base import BasePage


class App(tk.Tk):

    def __init__(self, con):
        super().__init__()
        self.title("Inventory System")
        self.geometry("1200x800")

        self.con = con

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        self._discover_pages(container)
        # Стартовая страница: LoginPage если есть, иначе первая найденная
        start = 'LoginPage' if 'LoginPage' in self.frames else (next(iter(self.frames), None))
        if start:
            self.show(start)

    def show(self, page_name):
        frame = self.frames.get(page_name)
        if frame:
            frame.tkraise()
            # If страница реализует on_show, вызывем её
            try:
                if hasattr(frame, 'on_show'):
                    frame.on_show()
            except Exception:
                pass
        else:
            container = None
            if self.frames:
                container = self.frames[next(iter(self.frames))].master
            self._discover_pages(container)
            frame = self.frames.get(page_name)
            if frame:
                frame.tkraise()
                try:
                    if hasattr(frame, 'on_show'):
                        frame.on_show()
                except Exception:
                    pass
            else:
                print(f"Page not found: {page_name}")

    def _discover_pages(self, container):
        package = 'ui.pages'
        try:
            pkg = importlib.import_module(package)
            pkg_path = pkg.__path__
        except Exception as e:
            print(f"Cannot import package {package}: {e}")
            pkg_path = []

        for finder, modname, ispkg in pkgutil.walk_packages(path=pkg_path, prefix=package + '.'):
            if modname.endswith('.base'):
                continue
            try:
                mod = importlib.import_module(modname)
            except Exception as e:
                print(f"Failed to import {modname}: {e}")
                continue

            for _, cls in inspect.getmembers(mod, inspect.isclass):
                if issubclass(cls, BasePage) and cls is not BasePage:
                    if cls.__name__ in self.frames:
                        continue
                    if container is None:
                        continue
                    try:
                        frame = cls(container, self)
                        self.frames[cls.__name__] = frame
                        frame.place(relwidth=1, relheight=1)
                    except Exception as e:
                        print(f"Failed to initialize page {cls.__name__}: {e}")
