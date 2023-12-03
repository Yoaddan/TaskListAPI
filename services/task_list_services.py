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
            log.info('Succesful request, fetched task lists')
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
        
    def get_filtered_tasks_by_status(self, status):
        """
        Method in charge of filtering tasks by status complete or pending across all task lists.

        Args:
            status: Status to filter tasks by (complete or pending).

        Returns:
            A list of task lists with filtered tasks or an error and a 500 code.
        """
        try:
            filtered_task_lists = []
            all_task_lists = self.get_all_task_lists()
            for task_list in all_task_lists:
                filtered_tasks = [task for task in task_list.get('tasks', []) if task.get('status').lower() == status]
                log.debug(f'filtered_tasks: {filtered_tasks}')
                filtered_task_list = dict(task_list)
                filtered_task_list['tasks'] = filtered_tasks
                filtered_task_lists.append(filtered_task_list)
            log.info('Tasks filtered succesfully')
            return filtered_task_lists
        except Exception as e:
            log.critical(f'Error filtering tasks by status: {e}')
            return jsonify({'error': f'Error filtering tasks by status: {e}'}), 500
        
    def get_task_by_id(self, task_list_id, task_id):
        """
        Method in charge of obtaining a task by its id within a specific task list.

        Args:
            task_list_id: Id of the task list containing the task.
            task_id: Id of the task to be obtained.

        Returns:
            The task with the specified id, None if not found or an error with a 500 code.
        """
        try:
            self.task_list = self.get_task_list_by_id(task_list_id)
            if self.task_list:
                for self.task in self.task_list.get('tasks', []):
                    if self.task.get('_id') == task_id:
                        log.info('Task obtained successfully')
                        return self.task
                return 'task'
            return None
        except Exception as e:
            log.critical(f'Error obtaining task by id: {e}')
            return jsonify({'error': f'Error obtaining task by id: {e}'}), 500
    
    def update_task_status(self, task_list_id, task_id):
        """
        Method to update the status of a task from 'pending' to 'complete' and vice versa.

        Args:
            task_list_id: Id of the task list containing the task.
            task_id: Id of the task to update.

        Returns:
            A message indicating the status update or an error and a 500 code.
        """
        try:
            self.task = self.get_task_by_id(task_list_id, task_id)
            if self.task:
                if self.task == 'task':
                    return self.task
                else:
                    self.current_status = self.task.get('status')
                    self.new_status = 'Complete' if self.current_status == 'Pending' else 'Pending'
                    self.task['status'] = self.new_status
                    self.update_query = {'_id': task_list_id, 'tasks._id': task_id}
                    self.update_statement = {'$set': {'tasks.$.status': self.new_status}}
                    self.db_connector.db.task_lists.update_one(self.update_query, self.update_statement)
                    log.info(f'Task status updated successfully. New status: {self.new_status}')
                    return {'status': 'Task status updated successfully', 'new_status': self.new_status}
            else:
                return None
        except Exception as e:
            log.critical(f'Error updating task status: {e}')
            return jsonify({'error': f'Error updating task status: {e}'}), 500


        
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
                log.info('Task List deleted succesfully')
                return {'status': 'Task List deleted succesfully'}
            else:
                return None
        except Exception as e:
            log.critical(f'Error deleting task list data from the database: {e}')
            return jsonify({'error': f'Error deleting task list data: {e}'}), 500
        
    