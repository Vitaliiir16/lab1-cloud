class ScheduleService:
    def __init__(self, dao):
        self.dao = dao

    def get_all(self):
        schedules = self.dao.get_all()
        for schedule in schedules:
            if 'open_time' in schedule and schedule['open_time']:
                schedule['open_time'] = str(schedule['open_time'])
            if 'close_time' in schedule and schedule['close_time']:
                schedule['close_time'] = str(schedule['close_time'])
        return schedules

    def add(self, service_id, day_of_week, open_time, close_time):
        self.dao.add(service_id, day_of_week, open_time, close_time)

    def update(self, schedule_id, service_id, day_of_week, open_time, close_time):
        self.dao.update(schedule_id, service_id, day_of_week, open_time, close_time)

    def delete(self, schedule_id):
        self.dao.delete(schedule_id)
    
    def get_by_id(self, schedule_id):
        result = self.dao.get_by_id(schedule_id)
        if result:
            if 'open_time' in result and result['open_time']:
                result['open_time'] = str(result['open_time'])
            if 'close_time' in result and result['close_time']:
                result['close_time'] = str(result['close_time'])
        return result
