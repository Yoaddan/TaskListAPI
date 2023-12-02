from flask import Blueprint, jsonify, request
from logger.logger_base import log
from marshmallow import ValidationError

class TaskListRoutes(Blueprint):
    """
    Class that defines api routes.

    Attributes:
        Blueprint: Instance of flask Blueprint class.
    """

    def __init__(self, task_list_service, task_list_schema):
        """
        Constructor of the TaskListService Class.

        Args:
            task_list_service: Instance that implements the Service.
            task_list_schema: Instance for validations.
        """
        super().__init__('task_list', __name__)
        self.task_list_service = task_list_service
        self.task_list_schema = task_list_schema
        self.register_routes()

    def register_routes(self):
        """
        Method in charge of setting the endpoints.
        """
        self.route('/api/task_lists', methods=['GET'])(self.get_task_lists)
        
    def get_task_lists(self):
        """
        Method in charge of getting all task lists.

        Returns:
            A json response with all task lists and a 200 code or with an error and a 500.
        """
        try:
            self.task_lists = self.task_list_service.get_all_task_lists()
            log.info('Succesful request, fetched task lists')
            return jsonify(self.task_lists), 200
        except Exception as e:
            log.exception(f'Error getting data from the database: {e}')
            return jsonify({'error': 'Failed to get data from the database'}), 500
    