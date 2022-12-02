import tkinter as tk
import menu
from typing import List
import sqlite3
import random

# TODO Structure code and recode classes


class Training(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)
        self.add_widgets()

    def add_widgets(self):
        self.label = tk.Label(self,
                              text='TrainingPage')
        self.label.pack()
        # Create Button to go back to MainPage
        self.goto_Menu = tk.Button(self,
                                   text='Return to Menu',
                                   command=lambda: self.parent.show(menu.Menu))
        self.goto_Menu.pack()


class WordFrame(tk.Frame):
    pass


class TrainingSession():
    def __init__(self, lectures: List, words: float, mode: int):
        self.lectures = lectures
        self.words = words
        self.mode = mode
        self.session = self.load_session(self.lectures,
                                         self.words,
                                         self.mode)
        for item in self.session:
            self.wordframe = WordFrame(self, item)
            self.wordframe.destroy()
        self.label_finish = tk.Label(self, text='Training finished')
        self.label_finish.pack()

    def load_session(self, lectures: List, words: float, mode: int) -> List:
        session_container = []
        con = sqlite3.connect('vocabulary.db')
        cur = con.cursor()
        # to include: AND percentage <=? --- percentage
        for item in lectures:
            cur.execute("""SELECT * FROM words
            WHERE lecture_id = (SELECT lecture_id FROM lectures
            WHERE lecture_name = ?);""", (item,))
            session_container.append(cur.fetchall())
        cur.close()
        con.close()
        vocabulary_list = [item
                           for sublist in session_container
                           for item in sublist]
        if mode == 1:
            random.shuffle(vocabulary_list)
        return session_container

    def query_session(self, session_words: dict, mode: int):
        pass

    def save_session(self, session_words: dict):
        pass
