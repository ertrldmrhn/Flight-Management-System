import sqlite3

class ControlsDatabase:
    def __init__(self, db_name="controls.db"):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.db_name)

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def create_tables(self):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS mappings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER NOT NULL,
            buttons TEXT NOT NULL,
            function TEXT NOT NULL,
            FOREIGN KEY (profile_id) REFERENCES profiles (id) ON DELETE CASCADE
        );
        """)
        self.conn.commit()

    def add_profile(self, name, type):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO profiles (name, type) VALUES (?, ?)", (name, type))
        self.conn.commit()

    def get_profiles(self):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM profiles")
        return cursor.fetchall()

    def delete_profile(self, profile_id):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
        self.conn.commit()

    def add_mapping(self, profile_id, buttons, function):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO mappings (profile_id, buttons, function) VALUES (?, ?, ?)",
                       (profile_id, buttons, function))
        self.conn.commit()

    def get_mappings(self, profile_id):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM mappings WHERE profile_id = ?", (profile_id,))
        return cursor.fetchall()

    def delete_mapping(self, mapping_id):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM mappings WHERE id = ?", (mapping_id,))
        self.conn.commit()

    def update_mapping(self, mapping_id, buttons=None, function=None):
        self.connect()
        cursor = self.conn.cursor()

        updates = []
        params = []

        if buttons:
            updates.append("buttons = ?")
            params.append(buttons)
        if function:
            updates.append("function = ?")
            params.append(function)

        if not updates:
            print("No updates provided.")
            return
        params.append(mapping_id)
        query = f"UPDATE mappings SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        self.conn.commit()
        print("Mapping updated successfully!")