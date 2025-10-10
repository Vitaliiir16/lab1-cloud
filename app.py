#перевірка автоматичного деплою та налаштувань CI CD lab1 cloud test before passing
from flask import Flask
from flask_mysqldb import MySQL
from flasgger import Swagger
import os

app = Flask(__name__)


app.config['MYSQL_HOST'] = os.getenv('DB_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('DB_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASS', '')
app.config['MYSQL_DB'] = os.getenv('DB_NAME', 'fitness_db')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger_template = {
    "info": {
        "title": "Fitness Management API",
        "description": "REST API для управління фітнес-клубом: клієнти, тренери, послуги, вправи, абонементи та обладнання",
        "version": "1.0.0",
        "contact": {
            "name": "Fitness Management System",
            "url": "http://34.116.176.94:8080"
        }
    },
    "host": "34.116.176.94:8080",
    "basePath": "/api/v1",
    "schemes": ["http"],
    "tags": [
        {"name": "Clients", "description": "Операції з клієнтами"},
        {"name": "Trainers", "description": "Операції з тренерами"},
        {"name": "Services", "description": "Операції з послугами"},
        {"name": "Exercises", "description": "Операції з вправами"},
        {"name": "Memberships", "description": "Операції з абонементами"},
        {"name": "Equipment", "description": "Операції з обладнанням"},
        {"name": "Workout Programs", "description": "Програми тренувань"},
        {"name": "Exercise-Equipment Relations", "description": "Зв'язки вправ та обладнання"},
        {"name": "Service Schedule", "description": "Розклад послуг"},
        {"name": "Trainer Schedule", "description": "Розклад тренерів"}
    ]
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)


from my_project.auth.controller import clients_controller
from my_project.auth.controller import trainers_controller
from my_project.auth.controller import services_controller
from my_project.auth.controller import exercises_controller
from my_project.auth.controller import memberships_controller
from my_project.auth.controller import equipment_controller
from my_project.auth.controller import workout_programs_controller
from my_project.auth.controller import exercise_equipment_controller
from my_project.auth.controller import schedules_controller
from my_project.auth.controller import trainer_schedule_controller


clients_bp = clients_controller.create_blueprint(mysql)
trainers_bp = trainers_controller.create_blueprint(mysql)
services_bp = services_controller.create_blueprint(mysql)
exercises_bp = exercises_controller.create_blueprint(mysql)
memberships_bp = memberships_controller.create_blueprint(mysql)
equipment_bp = equipment_controller.create_blueprint(mysql)
workout_programs_bp = workout_programs_controller.create_blueprint(mysql)
exercise_equipment_bp = exercise_equipment_controller.create_blueprint(mysql)
schedules_bp = schedules_controller.create_blueprint(mysql)
trainer_schedule_bp = trainer_schedule_controller.create_blueprint(mysql)


app.register_blueprint(clients_bp, url_prefix='/api/v1/clients')
app.register_blueprint(trainers_bp, url_prefix='/api/v1/trainers')
app.register_blueprint(services_bp, url_prefix='/api/v1/services')
app.register_blueprint(exercises_bp, url_prefix='/api/v1/exercises')
app.register_blueprint(memberships_bp, url_prefix='/api/v1/memberships')
app.register_blueprint(equipment_bp, url_prefix='/api/v1/equipment')
app.register_blueprint(workout_programs_bp, url_prefix='/api/v1/workout-programs')
app.register_blueprint(exercise_equipment_bp, url_prefix='/api/v1/exercise-equipment')
app.register_blueprint(schedules_bp, url_prefix='/api/v1/schedules')
app.register_blueprint(trainer_schedule_bp, url_prefix='/api/v1/trainer-schedules')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
