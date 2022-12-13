import tkinter as tk
from app_frames import menu
from app_modules.session import Session as session
from functools import partial

# TODO Structure code and recode classes


class Training(tk.Frame):
    def __init__(self,
                 parent):
        self.parent = parent
        super().__init__(self.parent)
        # Start test variables
        self.new_session = session(x, y, z)
        self.add_widgets()
        

    def add_widgets(self):
        # Create widgets for Session Informations.
        self.session_info = tk.LabelFrame(self,
                                          text='Session Info')
        self.session_info.pack()
        self.progress = tk.Label(self.session_info,
                                 text='Test')
        self.progress.pack()
        self.wordframe = tk.LabelFrame(self,
                                       text='Vocabulary') 
        self.wordframe.pack()
        self.start_training = tk.Button(self.wordframe,
                                        text='Start training',
                                        command=partial(self.show_word,
                                                        self.new_session.word_ids[self.new_session.word_number]))
        self.start_training.pack()
        
    def show_word(self, id):
        self.wordframe.destroy()
        self.word = session.load_word(id)
        print(self.word)
        self.wordframe = tk.LabelFrame(self,
                                        text='Vocabulary')
        self.wordframe.pack()
        self.entryVar = tk.StringVar()
        self.german_word = tk.Label(self.wordframe,
                                    text=self.word[1])
        self.german_word.pack()
        self.english_word = tk.Entry(self.wordframe,
                                     textvariable=self.entryVar)
        self.english_word.pack()
        self.english_word.focus()
        
        self.english_word.bind('<Return>', self.check_result)
        self.info = tk.Label(self.wordframe,
                             text='Press Enter to check result')
        self.info.pack()
        
    def check_result(self, event):
        if self.word[2] == self.entryVar.get():
            self.word[3] += 1
            self.label_correct = tk.Label(self.wordframe,
                                          text='Correct')
            self.label_correct.pack()
        else:
            self.label_false = tk.Label(self.wordframe,
                                        text='False')
            self.label_false.pack()
            self.label_correct_answer = tk.Label(self.wordframe,
                                                 text=self.word[2])
            self.label_correct_answer.pack()
        self.word[4] += 1
        self.word[5] = self.word[3] / self.word[4]
        session.save_word(self.word)
        self.new_session.word_number += 1
        if self.new_session.word_number < (self.new_session.word_count - 1):
            
            self.next = tk.Button(self.wordframe,
                                  text='Press Spacebar for the next word',
                                  command=partial(self.show_word, self.new_session.word_ids[self.new_session.word_number]))
            self.next.pack()
            self.next.bind('<space>', lambda event:self.show_word(self.new_session.word_ids[self.new_session.word_number]))
            self.next.focus()
        else:
            self.show_result()

        
        
    def show_result(self):
        self.wordframe.destroy()
        self.result_frame = tk.LabelFrame(self,
                                          text='Result')
        self.result_frame.pack()
        self.test_label = tk.Label(self.result_frame,
                                   text="tata")
        self.test_label.pack()
        self.goto_Menu = tk.Button(self,
                                   text='Return to Menu',
                                   command=partial(self.parent.show,
                                                   menu.Menu))
        self.goto_Menu.pack()
        
def create_training(lectures, wordacc: float, mode: int):
    global x
    x = lectures
    global y
    y = wordacc
    global z
    z = mode