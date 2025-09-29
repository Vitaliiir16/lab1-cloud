class ExercisesService:
    def __init__(self, dao):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def add(self, exercise_name, workout_program_id):
        self.dao.add(exercise_name, workout_program_id)

    def update(self, exercise_id, exercise_name, workout_program_id):
        self.dao.update(exercise_id, exercise_name, workout_program_id)

    def delete(self, exercise_id):
        self.dao.delete(exercise_id)
        
    def add_exercise_equipment(self, exercise_name, equipment_name):
        self.dao.add_exercise_equipment(exercise_name, equipment_name)

