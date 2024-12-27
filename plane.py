from logbook import LogbookDatabase
from checklist import ChecklistDatabase
from plane_database import PlaneDatabase

class Plane:
    def __init__(self, model):
        self.model = model
        self.num_flights = 0
        self.total_duration = 0.0
        self.total_distance = 0.0
        self.checklist = ChecklistDatabase()
        self.missing_durations = 0

    def update_statistics(self, logbook):
        """Calculate and update flight statistics using the logbook."""
        flights = logbook.load_flights()
        model_flights = [flight for flight in flights if flight.model == self.model]

        self.number_of_flights = len(model_flights)
        self.total_duration = sum(float(flight.duration or 0) for flight in model_flights)
        self.total_distance = sum(float(flight.distance or 0) for flight in model_flights)

        self.database.update_statistics(
            self.model, self.number_of_flights, self.total_duration, self.total_distance
        )
        #TODO: add distance calculation after implementation of route planner
    

    def add_checklist(self, phase, items):
        """Add a checklist for a specific phase using the checklist manager."""
        self.checklist.add_checklist(self.model, phase, items)

    def get_checklist(self, phase):
        """Retrieve the checklist for a specific phase."""
        return self.checklist.get_checklist(self.model, phase)

    def display_checklists(self):
        """Display all checklists for this plane model."""
        self.checklist.display_checklists(self.model)

    def remove_checklist(self, phase):
        """Remove the checklist for a specific phase."""
        self.checklist.remove_checklist(self.model, phase)