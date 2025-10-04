from flask import Blueprint, jsonify, request
from flasgger import swag_from
from my_project.auth.dao.services_dao import ServicesDAO
from my_project.auth.service.services_service import ServicesService


def create_blueprint(mysql):
    blueprint = Blueprint("services", __name__)
    dao = ServicesDAO(mysql)
    service = ServicesService(dao)

    @blueprint.route("/", methods=["GET"])
    @swag_from('swagger_specs/services_get_all.yml')
    def get_all():
        services = service.get_all()
        return jsonify(services), 200

    @blueprint.route("/", methods=["POST"])
    @swag_from('swagger_specs/services_post.yml')
    def add():
        data = request.json
        if "service_name" not in data or "price" not in data:
            return jsonify({"error": "Missing required fields"}), 400
        service.add(data["service_name"], data["price"])
        return jsonify({"message": "Service added successfully"}), 201

    @blueprint.route("/<int:service_id>", methods=["GET"])
    @swag_from('swagger_specs/services_get_one.yml')
    def get_by_id(service_id):
        """
        Отримати послугу за ID
        ---
        tags:
          - Services
        """
        svc = service.get_by_id(service_id)
        if svc is None:
            return jsonify({"error": "Service not found"}), 404
        return jsonify(svc)

    @blueprint.route("/<int:service_id>", methods=["PUT"])
    @swag_from('swagger_specs/services_put.yml')
    def update(service_id):
        data = request.json
        if "service_name" not in data or "price" not in data:
            return jsonify({"error": "Missing required fields"}), 400
        service.update(service_id, data["service_name"], data["price"])
        return jsonify({"message": "Service updated successfully"}), 200

    @blueprint.route("/<int:service_id>", methods=["DELETE"])
    @swag_from('swagger_specs/services_delete.yml')
    def delete(service_id):
        service.delete(service_id)
        return jsonify({"message": "Service deleted successfully"}), 200

    @blueprint.route("/stats", methods=["GET"])
    def get_stats():
        """
        Отримати статистику колонки таблиці
        ---
        tags:
          - Services
        parameters:
          - name: table_name
            in: query
            type: string
            required: true
            description: Назва таблиці
          - name: column_name
            in: query
            type: string
            required: true
            description: Назва колонки
          - name: operation
            in: query
            type: string
            required: true
            enum: [SUM, AVG, MIN, MAX, COUNT]
            description: Операція агрегації
        responses:
          200:
            description: Результат статистики
          400:
            description: Відсутні параметри
          500:
            description: Помилка обчислення
        """
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
