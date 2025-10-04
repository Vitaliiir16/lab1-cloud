from flask import Blueprint, jsonify, request
from flasgger import swag_from
from my_project.auth.dao.memberships_dao import MembershipsDAO
from my_project.auth.service.memberships_service import MembershipsService


def create_blueprint(mysql):
    blueprint = Blueprint("memberships", __name__)
    dao = MembershipsDAO(mysql)
    service = MembershipsService(dao)

    @blueprint.route("/", methods=["GET"])
    @swag_from('swagger_specs/memberships_get_all.yml')
    def get_all():
        memberships = service.get_all()
        return jsonify(memberships)

    @blueprint.route("/", methods=["POST"])
    @swag_from('swagger_specs/memberships_post.yml')
    def add():
        data = request.json
        service.add(
            data["client_id"],
            data["membership_type"],
            data["start_date"],
            data["end_date"]
        )
        return jsonify({"message": "Membership added successfully"}), 201

    @blueprint.route("/<int:membership_id>", methods=["GET"])
    @swag_from('swagger_specs/memberships_get_one.yml')
    def get_by_id(membership_id):
        """
        Отримати абонемент за ID
        ---
        tags:
          - Memberships
        parameters:
          - name: membership_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Абонемент знайдений
          404:
            description: Абонемент не знайдений
        """
        membership = service.get_by_id(membership_id)
        if membership is None:
            return jsonify({"error": "Membership not found"}), 404
        return jsonify(membership)

    @blueprint.route("/<int:membership_id>", methods=["PUT"])
    @swag_from('swagger_specs/memberships_put.yml')
    def update(membership_id):
        """
        Оновити абонемент
        ---
        tags:
          - Memberships
        parameters:
          - name: membership_id
            in: path
            type: integer
            required: true
          - name: body
            in: body
            required: true
            schema:
              type: object
        responses:
          200:
            description: Абонемент оновлений
        """
        data = request.json
        service.update(
            membership_id,
            data.get("client_id"),
            data.get("membership_type"),
            data.get("start_date"),
            data.get("end_date")
        )
        return jsonify({"message": "Membership updated successfully"}), 200

    @blueprint.route("/<int:membership_id>", methods=["DELETE"])
    @swag_from('swagger_specs/memberships_delete.yml')
    def delete(membership_id):
        """
        Видалити абонемент
        ---
        tags:
          - Memberships
        """
        service.delete(membership_id)
        return jsonify({"message": "Membership deleted successfully"}), 200

    return blueprint
