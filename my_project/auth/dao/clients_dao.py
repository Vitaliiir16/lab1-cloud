class ClientsDAO:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM Clients")
        results = cursor.fetchall()
        cursor.close()
        return results

    def add(self, name, surname, phone_number, trainer_id):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "INSERT INTO Clients (name, surname, phone_number, trainer_id) VALUES (%s, %s, %s, %s)",
            (name, surname, phone_number, trainer_id),
        )
        self.db.connection.commit()
        cursor.close()

    def update(self, client_id, name, surname, phone_number, trainer_id):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "UPDATE Clients SET name = %s, surname = %s, phone_number = %s, trainer_id = %s WHERE client_id = %s",
            (name, surname, phone_number, trainer_id, client_id),
        )
        self.db.connection.commit()
        cursor.close()

    def delete(self, client_id):
        cursor = self.db.connection.cursor()
        cursor.execute("DELETE FROM Clients WHERE client_id = %s", (client_id,))
        self.db.connection.commit()
        cursor.close()
        
    def get_client_by_id(self, client_id):
        query = "SELECT * FROM Clients WHERE client_id = %s"
        cursor = self.db.connection.cursor()
        cursor.execute(query, (client_id,))
        result = cursor.fetchone()
        return result    
        
    def get_client_by_id(self, client_id):
        cursor = self.db.connection.cursor()
        query = "SELECT * FROM Clients WHERE client_id = %s"
        cursor.execute(query, (client_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            
            client = {
                "client_id": result[0],
                "name": result[1],
                "surname": result[2],
                "phone_number": result[3],
                "trainer_id": result[4]
            }
            return client
        return None
    
    def get_client_by_id(self, client_id):
        """Отримати клієнта за ID."""
        cursor = self.db.connection.cursor()
        query = "SELECT * FROM Clients WHERE client_id = %s"
        cursor.execute(query, (client_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return {
                "client_id": result[0],
                "name": result[1],
                "surname": result[2],
                "phone_number": result[3],
                "trainer_id": result[4],
        }
        return None

    def patch(self, client_id, updates):
        """Частково оновити клієнта."""
        fields = []
        values = []

        for key, value in updates.items():
            fields.append(f"{key} = %s")
            values.append(value)

        values.append(client_id)

        query = f"UPDATE Clients SET {', '.join(fields)} WHERE client_id = %s"
        cursor = self.db.connection.cursor()
        cursor.execute(query, tuple(values))
        self.db.connection.commit()
        cursor.close()
        return self.get_client_by_id(client_id)

    
    def get_clients_by_trainer_id(self, trainer_id):
        """Отримати список клієнтів за ID тренера."""
        query = """
            SELECT client_id, name, surname, phone_number
            FROM Clients
            WHERE trainer_id = %s
        """
        cursor = self.db.connection.cursor()
        cursor.execute(query, (trainer_id,))
        results = cursor.fetchall()
        cursor.close()


        return [
            {
                "client_id": row[0],
                "name": row[1],
                "surname": row[2],
                "phone_number": row[3],
            }
            for row in results
        ]

    def split_table_randomly(self, parent_table):
        cursor = self.db.connection.cursor()
        cursor.callproc('split_table_randomly', [parent_table])
        self.db.connection.commit()
        cursor.close()
