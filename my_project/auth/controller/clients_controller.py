from flask import Blueprint, jsonify, request
from my_project.auth.dao.clients_dao import ClientsDAO
from my_project.auth.service.clients_service import ClientsService
from my_project.auth.dao.trainers_dao import TrainersDAO

def create_blueprint(mysql):
    blueprint = Blueprint("clients", __name__)
    dao = ClientsDAO(mysql)
    service = ClientsService(dao)
    trainers_dao = TrainersDAO(mysql)

    @blueprint.route("/", methods=["GET"])
    def get_all():
        clients = service.get_all()
        return jsonify(clients)

    @blueprint.route("/", methods=["POST"])
    def add():
        data = request.json
        service.add(data["name"], data["surname"], data["phone_number"], data["trainer_id"])
        return jsonify({"message": "Client added successfully"}), 201

    @blueprint.route("/<int:client_id>", methods=["GET"])
    def get_client_by_id(client_id):
        client = service.get_client_by_id(client_id)
        if client is None:
            return jsonify({"error": "Client not found"}), 404
        return jsonify(client)

    @blueprint.route("/<int:client_id>", methods=["PUT"])
    def update(client_id):
        data = request.json
        service.update(client_id, data["name"], data["surname"], data["phone_number"], data["trainer_id"])
        return jsonify({"message": "Client updated successfully"}), 200

    @blueprint.route("/<int:client_id>", methods=["PATCH"])
    def patch_client(client_id):
        data = request.json
        updated_client = service.patch(client_id, data)
        if updated_client is None:
            return jsonify({"error": "Client not found"}), 404
        return jsonify(updated_client)

    @blueprint.route("/<int:client_id>", methods=["DELETE"])
    def delete(client_id):
        service.delete(client_id)
        return jsonify({"message": "Client deleted successfully"}), 200

    @blueprint.route("/<int:client_id>/trainer", methods=["GET"])
    def get_client_trainer(client_id):
        client = dao.get_client_by_id(client_id)
        if client is None:
            return jsonify({"error": "Client not found"}), 404

        trainer = trainers_dao.get_trainer_by_id(client["trainer_id"])
        if trainer is None:
            return jsonify({"error": "Trainer not found for this client"}), 404

        return jsonify({"client": client, "trainer": trainer})

    @blueprint.route("/split_table", methods=["POST"])
    def split_table():
        data = request.json
        service.split_table_randomly(data["parent_table"])
        return jsonify({"message": "Table split successfully"}), 201

    return blueprint
