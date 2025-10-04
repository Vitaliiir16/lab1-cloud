class TrainerScheduleDAO:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM trainer_schedule")
        results = cursor.fetchall()
        cursor.close()
        return results

    def add(self, trainer_id, day_of_week):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "INSERT INTO trainer_schedule (trainer_id, day_of_week) VALUES (%s, %s)",
            (trainer_id, day_of_week)
        )
        self.db.connection.commit()
        cursor.close()

    def update(self, schedule_id, trainer_id, day_of_week):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "UPDATE trainer_schedule SET trainer_id = %s, day_of_week = %s WHERE schedule_id = %s",
            (trainer_id, day_of_week, schedule_id)
        )
        self.db.connection.commit()
        cursor.close()

    def delete(self, schedule_id):
        cursor = self.db.connection.cursor()
        cursor.execute("DELETE FROM trainer_schedule WHERE schedule_id = %s", (schedule_id,))
        self.db.connection.commit()
        cursor.close()

    def get_by_id(self, schedule_id):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM trainer_schedule WHERE schedule_id = %s", (schedule_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
