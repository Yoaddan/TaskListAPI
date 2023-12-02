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
        self.route('/api/task_lists/<int:task_list_id>', methods=['DELETE'])(self.delete_task_list)
        
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
    
    def delete_task_list(self, task_list_id):
        """
        Method in charge of deleting a task list

        Args:
            task_list_id: Id from the task list we want to delete.
        
        Returns:
            A json response with success and a 200 code or an error and a 404 code.
        """
        try:
            self.task_list_deleted = self.task_list_service.delete_task_list(task_list_id)
            if self.task_list_deleted:
                log.info('Task List deleted succesfully!')
                return jsonify({'state': 'Task List deleted succesfully!'}), 200
            else:
                log.error('Task list not found')
                return jsonify({'error': 'Task list not found'}), 404
        except Exception as e:
            log.exception(f'Error deleting the task list in the database: {e}')
    