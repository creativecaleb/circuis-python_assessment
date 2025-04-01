from tkinter import *
from tkinter.ttk import Combobox
from ctypes import windll

class Window():
    def __init__(self, root):
        self.root = root
        self.times = ["10 AM", "3 PM", "8 PM"]
        
        # Creates the main 'canvas' or background window for the rest of the GUI elements to go on
        canvas = Canvas(root, width=1300, height=700, bg='grey')
        canvas.grid()

        # Data and inputs
        
        # Time selection
        canvas.create_text(10, 20, text='Select a time', font=('Arial  20'), anchor=W)
        # Dropdown box (Combobox)
        self.dropdown = Combobox(root, values=self.times, state='readonly', width=15)
        self.dropdown.set("Times")
        self.dropdown.place(x=177, y=12)

        # Avaliable seats
        canvas.create_text(10, 60, text='Available seats:', font=('Arial  20'), anchor=W)
        canvas.create_text(10, 90, text='10 AM:', font=('Arial  15'), anchor=W)

        # Line to separate stage and seats from data and inputs
        canvas.create_rectangle(300, 0, 300, 700, width=3)

        # Stage Rectangle
        canvas.create_rectangle(500, 0, 1100, 70, width=2)
        # Stage Text
        canvas.create_text(800, 35, text='Stage', font=('Arial  45'))

class Data():
    def __init__(self):
        pass

    
    
def main():
    main_window = Tk()
    windll.shcore.SetProcessDpiAwareness(1)
    Window(main_window)
    main_window.title('Circus tickets')
    main_window.mainloop()

if __name__ == '__main__':
    main()

