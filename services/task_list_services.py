from logger.logger_base import log
from flask import jsonify

class TaskListService:
    """
    Class for service implementation.
    """

    def __init__(self, db_connector):
        """
        Constructor of the TaskListService Class.

        Args:
            db_connector: Instance used to connect to DB (mongo).
        """
        self.db_connector = db_connector
        

    def get_all_task_lists(self):
        """
        Method to get all task lists in the DB.

        Returns:
            A json response with all task lists and a 200 code or the error description and a 500 code.
        """
        try:
            self.task_lists= list(self.db_connector.db.task_lists.find())
            return self.task_lists
        except Exception as e:
            log.critical(f'Error fetching all task lists from the database: {e}')
            return jsonify({'error': f'Error fetching all task lists from the database: {e}'}), 500
        
    def get_task_list_by_id(self, task_list_id):
        """
        Method in charge of searching a task list by id.

        Args:
            task_list_id: Id from the task list we want to search.
        
        Returns:
            A json response with the task list or an error and a 500 code.
        """
        try:
            self.task_list = self.db_connector.db.task_lists.find_one({'_id': task_list_id})
            return self.task_list
        except Exception as e:
            log.critical(f'Error fetching the task list id from the database: {e}')
            return jsonify({'error': f'Error fetching the task list id from the database: {e}'}), 500
        
    def delete_task_list(self, task_list_id):
        """
        Method in charge of deleting a task list

        Args:
            task_list_id: Id from the task list we want to delete.
        
        Returns:
            A json response with success and a 200 code, none or an error and a 500 code.
        """
        try:
            deleted_task_list = self.get_task_list_by_id(task_list_id)
            if deleted_task_list:
                self.db_connector.db.task_lists.delete_one({'_id': task_list_id})
                return jsonify({'state': 'Task List deleted succesfully'}), 200
            else:
                return None
        except Exception as e:
            log.critical(f'Error deleting task list data: {e}')
            return jsonify({'error': f'Error deleting task list data: {e}'}), 500
        
    