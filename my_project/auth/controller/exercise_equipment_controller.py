from flask import Blueprint, jsonify, request
from flasgger import swag_from
from my_project.auth.dao.exercise_equipment_dao import ExerciseEquipmentDAO
from my_project.auth.service.exercise_equipment_service import ExerciseEquipmentService


def create_blueprint(mysql):
    blueprint = Blueprint("exercise_equipment", __name__)
    dao = ExerciseEquipmentDAO(mysql)
    service = ExerciseEquipmentService(dao)

    @blueprint.route("/", methods=["GET"])
    @swag_from('swagger_specs/exercise_equipment_get_all.yml')
    def get_all():
        exercise_equipment = service.get_all()
        return jsonify(exercise_equipment)

    @blueprint.route("/", methods=["POST"])
    @swag_from('swagger_specs/exercise_equipment_post.yml')
    def add():
        data = request.json
        service.add(data["exercise_id"], data["equipment_id"])
        return jsonify({"message": "Exercise and Equipment association added successfully"}), 201

    @blueprint.route("/", methods=["DELETE"])
    @swag_from('swagger_specs/exercise_equipment_delete.yml')
    def delete():
        data = request.json
        service.delete(data["exercise_id"], data["equipment_id"])
        return jsonify({"message": "Exercise and Equipment association deleted successfully"}), 200

    @blueprint.route("/equipment/<int:equipment_id>/exercises", methods=["GET"])
    def get_exercises_for_equipment(equipment_id):
        """
        Отримати всі вправи для конкретного обладнання
        ---
        tags:
          - Exercise-Equipment Relations
        parameters:
          - name: equipment_id
            in: path
            type: integer
            required: true
            description: ID обладнання
        responses:
          200:
            description: Список вправ
          404:
            description: Вправи не знайдені
          500:
            description: Помилка сервера
        """
        try:
            exercises = dao.get_exercises_by_equipment(equipment_id)
            if not exercises:
                return jsonify({"message": "No exercises found for this equipment"}), 404
            return jsonify(exercises), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @blueprint.route("/exercises-with-equipment", methods=["GET"])
    def get_exercises_with_equipment():
        """
        Отримати всі вправи з відповідним обладнанням
        ---
        tags:
          - Exercise-Equipment Relations
        responses:
          200:
            description: Список вправ з обладнанням
          404:
            description: Вправи не знайдені
          500:
            description: Помилка сервера
        """
        try:
            exercises_with_equipment = service.get_exercises_with_equipment()
            if not exercises_with_equipment:
                return jsonify({"message": "No exercises found"}), 404
            return jsonify(exercises_with_equipment), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return blueprint
