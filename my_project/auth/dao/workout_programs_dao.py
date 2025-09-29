class WorkoutProgramsDAO:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM Workout_Programs")
        results = cursor.fetchall()
        cursor.close()
        return results

    def add(self, program_name, trainer_id):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "INSERT INTO Workout_Programs (program_name, trainer_id) VALUES (%s, %s)",
            (program_name, trainer_id),
        )
        self.db.connection.commit()
        cursor.close()

    def update(self, workout_program_id, program_name, trainer_id):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "UPDATE Workout_Programs SET program_name = %s, trainer_id = %s WHERE workout_program_id = %s",
            (program_name, trainer_id, workout_program_id),
        )
        self.db.connection.commit()
        cursor.close()

    def delete(self, workout_program_id):
        cursor = self.db.connection.cursor()
        cursor.execute("DELETE FROM Workout_Programs WHERE workout_program_id = %s", (workout_program_id,))
        self.db.connection.commit()
        cursor.close()
