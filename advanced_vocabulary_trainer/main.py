import tkinter as tk
from app_frames import menu
import os.path


class VocabularyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.set_basic_app_infos()
        # Instead of choose MainPage() as self.frame we use None because the
        # correct frame is choosen by the following function call
        self.frame = None
        self.show(menu.Menu)

    def set_basic_app_infos(self):
        self.title("CJ\'s Vocabulary Trainer")
        self.geometry('400x400')
        self.resizable(False, False)

    def show(self, targetframe):
        new_frame = targetframe(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack()


if __name__ == '__main__':
    root = VocabularyApp()
    root.mainloop()
