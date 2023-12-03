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
        self.route('/api/task_lists/tasks/<string:status>', methods=['GET'])(self.get_filtered_tasks_by_status)
        self.route('/api/task_lists/<int:task_list_id>', methods=['DELETE'])(self.delete_task_list)
        
    def get_task_lists(self):
        """
        Method in charge of getting all task lists.

        Returns:
            A json response with all task lists and a 200 code or with an error and a 500.
        """
        try:
            self.task_lists = self.task_list_service.get_all_task_lists()
            return jsonify(self.task_lists), 200
        except Exception as e:
            log.exception(f'Error getting data from the database: {e}')
            return jsonify({'error': 'Failed to get data from the database'}), 500
    
    def get_filtered_tasks_by_status(self, status):
        """
        Method in charge of filtering tasks by status complete or pending across all task lists.

        Args:
            status: Status to filter tasks by (complete or pending).

        Returns:
            A json response including the lists with filtered tasks and a 200 code, an error and a 400 code or an error and a 500 code.
        """
        try:
            if status.lower() in ['complete', 'pending']:
                filtered_tasks = self.task_list_service.get_filtered_tasks_by_status(status.lower())
                return jsonify(filtered_tasks), 200
            else:
                return jsonify({'error': 'Invalid status parameter'}), 400
        except Exception as e:
            log.exception(f'Error filtering tasks: {e}')
            return jsonify({'error': 'Failed to filter tasks'}), 500
    
    def delete_task_list(self, task_list_id):
        """
        Method in charge of deleting a task list

        Args:
            task_list_id: Id from the task list we want to delete.
        
        Returns:
            A json response with success and a 200 code, an error and a 500 code or an error and a 404 code.
        """
        try:
            self.task_list_deleted = self.task_list_service.delete_task_list(task_list_id)
            log.debug(f'{self.task_list_deleted}')
            if self.task_list_deleted:
                return jsonify(self.task_list_deleted), 200
            else:
                log.error('Task list not found')
                return jsonify({'error': 'Task list not found'}), 404
        except Exception as e:
            log.exception(f'Error deleting data from the database: {e}')
            return jsonify({'error': 'Failed to delete data from the database'}), 500
    