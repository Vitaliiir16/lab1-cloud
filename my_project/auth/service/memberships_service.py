class MembershipsService:
    def __init__(self, dao):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def add(self, client_id, membership_type, start_date, end_date):
        self.dao.add(client_id, membership_type, start_date, end_date)
