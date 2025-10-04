class MembershipsService:
    def __init__(self, dao):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def add(self, client_id, membership_type, start_date, end_date):
        self.dao.add(client_id, membership_type, start_date, end_date)
    
    def get_by_id(self, membership_id):
        return self.dao.get_by_id(membership_id)
    
    def update(self, membership_id, client_id, membership_type, start_date, end_date):
        self.dao.update(membership_id, client_id, membership_type, start_date, end_date)
    
    def delete(self, membership_id):
        self.dao.delete(membership_id)
