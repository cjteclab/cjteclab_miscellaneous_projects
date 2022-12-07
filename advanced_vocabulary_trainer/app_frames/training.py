import tkinter as tk
from tkinter import ttk
from typing import List
import sqlite3
import random
from app_frames import menu, selecttraining
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
        # Create wordframes in a for loop
        for item in current_session.word_ids:
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

    def __init__(self,
                 lectures: List,
                 word_accuracy: float,
                 mode: int):
        self.lectures = lectures
        self.word_accuracy = word_accuracy
        self.mode = mode
        self.word_ids = self.load_word_ids(self.lectures,
                                           self.word_accuracy,
                                           self.mode)
        self.word_count = len(self.word_ids)

    def load_word_ids(self,
                      lectures: List,
                      word_accuracy: float,
                      mode: int) -> List:
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
        connect = sqlite3.connect(configuration.database)
        connect.row_factory = lambda cursor, row: row[0]
        cursor = connect.cursor()
        for lecture in lectures:
            cursor.execute("""SELECT word_id FROM words
                           WHERE lecture_id = (SELECT lecture_id FROM lectures
                           WHERE lecture_name = ?) AND percentage <= ?;""",
                           (lecture, word_accuracy))
            word_ids_session += cursor.fetchall()
        cursor.close()
        connect.close()
        if mode == 1:
            random.shuffle(word_ids_session)
        return word_ids_session

    def query_session(self, session_words: dict, mode: int):
        pass

    def save_session(self, session_words: dict):
        pass
