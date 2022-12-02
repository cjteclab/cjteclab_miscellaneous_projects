import tkinter as tk
import training
import menu
import sqlite3
from functools import partial


class SelectTraining(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)
        self.add_variables()
        self.add_widgets()
        self.add_bindings()

    def add_variables(self):
        # Create variable for words selection Radiobutton
        self.var_wordselect = tk.DoubleVar(value=1.0)
        # Create variable for query mode Radiobutton
        self.var_querymode = tk.IntVar(value=0)

    def add_widgets(self):
        # Create Frame for lecture Listbox
        self.frame_lecture = tk.LabelFrame(self,
                                           text='Lecture Selection')
        self.frame_lecture.grid(row=0,
                                column=0,
                                columnspan=2,
                                padx=5,
                                pady=5)
        # Create lecture Listbox
        # TODO Add padding to listbox
        self.box_lectures = tk.Listbox(self.frame_lecture,
                                       exportselection=0,
                                       selectmode='multiple',
                                       width=35,
                                       heigh=10)
        self.box_lectures.grid(column=0,
                               row=1,
                               sticky='nswe')
        self.box_scrollbar = tk.Scrollbar(self.frame_lecture,
                                          orient='vertical',
                                          command=self.box_lectures.yview)
        self.box_scrollbar.grid(column=1,
                                row=1,
                                sticky='ns')
        self.box_lectures['yscrollcommand'] = self.box_scrollbar.set
        self.box_lectures.insert('end', *[i[1] for i in get_lectures()])
        # Create Frame for words Radiobuttons
        self.frame_words = tk.LabelFrame(self,
                                         text='Word Selection')
        self.frame_words.grid(row=1,
                              column=0,
                              columnspan=2,
                              padx=5,
                              pady=5)
        # Create words Radiobuttons
        words_buttons = [['All words', 1.0],
                         ['Words below 75% accuracy', 0.75],
                         ['Words below 50% accuracy', 0.5],
                         ['Worfs below 25% accuracy', 0.25]]
        for num, info in enumerate(words_buttons):
            self.num = tk.Radiobutton(self.frame_words,
                                      text=info[0],
                                      variable=self.var_wordselect,
                                      value=info[1],
                                      command=partial(self.change_selection,
                                                      None))
            self.num.pack()
        # Create Frame for selected words Label
        self.frame_showcount = tk.LabelFrame(self,
                                             text='Number of selected words')
        self.frame_showcount.grid(row=2,
                                  column=0,
                                  columnspan=2,
                                  padx=5,
                                  pady=5)
        # Create Label for selected word count
        self.wordcount = tk.Label(self.frame_showcount)
        self.wordcount.pack()
        # Create Frame for query mode Radiobuttons
        self.frame_querymode = tk.LabelFrame(self,
                                             text='Query Mode')
        self.frame_querymode.grid(row=3,
                                  column=0,
                                  columnspan=2,
                                  padx=5,
                                  pady=5)
        # Create Radiobuttons for query mode
        query_mode = [['Ordered query', 0],
                      ['Random query', 1]]
        for num, info in enumerate(query_mode):
            self.num = tk.Radiobutton(self.frame_querymode,
                                      text=info[0],
                                      variable=self.var_querymode,
                                      value=info[1])
            self.num.pack()
        # Create Frame for navigation buttons
        self.frame_navi = tk.LabelFrame(self)
        self.frame_navi.grid(row=3,
                             column=0,
                             columnspan=2,
                             padx=5,
                             pady=5)
        # Create Buttons for navigation
        self.start = tk.Button(self.frame_navi,
                               text='Start Training',
                               # ! Append command with self.set_selection
                               command=[partial(self.parent.show,
                                                training.Training)])
        self.start.pack()
        # !When pressing the 'Start Training' button call a Training Instance
        # Create Button to go back to MainPage
        self.goto_Menu = tk.Button(self.frame_navi,
                                   text='Return to Menu',
                                   command=partial(self.parent.show,
                                                   menu.Menu))
        self.goto_Menu.pack()

    def add_bindings(self):
        self.box_lectures.bind('<<ListboxSelect>>', self.change_selection)

    def change_selection(self, event):
        self.wordcount['text'] = get_w_count([self.box_lectures.get(i)
                                             for i in
                                             self.box_lectures.curselection()],
                                             self.var_wordselect.get())


def get_lectures():
    con = sqlite3.connect('vocabulary.db')
    cur = con.cursor()
    cur.execute("""SELECT * FROM lectures;""")
    lectures = cur.fetchall()
    cur.close()
    con.close()
    return lectures


def get_w_count(lectures, percentage):
    wordcount = 0
    con = sqlite3.connect('vocabulary.db')
    for lecture in lectures:
        cur = con.cursor()
        cur.execute("""SELECT COUNT(*) FROM words
                    WHERE lecture_id = (SELECT lecture_id FROM lectures
                    WHERE lecture_name = ?) AND percentage <= ?;""",
                    (lecture, percentage))
        wordcount += cur.fetchone()[0]
        cur.close()
    con.close()
    return wordcount
