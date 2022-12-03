import tkinter as tk
from app_frames import menu


class VocabularyApp(tk.Tk):
    """Create the 'root' toplevel window.

    Attributes
    ----------
    frame : instance_str, default None
        The currently app_frame shown in the root window.

    Methods
    -------
    set_basic_app_infos
        Set basic informations for root window.
    show
        Pack a specific frame into the root window.
    """
    def __init__(self):
        super().__init__()
        self.set_basic_app_infos()
        # Instead of choose MainPage() as self.frame we use None because the
        # correct frame is choosen by the following function call
        self.frame = None
        self.show(menu.Menu)

    def set_basic_app_infos(self):
        """Set basic informations about the toplevel window."""
        self.title("CJ\'s Vocabulary Trainer")
        self.geometry('400x400')
        self.resizable(False, False)

    def show(self, targetframe):
        """Pack a specific frame into the root window.

        Create a new instance of the target frame and pack it into roo.

        Parameters
        ----------
        targetframe : class_str
            The frame that will be shown in the root window.
        """
        new_frame = targetframe(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack()


if __name__ == '__main__':
    root = VocabularyApp()
    root.mainloop()
