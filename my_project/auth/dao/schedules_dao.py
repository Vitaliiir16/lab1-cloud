class ScheduleDAO:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM schedule")
        results = cursor.fetchall()
        cursor.close()
        return results

    def add(self, service_id, day_of_week, open_time, close_time):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "INSERT INTO schedule (service_id, day_of_week, open_time, close_time) VALUES (%s, %s, %s, %s)",
            (service_id, day_of_week, open_time, close_time)
        )
        self.db.connection.commit()
        cursor.close()

    def update(self, schedule_id, service_id, day_of_week, open_time, close_time):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "UPDATE schedule SET service_id = %s, day_of_week = %s, open_time = %s, close_time = %s WHERE schedule_id = %s",
            (service_id, day_of_week, open_time, close_time, schedule_id)
        )
        self.db.connection.commit()
        cursor.close()

    def delete(self, schedule_id):
        cursor = self.db.connection.cursor()
        cursor.execute("DELETE FROM schedule WHERE schedule_id = %s", (schedule_id,))
        self.db.connection.commit()
        cursor.close()
