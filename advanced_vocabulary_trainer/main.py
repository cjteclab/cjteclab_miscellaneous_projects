import tkinter as tk
import trainingsession


class VocabularyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.set_basic_app_infos()
        # Instead of choose MainPage() as self.frame we use None because the
        # correct frame is choosen by the following function call
        self.frame = None
        self.switch_frame(MainPage)

    def set_basic_app_infos(self):
        self.title("CJ\'s Vocabulary Trainer")
        self.geometry('400x400')
        self.resizable(False, False)

    def switch_frame(self, targetframe):
        self.new_frame = targetframe(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = self.new_frame
        self.frame.pack()


class MainPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.add_widgets()

    def add_widgets(self):
        # Button for Training Session
        self.button_TrainingSession = tk.Button(self, text='Start Training Session',
                                                command=lambda: root.switch_frame(trainingsession.TrainingSession))
        self.button_TrainingSession.pack()
        # Button for Adding Vocabularies
        self.button_AddVocabulary = tk.Button(self, text='Adding Vocabularies',
                                              command=lambda: root.switch_frame(AddVocabulary))
        self.button_AddVocabulary.pack()
        # Button for Session History
        self.button_SessionHistory = tk.Button(self, text='View Session History',
                                               command=lambda: root.switch_frame(SessionHistory))
        self.button_SessionHistory.pack()
        # Button for StatisticPage
        self.button_StatisticPage = tk.Button(self, text='View Statistics',
                                              command=lambda: root.switch_frame(StatisticPage))
        self.button_StatisticPage.pack()
        # Button for Exit
        self.button_Exit = tk.Button(self, text='Exit',
                                     command=lambda: root.destroy())
        self.button_Exit.pack()


if __name__ == '__main__':
    root = VocabularyApp()
    root.mainloop()
