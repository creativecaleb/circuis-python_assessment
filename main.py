from tkinter import *

class Window():
    def __init__(self, root):
        self.root = root
        # Creates the main 'canvas' or background window for the rest of the GUI elements to go on
        canvas = Canvas(root, width=1300, height=700, bg='grey')
        canvas.grid()

        canvas.create_rectangle(300, 0, 301, 700)

class Data():
    def __init__(self):
        pass
    
def main():
    main_window = Tk()
    Window(main_window)
    main_window.title('Circus tickets')
    main_window.mainloop()

if __name__ == '__main__':
    main()

