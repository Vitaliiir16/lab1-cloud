from flask import Blueprint, jsonify, request
from flasgger import swag_from
from my_project.auth.dao.exercises_dao import ExercisesDAO
from my_project.auth.service.exercises_service import ExercisesService


def create_blueprint(mysql):
    blueprint = Blueprint("exercises", __name__)
    dao = ExercisesDAO(mysql)
    service = ExercisesService(dao)

    @blueprint.route("/", methods=["GET"])
    @swag_from('swagger_specs/exercises_get_all.yml')
    def get_all():
        exercises = service.get_all()
        return jsonify(exercises)

    @blueprint.route("/", methods=["POST"])
    @swag_from('swagger_specs/exercises_post.yml')
    def add():
        data = request.json
        service.add(data["exercise_name"], data["workout_program_id"])
        return jsonify({"message": "Exercise added successfully"}), 201

    @blueprint.route("/<int:exercise_id>", methods=["GET"])
    @swag_from('swagger_specs/exercises_get_one.yml')
    def get_by_id(exercise_id):
        """
        Отримати вправу за ID
        ---
        tags:
          - Exercises
        parameters:
          - name: exercise_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Вправа знайдена
          404:
            description: Вправа не знайдена
        """
        exercise = service.get_by_id(exercise_id)
        if exercise is None:
            return jsonify({"error": "Exercise not found"}), 404
        return jsonify(exercise)

    @blueprint.route("/<int:exercise_id>", methods=["PUT"])
    @swag_from('swagger_specs/exercises_put.yml')
    def update(exercise_id):
        data = request.json
        service.update(exercise_id, data["exercise_name"], data["workout_program_id"])
        return jsonify({"message": "Exercise updated successfully"}), 200

    @blueprint.route("/<int:exercise_id>", methods=["DELETE"])
    @swag_from('swagger_specs/exercises_delete.yml')
    def delete(exercise_id):
        service.delete(exercise_id)
        return jsonify({"message": "Exercise deleted successfully"}), 200

    @blueprint.route("/<int:exercise_id>/equipment", methods=["GET"])
    @swag_from('swagger_specs/exercise_equipment_get_by_exercise.yml')
    def get_equipment_for_exercise(exercise_id):
        try:
            equipment = dao.get_equipment_by_exercise(exercise_id)
            if not equipment:
                return jsonify({"message": "No equipment found for this exercise"}), 404
            return jsonify(equipment), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @blueprint.route("/equipment", methods=["POST"])
    def add_exercise_equipment():
        """
        Додати зв'язок вправи та обладнання
        ---
        tags:
          - Exercises
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                exercise_name:
                  type: string
                  example: "Жим лежачи"
                equipment_name:
                  type: string
                  example: "Штанга"
        responses:
          201:
            description: Зв'язок створено
        """
        data = request.json
        service.add_exercise_equipment(data["exercise_name"], data["equipment_name"])
        return jsonify({"message": "Exercise and equipment linked successfully"}), 201

    return blueprint
