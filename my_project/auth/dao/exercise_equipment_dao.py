class ExerciseEquipmentDAO:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM exercise_equipment")
        results = cursor.fetchall()
        cursor.close()
        return results

    def add(self, exercise_id, equipment_id):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "INSERT INTO exercise_equipment (exercise_id, equipment_id) VALUES (%s, %s)",
            (exercise_id, equipment_id)
        )
        self.db.connection.commit()
        cursor.close()

    def delete(self, exercise_id, equipment_id):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "DELETE FROM exercise_equipment WHERE exercise_id = %s AND equipment_id = %s",
            (exercise_id, equipment_id)
        )
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

    def get_exercises_with_equipment(self):
        query = """
        SELECT ex.exercise_id, ex.exercise_name, eq.equipment_id, eq.equipment_name
        FROM exercises ex
        LEFT JOIN exercise_equipment ee ON ex.exercise_id = ee.exercise_id
        LEFT JOIN equipment eq ON ee.equipment_id = eq.equipment_id
        ORDER BY ex.exercise_id;
        """
        cursor = self.db.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        exercises = {}
        for row in results:
            exercise_id = row[0]
            exercise_name = row[1]
            equipment_id = row[2]
            equipment_name = row[3]

            if exercise_id not in exercises:
                exercises[exercise_id] = {
                    "exercise_id": exercise_id,
                    "exercise_name": exercise_name,
                    "equipment": []
                }

            if equipment_id:
                exercises[exercise_id]["equipment"].append({
                    "equipment_id": equipment_id,
                    "equipment_name": equipment_name
                })

        return list(exercises.values())
