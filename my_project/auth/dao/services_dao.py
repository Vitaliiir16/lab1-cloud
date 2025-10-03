class ServicesDAO:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM services")
        results = cursor.fetchall()
        cursor.close()
        return results

    def add(self, service_name, price):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "INSERT INTO services (service_name, price) VALUES (%s, %s)",
            (service_name, price),
        )
        self.db.connection.commit()
        cursor.close()

    def update(self, service_id, service_name, price):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "UPDATE services SET service_name = %s, price = %s WHERE service_id = %s",
            (service_name, price, service_id),
        )
        self.db.connection.commit()
        cursor.close()

    def delete(self, service_id):
        cursor = self.db.connection.cursor()
        cursor.execute("DELETE FROM services WHERE service_id = %s", (service_id,))
        self.db.connection.commit()
        cursor.close()

    def get_column_stats(self, table_name, column_name, operation):
        cursor = self.db.connection.cursor()
        try:
            cursor.callproc('calculate_column_stats', [table_name, column_name, operation])
            result_set = cursor.fetchall()

            if result_set and len(result_set) > 0:
                return result_set[0][0]
            else:
                return None
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
        finally:
            cursor.close()
