from flask import Flask
from models.task_list_models import TaskListModel
from services.task_list_services import TaskListService
from routes.task_list_routes import TaskListRoutes
from schemas.task_list_schemas import TaskListSchema
from schemas.task_list_schemas import TaskSchema
from flask_cors import CORS

app = Flask(__name__)

db_connector = TaskListModel()
db_connector.connect_to_database()

task_list_services = TaskListService(db_connector)
task_list_schemas = TaskListSchema()
task_schemas = TaskSchema()

task_list_blueprint = TaskListRoutes(task_list_services, task_list_schemas, task_schemas)
app.register_blueprint(task_list_blueprint)

CORS(app, resources={r'/*': {'origins': '*'}})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        db_connector.close_connection()
