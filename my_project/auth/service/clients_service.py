class ClientsService:
    def __init__(self, dao):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def add(self, name, surname, phone_number, trainer_id):
        self.dao.add(name, surname, phone_number, trainer_id)

    def update(self, client_id, name, surname, phone_number, trainer_id):
        self.dao.update(client_id, name, surname, phone_number, trainer_id)

    def delete(self, client_id):
        self.dao.delete(client_id)

    def get_client_by_id(self, client_id):
        return self.dao.get_client_by_id(client_id)
    
    def get_by_id(self, client_id):
        return self.get_client_by_id(client_id)

    def patch(self, client_id, updates):
        client = self.dao.get_client_by_id(client_id)
        if not client:
            return None
        return self.dao.patch(client_id, updates)

    def split_table_randomly(self, parent_table):
        self.dao.split_table_randomly(parent_table)
