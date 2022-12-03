import tkinter as tk
from functools import partial
from app_frames import menu


class StatPage(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)
        self.add_widgets()

    def add_widgets(self):
        self.label = tk.Label(self,
                              text='StatisticsPage')
        self.label.pack()
        # Create Button to go back to MainPage
        self.goto_Menu = tk.Button(self,
                                   text='Return to Menu',
                                   command=partial(self.parent.show,
                                                   menu.Menu))
        self.goto_Menu.pack()
