from flask import Blueprint, jsonify, request
from my_project.auth.dao.memberships_dao import MembershipsDAO
from my_project.auth.service.memberships_service import MembershipsService

def create_blueprint(mysql):
    blueprint = Blueprint("memberships", __name__)
    dao = MembershipsDAO(mysql)
    service = MembershipsService(dao)

    @blueprint.route("/", methods=["GET"])
    def get_all():
        memberships = service.get_all()
        return jsonify(memberships)

    @blueprint.route("/", methods=["POST"])
    def add():
        data = request.json
        service.add(
            data["client_id"],
            data["membership_type"],
            data["start_date"],
            data["end_date"]
        )
        return jsonify({"message": "Membership added successfully"}), 201

    return blueprint
