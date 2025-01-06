from flight import Flight
from logbook import LogbookDatabase
from plane import Plane
from checklist import ChecklistDatabase
from plane_database import PlaneDatabase
from controls import ControlsDatabase

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
        print("0. Back to Main Menu")

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
        elif choice == "0":
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
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            model = input("Enter the model of the plane: ").strip().upper()
            plane_db.add_plane(model)

        elif choice == "2":
            model = input("Enter the model of the plane to view statistics: ").strip().upper()
            plane_data = plane_db.get_plane(model)
            if plane_data:
                num_flights, total_duration = plane_db.update_statistics(model, logbook)
                print(f"--- Statistics for {model} ---")
                print(f"Number of Flights: {num_flights}")
                print(f"Total Duration: {total_duration:.2f} hours")
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

        elif choice == "0":
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
        print("0. Back to Main Menu")
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

        elif choice == "0":
            break

        else:
            print("Invalid choice. Please try again.")

def controls_menu(controls):
    while True:
        print("\n--- Controls Menu ---")
        print("1. Create a New Profile")
        print("2. View All Profiles")
        print("3. Delete a Profile")
        print("4. Add Button Mapping")
        print("5. View Mappings for a Profile")
        print("6. Delete a Mapping")
        print("7. Update a Mapping")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = input("Enter the profile name: ").strip()
            type = input("Enter the profile type (mouse/controller/joystick): ").strip().lower()
            controls.add_profile(name, type)
            print("Profile added successfully!")

        elif choice == "2":
            profiles = controls.get_profiles()
            print("\n--- Profiles ---")
            for profile in profiles:
                print(f"ID: {profile[0]}, Name: {profile[1]}, Type: {profile[2]}")

        elif choice == "3":
            profile_id = int(input("Enter the Profile ID to delete: "))
            controls.delete_profile(profile_id)

        elif choice == "4":
            profile_id = int(input("Enter the Profile ID: "))
            buttons = input("Enter the button combination: ").strip()
            function = input("Enter the function to assign: ").strip()
            controls.add_mapping(profile_id, buttons, function)
            print("Mapping added successfully!")

        elif choice == "5":
            profile_id = int(input("Enter the Profile ID: "))
            mappings = controls.get_mappings(profile_id)
            print("\n--- Mappings ---")
            for mapping in mappings:
                print(f"ID: {mapping[0]}, Buttons: {mapping[2]}, Function: {mapping[3]}")

        elif choice == "6":
            mapping_id = int(input("Enter the Mapping ID to delete: "))
            controls.delete_mapping(mapping_id)
            print("Mapping deleted successfully!")

        elif choice == "7":
            mapping_id = int(input("Enter the Mapping ID to update: "))
            print("Leave fields blank if you don't want to update them.")
            buttons = input("Enter the new button combination (or press Enter to skip): ").strip() or None
            function = input("Enter the new function (or press Enter to skip): ").strip() or None
            controls.update_mapping(mapping_id, buttons, function)

        elif choice == "0":
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
    controls = ControlsDatabase()
    controls.create_tables()

    while True:
        print("\n--- Main Menu ---")
        print("1. Logbook Menu")
        print("2. Plane Menu")
        print("3. Checklist Menu")
        print("4. Route Planner Menu")
        print("5. Controls Menu")
        print("0. Exit")
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
            controls_menu(controls)
        elif choice == "0":
            print("Exiting program.")
            logbook.close()
            plane_db.close()
            checklist.close()
            controls.close()
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()