import tkinter as tk
from tkinter import ttk
from typing import List
import sqlite3
import random
from app_frames import menu
import configuration

# TODO Structure code and recode classes


class Training(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)
        self.add_widgets()

    def add_widgets(self):
        # Create a Frame for Session Informations.
        self.frame_navi = tk.LabelFrame(self)
        self.frame_navi.grid(row=3,
                             column=0,
                             columnspan=2,
                             padx=5,
                             pady=5)
        # Create widgets for Session Informations.
        self.label = tk.Label(self.frame_navi,
                              text='Training Session')
        self.label.pack()
        self.progressbar = ttk.Progressbar(self.frame_navi,
                                           orient='horizintal',
                                           length=200,
                                           mode='determinate')
        self.progressbar.pack()
        # TODO Create for loop by word_ids from session instance and create WordFrame
        
        
        for item in self.session:
            self.wordframe = WordFrame(self, item)
            self.wordframe.destroy()
        self.label_finish = tk.Label(self, text='Training finished')
        self.label_finish.pack()
        
        
        # Create a Button to go back to MainPage.
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
        self.word_ids = self.load_word_ids(self.lectures,
                                           self.words,
                                           self.mode)
        self.word_count = len(self.word_ids)

    def load_word_ids(self, lectures: List, wordacc: float, mode: int) -> List:
        """ Return all word_ids of the words to query.

        Parameters
        ----------
        lectures : list of str
            The lectures the user choosed for his session.
        wordacc : {1.0, 0.75, 0.5, 0.25}
            The accuracy of the words the user selected.
        mode : {0, 1}
            The query mode the user selected.
            '0' for ordered and '1' for random query.

        Returns
        -------
        list
            All word_ids of the words for the selected query.
        """
        word_ids_session = []
        con = sqlite3.connect(configuration.database)
        con.row_factory = lambda cursor, row: row[0]
        cur = con.cursor()
        for lecture in lectures:
            cur.execute("""SELECT word_id FROM words
                        WHERE lecture_id = (SELECT lecture_id FROM lectures
                        WHERE lecture_name = ?) AND percentage <= ?;""",
                        (lecture, wordacc))
            word_ids_session += cur.fetchall()
        cur.close()
        con.close()
        if mode == 1:
            random.shuffle(word_ids_session)
        return word_ids_session

    def query_session(self, session_words: dict, mode: int):
        pass

    def save_session(self, session_words: dict):
        pass
