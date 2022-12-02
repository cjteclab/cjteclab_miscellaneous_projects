import tkinter as tk
import menu
from functools import partial


class History(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)
        self.add_widgets()

    def add_widgets(self):
        self.label = tk.Label(self,
                              text='HistoryPage')
        self.label.pack()
        # Create Button to go back to MainPage
        self.goto_Menu = tk.Button(self,
                                   text='Return to Menu',
                                   command=partial(self.parent.show,
                                                   menu.Menu))
        self.goto_Menu.pack()
