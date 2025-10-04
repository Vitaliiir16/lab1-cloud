from flask import Blueprint, jsonify, request
from flasgger import swag_from
from my_project.auth.dao.trainer_schedule_dao import TrainerScheduleDAO
from my_project.auth.service.trainer_schedule_service import TrainerScheduleService


def create_blueprint(mysql):
    blueprint = Blueprint("trainer_schedule", __name__)
    dao = TrainerScheduleDAO(mysql)
    service = TrainerScheduleService(dao)

    @blueprint.route("/", methods=["GET"])
    @swag_from('swagger_specs/trainer_schedule_get_all.yml')
    def get_all():
        schedule = service.get_all()
        return jsonify(schedule)

    @blueprint.route("/", methods=["POST"])
    @swag_from('swagger_specs/trainer_schedule_post.yml')
    def add():
        data = request.json
        service.add(data["trainer_id"], data["day_of_week"])
        return jsonify({"message": "Trainer schedule added successfully"}), 201

    @blueprint.route("/<int:schedule_id>", methods=["GET"])
    @swag_from('swagger_specs/trainer_schedule_get_one.yml')
    def get_by_id(schedule_id):
        """
        Отримати розклад тренера за ID
        ---
        tags:
          - Trainer Schedule
        """
        schedule = service.get_by_id(schedule_id)
        if schedule is None:
            return jsonify({"error": "Trainer schedule not found"}), 404
        return jsonify(schedule)

    @blueprint.route("/<int:schedule_id>", methods=["PUT"])
    @swag_from('swagger_specs/trainer_schedule_put.yml')
    def update(schedule_id):
        data = request.json
        service.update(schedule_id, data["trainer_id"], data["day_of_week"])
        return jsonify({"message": "Trainer schedule updated successfully"}), 200

    @blueprint.route("/<int:schedule_id>", methods=["DELETE"])
    @swag_from('swagger_specs/trainer_schedule_delete.yml')
    def delete(schedule_id):
        service.delete(schedule_id)
        return jsonify({"message": "Trainer schedule deleted successfully"}), 200

    return blueprint
