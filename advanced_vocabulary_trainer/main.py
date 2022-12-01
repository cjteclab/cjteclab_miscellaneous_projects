import tkinter as tk
import sqlite3
import random
import menu


class VocabularyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.set_basic_app_infos()
        # Instead of choose MainPage() as self.frame we use None because the
        # correct frame is choosen by the following function call
        self.frame = None
        self.show(menu.Menu)

    def set_basic_app_infos(self):
        self.title("CJ\'s Vocabulary Trainer")
        self.geometry('400x400')
        self.resizable(False, False)

    def show(self, targetframe):
        new_frame = targetframe(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack()


class TrainingSelect(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.add_variables()
        self.add_widgets()
        self.add_bindings()

    def add_variables(self):
        # Create variable for Radiobuttons
        self.var_percentage = tk.DoubleVar(value=1.0)
        # Create variable for Checkbutton
        self.var_querymode = tk.IntVar(value=0)

    def add_widgets(self):
        # Create Label for headline
        self.label_headline = tk.Label(self)
        self.label_headline['text'] = 'Please choose your training:'
        self.label_headline.grid(column=0, row=0)
        # Create a Listbox with Scrollbar for lecture selection
        self.box_lectures = tk.Listbox(self, exportselection=0,
                                       selectmode='multiple', heigh=10)
        self.box_lectures.grid(column=0, row=1, sticky='nswe')
        self.box_scrollbar = tk.Scrollbar(self, orient='vertical',
                                          command=self.box_lectures.yview)
        self.box_scrollbar.grid(column=1, row=1, sticky='ns')
        self.box_lectures['yscrollcommand'] = self.box_scrollbar.set
        self.box_lectures.insert('end', *[i[1] for i in get_lectures()])
        # Create Radiobuttons for word selection
        self.label_words = tk.Label(self)
        self.label_words['text'] = 'Word selection:'
        self.label_words.grid(column=0, row=2)
        self.all = tk.Radiobutton(self, text='All words',
                                  variable=self.var_percentage, value=1.0,
                                  command=lambda: self.change_selection(None))
        self.all.grid(column=0, row=3)
        self.l90 = tk.Radiobutton(self, text='Words below 90% accuracy',
                                  variable=self.var_percentage, value=0.9,
                                  command=lambda: self.change_selection(None))
        self.l90.grid(column=0, row=4)
        self.l75 = tk.Radiobutton(self, text='Words below 75% accuracy',
                                  variable=self.var_percentage, value=0.75,
                                  command=lambda: self.change_selection(None))
        self.l75.grid(column=0, row=5)
        self.l50 = tk.Radiobutton(self, text='Words below 50% accuracy',
                                  variable=self.var_percentage, value=0.5,
                                  command=lambda: self.change_selection(None))
        self.l50.grid(column=0, row=6)
        # Create Frame for showing selected words
        # !Must be updated every time user change selection in Listbox or Scale
        self.wordcount = tk.Label(self)
        self.wordcount.grid(column=0, row=7)
        # Create Checkbutton for query mode
        self.selectorder = tk.Label(self, text='Select order:')
        self.selectorder.grid(column=0, row=8)
        self.sortedorder = tk.Radiobutton(self, text='Sorted Order',
                                          variable=self.var_querymode, value=0)
        self.sortedorder.grid(column=0, row=9)
        self.randomorder = tk.Radiobutton(self, text='Random Order',
                                          variable=self.var_querymode, value=1)
        self.randomorder.grid(column=0, row=10)
        # Create Button to start training
        self.start = tk.Button(self, text='Start Training',
                               command=lambda: [self.set_selection(),
                                                root.show(TrainingPage)])
        self.start.grid(column=0, row=11)
        # !When pressing the 'Start Training' button call a Training Instance
        # Create Button to go back to MainPage
        self.goto_Menu = tk.Button(self, text='Return to Menu',
                                   command=lambda: root.show(Menu))
        self.goto_Menu.grid(column=0, row=12)

    def add_bindings(self):
        self.box_lectures.bind('<<ListboxSelect>>', self.change_selection)

    def change_selection(self, event):
        self.wordcount['text'] = get_w_count([self.box_lectures.get(i)
                                             for i in
                                             self.box_lectures.curselection()],
                                             self.var_percentage.get())

    def set_selection(self):
        global training_lectures
        training_lectures = [self.box_lectures.get(
            i) for i in self.box_lectures.curselection()]
        global training_percentage
        training_percentage = self.var_percentage
        global training_order
        training_order = self.var_querymode


class TrainingPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.lectures = training_lectures
        self.percentage = training_percentage
        self.order = training_order
        self.vocabulary_list = get_vocabulary_list(self.lectures,
                                                   self.percentage,
                                                   self.order)
        self.word_count = len(self.vocabulary_list)
        for item in self.vocabulary_list:
            self.wordframe = WordFrame(self, item)
            self.wordframe.destroy()
        self.label_finish = tk.Label(self, text='Training finished')
        self.label_finish.pack()


class WordFrame(tk.Frame):
    def __init__(self, parent, item):
        super().__init__(parent)
        self.item = item
        self.parent = parent
        self.add_variables()
        self.add_widgets()
        self.add_bindings()
        self.pack()
        self.wait_variable(self.var_entry_pass)
        self.wait_variable(self.var_frame_pass)

    def add_variables(self):
        self.var_correct = tk.StringVar(value='')
        self.var_answer = tk.StringVar(value='')
        self.var_entry_pass = tk.IntVar(value=0)
        self.var_frame_pass = tk.IntVar(value=0)
        self.var_entry = tk.StringVar()

    def add_widgets(self):
        self.label_nativword = tk.Label(self, text=self.item[1])
        self.label_nativword.pack()
        self.entry_translation = tk.Entry(self, textvariable=self.var_entry)
        self.entry_translation.pack()
        self.entry_translation.focus()
        self.label_correct = tk.Label(self, textvariable=self.var_correct)
        self.label_correct.pack()
        self.label_answer = tk.Label(self, textvariable=self.var_answer)
        self.label_answer.pack()

    def add_bindings(self):
        self.entry_translation.bind('<Return>', self.correct_word)
        self.bind('<Return>', self.next_word)

    def correct_word(self, event):
        self.var_entry_pass.set(1)
        if self.var_entry.get() == self.item[2]:
            self.var_correct.set('Correct')
        else:
            self.var_correct.set('Not Correct')
            self.var_answer.set(self.item[2])
        self.focus()

    def next_word(self, event):
        self.var_frame_pass.set(1)


class AddVocabularies():
    def __init__(self, parent):
        super().__init__(parent)
        self.add_widgets()

    def add_widgets(self):
        self.label = tk.Label(self, text='ImportPage')
        self.label.pack()

        self.goback = tk.Button(self, text='Back to Main Page',
                                command=lambda: root.show(menu.Menu))
        self.goback.pack()


class SessionHistory():
    pass


class StatsPage():
    def __init__(self, parent):
        super().__init__(parent)
        self.add_widgets()

    def add_widgets(self):
        self.label = tk.Label(self, text='StatisticPage')
        self.label.pack()

        self.goback = tk.Button(self, text='Back to Main Page',
                                command=lambda: root.show(menu.Menu))
        self.goback.pack()


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


def get_vocabulary_list(lectures, percentage, order):
    lecture_box = []
    con = sqlite3.connect('vocabulary.db')
    cur = con.cursor()
    # to include: AND percentage <=? --- percentage
    for item in lectures:
        cur.execute("""SELECT * FROM words
                    WHERE lecture_id = (SELECT lecture_id FROM lectures
                    WHERE lecture_name = ?);""", (item,))
        lecture_box.append(cur.fetchall())
    cur.close()
    con.close()
    vocabulary_list = [item for sublist in lecture_box for item in sublist]
    if order == 1:
        random.shuffle(vocabulary_list)
    return vocabulary_list


if __name__ == '__main__':
    root = VocabularyApp()
    root.mainloop()
