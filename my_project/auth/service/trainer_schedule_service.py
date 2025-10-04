class TrainerScheduleService:
    def __init__(self, dao):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def add(self, trainer_id, day_of_week):
        self.dao.add(trainer_id, day_of_week)

    def update(self, schedule_id, trainer_id, day_of_week):
        self.dao.update(schedule_id, trainer_id, day_of_week)

    def delete(self, schedule_id):
        self.dao.delete(schedule_id)
    
    def get_by_id(self, schedule_id):
        return self.dao.get_by_id(schedule_id)
