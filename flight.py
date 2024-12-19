class Flight:
    def __init__(self, date, departure, arrival, runway, gate):
        self.id = None 
        self.date = date
        self.departure = departure
        self.arrival = arrival
        self.runway = runway
        self.gate = gate
        self.duration = None
        self.notes = None

    def to_dict(self):
        """Convert the Flight object to a dictionary."""
        return {
            "id": self.id,
            "date": self.date,
            "departure": self.departure,
            "arrival": self.arrival,
            "runway": self.runway,
            "gate": self.gate,
            "duration": self.duration,
            "notes": self.notes
        }

    def __str__(self):
        """Define the string representation of a Flight object."""
        return (f"Flight on {self.date}: {self.departure} -> {self.arrival} | "
                f"Runway: {self.runway}, Gate: {self.gate} | "
                f"Duration: {self.duration or 'N/A'} | Notes: {self.notes or 'N/A'}")

    def set_duration(self, duration):
        """Set the flight duration."""
        self.duration = duration

    def add_notes(self, notes):
        """Add notes to the flight."""
        self.notes = notes

