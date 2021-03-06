import sys
from Tkinter import *
from trial_runner import TrialRunner

def main():
    menu = MainMenu()
    menu.run()

class MainMenu(object):
    def __init__(self):
        self.root = Tk()
        self.root.title('Trial launcher')
        self.root.protocol("WM_DELETE_WINDOW", self.__exit)
        self.frame = Frame(self.root).pack()
        self.x_pad = 40

        self.__add_name_field()
        self.__add_info_fied()
        self.__bind_keys()
        self.__add_start_button()
        self.__add_exit_button()

        self.trial_runner = TrialRunner()

    def __add_name_field(self):
        self.__add_label('Enter subject name:')
        self.name_field = Entry(self.frame, width = 10)
        self.name_field.pack(padx = self.x_pad, pady = 5)

    def __add_info_fied(self):
        self.__add_label('Additional information:')
        self.info_field = Text(self.frame, width = 20, height = 3)
        self.info_field.pack(padx = self.x_pad, pady = 5)

    def __add_label(self, text):
        Label(self.frame, text=text).pack(padx = self.x_pad, pady = 5)

    def __bind_keys(self):
        self.root.bind('<Return>', self.__try_start)
        self.root.bind('<Escape>', self.__exit)

    def __add_start_button(self):
        self.start_button = Button(self.frame, text = 'Start',
            command = self.__try_start)
        self.start_button.pack(padx = self.x_pad, pady = 5)

    def __try_start(self, event = None):
        self.username = self.name_field.get()
        if self.username == '':
            dialog = Dialog(self.root, "Give subject name before proceeding")
            dialog.show()
            self.root.focus_set()
        else:
            self.info = self.info_field.get(1.0, END)
            self.trial_runner.new_trial(self.username, self.info)
            self.trial_runner.run()

    def __add_exit_button(self):
        self.exit_button = Button(self.frame, text = 'Exit', command = self.__exit)
        self.exit_button.pack(padx = self.x_pad, pady = 15)

    def __exit(self, event = None):
        sys.exit(0)

    def run(self):
        self.root.update()
        self.root.mainloop()

class Dialog(object):
    def __init__(self, parent, dialog_text):
        self.parent = parent
        top = self.top = Toplevel(parent)
        top.transient(parent)
        self.top.grab_set()
        self.top.protocol("WM_DELETE_WINDOW", self.__exit)
        top.title('Error')

        self.label = Label(top, text = dialog_text)
        self.label.pack(padx = 10, pady = 10)
        self.okbutton = Button(top, text = 'OK', command = self.__exit)
        self.okbutton.pack(pady = 5)

    def __exit(self):
        self.top.destroy()

    def show(self):
        self.top.focus_set()
        self.parent.wait_window(self.top)

if __name__ == '__main__':
    main()
