from flask import Blueprint, jsonify, request
from my_project.auth.dao.services_dao import ServicesDAO
from my_project.auth.service.services_service import ServicesService

def create_blueprint(mysql):
    blueprint = Blueprint("services", __name__)
    dao = ServicesDAO(mysql)
    service = ServicesService(dao)

    @blueprint.route("/", methods=["GET"])
    def get_all():
        services = service.get_all()
        return jsonify(services), 200

    @blueprint.route("/", methods=["POST"])
    def add():
        data = request.json
        if "service_name" not in data or "price" not in data:
            return jsonify({"error": "Missing required fields"}), 400
        service.add(data["service_name"], data["price"])
        return jsonify({"message": "Service added successfully"}), 201

    @blueprint.route("/<int:service_id>", methods=["PUT"])
    def update(service_id):
        data = request.json
        if "service_name" not in data or "price" not in data:
            return jsonify({"error": "Missing required fields"}), 400
        service.update(service_id, data["service_name"], data["price"])
        return jsonify({"message": "Service updated successfully"}), 200

    @blueprint.route("/<int:service_id>", methods=["DELETE"])
    def delete(service_id):
        service.delete(service_id)
        return jsonify({"message": "Service deleted successfully"}), 200

    @blueprint.route("/stats", methods=["GET"])
    def get_stats():
        table_name = request.args.get('table_name')
        column_name = request.args.get('column_name')
        operation = request.args.get('operation')

        if not all([table_name, column_name, operation]):
            return jsonify({"error": "Missing required query parameters"}), 400

        result = service.get_column_stats(table_name, column_name, operation.upper())

        if result is not None:
            return jsonify({"result": float(result)}), 200
        else:
            return jsonify({"error": "Unable to calculate stats"}), 500

    return blueprint
