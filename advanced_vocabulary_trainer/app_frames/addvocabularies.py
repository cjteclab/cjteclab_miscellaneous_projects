import tkinter as tk
from functools import partial
from app_frames import menu


class AddVocabularies(tk.Frame):
    """Create AddVocabularies frame with its widgets."""
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)
        self.add_widgets()

    def add_widgets(self):
        self.label = tk.Label(self,
                              text='AddVocabulariesPage')
        self.label.pack()
        # Create a Button to go back to MainPage.
        self.goto_Menu = tk.Button(self,
                                   text='Return to Menu',
                                   command=partial(self.parent.show,
                                                   menu.Menu))
        self.goto_Menu.pack()
