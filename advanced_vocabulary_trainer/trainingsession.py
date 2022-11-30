import tkinter as tk
import main


class TrainingSession(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.add_variables()
        self.add_widgets()
        self.add_bindings()

    def add_variables(self):
        self.var_register = tk.DoubleVar(value=1.0)
        self.var_order = tk.IntVar(value=0)

    def add_widgets(self):
        # Create a Listbox with Scrollbar
        self.label_selectlectures = tk.Label(self,
                                             text='Select one or multiple lectures')
        self.label_selectlectures.grid(column=0, row=0)
        self.listbox_lectures = tk.Listbox(self, exportselection=0,
                                           selectmode='multiple', heigh=5)
        self.listbox_lectures.grid(column=0, row=1, sticky='nswe')
        self.scrollbar_lectures = tk.Scrollbar(self, orient='vertical',
                                               command=self.listbox_lectures.yview)
        self.scrollbar_lectures.grid(column=1, row=1, sticky='ns')
        self.listbox_lectures['yscrollcommand'] = self.scrollbar_lectures.set
        self.listbox_lectures.insert(
            'end', *[i[1] for i in ['test1', 'test2', 'test3']])    # ! insert get_lecture()
        # Create Radiobuttons for select percentage
        self.label_selectpercentage = tk.Label(self,
                                               text='Select words:')
        self.label_selectpercentage.grid(column=0, row=2)
        # Add Radiobutton 'Select All'
        self.select_all = tk.Radiobutton(self, text='All words',
                                         variable=self.var_register, value=1.0)
        self.select_all.grid(column=0, row=3)
        # Add Radiobutton 'Select Register 90%'
        self.select_below90 = tk.Radiobutton(self, text='All words below 90%',
                                             variable=self.var_register, value=0.9)
        self.select_below90.grid(column=0, row=4)
        # Add Radiobutton 'Select Register 75%'
        self.select_below75 = tk.Radiobutton(self, text='All words below 75%',
                                             variable=self.var_register, value=0.75)
        self.select_below75.grid(column=0, row=5)
        # Add Radiobutton 'Select Register 50%'
        self.select_below50 = tk.Radiobutton(self, text='All words below 50%',
                                             variable=self.var_register, value=0.5)
        self.select_below50.grid(column=0, row=6)
        # Create Radiobuttons for select order
        self.label_selectorder = tk.Label(self, text='Select order:')
        self.label_selectorder.grid(column=0, row=7)
        # Add Radiobutton 'Sorted Order'
        self.select_sortedorder = tk.Radiobutton(self, text='Sorted Order',
                                                 variable=self.var_order, value=0)
        self.select_sortedorder.grid(column=0, row=8)
        # Add Radiobutton 'Random Order'
        self.select_randomorder = tk.Radiobutton(self, text='Random Order',
                                                 variable=self.var_order, value=1)
        self.select_randomorder.grid(column=0, row=9)
        # Create Label for wordcount
        self.label_wordcount = tk.Label(self)
        self.label_wordcount.grid(column=0, row=10)
        # Create buttons for start training and Go to MainPage
        self.goto_TrainingPage = tk.Button(self, text='Start Training',
                                           command=lambda: [self.set_selection(),
                                                            root.switch_frame(TrainingPage)])
        self.goto_TrainingPage.grid(column=0, row=11)
        self.goto_MainPage = tk.Button(self, text='Go back to Main Page',
                                       command=lambda: main.root.switch_frame(main.MainPage))
        self.goto_MainPage.grid(column=0, row=12)

    def add_bindings(self):
        self.listbox_lectures.bind('<<ListboxSelect>>', self.change_selection)

    def change_selection(self, event):
        self.label_wordcount['text'] = get_wordcount([self.listbox_lectures.get(
            i) for i in self.listbox_lectures.curselection()], self.var_register.get())

    def set_selection(self):
        global training_lectures
        training_lectures = [self.listbox_lectures.get(
            i) for i in self.listbox_lectures.curselection()]
        global training_percentage
        training_percentage = self.var_register
        global training_order
        training_order = self.var_order
