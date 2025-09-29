class TrainersDAO:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM Trainers")
        results = cursor.fetchall()
        cursor.close()
        return results

    def add(self, name, surname, phone_number):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "INSERT INTO Trainers (name, surname, phone_number) VALUES (%s, %s, %s)",
            (name, surname, phone_number),
        )
        self.db.connection.commit()
        cursor.close()

    def update(self, trainer_id, name, surname, phone_number):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "UPDATE Trainers SET name = %s, surname = %s, phone_number = %s WHERE trainer_id = %s",
            (name, surname, phone_number, trainer_id),
        )
        self.db.connection.commit()
        cursor.close()

    def delete(self, trainer_id):
        cursor = self.db.connection.cursor()
        cursor.execute("DELETE FROM Trainers WHERE trainer_id = %s", (trainer_id,))
        self.db.connection.commit()
        cursor.close()
        
    def get_trainer_by_id(self, trainer_id):
        query = "SELECT * FROM Trainers WHERE trainer_id = %s"
        cursor = self.db.connection.cursor()
        cursor.execute(query, (trainer_id,))
        result = cursor.fetchone()
        return result    

    def get_trainer_by_id(self, trainer_id):
        query = """
        SELECT trainer_id, name, surname, phone_number
        FROM Trainers
        WHERE trainer_id = %s
        """
        cursor = self.db.connection.cursor()
        cursor.execute(query, (trainer_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return {
                "trainer_id": result[0],
                "name": result[1],
                "surname": result[2],
                "phone_number": result[3],
            }
        return None


