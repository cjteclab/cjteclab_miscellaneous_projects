import tkinter as tk
from app_frames import menu 
from app_modules.session import Session as session

# TODO Structure code and recode classes


class Training(tk.Frame):
    def __init__(self,
                 parent):
        self.parent = parent
        super().__init__(self.parent)
        # Start test variables
        self.lectures = ['human body', 'health and medical care']
        self.wordacc = 1.0
        self.mode = 0
        self.word_ids_list = [1, 7, 8, 4, 10]
        self.word_count = len(self.word_ids_list)
        # End test variables
        self.add_widgets()

    def add_widgets(self):
        # Create widgets for Session Informations.
        # TODO Create for loop by word_ids from session instance and create WordFrame
        # Create wordframes in a for loop
        for item in self.word_ids_list:
            self.wordframe = WordFrame(self, item)
        # Create a Button to go back to MainPage.
        
        

class WordFrame(tk.LabelFrame):
    def __init__(self, parent, id: int):
        self.parent = parent
        super().__init__(self.parent)
        self.id = id
        self.word = session.load_word(self.id)
        self.add_variables()
        self.add_widgets()
        self.add_bindings()
        self.grid(row=2,
                             column=0,
                             columnspan=2,
                             padx=5,
                             pady=5)
        
    def add_variables(self):
        self.entryVar = tk.StringVar()
                
    def add_widgets(self):
        self.german_word = tk.Label(self, text=self.word[1])
        self.german_word.pack()
        self.english_word = tk.Entry(self,
                                     textvariable=self.entryVar)
        self.english_word.pack()
        self.english_word.focus()
        
        self.label_continue = tk.Label(self)
        
    def add_bindings(self):
        self.english_word.bind('<Return>', self.check_result)

    def check_result(self, event):
        if self.word[2] == self.entryVar.get():
            self.word[3] += 1
            self.label_correct = tk.Label(self,
                                          text='Correct')
            self.label_correct.pack()
        else:
            self.label_false = tk.Label(self,
                                        text='False')
            self.label_false.pack()
            self.label_correct_answer = tk.Label(self,
                                                 text=self.word[2])
            self.label_correct_answer.pack()
        self.word[4] += 1
        self.word[5] = self.word[3] / self.word[4]
        session.save_word(self.word)
        self.next = tk.Button(self,
                              text='Next word',
                              command=self.destroy)
        self.next.pack()
        self.next.focus()
        self.next.bind('<Return>', lambda event: self.destroy())
        self.next.focus()

        
