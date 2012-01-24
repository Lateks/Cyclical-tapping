from Tkinter import *
import sys

class MainMenu(object):
    def __init__(self, starter_fun):
        self.root = Tk()
        self.root.title('Trial launcher')
        self.frame = Frame(self.root).pack()
        self.x_pad = 40
        self.start_trial = starter_fun

        self.__add_name_field()
        self.__add_start_button()
        self.__add_exit_button()

    def __add_name_field(self):
        Label(self.frame, text='Enter subject name:').pack(padx = self.x_pad)
        self.name_field = Entry(self.frame, width = 10)
        self.name_field.pack(padx = self.x_pad)

    def __add_start_button(self):
        self.start_button = Button(self.frame, text = 'Start', command = self.__start)
        self.start_button.pack(padx = self.x_pad, pady = 5)

    def __start(self):
        username = self.name_field.get()
        if username == '':
            dialog = Dialog(self.root, "Give subject name before proceeding")
            dialog.show()
        else:
            self.start_trial(username)

    def __add_exit_button(self):
        self.exit_button = Button(self.frame, text = 'Exit', command = self.__exit)
        self.exit_button.pack(padx = self.x_pad, pady = 15)

    def __exit(self):
        sys.exit(0)

    def run(self):
        self.root.update()
        self.root.mainloop()

class Dialog(object):
    def __init__(self, parent, dialog_text):
        self.parent = parent
        top = self.top = Toplevel(parent)
        top.title('Error')
        self.label = Label(top, text = dialog_text)
        self.label.pack(padx = 10, pady = 10)
        self.okbutton = Button(top, text = 'OK', command = self.__exit)
        self.okbutton.pack(pady = 5)

    def __exit(self):
        self.top.destroy()

    def show(self):
        self.parent.wait_window(self.top)
