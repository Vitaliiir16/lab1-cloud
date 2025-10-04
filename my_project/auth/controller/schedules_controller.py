from flask import Blueprint, jsonify, request
from flasgger import swag_from
from my_project.auth.dao.schedules_dao import ScheduleDAO
from my_project.auth.service.schedules_service import ScheduleService


def create_blueprint(mysql):
    blueprint = Blueprint("schedule", __name__)
    dao = ScheduleDAO(mysql)
    service = ScheduleService(dao)

    @blueprint.route("/", methods=["GET"])
    @swag_from('swagger_specs/schedule_get_all.yml')
    def get_all():
        schedules = service.get_all()
        return jsonify(schedules)

    @blueprint.route("/", methods=["POST"])
    @swag_from('swagger_specs/schedule_post.yml')
    def add():
        data = request.json
        service.add(data["service_id"], data["day_of_week"], data["open_time"], data["close_time"])
        return jsonify({"message": "Schedule added successfully"}), 201

    @blueprint.route("/<int:schedule_id>", methods=["GET"])
    @swag_from('swagger_specs/schedule_get_one.yml')
    def get_by_id(schedule_id):
        """
        Отримати розклад за ID
        ---
        tags:
          - Service Schedule
        """
        schedule = service.get_by_id(schedule_id)
        if schedule is None:
            return jsonify({"error": "Schedule not found"}), 404
        return jsonify(schedule)

    @blueprint.route("/<int:schedule_id>", methods=["PUT"])
    @swag_from('swagger_specs/schedule_put.yml')
    def update(schedule_id):
        data = request.json
        service.update(schedule_id, data["service_id"], data["day_of_week"], data["open_time"], data["close_time"])
        return jsonify({"message": "Schedule updated successfully"}), 200

    @blueprint.route("/<int:schedule_id>", methods=["DELETE"])
    @swag_from('swagger_specs/schedule_delete.yml')
    def delete(schedule_id):
        service.delete(schedule_id)
        return jsonify({"message": "Schedule deleted successfully"}), 200

    return blueprint
