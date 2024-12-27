import sqlite3

class PlaneDatabase:
    def __init__(self, db_name="planes.db"):
        """Initialize the database connection."""
        self.db_name = db_name
        self.conn = None

    def connect(self):
        """Connect to the database."""
        if not self.conn:
            self.conn = sqlite3.connect(self.db_name)

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def create_table(self):
        """Create the planes table in the database."""
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS planes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT UNIQUE,
            number_of_flights INTEGER DEFAULT 0,
            total_duration REAL DEFAULT 0.0,
            total_distance REAL DEFAULT 0.0
        )
        """)
        self.conn.commit()

    def add_plane(self, model):
        """Add a new plane to the database."""
        self.connect()
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO planes (model) VALUES (?)
            """, (model,))
            self.conn.commit()
            print(f"Plane '{model}' added successfully.")
        except sqlite3.IntegrityError:
            print(f"Plane '{model}' already exists.")

    def get_plane(self, model):
        """Retrieve a plane's data from the database."""
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT * FROM planes WHERE model = ?
        """, (model,))
        return cursor.fetchone()

    def delete_plane(self, model):
        """Delete a plane by its model."""
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM planes WHERE model = ?", (model,))
        self.conn.commit()
        print(f"Plane '{model}' deleted successfully.")

    #TODO: statistics don't update from logbook  
    def update_statistics(self, model, number_of_flights, total_duration, total_distance=0.0):
        """Update a plane's statistics."""
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("""
        UPDATE planes
        SET number_of_flights = ?, total_duration = ?, total_distance = ?
        WHERE model = ?
        """, (number_of_flights, total_duration, total_distance, model))
        self.conn.commit()

    def list_planes(self):
        """List all planes in the database."""
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT model FROM planes
        """)
        return [row[0] for row in cursor.fetchall()]