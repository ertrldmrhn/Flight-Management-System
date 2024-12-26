import sqlite3

class ChecklistDatabase:
    def __init__(self, db_name="checklist.db"):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        """Establish a connection to the database."""
        if not self.conn:
            self.conn = sqlite3.connect(self.db_name)

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def create_table(self):
        """Create the checklists table in the database."""
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS checklists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT,
            phase TEXT,
            item TEXT
        )
        """)
        self.conn.commit()

    def add_checklist(self, model, phase, items):
        """Add or update a checklist for a specific plane model and phase."""
        self.connect()
        cursor = self.conn.cursor()
        # Remove existing checklist items for this model and phase
        cursor.execute("""
        DELETE FROM checklists WHERE model = ? AND phase = ?
        """, (model, phase))
        # Insert the new checklist items
        for item in items:
            cursor.execute("""
            INSERT INTO checklists (model, phase, item)
            VALUES (?, ?, ?)
            """, (model, phase, item))
        self.conn.commit()

    def get_checklist(self, model, phase):
        """Retrieve the checklist for a specific plane model and phase."""
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT item FROM checklists WHERE model = ? AND phase = ?
        """, (model, phase))
        rows = cursor.fetchall()
        return [row[0] for row in rows]

    def remove_checklist(self, model, phase):
        """Remove the checklist for a specific plane model and phase."""
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("""
        DELETE FROM checklists WHERE model = ? AND phase = ?
        """, (model, phase))
        self.conn.commit()

    def list_phases(self, model):
        """List all phases with checklists for a specific plane model."""
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT DISTINCT phase FROM checklists WHERE model = ?
        """, (model,))
        rows = cursor.fetchall()
        return [row[0] for row in rows]

    def display_checklists(self, model):
        """Display all checklists for a specific plane model."""
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT phase, item FROM checklists WHERE model = ?
        ORDER BY phase
        """, (model,))
        rows = cursor.fetchall()
        current_phase = None
        for phase, item in rows:
            if phase != current_phase:
                if current_phase is not None:
                    print() 
                current_phase = phase
                print(f"{phase.capitalize()} Checklist:")
            print(f"  - {item}")

