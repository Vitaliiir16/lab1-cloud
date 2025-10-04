class MembershipsDAO:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM memberships")
        results = cursor.fetchall()
        cursor.close()
        return results

    def add(self, client_id, membership_type, start_date, end_date):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "INSERT INTO memberships (client_id, membership_type, start_date, end_date) VALUES (%s, %s, %s, %s)",
            (client_id, membership_type, start_date, end_date),
        )
        self.db.connection.commit()
        cursor.close()

    def get_by_id(self, membership_id):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM memberships WHERE membership_id = %s", (membership_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def update(self, membership_id, client_id, membership_type, start_date, end_date):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "UPDATE memberships SET client_id = %s, membership_type = %s, start_date = %s, end_date = %s WHERE membership_id = %s",
            (client_id, membership_type, start_date, end_date, membership_id)
        )
        self.db.connection.commit()
        cursor.close()

    def delete(self, membership_id):
        cursor = self.db.connection.cursor()
        cursor.execute("DELETE FROM memberships WHERE membership_id = %s", (membership_id,))
        self.db.connection.commit()
        cursor.close()
