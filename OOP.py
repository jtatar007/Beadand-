from abc import ABC, abstractmethod
from datetime import date, datetime

class Room(ABC):
    def __init__(self, price, room_number):
        self.price = price
        self.room_number = room_number

    @abstractmethod
    def info(self):
        pass

class SingleRoom(Room):
    def __init__(self, room_number, price=5000):
        super().__init__(price, room_number)
        self.bed_type = "single"

    def info(self):
        return f"Room number: {self.room_number}, Price: {self.price}, Bed type: {self.bed_type}"

class DoubleRoom(Room):
    def __init__(self, room_number, price=8000):
        super().__init__(price, room_number)
        self.beds_count = 2

    def info(self):
        return f"Room number: {self.room_number}, Price: {self.price}, Beds count: {self.beds_count}"

class Booking:
    next_id = 1

    def __init__(self, room, booking_date, guest_name):
        if not isinstance(room, Room):
            raise TypeError("Only Room type objects can be booked.")
        self.id = f"{Booking.next_id:04d}"
        Booking.next_id += 1
        self.room = room
        self.booking_date = booking_date
        self.guest_name = guest_name

    def info(self):
        return f"Booking ID: {self.id}, Booking date: {self.booking_date.strftime('%d-%m-%Y')}, Guest name: {self.guest_name}, {self.room.info()}"

class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms = []
        self.bookings = []

    def add_room(self, room):
        if isinstance(room, Room):
            self.rooms.append(room)
        else:
            raise TypeError("Only Room type objects can be added.")

    def book_room(self, room_number, booking_date, guest_name):
        if booking_date <= date.today():
            raise Exception("The booking date must be in the future.")
        
        for booking in self.bookings:
            if booking.room.room_number == room_number and booking.booking_date == booking_date:
                raise Exception("This room is already booked for this date.")
        
        for room in self.rooms:
            if room.room_number == room_number:
                new_booking = Booking(room, booking_date, guest_name)
                self.bookings.append(new_booking)
                return new_booking
        
        raise Exception("No room found with this room number in the hotel.")

    def cancel_booking(self, booking_id):
        for booking in self.bookings:
            if booking.id == booking_id:
                self.bookings.remove(booking)
                return f"Booking {booking.id} for date {booking.booking_date.strftime('%d-%m-%Y')} has been successfully cancelled."
        
        raise Exception("No booking found with this ID.")

    def list_bookings(self):
        if not self.bookings:
            return "No bookings found."
        return "\n".join(booking.info() for booking in self.bookings)

    def info(self):
        hotel_info = f"Hotel name: {self.name}\nNumber of rooms: {len(self.rooms)}"
        rooms_info = "\n".join(room.info() for room in self.rooms)
        bookings_info = "\n".join(booking.info() for booking in self.bookings)
        return f"{hotel_info}\n\nRooms:\n{rooms_info}\n\nBookings:\n{bookings_info}"

# Create an instance of the Hotel
hotel = Hotel("Sample Hotel")

# Adding initial rooms
single_rooms = [SingleRoom(room_number) for room_number in range(101, 104)]
double_rooms = [DoubleRoom(room_number) for room_number in range(201, 204)]

# Adding rooms to the hotel
for room in single_rooms + double_rooms:
    hotel.add_room(room)

# Adding initial bookings
initial_bookings = [
    (101, date(2024, 6, 1), "John Doe"),
    (102, date(2024, 6, 2), "Jane Smith"),
    (103, date(2024, 6, 3), "Alice Johnson"),
    (201, date(2024, 6, 4), "Robert Brown"),
    (202, date(2024, 6, 5), "Emily Davis")
]

for room_number, booking_date, guest_name in initial_bookings:
    hotel.book_room(room_number, booking_date, guest_name)

def user_interface():
    while True:
        print("\nHotel Menu:")
        print("1. Book a room")
        print("2. Cancel a booking")
        print("3. List all bookings")
        print("4. Hotel information")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ")
        
        if choice == "1":
            try:
                room_number = int(input("Enter room number: "))
                date_str = input("Enter date (dd-mm-yyyy): ")
                booking_date = datetime.strptime(date_str, "%d-%m-%Y").date()
                guest_name = input("Enter guest name: ")
                booking = hotel.book_room(room_number, booking_date, guest_name)
                print(f"Booking successful! Booking ID: {booking.id}, Room number: {booking.room.room_number}, Date: {booking.booking_date.strftime('%d-%m-%Y')}, Guest name: {booking.guest_name}")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "2":
            try:
                booking_id = input("Enter booking ID: ")
                message = hotel.cancel_booking(booking_id)
                print(message)
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "3":
            print("List of bookings:")
            print(hotel.list_bookings())
        
        elif choice == "4":
            print(hotel.info())
        
        elif choice == "5":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice, please try again.")

# Start the user interface
user_interface()
