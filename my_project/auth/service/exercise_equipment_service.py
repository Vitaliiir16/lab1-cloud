class ExerciseEquipmentService:
    def __init__(self, dao):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def add(self, exercise_id, equipment_id):
        self.dao.add(exercise_id, equipment_id)

    def delete(self, exercise_id, equipment_id):
        self.dao.delete(exercise_id, equipment_id)

    def get_exercises_by_equipment(self, equipment_id):
        return self.dao.get_exercises_by_equipment(equipment_id)

    def get_exercises_with_equipment(self):
        return self.dao.get_exercises_with_equipment()
