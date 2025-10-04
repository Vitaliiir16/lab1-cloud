class WorkoutProgramsService:
    def __init__(self, dao):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def add(self, program_name, trainer_id):
        self.dao.add(program_name, trainer_id)

    def update(self, workout_program_id, program_name, trainer_id):
        self.dao.update(workout_program_id, program_name, trainer_id)

    def delete(self, workout_program_id):
        self.dao.delete(workout_program_id)
    
    def get_by_id(self, workout_program_id):
        return self.dao.get_by_id(workout_program_id)
