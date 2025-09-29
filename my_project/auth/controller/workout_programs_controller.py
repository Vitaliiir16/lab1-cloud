from flask import Blueprint, jsonify, request
from my_project.auth.dao.workout_programs_dao import WorkoutProgramsDAO
from my_project.auth.service.workout_programs_service import WorkoutProgramsService

def create_blueprint(mysql):
    blueprint = Blueprint("workout_programs", __name__)
    dao = WorkoutProgramsDAO(mysql)
    service = WorkoutProgramsService(dao)

    @blueprint.route("/", methods=["GET"])
    def get_all():
        programs = service.get_all()
        return jsonify(programs)

    @blueprint.route("/", methods=["POST"])
    def add():
        data = request.json
        service.add(data["program_name"], data["trainer_id"])
        return jsonify({"message": "Workout program added successfully"}), 201

    @blueprint.route("/<int:workout_program_id>", methods=["PUT"])
    def update(workout_program_id):
        data = request.json
        service.update(workout_program_id, data["program_name"], data["trainer_id"])
        return jsonify({"message": "Workout program updated successfully"}), 200

    @blueprint.route("/<int:workout_program_id>", methods=["DELETE"])
    def delete(workout_program_id):
        service.delete(workout_program_id)
        return jsonify({"message": "Workout program deleted successfully"}), 200

    return blueprint
