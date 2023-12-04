from flask import Flask
from models.task_list_models import TaskListModel
from services.task_list_services import TaskListService
from routes.task_list_routes import TaskListRoutes
from schemas.task_list_schemas import TaskListSchema
from schemas.task_list_schemas import TaskSchema
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

app = Flask(__name__)

SWAGGER_URL = '/apitasklist/swagger'
API_URL = '/static/swagger.json'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Task List API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


db_connector = TaskListModel()
db_connector.connect_to_database()

task_list_services = TaskListService(db_connector)
task_list_schemas = TaskListSchema()
task_schemas = TaskSchema()

task_list_blueprint = TaskListRoutes(task_list_services, task_list_schemas, task_schemas)
app.register_blueprint(task_list_blueprint)

CORS(app, resources={r'/apitasklist/*': {'origins': 'http://localhost:3000'}})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        db_connector.close_connection()
