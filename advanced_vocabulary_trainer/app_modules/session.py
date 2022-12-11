from typing import List
import sqlite3
import configuration
import random

class Session():
    def __init__(self, lectures: List, wordacc: float, mode: int):
        self.lectures = lectures
        self.wordacc = wordacc
        self.mode = mode
        self.word_ids = self.get_word_ids(self.lectures,
                                          self.wordacc,
                                          self.mode)
        self.word_count = len(self.word_ids)
        self.word_number = 0

        
    def get_word_ids(self, lectures: List, wordacc: float, mode: int):
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
        word_ids = []
        connect = sqlite3.connect(configuration.database)
        cursor = connect.cursor()
        for lecture in lectures:
            cursor.execute("""SELECT word_id FROM words
                           WHERE lecture_id = (SELECT lecture_id FROM lectures
                           WHERE lecture_name = ?) AND percentage <= ?;""",
                           (lecture, wordacc))
            word_ids += cursor.fetchall()
        cursor.close()
        connect.close()
        if mode == 1:
            random.shuffle(word_ids)
    
    @staticmethod
    def load_word(id: int) -> List:
        connect = sqlite3.connect(configuration.database)
        cursor = connect.cursor()
        cursor.execute("""SELECT word_id,
                                 german,
                                 english,
                                 correct_count,
                                 frequency_count,
                                 percentage
                       FROM words
                       WHERE word_id = ?;""",
                       (id,))
        current_word = cursor.fetchone()
        cursor.close()
        connect.close()
        return list(current_word)
    
    @staticmethod
    def save_word(word: List):
        connect = sqlite3.connect(configuration.database)
        cursor = connect.cursor()
        cursor.execute("""UPDATE words 
                       SET correct_count = ?,
                           frequency_count = ?,
                           percentage = ?
                       WHERE word_id = ?;""",
                       (word[3],
                        word[4],
                        word[5],
                        word[0]))

        
    @staticmethod
    def get_lectures() -> List:
        """Return lectures of the database.
        
        Returns
        -------
        list of str
            A list of lectures in the database 'vocabulary.db'.
        """
        connect = sqlite3.connect(configuration.database)
        cursor = connect.cursor()
        cursor.execute("""SELECT * FROM lectures;""")
        lectures = cursor.fetchall()
        cursor.close()
        connect.close()
        return lectures
    
    
    @staticmethod
    def get_w_count(lectures: List, wordacc: float) -> int:
        """Get the word count of the combined lessons.

        Parameters
        ----------
        lectures : list of str
            The lectures the user choosed for his session.
        wordacc : float
            The accuracy of the words the user selected.

        Returns
        -------
        int
            Word count of the selected options.
        """
        wordcount = 0
        connect = sqlite3.connect(configuration.database)
        for lecture in lectures:
            cursor = connect.cursor()
            cursor.execute("""SELECT COUNT(*) FROM words
                          WHERE lecture_id = (SELECT lecture_id FROM lectures
                          WHERE lecture_name = ?) AND percentage <= ?;""",
                          (lecture, wordacc))
            wordcount += cursor.fetchone()[0]
            cursor.close()
        connect.close()
        return wordcount
