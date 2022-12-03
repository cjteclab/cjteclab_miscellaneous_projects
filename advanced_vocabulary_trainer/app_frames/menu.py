import tkinter as tk
from functools import partial
from app_frames import selecttraining, addvocabularies, history, statpage


class Menu(tk.Frame):
    """Create Menu frame with its widgets."""
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)
        self.add_widgets()

    def add_widgets(self):
        """Create and pack widgets into the menu frame."""
        # Create navigation buttons.
        nav = [['Start Training Session', selecttraining.SelectTraining],
               ['Adding Vocabularies', addvocabularies.AddVocabularies],
               ['View History', history.History],
               ['View Statistics', statpage.StatPage]]
        self.button = []
        for num, info in enumerate(nav):
            # Instead of using the commonly command method with lambda function
            # which needs a additional i=i extension to handle informations
            # in a loop, the partial() method is used.
            self.button.append(tk.Button(self,
                                         text=info[0],
                                         command=partial(self.parent.show,
                                                         info[1])))
            self.button[num].pack()
        # Create a Button for Exit.
        self.B_Exit = tk.Button(self,
                                text='Exit',
                                command=self.parent.destroy)
        self.B_Exit.pack()
