import tkinter as tk


class History(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.add_widgets()

    def add_widgets(self):
        self.label = tk.Label(self,
                              text='HistoryPage')
        self.label.pack()
