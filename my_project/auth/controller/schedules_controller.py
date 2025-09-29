from flask import Blueprint, jsonify, request
from my_project.auth.dao.schedules_dao import ScheduleDAO
from my_project.auth.service.schedules_service import ScheduleService

def create_blueprint(mysql):
    blueprint = Blueprint("schedule", __name__)
    dao = ScheduleDAO(mysql)
    service = ScheduleService(dao)

    @blueprint.route("/", methods=["GET"])
    def get_all():
        schedules = service.get_all()
        return jsonify(schedules)

    @blueprint.route("/", methods=["POST"])
    def add():
        data = request.json
        service.add(data["service_id"], data["day_of_week"], data["open_time"], data["close_time"])
        return jsonify({"message": "Schedule added successfully"}), 201

    @blueprint.route("/<int:schedule_id>", methods=["PUT"])
    def update(schedule_id):
        data = request.json
        service.update(schedule_id, data["service_id"], data["day_of_week"], data["open_time"], data["close_time"])
        return jsonify({"message": "Schedule updated successfully"}), 200

    @blueprint.route("/<int:schedule_id>", methods=["DELETE"])
    def delete(schedule_id):
        service.delete(schedule_id)
        return jsonify({"message": "Schedule deleted successfully"}), 200

    return blueprint
