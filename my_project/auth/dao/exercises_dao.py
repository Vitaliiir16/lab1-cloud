class ExercisesDAO:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM exercises")
        results = cursor.fetchall()
        cursor.close()
        return results

    def add(self, exercise_name, workout_program_id):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "INSERT INTO exercises (exercise_name, workout_program_id) VALUES (%s, %s)",
            (exercise_name, workout_program_id),
        )
        self.db.connection.commit()
        cursor.close()

    def update(self, exercise_id, exercise_name, workout_program_id):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "UPDATE exercises SET exercise_name = %s, workout_program_id = %s WHERE exercise_id = %s",
            (exercise_name, workout_program_id, exercise_id),
        )
        self.db.connection.commit()
        cursor.close()

    def delete(self, exercise_id):
        cursor = self.db.connection.cursor()
        cursor.execute("DELETE FROM exercises WHERE exercise_id = %s", (exercise_id,))
        self.db.connection.commit()
        cursor.close()

    def get_exercises_by_equipment(self, equipment_id):
        query = """
        SELECT ex.exercise_id, ex.exercise_name
        FROM exercises ex
        JOIN exercise_equipment ee ON ex.exercise_id = ee.exercise_id
        WHERE ee.equipment_id = %s;
        """
        cursor = self.db.connection.cursor()
        cursor.execute(query, (equipment_id,))
        results = cursor.fetchall()
        cursor.close()
        return [{"exercise_id": row[0], "exercise_name": row[1]} for row in results]

    def get_equipment_by_exercise(self, exercise_id):
        query = """
        SELECT e.equipment_id, e.equipment_name
        FROM equipment e
        JOIN exercise_equipment ee ON e.equipment_id = ee.equipment_id
        WHERE ee.exercise_id = %s;
        """
        cursor = self.db.connection.cursor()
        cursor.execute(query, (exercise_id,))
        results = cursor.fetchall()
        cursor.close()
        return [{"equipment_id": row[0], "equipment_name": row[1]} for row in results]

    def add_exercise_equipment(self, exercise_name, equipment_name):
        cursor = self.db.connection.cursor()
        cursor.callproc('add_exercise_equipment', [exercise_name, equipment_name])
        self.db.connection.commit()
        cursor.close()

    def insert_multiple_equipment(self):
        cursor = self.db.connection.cursor()
        cursor.callproc('insert_multiple_equipment')
        self.db.connection.commit()
        cursor.close()

    def get_by_id(self, exercise_id):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM exercises WHERE exercise_id = %s", (exercise_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
