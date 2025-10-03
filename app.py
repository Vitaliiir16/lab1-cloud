from flask import Flask
from flask_mysqldb import MySQL
from my_project.auth.controller import (
    clients_controller,
    trainers_controller,
    services_controller,
    workout_programs_controller,
    exercises_controller,
    equipment_controller,
    trainer_schedule_controller,
    schedules_controller, 
    exercise_equipment_controller,
    memberships_controller,
)

app = Flask(__name__)

import os

app.config['MYSQL_HOST'] = os.environ.get('DB_HOST')
app.config['MYSQL_USER'] = os.environ.get('DB_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('DB_PASS')
app.config['MYSQL_DB'] = os.environ.get('DB_NAME')

mysql = MySQL(app)

app.register_blueprint(clients_controller.create_blueprint(mysql), url_prefix="/api/v1/clients")
app.register_blueprint(trainers_controller.create_blueprint(mysql), url_prefix="/api/v1/trainers")
app.register_blueprint(services_controller.create_blueprint(mysql), url_prefix="/api/v1/services")
app.register_blueprint(workout_programs_controller.create_blueprint(mysql), url_prefix="/api/v1/workout_programs")
app.register_blueprint(exercises_controller.create_blueprint(mysql), url_prefix="/api/v1/exercises")
app.register_blueprint(equipment_controller.create_blueprint(mysql), url_prefix="/api/v1/equipment")
app.register_blueprint(trainer_schedule_controller.create_blueprint(mysql), url_prefix="/api/v1/trainer_schedule")
app.register_blueprint(schedules_controller.create_blueprint(mysql), url_prefix="/api/v1/schedules")
app.register_blueprint(exercise_equipment_controller.create_blueprint(mysql), url_prefix="/api/v1/exercise_equipment")
app.register_blueprint(memberships_controller.create_blueprint(mysql), url_prefix="/api/v1/memberships")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
