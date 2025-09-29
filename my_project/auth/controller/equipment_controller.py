from flask import Blueprint, jsonify, request
from my_project.auth.dao.equipment_dao import EquipmentDAO
from my_project.auth.service.equipment_service import EquipmentService  # Змінено імпорт

def create_blueprint(mysql):
    blueprint = Blueprint("equipment", __name__)
    dao = EquipmentDAO(mysql)
    service = EquipmentService(dao)

    @blueprint.route("/", methods=["GET"])
    def get_all():
        equipment = service.get_all()
        return jsonify(equipment)

    @blueprint.route("/", methods=["POST"])
    def add():
        data = request.json
        service.add(data["equipment_name"])
        return jsonify({"message": "Equipment added successfully"}), 201

    @blueprint.route("/<int:equipment_id>", methods=["PUT"])
    def update(equipment_id):
        data = request.json
        service.update(equipment_id, data["equipment_name"])
        return jsonify({"message": "Equipment updated successfully"}), 200

    @blueprint.route("/<int:equipment_id>", methods=["DELETE"])
    def delete(equipment_id):
        service.delete(equipment_id)
        return jsonify({"message": "Equipment deleted successfully"}), 200
    
    @blueprint.route("/procedure", methods=["POST"])
    def add_using_procedure():
        data = request.json
        service.add_using_procedure(data["equipment_name"])
        return jsonify({"message": "Equipment added using procedure successfully"}), 201
    
    @blueprint.route("/bulk_insert", methods=["POST"])
    def bulk_insert():
        service.insert_multiple_equipment()
        return jsonify({"message": "10 equipment records inserted successfully"}), 201


    return blueprint
