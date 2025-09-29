class EquipmentDAO:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM Equipment")
        results = cursor.fetchall()
        cursor.close()
        return results

    def add(self, equipment_name):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "INSERT INTO Equipment (equipment_name) VALUES (%s)",
            (equipment_name,)
        )
        self.db.connection.commit()
        cursor.close()

    def update(self, equipment_id, equipment_name):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "UPDATE Equipment SET equipment_name = %s WHERE equipment_id = %s",
            (equipment_name, equipment_id)
        )
        self.db.connection.commit()
        cursor.close()

    def delete(self, equipment_id):
        cursor = self.db.connection.cursor()
        cursor.execute("DELETE FROM Equipment WHERE equipment_id = %s", (equipment_id,))
        self.db.connection.commit()
        cursor.close()
        
    def add_using_procedure(self, equipment_name):
        cursor = self.db.connection.cursor()
        cursor.callproc('insert_equipment', [equipment_name])
        self.db.connection.commit()
        cursor.close()
        
    def insert_multiple_equipment(self):
        cursor = self.db.connection.cursor()
        cursor.callproc('insert_multiple_equipment')
        self.db.connection.commit()
        cursor.close()

