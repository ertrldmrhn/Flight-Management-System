from flight import Flight
from logbook import LogbookDatabase
from plane import Plane
from checklist import ChecklistDatabase
from plane_database import PlaneDatabase

def logbook_menu(logbook):
    def create_flight():
        date = input('Enter date: ')
        model = input('Enter aircraft: ').upper()
        departure = input('Enter departure: ').upper()
        arrival = input('Enter arrival: ').upper()
        runway = input('Enter runway: ').upper()
        gate = input('Enter gate: ').upper()
        flight = Flight(date, model, departure, arrival, runway, gate)
        return flight

    def add_flight(logbook):
        while True:
            flight = create_flight()
            logbook.save_flight(flight)
            print("Flight succesfully added")
            add_another = input("Do you want to add another flight? (yes/no): ").strip().lower()
            if add_another != 'yes':
                break

    def view_flights(logbook):
        flights = logbook.load_flights()
        if not flights:
            print("No flights found.")
            return
        for flight in flights:
            print(f"ID: {flight.id} | {flight}")

    def search_flights(logbook):
        criteria = input("Search by (date, departure, arrival): ").strip().lower()
        value = input(f"Enter {criteria}: ").strip()

        flights = logbook.load_flights()
        results = [
            flight for flight in flights 
            if getattr(flight, criteria, '').lower() == value.lower()
        ]

        if results:
            for flight in results:
                print(flight)
        else:
            print("No matching flights found.")

    def update_flight(logbook):
        view_flights(logbook)  
        flight_id = input("Enter the ID of the flight to update: ").strip()

        flights = logbook.load_flights()
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

                logbook.update_flight(flight)
                print("Flight updated successfully.")
                return
        print("Flight not found.")

    def delete_flight(logbook):
        view_flights(logbook)  
        flight_id = input("Enter the ID of the flight to delete: ").strip()

        flights = logbook.load_flights()
        for flight in flights:
            if str(flight.id) == flight_id:
                logbook.delete_flight(flight_id)
                print("Flight deleted successfully.")
                return
        print("Flight not found.")
    
    while True:
        print('\n--- Logbook Menu ---')
        print("1. Add Flight")
        print("2. View Flights")
        print("3. Search Flights")
        print("4. Delete Flight")
        print("5. Update Flight")
        print("6. Back to Main Menu")

        choice = input("Choose an option: ").strip()
        print()

        if choice == "1":
            add_flight(logbook)
        elif choice == "2":
            view_flights(logbook)
        elif choice == "3":
            search_flights(logbook)
        elif choice == "4":
            delete_flight(logbook)
        elif choice == "5":
            update_flight(logbook)
        elif choice == "6":
            break
        else:
            print("Invalid option. Please try again.")


def plane_menu(plane_db, logbook):
    while True:
        print("\n--- Plane Menu ---")
        print("1. Add a new plane")
        print("2. View plane statistics")
        print("3. List all planes")
        print("4. Delete Plane")
        print("5. Back to Main Menu")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            model = input("Enter the model of the plane: ").strip().upper()
            plane_db.add_plane(model)

        elif choice == "2":
            model = input("Enter the model of the plane to view statistics: ").strip().upper()
            plane_data = plane_db.get_plane(model)
            if plane_data:
                print(f"--- Statistics for {model} ---")
                print(f"Number of Flights: {plane_data[2]}")
                print(f"Total Duration: {plane_data[3]:.2f} hours")
                print(f"Total Distance: {plane_data[4]:.2f} nautical miles")
            else:
                print(f"Plane '{model}' not found.")

        elif choice == "3":
            planes = plane_db.list_planes()
            print("\n--- List of Planes ---")
            for plane in planes:
                print(f"- {plane}")

        elif choice == "4":
            model = input("Enter the model of the plane to delete: ").strip().upper()
            plane_data = plane_db.get_plane(model)
            if plane_data:
                confirm = input(f"Are you sure you want to delete plane '{model}'? (yes/no): ").strip().lower()
                if confirm == "yes":
                    plane_db.delete_plane(model)
                else:
                    print("Deletion canceled.")
            else:
                print(f"Plane '{model}' not found.")

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please try again.")

def checklist_menu(checklist, plane_db):
    while True:
        print("\n--- Checklist Menu ---")
        print("1. Add a Checklist")
        print("2. View a Checklist")
        print("3. Remove a Checklist")
        print("4. Display All Checklists for a Plane")
        print("5. Back to Main Menu")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            model = input("Enter the model of the plane: ").strip().upper()
            if not plane_db.get_plane(model):
                print(f"Plane '{model}' not found. Add the plane first.")
                continue
            phase = input("Enter flight phase (pre-flight, in-flight, post-flight): ").strip().lower()
            items = input("Enter checklist items (comma-separated): ").strip().split(",")
            checklist.add_checklist(model, phase, items)
            print(f"Checklist for '{model}' ({phase}) added successfully.")

        elif choice == "2":
            model = input("Enter the model of the plane: ").strip().upper()
            phase = input("Enter flight phase (pre-flight, in-flight, post-flight): ").strip().lower()
            checklist = checklist.get_checklist(model, phase)
            if checklist:
                print(f"{phase.capitalize()} Checklist for {model}:")
                for item in checklist:
                    print(f"  - {item}")
            else:
                print(f"No checklist found for '{model}' ({phase}).")

        elif choice == "3":
            model = input("Enter the model of the plane: ").strip().upper()
            phase = input("Enter flight phase (pre-flight, in-flight, post-flight): ").strip().lower()
            checklist.remove_checklist(model, phase)
            print(f"Checklist for '{model}' ({phase}) removed successfully.")

        elif choice == "4":
            model = input("Enter the model of the plane to display all checklists: ").strip().upper()
            if not plane_db.get_plane(model):
                print(f"Plane '{model}' not found. Add the plane first.")
                continue
            print(f"All Checklists for {model}:")
            checklist.display_checklists(model)

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please try again.")



def main_menu():
    logbook = LogbookDatabase()
    logbook.create_table()
    plane_db = PlaneDatabase()
    plane_db.create_table()
    checklist = ChecklistDatabase()
    checklist.create_table()


    while True:
        print("\n--- Main Menu ---")
        print("1. Logbook Menu")
        print("2. Plane Menu")
        print("3. Checklist Menu")
        print("4. Route Planner Menu")
        print("5. Controls Menu")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            logbook_menu(logbook) 
        elif choice == "2":
            plane_menu(plane_db, logbook)
        elif choice == "3":
            checklist_menu(checklist, plane_db)
        elif choice == "4":
            #route_planner_menu()
            print("\nSorry, this function is under development")
        elif choice == "5":
            #controls_menu()
            print("\nSorry, this function is under development")
        elif choice == "6":
            print("Exiting program.")
            logbook.close()
            plane_db.close()
            checklist.close()
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()