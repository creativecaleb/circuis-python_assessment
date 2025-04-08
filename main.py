from tkinter import *
from tkinter.ttk import Combobox

class Window():
    def __init__(self, root, data):
        self.root = root
        self.data = data
        
        # Creates the main 'canvas' or background window for the rest of the GUI elements to go on
        canvas = Canvas(root, width=1300, height=700, bg='grey')
        canvas.grid()
        self.canvas = canvas

        # Data and inputs
        
        # Time selection
        canvas.create_text(10, 20, text='Select a time', font=('Arial  20'), anchor=W)
        # Dropdown box (Combobox)
        self.dropdown = Combobox(root, values=list(data.times), state='readonly', width=15)
        self.dropdown.set(list(data.times)[0])  # Set default to the first valid time
        self.dropdown.place(x=177, y=12)
        self.dropdown.bind('<<ComboboxSelected>>', lambda event: self.update_day())

        # Avaliable seats
        self.update_day()

        # Ticket Cost
        canvas.create_text(10, 160, text='Ticket cost:', font=('Arial  20'), anchor=W)

        """
            # Removed because the number of seats to select is limited by the seat selector GUI
        # Seat selection
        canvas.create_text(8, 250, text='Number of seats to buy', font=('Arial  20'), anchor=W)
        # Seat number input
        validation = root.register(self.only_numbers)
        self.seat_input = Entry(root, validate = 'key', validatecommand = (validation, '%S'))
        self.seat_input.place(x=10, y=270, width=100, height=30)
        # Button to confirm seat number
        self.seat_button = Button(root, text='Select', font='Arial 15', command=lambda: self.confirm_seat_number())
        self.seat_button.place(x=120, y=270, width=100, height=30)
        # Button to confirm seat selection
        self.confirm_button = Button(root, text='Confirm Selection', font='Arial 15', command=lambda: self.confirm_seat_selection())
        self.confirm_button.place(x=10, y=310, width=210, height=30)
        """
        
        # Seats sold data display
        canvas.create_text(10, 600, text=f'Tickets sold: {self.data.tickets_sold}', font=('Arial  18'), anchor=W)
        canvas.create_text(10, 630, text=f'Value of tickets sold: {self.data.value_tickets_sold}', font=('Arial  18'), anchor=W)

        # Day reset button
        self.reset_button = Button(root, text='Reset Day', font='Arial 20', command=lambda: self.data.reset_day(), fg='red')
        self.reset_button.place(x=10, y=650, width=280, height=40)

        # Line to separate stage and seats from data and inputs
        canvas.create_rectangle(300, 0, 300, 700, width=3)

        # Stage Rectangle
        canvas.create_rectangle(500, 0, 1100, 70, width=2)
        # Stage Text
        canvas.create_text(800, 35, text='Stage', font=('Arial  45'))

        self.create_seats()
    

    # Function to only allow numbers in the seat input box
    def only_numbers(self, char):
        return char.isdigit()

    def update_day(self):
        time = self.dropdown.get()
        cost = self.data.costs.get(time, 0)

        # Update available seats
        self.canvas.create_text(10, 60, text='Available seats:', font=('Arial  20'), anchor=W)
    	
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

        # Update cost text
        self.canvas.create_rectangle(10, 188, 100, 212, fill='grey', outline='grey')
        self.canvas.create_text(10, 200, text=f'${cost}', font=('Arial  20'), anchor=W)
        # Update available seats on GUI

        # Update seats
        self.create_seats()

    def create_seats(self):
        # Clear previous seat selection
        self.canvas.create_rectangle(307, 90, 1300, 700, fill='grey', outline='grey')
        # Use the data from the selected time .csv file to create the seat selection GUI
        time = self.dropdown.get()
        with open(f'{time}.csv', 'r') as file:
            lines = file.readlines()
            
            row_count = sum(1 for row in file)

            # Generic seat selection GUI
            xleft = 314
            ytop = 90
            for line in lines:
                seats = line.strip().split(',')
                for seat in seats:
                    self.canvas.create_rectangle(xleft, ytop, xleft + 45, ytop + 45, fill='grey', outline='black')
                    xleft += 49
                ytop += 49
                xleft = 314

class Data():
    def __init__(self, times, costs):
        self.times = times
        self.costs = costs

        self.time_1 = list(times)[0]
        self.time_2 = list(times)[1]
        self.time_3 = list(times)[2]

        self.total_seats_time_1 = self.times[self.time_1]
        self.total_seats_time_2 = self.times[self.time_2]
        self.total_seats_time_3 = self.times[self.time_3]

        self.cost_1 = self.costs[self.time_1]
        self.cost_2 = self.costs[self.time_2]
        self.cost_3 = self.costs[self.time_3]

        self.seats_to_select = 0
        self.seats_selected = 0

        self.tickets_sold = 0
        self.value_tickets_sold = 0

    def reset_day(self):
        self.tickets_sold = 0
        self.value_tickets_sold = 0
        for time in self.times:
            with open(f'{time}.csv', 'w') as file:
                file.write('')
        self.time_file_create()

    def time_file_create(self):
        for time in self.times:
            with open(f'{time}.csv', 'w') as file:
                for seat in range(1, self.times.get(time) + 1, 20):
                    row = ','.join(f'{seat + seat_index}:0' for seat_index in range(20) if seat + seat_index <= self.times.get(time))
                    file.write(f'{row}\n')

    def sell_seat(self, time, seat):
        with open(f'{time}.csv', 'r') as file:
            lines = file.readlines()
        with open(f'{time}.csv', 'w') as file:
            for line in lines:
                if f'{seat}:0' in line:
                    line = line.replace(f'{seat}:0', f'{seat}:1')
                file.write(line)

    def available_seats_num(self, time):
        with open(f'{time}.csv', 'r') as file:
            lines = file.readlines()
        available = []
        for line in lines:
            seats = line.strip().split(',')
            for seat in seats:
                seat_number, status = seat.split(':')
                if status == '0':
                    available.append(int(seat_number))
        return len(available)


def main():
    times = {'10am': 150, '3pm': 150, '8pm': 250}
    costs = {'10am': 5, '3pm': 5, '8pm': 12}
    data = Data(times, costs)
    data.time_file_create()
    main_window = Tk()
    Window(main_window, data)
    main_window.title('Circus tickets')
    main_window.mainloop()

if __name__ == '__main__':
    main()

