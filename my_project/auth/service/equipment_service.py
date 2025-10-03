class EquipmentService:
    def __init__(self, dao):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def add(self, equipment_name):
        self.dao.add(equipment_name)

    def update(self, equipment_id, equipment_name):
        self.dao.update(equipment_id, equipment_name)

    def delete(self, equipment_id):
        self.dao.delete(equipment_id)

    def add_using_procedure(self, equipment_name):
        self.dao.add_using_procedure(equipment_name)

    def insert_multiple_equipment(self):
        self.dao.insert_multiple_equipment()
