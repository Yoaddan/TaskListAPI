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
    