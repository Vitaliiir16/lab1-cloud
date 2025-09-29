class MembershipsDAO:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM Memberships")
        results = cursor.fetchall()
        cursor.close()
        return results

    def add(self, client_id, membership_type, start_date, end_date):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "INSERT INTO Memberships (client_id, membership_type, start_date, end_date) VALUES (%s, %s, %s, %s)",
            (client_id, membership_type, start_date, end_date),
        )
        self.db.connection.commit()
        cursor.close()
