import tkinter as tk
import sqlite3
import random


class VocabularyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.set_basic_app_infos()
        # Instead of choose MainPage() as self.frame we use None because the
        # correct frame is choosen by the following function call
        self.frame = None
        self.show(Menu)

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


class Menu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.add_widgets()

    def add_widgets(self):
        # Button for Training Session
        self.B_Training = tk.Button(self, text='Start Training Session',
                                    command=lambda: root.show(Training))
        self.B_Training.pack()
        # Button for Adding Vocabularies
        self.B_Add = tk.Button(self, text='Adding Vocabularies',
                               command=lambda: root.show(Add_Vocabularies))
        self.B_Add.pack()
        # Button for Session History
        self.B_History = tk.Button(self, text='View Session History',
                                   command=lambda: root.show(SessionHistory))
        self.B_History.pack()
        # Button for StatisticPage
        self.B_Stats = tk.Button(self, text='View Statistics',
                                 command=lambda: root.show(StatsPage))
        self.B_Stats.pack()
        # Button for Exit
        self.B_Exit = tk.Button(self, text='Exit',
                                command=lambda: root.destroy())
        self.B_Exit.pack()


class Training(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.add_variables()
        self.add_widgets()
        self.add_bindings()

    def add_variables(self):
        self.var_percentage = tk.DoubleVar(value=1.0)
        self.var_order = tk.IntVar(value=0)

    def add_widgets(self):
        # Create a Listbox with Scrollbar
        self.selectlectures = tk.Label(self, text='Select your lectures')
        self.selectlectures.grid(column=0, row=0)
        self.box_lectures = tk.Listbox(self, exportselection=0,
                                       selectmode='multiple', heigh=5)
        self.box_lectures.grid(column=0, row=1, sticky='nswe')
        self.scrollbar = tk.Scrollbar(self, orient='vertical',
                                      command=self.box_lectures.yview)
        self.scrollbar.grid(column=1, row=1, sticky='ns')
        self.box_lectures['yscrollcommand'] = self.scrollbar.set
        self.box_lectures.insert('end', *[i[1] for i in get_lectures()])
        # Create Radiobuttons for select percentage
        self.wordselection = tk.Label(self, text='Select words:')
        self.wordselection.grid(column=0, row=2)
        self.all = tk.Radiobutton(self, text='All words',
                                  variable=self.var_percentage, value=1.0)
        self.all.grid(column=0, row=3)
        self.below90 = tk.Radiobutton(self, text='All words below 90%',
                                      variable=self.var_percentage, value=0.9)
        self.below90.grid(column=0, row=4)
        self.below75 = tk.Radiobutton(self, text='All words below 75%',
                                      variable=self.var_percentage, value=0.75)
        self.below75.grid(column=0, row=5)
        self.below50 = tk.Radiobutton(self, text='All words below 50%',
                                      variable=self.var_percentage, value=0.5)
        self.below50.grid(column=0, row=6)
        # Create Radiobuttons for select order
        self.selectorder = tk.Label(self, text='Select order:')
        self.selectorder.grid(column=0, row=7)
        self.sortedorder = tk.Radiobutton(self, text='Sorted Order',
                                          variable=self.var_order, value=0)
        self.sortedorder.grid(column=0, row=8)
        self.randomorder = tk.Radiobutton(self, text='Random Order',
                                          variable=self.var_order, value=1)
        self.randomorder.grid(column=0, row=9)
        # Create Label for wordcount
        self.wordcount = tk.Label(self)
        self.wordcount.grid(column=0, row=10)
        # Create buttons for start training and Go to MainPage
        self.start = tk.Button(self, text='Start Training',
                               command=lambda: [self.set_selection(),
                                                root.show(TrainingPage)])
        self.start.grid(column=0, row=11)
        self.go_back = tk.Button(self, text='Return to Main Page',
                                 command=lambda: root.show(Menu))
        self.go_back.grid(column=0, row=12)

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
        training_order = self.var_order


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


class Add_Vocabularies():
    def __init__(self, parent):
        super().__init__(parent)
        self.add_widgets()

    def add_widgets(self):
        self.label = tk.Label(self, text='ImportPage')
        self.label.pack()

        self.goback = tk.Button(self, text='Back to Main Page',
                                command=lambda: root.show(Menu))
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
                                command=lambda: root.show(Menu))
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
