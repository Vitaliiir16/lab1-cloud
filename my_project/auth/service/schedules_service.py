class ScheduleService:
    def __init__(self, dao):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def add(self, service_id, day_of_week, open_time, close_time):
        self.dao.add(service_id, day_of_week, open_time, close_time)

    def update(self, schedule_id, service_id, day_of_week, open_time, close_time):
        self.dao.update(schedule_id, service_id, day_of_week, open_time, close_time)

    def delete(self, schedule_id):
        self.dao.delete(schedule_id)
