import sqlite3
from flight import Flight

class LogbookDatabase:
    def __init__(self, db_name="logbook.db"):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        """Establish a connection to the database."""
        if not self.conn:
            self.conn = sqlite3.connect(self.db_name)
            

    def close(self):
        """Close the connection to the database."""
        if self.conn:
            self.conn.close()
            self.conn = None
        else:
            print("Error: Connection doesn't exist")

    def create_table(self):
        """Create the logbook table if it doesn't exist."""
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS logbook (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            model TEXT,
            departure TEXT,
            arrival TEXT,
            runway TEXT,
            gate TEXT,
            duration TEXT,
            notes TEXT
        )
        """)
        self.conn.commit()

    def save_flight(self, flight):
        """Save a Flight object to the database."""
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO logbook (date, model, departure, arrival, runway, gate, duration, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (flight.date, flight.model, flight.departure, flight.arrival, flight.runway, flight.gate, flight.duration, flight.notes))
        flight.id = cursor.lastrowid  # Retrieve the auto-generated ID
        self.conn.commit()


    def update_flight(self, flight):
        """Update a flight's details."""
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("""
        UPDATE logbook
        SET date = ?, model = ?, departure = ?, arrival = ?, runway = ?, gate = ?, duration = ?, notes = ?
        WHERE id = ?
        """, (flight.date, flight.model, flight.departure, flight.arrival, flight.runway, flight.gate, flight.duration, flight.notes, flight.id))
        self.conn.commit()

    def delete_flight(self, flight_id):
        """Delete a flight by its ID."""
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM logbook WHERE id = ?", (flight_id,))
        self.conn.commit()

    def load_flights(self):
        """Load all flights from the database into a list of Flight objects."""
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM logbook")
        rows = cursor.fetchall()
        flights = []
        for row in rows:
            flight = Flight(row[1], row[2], row[3], row[4], row[5], row[6])
            flight.id = row[0]
            flight.set_duration(row[7])
            flight.add_notes(row[8])
            flights.append(flight)
        return flights