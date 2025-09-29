from flask import Blueprint, jsonify, request
from my_project.auth.dao.trainers_dao import TrainersDAO
from my_project.auth.service.trainers_service import TrainersService
from my_project.auth.dao.clients_dao import ClientsDAO
def create_blueprint(mysql):
    blueprint = Blueprint("trainers", __name__)
    dao = TrainersDAO(mysql)
    service = TrainersService(dao)
    clients_dao = ClientsDAO(mysql)

    @blueprint.route("/", methods=["GET"])
    def get_all():
        trainers = service.get_all()
        return jsonify(trainers)

    @blueprint.route("/", methods=["POST"])
    def add():
        data = request.json
        service.add(data["name"], data["surname"], data["phone_number"])
        return jsonify({"message": "Trainer added successfully"}), 201

    @blueprint.route("/<int:trainer_id>", methods=["PUT"])
    def update(trainer_id):
        data = request.json
        service.update(trainer_id, data["name"], data["surname"], data["phone_number"])
        return jsonify({"message": "Trainer updated successfully"}), 200

    @blueprint.route("/<int:trainer_id>", methods=["DELETE"])
    def delete(trainer_id):
        service.delete(trainer_id)
        return jsonify({"message": "Trainer deleted successfully"}), 200

    @blueprint.route("/<int:trainer_id>/clients", methods=["GET"])
    def get_clients_by_trainer_id(self, trainer_id):
        """
        Отримати список клієнтів тренера у вигляді словників.
        """
        query = """
        SELECT client_id, name, surname, phone_number
        FROM Clients
        WHERE trainer_id = %s
        """
        cursor = self.db.connection.cursor()
        cursor.execute(query, (trainer_id,))
        results = cursor.fetchall()
        cursor.close()

        return [
            {
            "client_id": row[0],
            "name": row[1],
            "surname": row[2],
            "phone_number": row[3],
             }
            for row in results
        ]

    
    @blueprint.route("/<int:client_id>/trainer", methods=["GET"])
    def get_client_trainer(client_id):

        client = dao.get_client_by_id(client_id)
        if client is None:
            return jsonify({"error": "Client not found"}), 404
    
        trainer = dao.get_trainer_by_id(client["trainer_id"])
        if trainer is None:
            return jsonify({"error": "Trainer not found for this client"}), 404
    
        return jsonify({"client": client, "trainer": trainer})
    
    @blueprint.route("/<int:trainer_id>/clients", methods=["GET"])
    def get_trainer_with_clients(trainer_id):
        trainer = dao.get_trainer_by_id(trainer_id)
        if trainer is None:
            return jsonify({"error": "Trainer not found"}), 404


        clients = clients_dao.get_clients_by_trainer_id(trainer_id)


        result = {
            "trainer_id": trainer["trainer_id"],
            "name": trainer["name"],
            "surname": trainer["surname"],
            "phone_number": trainer["phone_number"],
            "clients": clients,
        }

        return jsonify(result), 200




    return blueprint
