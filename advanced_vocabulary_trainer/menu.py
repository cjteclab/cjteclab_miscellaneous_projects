import tkinter as tk
import history
import addvocabularies
import selecttraining
import statistics


class Menu(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.add_widgets()

    def add_widgets(self):
        # Create navigation buttons:
        nav = [['Start Training Session', selecttraining.SelectTraining],
               ['Adding Vocabularies', addvocabularies.AddVocabularies],
               ['View Sission History', history.History],
               ['View Statistics', statistics.Statistics]]

        for num, info in enumerate(nav):
            self.num = tk.Button(self,
                                 text=info[0],
                                 command=lambda: self.parent.show(info[1]))
            self.num.pack()
        # Button for Exit
        self.B_Exit = tk.Button(self,
                                text='Exit',
                                command=lambda: self.parent.destroy())
        self.B_Exit.pack()
