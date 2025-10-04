from flask import Blueprint, jsonify, request
from flasgger import swag_from
from my_project.auth.dao.equipment_dao import EquipmentDAO
from my_project.auth.service.equipment_service import EquipmentService


def create_blueprint(mysql):
    blueprint = Blueprint("equipment", __name__)
    dao = EquipmentDAO(mysql)
    service = EquipmentService(dao)

    @blueprint.route("/", methods=["GET"])
    @swag_from('swagger_specs/equipment_get_all.yml')
    def get_all():
        equipment = service.get_all()
        return jsonify(equipment)

    @blueprint.route("/", methods=["POST"])
    @swag_from('swagger_specs/equipment_post.yml')
    def add():
        data = request.json
        service.add(data["equipment_name"])
        return jsonify({"message": "Equipment added successfully"}), 201

    @blueprint.route("/<int:equipment_id>", methods=["GET"])
    @swag_from('swagger_specs/equipment_get_one.yml')
    def get_by_id(equipment_id):
        """
        Отримати обладнання за ID
        ---
        tags:
          - Equipment
        parameters:
          - name: equipment_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Обладнання знайдено
          404:
            description: Обладнання не знайдено
        """
        equipment = service.get_by_id(equipment_id)
        if equipment is None:
            return jsonify({"error": "Equipment not found"}), 404
        return jsonify(equipment)

    @blueprint.route("/<int:equipment_id>", methods=["PUT"])
    @swag_from('swagger_specs/equipment_put.yml')
    def update(equipment_id):
        data = request.json
        service.update(equipment_id, data["equipment_name"])
        return jsonify({"message": "Equipment updated successfully"}), 200

    @blueprint.route("/<int:equipment_id>", methods=["DELETE"])
    @swag_from('swagger_specs/equipment_delete.yml')
    def delete(equipment_id):
        service.delete(equipment_id)
        return jsonify({"message": "Equipment deleted successfully"}), 200

    @blueprint.route("/procedure", methods=["POST"])
    def add_using_procedure():
        """
        Додати обладнання через процедуру
        ---
        tags:
          - Equipment
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                equipment_name:
                  type: string
                  example: "Гантелі"
        responses:
          201:
            description: Обладнання додано через процедуру
        """
        data = request.json
        service.add_using_procedure(data["equipment_name"])
        return jsonify({"message": "Equipment added using procedure successfully"}), 201

    @blueprint.route("/bulk_insert", methods=["POST"])
    def bulk_insert():
        """
        Масове додавання обладнання
        ---
        tags:
          - Equipment
        responses:
          201:
            description: 10 записів обладнання додано
        """
        service.insert_multiple_equipment()
        return jsonify({"message": "10 equipment records inserted successfully"}), 201

    return blueprint
