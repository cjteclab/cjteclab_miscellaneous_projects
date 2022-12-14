import tkinter as tk
from functools import partial
from app_frames import training, menu
from app_modules.session import Session as session


class SelectTraining(tk.Frame):
    """Create SelectTraining frame with its variables, widgets and bindings."""
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)
        self.add_variables()
        self.add_widgets()
        self.add_bindings()

    def add_variables(self):
        # Create a variable for words selection Radiobutton.
        self.var_wordselect = tk.DoubleVar(value=1.0)
        # Create a variable for query mode Radiobutton.
        self.var_querymode = tk.IntVar(value=0)

    def add_widgets(self):
        # Create a Frame for lecture Listbox.
        self.frame_lecture = tk.LabelFrame(self,
                                           text='Lecture Selection')
        self.frame_lecture.grid(row=0,
                                column=0,
                                columnspan=2,
                                padx=5,
                                pady=5)
        # Create a lecture Listbox with Scrollbar.
        # TODO Add padding to listbox
        self.box_lectures = tk.Listbox(self.frame_lecture,
                                       exportselection=0,
                                       selectmode='multiple',
                                       width=35,
                                       heigh=10)
        self.box_lectures.insert('end',
                                 *[i[1] for i in session.get_lectures()])
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
        # Create a Frame for words Radiobuttons.
        self.frame_words = tk.LabelFrame(self,
                                         text='Word Selection')
        self.frame_words.grid(row=1,
                              column=0,
                              columnspan=2,
                              padx=5,
                              pady=5)
        # Create words Radiobuttons.
        # With these buttons user can select the word accuracy for the words
        # that will be query in the vocabulary test session.
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
        # Create a Frame for selected words Label.
        self.frame_showcount = tk.LabelFrame(self,
                                             text='Number of selected words')
        self.frame_showcount.grid(row=2,
                                  column=0,
                                  columnspan=2,
                                  padx=5,
                                  pady=5)
        # Create a Label for selected words count.
        self.wordcount = tk.Label(self.frame_showcount)
        self.wordcount.pack()
        # Create a Frame for query mode Radiobuttons.
        self.frame_querymode = tk.LabelFrame(self,
                                             text='Query Mode')
        self.frame_querymode.grid(row=3,
                                  column=0,
                                  columnspan=2,
                                  padx=5,
                                  pady=5)
        # Create Radiobuttons for query mode.
        query_mode = [['Ordered query', 0],
                      ['Random query', 1]]
        for num, info in enumerate(query_mode):
            self.num = tk.Radiobutton(self.frame_querymode,
                                      text=info[0],
                                      variable=self.var_querymode,
                                      value=info[1])
            self.num.pack()
        # Create a Frame for navigation buttons.
        self.frame_navi = tk.LabelFrame(self)
        self.frame_navi.grid(row=3,
                             column=0,
                             columnspan=2,
                             padx=5,
                             pady=5)
        # Create Buttons for navigation.
        self.go_to_training = tk.Button(self.frame_navi,
                               text='Got to Training',
                               # use lambda func to combine multiple commands
                               # First command: set global variables with whom 
                               # a instance of the class session will be created.
                               # TODO This method work but it very ugly. Recode it!
                               # Second command: create a frame ot the Training frame.
                               command=lambda:[training.create_training([self.box_lectures.get(i)
                                                                        for i in
                                                                        self.box_lectures.curselection()],
                                                                        self.var_wordselect.get(),
                                                                        self.var_querymode.get()),
                                              self.parent.show(training.Training)])
        self.go_to_training.pack()
        # ! When pressing the 'Start Training' button call a Training Instance
        # ! with the name 'current_session'
        # Create a Button to go back to MainPage.
        self.goto_Menu = tk.Button(self.frame_navi,
                                   text='Return to Menu',
                                   command=partial(self.parent.show,
                                                   menu.Menu))
        self.goto_Menu.pack()

    def add_bindings(self):
        """Add bindings to the Listbox widget."""
        self.box_lectures.bind('<<ListboxSelect>>', self.change_selection)

    def change_selection(self, event):
        """Change the text in the wordcount Label."""
        self.wordcount['text'] = session.get_w_count([self.box_lectures.get(i)
                                                     for i in
                                                     self.box_lectures.curselection()],
                                                     self.var_wordselect.get())
