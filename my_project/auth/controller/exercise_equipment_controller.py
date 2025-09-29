from flask import Blueprint, jsonify, request
from my_project.auth.dao.exercise_equipment_dao import ExerciseEquipmentDAO
from my_project.auth.service.exercise_equipment_service import ExerciseEquipmentService

def create_blueprint(mysql):
    blueprint = Blueprint("exercise_equipment", __name__)
    dao = ExerciseEquipmentDAO(mysql)
    service = ExerciseEquipmentService(dao)

    @blueprint.route("/", methods=["GET"])
    def get_all():
        exercise_equipment = service.get_all()
        return jsonify(exercise_equipment)

    @blueprint.route("/", methods=["POST"])
    def add():
        data = request.json
        service.add(data["exercise_id"], data["equipment_id"])
        return jsonify({"message": "Exercise and Equipment association added successfully"}), 201

    @blueprint.route("/", methods=["DELETE"])
    def delete():
        data = request.json
        service.delete(data["exercise_id"], data["equipment_id"])
        return jsonify({"message": "Exercise and Equipment association deleted successfully"}), 200

    @blueprint.route("/equipment/<int:equipment_id>/exercises", methods=["GET"])
    def get_exercises_for_equipment(equipment_id):
        try:
            exercises = dao.get_exercises_by_equipment(equipment_id)
            if not exercises:
                return jsonify({"message": "No exercises found for this equipment"}), 404
            return jsonify(exercises), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @blueprint.route("/exercises-with-equipment", methods=["GET"])
    def get_exercises_with_equipment():
        try:
            exercises_with_equipment = service.get_exercises_with_equipment()
            if not exercises_with_equipment:
                return jsonify({"message": "No exercises found"}), 404
            return jsonify(exercises_with_equipment), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500




    return blueprint
 