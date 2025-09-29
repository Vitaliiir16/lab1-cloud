class TrainersService:
    def __init__(self, dao):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def add(self, name, surname, phone_number):
        self.dao.add(name, surname, phone_number)

    def update(self, trainer_id, name, surname, phone_number):
        self.dao.update(trainer_id, name, surname, phone_number)

    def delete(self, trainer_id):
        self.dao.delete(trainer_id)
