import tkinter as tk
import main


class Menu(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.add_widgets()
        
    def add_widgets(self):
        # Create navigation buttons:
        nav = [['Start Training Session', main.TrainingSelect],
               ['Adding Vocabularies', main.AddVocabularies],
               ['View Sission History', main.SessionHistory],
               ['View Statistics', main.StatsPage]]
        
        for num, info in enumerate(nav):
            self.num = tk.Button(self, text=info[0],
                                 command=lambda: self.parent.show(info[1]))
            self.num.pack()
        # Button for Exit
        self.B_Exit = tk.Button(self, text='Exit',
                                command=lambda: self.parent.destroy())
        self.B_Exit.pack()