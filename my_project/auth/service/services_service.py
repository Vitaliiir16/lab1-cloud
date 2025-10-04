class ServicesService:
    def __init__(self, dao):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def add(self, service_name, price):
        self.dao.add(service_name, price)

    def update(self, service_id, service_name, price):
        self.dao.update(service_id, service_name, price)

    def delete(self, service_id):
        self.dao.delete(service_id)

    def get_column_stats(self, table_name, column_name, operation):
        return self.dao.get_column_stats(table_name, column_name, operation)
    
    def get_by_id(self, service_id):
        return self.dao.get_by_id(service_id)
