from flask import Blueprint, jsonify, request
from flasgger import swag_from
from my_project.auth.dao.workout_programs_dao import WorkoutProgramsDAO
from my_project.auth.service.workout_programs_service import WorkoutProgramsService


def create_blueprint(mysql):
    blueprint = Blueprint("workout_programs", __name__)
    dao = WorkoutProgramsDAO(mysql)
    service = WorkoutProgramsService(dao)

    @blueprint.route("/", methods=["GET"])
    @swag_from('swagger_specs/workout_programs_get_all.yml')
    def get_all():
        programs = service.get_all()
        return jsonify(programs)

    @blueprint.route("/", methods=["POST"])
    @swag_from('swagger_specs/workout_programs_post.yml')
    def add():
        data = request.json
        service.add(data["program_name"], data["trainer_id"])
        return jsonify({"message": "Workout program added successfully"}), 201

    @blueprint.route("/<int:workout_program_id>", methods=["GET"])
    @swag_from('swagger_specs/workout_programs_get_one.yml')
    def get_by_id(workout_program_id):
        """
        Отримати програму тренувань за ID
        ---
        tags:
          - Workout Programs
        """
        program = service.get_by_id(workout_program_id)
        if program is None:
            return jsonify({"error": "Workout program not found"}), 404
        return jsonify(program)

    @blueprint.route("/<int:workout_program_id>", methods=["PUT"])
    @swag_from('swagger_specs/workout_programs_put.yml')
    def update(workout_program_id):
        data = request.json
        service.update(workout_program_id, data["program_name"], data["trainer_id"])
        return jsonify({"message": "Workout program updated successfully"}), 200

    @blueprint.route("/<int:workout_program_id>", methods=["DELETE"])
    @swag_from('swagger_specs/workout_programs_delete.yml')
    def delete(workout_program_id):
        service.delete(workout_program_id)
        return jsonify({"message": "Workout program deleted successfully"}), 200

    return blueprint
