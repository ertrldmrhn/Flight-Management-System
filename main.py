from flight import Flight
from logbook import Logbook
from plane import Plane


def initialize_logbook():    
    db = Logbook()
    db.create_table()
    return db

def create_flight():
    date = input('Enter date: ')
    model = input('Enter aircraft: ')
    departure = input('Enter departure: ').upper()
    arrival = input('Enter arrival: ').upper()
    runway = input('Enter runway: ').upper()
    gate = input('Enter gate: ').upper()
    flight = Flight(date, model, departure, arrival, runway, gate)
    return flight

def add_flight(db):
    while True:
        flight = create_flight()
        db.save_flight(flight)
        print("Flight succesfully added")
        add_another = input("Do you want to add another flight? (yes/no): ").strip().lower()
        if add_another != 'yes':
            break

def view_flights(db):
    flights = db.load_flights()
    if not flights:
        print("No flights found.")
        return
    for flight in flights:
        print(f"ID: {flight.id} | {flight}")

def search_flights(db):
    criteria = input("Search by (date, departure, arrival): ").strip().lower()
    value = input(f"Enter {criteria}: ").strip()

    flights = db.load_flights()
    results = [
        flight for flight in flights 
        if getattr(flight, criteria, '').lower() == value.lower()
    ]

    if results:
        for flight in results:
            print(flight)
    else:
        print("No matching flights found.")

def update_flight(db):
    view_flights(db)  # Show all flights first
    flight_id = input("Enter the ID of the flight to update: ").strip()

    flights = db.load_flights()
    for flight in flights:
        if str(flight.id) == flight_id:
            print("Leave fields blank to keep the current value.")
            flight.date = input(f"Enter new date ({flight.date}): ") or flight.date
            flight.model = input(f"Enter new aircraft ({flight.model}): ") or flight.model
            flight.departure = input(f"Enter new departure ({flight.departure}): ").upper() or flight.departure
            flight.arrival = input(f"Enter new arrival ({flight.arrival}): ").upper() or flight.arrival
            flight.runway = input(f"Enter new runway ({flight.runway}): ").upper() or flight.runway
            flight.gate = input(f"Enter new gate ({flight.gate}): ").upper() or flight.gate
            flight.set_duration(input(f"Enter new duration ({flight.duration or 'N/A'}): ") or flight.duration)
            flight.add_notes(input(f"Enter new notes ({flight.notes or 'N/A'}): ") or flight.notes)

            db.update_flight(flight)
            print("Flight updated successfully.")
            return
    print("Flight not found.")

def delete_flight(db):
    view_flights(db)  # Show all flights first
    flight_id = input("Enter the ID of the flight to delete: ").strip()

    flights = db.load_flights()
    for flight in flights:
        if str(flight.id) == flight_id:
            db.delete_flight(flight_id)
            print("Flight deleted successfully.")
            return
    print("Flight not found.")
    
def main_menu():
    db = initialize_logbook()
    
    while True:
        print('\nFlight Logbook Menu')
        print("1. Add Flight")
        print("2. View Flights")
        print("3. Search Flights")
        print("4. Delete Flight")
        print("5. Update Flight")
        print("6. Exit")

        choice = input("Choose an option: ").strip()
        print()

        if choice == "1":
            add_flight(db)
        elif choice == "2":
            view_flights(db)
        elif choice == "3":
            search_flights(db)
        elif choice == "4":
            delete_flight(db)
        elif choice == "5":
            update_flight(db)
        elif choice == "6":
            print("Goodbye!")
            db.close()
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()