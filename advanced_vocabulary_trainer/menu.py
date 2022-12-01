import tkinter as tk
import history
import addvocabularies
import selecttraining
import statpage


class Menu(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)
        self.add_widgets()

    def add_widgets(self):
        # Create navigation buttons:
        nav = [['Start Training Session', selecttraining.SelectTraining],
               ['Adding Vocabularies', addvocabularies.AddVocabularies],
               ['View History', history.History],
               ['View Statistics', statpage.StatPage]]
        self.button = []
        for num, info in enumerate(nav):
            # Using i=i trick
            self.button.append(tk.Button(self,
                                         text=info[0],
                                         command=lambda i=info[1]: self.parent.show(i)))
            self.button[num].pack()
        # Button for Exit
        self.B_Exit = tk.Button(self,
                                text='Exit',
                                command=lambda: self.parent.destroy())
        self.B_Exit.pack()
