from tkinter import *
from tkinter.ttk import Combobox
from PIL import ImageGrab

class Window():
    def __init__(self, root, data):
        self.root = root
        self.data = data
        
        # Creates the main 'canvas' or background window for the rest of the GUI elements to go on
        canvas = Canvas(root, width=1300, height=750, bg='grey')
        canvas.grid()
        self.canvas = canvas
        
        # Time selection
        canvas.create_text(10, 20, text='Select a time', font=('Arial  20'), anchor=W)
        # Dropdown box (Combobox)
        self.dropdown = Combobox(root, values=list(data.times), state='readonly', width=15)
        self.dropdown.set(list(data.times)[0])  # Set default to the first valid time
        self.dropdown.place(x=177, y=12)
        self.dropdown.bind('<<ComboboxSelected>>', lambda event: self.update_day())

        # Avaliable seats
        self.update_day()

        # Button to confirm seat selection
        self.confirm_button = Button(root, text='Sell Selected Seats', font='Arial 20', command=lambda: self.confirm_seat_selection())
        self.confirm_button.place(x=10, y=190, width=270, height=40)

        # Button to refund seats
        self.confirm_button = Button(root, text='Refund Seats', font='Arial 20', command=lambda: self.refund_seats(), bg='white')
        self.confirm_button.place(x=10, y=240, width=270, height=40)

        # Day reset button
        self.reset_button = Button(root, text='Reset Day', font='Arial 20', command=lambda: self.reset_day(), fg='red')
        self.reset_button.place(x=10, y=700, width=280, height=40)

        # Line to separate stage and seats from data and inputs
        canvas.create_rectangle(300, 0, 300, 750, width=3)

        # Stage Rectangle
        canvas.create_rectangle(500, 0, 1100, 70, width=2)
        # Stage Text
        canvas.create_text(800, 35, text='Stage', font=('Arial  45'))

        self.create_seats()
        canvas.bind("<Button-1>", self.clicked)
    

    # Function to only allow numbers in the seat input box
    def only_numbers(self, char):
        return char.isdigit()

    def reset_day(self):
        self.data.reset_day()
        self.update_day()

    def update_day(self):
        time = self.dropdown.get()
        cost = self.data.costs.get(time, 0)
        self.data.seats_selected = []

        # Available seats text
        self.canvas.create_rectangle(8, 50, 290, 70, fill='grey', outline='grey')
        self.canvas.create_text(10, 60, text='Available seats:', font=('Arial  20'), anchor=W)

        # Update cost text
        self.canvas.create_rectangle(8, 148, 290, 173, fill='grey', outline='grey')
        self.canvas.create_text(10, 160, text=f'Ticket cost: ${cost}', font=('Arial  20'), anchor=W)

        # Seats sold data display
        self.canvas.create_rectangle(8, 638, 290, 690, fill='grey', outline='grey')
        self.canvas.create_text(10, 650, text=f'Tickets sold: {self.data.tickets_sold}', font=('Arial  17'), anchor=W)
        self.canvas.create_text(10, 680, text=f'Value of tickets sold: ${self.data.value_tickets_sold}', font=('Arial  17'), anchor=W)

        # Update refund mode buttons
        self.confirm_button = Button(self.root, text='Refund Seats', font='Arial 20', command=lambda: self.refund_seats(), bg='red' if self.data.refund_mode else 'white')
        self.confirm_button.place(x=10, y=240, width=270, height=40)

        # Update seats
        self.create_seats()
        self.show_avaliable_seats()

    def show_avaliable_seats(self):

        # Time 1
        self.canvas.create_rectangle(8, 80, 290, 100, fill='grey', outline='black')
        self.canvas.create_text(10, 90, text=f'{self.data.time_1}:', font=('Arial  15'), anchor=W)
        self.canvas.create_text(190, 90, text=f'{self.data.available_seats_num(self.data.time_1)}/{self.data.total_seats_time_1}', font=('Arial  15'), anchor=W)

        # Time 2
        self.canvas.create_rectangle(8, 100, 290, 120, fill='grey', outline='black')
        self.canvas.create_text(10, 110, text=f'{self.data.time_2}:', font=('Arial  15'), anchor=W)
        self.canvas.create_text(190, 110, text=f'{self.data.available_seats_num(self.data.time_2)}/{self.data.total_seats_time_2}', font=('Arial  15'), anchor=W)

        # Time 3
        self.canvas.create_rectangle(8, 120, 290, 140, fill='grey', outline='black')
        self.canvas.create_text(10, 130, text=f'{self.data.time_3}:', font=('Arial  15'), anchor=W)
        self.canvas.create_text(190, 130, text=f'{self.data.available_seats_num(self.data.time_3)}/{self.data.total_seats_time_3}', font=('Arial  15'), anchor=W)

    def create_seats(self):
        ytop = 80
        xleft = 314
        self.ytop = ytop
        self.xleft = xleft
        row_length = 20 
        self.row_length = row_length
        # Clear previous seat selection
        self.canvas.create_rectangle(307, 80, 1300, 750, fill='grey', outline='grey')
        # Use the data from the selected time .csv file to create the seat selection GUI
        time = self.dropdown.get()
        with open(f'{time}.csv', 'r') as file:
            lines = file.readlines()

            for line in lines:
                seats = line.strip().split(',')
                xleft = 314
                for seat in seats:
                    if seat.split(':')[1] == '0':
                        fill_colour = 'grey40' 
                    else:
                        fill_colour = 'red'
                    self.canvas.create_rectangle(xleft, ytop, xleft + 45, ytop + 45, fill=fill_colour, outline='black')
                    xleft += 49
                ytop += 49
    
    def clicked(self, event):
        x = event.x
        y = event.y

        # Check if the click is within the seat area
        if 314 < x < 1300 and 80 < y < 750:
            # Get the pixel colour at the clicked position
            clicked_pixel = self.canvas.find_closest(x, y)
            pixel_colour = self.canvas.itemcget(clicked_pixel, 'fill')

            # Calculate the row and column of the click location
            row = (y - self.ytop) // 49
            self.data.times[self.dropdown.get()] // self.row_length
            if True:
                column = (x - self.xleft) // 49

            self.select_seat(row, column, pixel_colour)


    def select_seat(self, row, column, colour):
        # Calculate the seat number based on the row and column clicked
        seat_number = 20*row + column + 1
        # Makes sure you cant select a seat that doesn't exist
        if seat_number > self.data.times[self.dropdown.get()]:
            return
        # Sets the location of the top left corner of the unselected seat
        xleft = self.xleft + column*49
        ytop = self.ytop + row*49

        # If refund mode isn't active, allow the user to select seats
        if self.data.refund_mode == False:
            # Check if the pixel color is grey40, which indicates an available seat
            if colour == 'grey40':
                # Add seat to the list of selected seats
                self.data.seats_selected.append(seat_number)
                # Update the gui to show the selected seat
                self.canvas.create_rectangle(xleft, ytop, xleft + 45, ytop + 45, fill='yellow', outline='black')
                                            

            # Check if the pixel color is yellow, which indicates a selected but not taken seat
            elif colour == 'yellow':
                # Remove seat from the list of selected seats
                self.data.seats_selected.remove(seat_number)
                # Changes the color of the unselected seat to grey40 to show that it's available
                self.canvas.create_rectangle(xleft, ytop, xleft + 45, ytop + 45, fill='grey40', outline='black')

        # If refund mode is active, allow the user to refund already selected seats
        elif self.data.refund_mode == True:
            # Check if the pixel color is red, which indicates a taken seat or black, which indicates the edge of a seat
            if colour == 'red':
                self.data.seats_selected.append(seat_number)
                # Change the color of the seat to grey40 to show that it's selected
                self.canvas.create_rectangle(xleft, ytop, xleft + 45, ytop + 45, fill='orange', outline='black')
    
    def refund_seats(self):
        self.data.seats_selected = []
        # If the button is pressed and the GUI isn't in refund mode, change it and show the user that it has changed
        if self.data.refund_mode == False:
            # Toggle refund mode
            self.data.refund_mode = True

            self.confirm_button.destroy()
            # Changes the colour of the refund seats button to show the user that refund mode is active
            self.confirm_button = Button(self.root, text='Refund Seats', font='Arial 20', command=lambda: self.refund_seats(), bg='red')
            self.confirm_button.place(x=10, y=240, width=270, height=40)

            # Adds a button to allow the user to refund the seats
            self.refund_seats_button = Button(self.root, text='Refund Selected Seats', font='Arial 18', command=lambda: self.refund_seat_selection())
            self.refund_seats_button.place(x=10, y=290, width=270, height=40)
        
        # If the button is pressed and the GUI is in refund mode, change it and show the user that it has changed
        elif self.data.refund_mode == True:
            # Toggle refund mode
            self.data.refund_mode = False
            # Remove the confirm refund seats button
            self.confirm_button.destroy()
            self.confirm_button = Button(self.root, text='Refund Seats', font='Arial 20', command=lambda: self.refund_seats(), bg='white')
            self.refund_seats_button.destroy()
        self.update_day()

    def refund_seat_selection(self):
        self.refund_seats_button.destroy()
        for seat in self.data.seats_selected:
            # Refund the seat
            self.data.change_seat_value(self.dropdown.get(), seat)
            # Remove the refunded seat from the tickets sold variable
            self.data.tickets_sold -= 1
            # Remove the cost of the refunded seat from the value of tickets sold variable
            self.data.value_tickets_sold -= self.data.costs[self.dropdown.get()]
        self.data.seats_selected = []
        # Update GUI
        self.data.refund_mode = False
        self.update_day()

    def confirm_seat_selection(self):
        for seat in self.data.seats_selected:
            # Sell the seat
            self.data.change_seat_value(self.dropdown.get(), seat)
            # Add the sold seat to the tickets sold variable
            self.data.tickets_sold += 1
            # Add the cost of the sold seat to the value of tickets sold variable
            self.data.value_tickets_sold += self.data.costs[self.dropdown.get()]
        self.data.seats_selected = []
        # Update GUI
        self.update_day()

class Data():
    def __init__(self, times, costs):
        self.times = times
        self.costs = costs
        self.refund_mode = False

        self.time_1 = list(times)[0]
        self.time_2 = list(times)[1]
        self.time_3 = list(times)[2]

        self.total_seats_time_1 = self.times[self.time_1]
        self.total_seats_time_2 = self.times[self.time_2]
        self.total_seats_time_3 = self.times[self.time_3]

        self.cost_1 = self.costs[self.time_1]
        self.cost_2 = self.costs[self.time_2]
        self.cost_3 = self.costs[self.time_3]

        self.reset_day()
        
    def reset_day(self):
        self.seats_selected = []
        self.tickets_sold = 0
        self.value_tickets_sold = 0
        # Create a CSV file for each time and create the seats in it
        for time in self.times:
            with open(f'{time}.csv', 'w') as file:
                for seat in range(1, self.times.get(time) + 1, 20):
                    row = ','.join(f'{seat + seat_index}:0' for seat_index in range(20) if seat + seat_index <= self.times.get(time))
                    file.write(f'{row}\n')

    def change_seat_value(self, time, seat_to_change):
        with open(f'{time}.csv', 'r') as file:
            lines = file.readlines()
        with open(f'{time}.csv', 'w') as file:
            for line in lines:
                seats = line.strip().split(',')
                updated_seats = []
                for seat in seats:
                    seat_number, status = seat.split(':')
                    if int(seat_number) == seat_to_change:
                        if int(status) == 0:
                            print(f'{seat_number}:1')
                            updated_seats.append(f'{seat_number}:1')  # Update the specific seat
                        elif int(status) == 1:
                            updated_seats.append(f'{seat_number}:0')  # Update the specific seat
                    else:
                        updated_seats.append(f'{seat_number}:{status}')
                file.write(','.join(updated_seats) + '\n')

    # Function to return the number of seats avaliable by reading the relevant csv file
    def available_seats_num(self, time):
        with open(f'{time}.csv', 'r') as file:
            lines = file.readlines()
            # Creates a list for available seats
            available = []
            for line in lines:
                seats = line.strip().split(',')
                for seat in seats:
                        seat_number, status = seat.split(':')
                        # Check if the seat == 0 which means it is available
                        if status == '0':
                            # Add any avaliable seats to the list
                            available.append(int(seat_number))
        return len(available)


def main():
    # Creates a dictionary of times and costs
    times = {'10am': 150, '3pm': 150, '8pm': 250}
    costs = {'10am': 5, '3pm': 5, '8pm': 12}

    data = Data(times, costs)
    main_window = Tk()
    Window(main_window, data)
    main_window.title('Circus tickets')
    main_window.mainloop()

if __name__ == '__main__':
    main()
