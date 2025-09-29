from flask import Blueprint, jsonify, request
from my_project.auth.dao.exercises_dao import ExercisesDAO
from my_project.auth.service.exercises_service import ExercisesService

def create_blueprint(mysql):
    blueprint = Blueprint("exercises", __name__)
    dao = ExercisesDAO(mysql)
    service = ExercisesService(dao)

    @blueprint.route("/", methods=["GET"])
    def get_all():
        exercises = service.get_all()
        return jsonify(exercises)

    @blueprint.route("/", methods=["POST"])
    def add():
        data = request.json
        service.add(data["exercise_name"], data["workout_program_id"])
        return jsonify({"message": "Exercise added successfully"}), 201

    @blueprint.route("/<int:exercise_id>", methods=["PUT"])
    def update(exercise_id):
        data = request.json
        service.update(exercise_id, data["exercise_name"], data["workout_program_id"])
        return jsonify({"message": "Exercise updated successfully"}), 200

    @blueprint.route("/<int:exercise_id>", methods=["DELETE"])
    def delete(exercise_id):
        service.delete(exercise_id)
        return jsonify({"message": "Exercise deleted successfully"}), 200
    
    @blueprint.route("/api/v1/exercises/<int:exercise_id>/equipment", methods=["GET"])
    def get_exercises_by_equipment(equipment_id):
        try:
            exercises = ExercisesDAO.get_exercises_by_equipment(equipment_id)
            if not exercises:
                return jsonify({"message": "No exercises found for this equipment"}), 404
            return jsonify(exercises), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @blueprint.route("/<int:exercise_id>/equipment", methods=["GET"])
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
        data = request.json
        service.add_exercise_equipment(data["exercise_name"], data["equipment_name"])
        return jsonify({"message": "Exercise and equipment linked successfully"}), 201



    return blueprint
