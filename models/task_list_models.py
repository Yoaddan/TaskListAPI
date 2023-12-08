import os
from pymongo import MongoClient
from logger.logger_base import log

class TaskListModel:
    """
    Class in charge of connection to DB.
    """

    def __init__(self):
        """
        Constructor of the TaskListService Class.
        """
        self.client = None
        self.db = None

    def connect_to_database(self):
        """
        Method in charge of connecting to MongoDB.

        Raises:
            ValueError: In case environment variables don´t exist.
            Exception: In case of a connection exception.
        """
        mongodb_user = os.environ.get('MONGODB_USER')
        mongodb_pass = os.environ.get('MONGODB_PASS')
        mongodb_host = os.environ.get('MONGODB_HOST')

        required_variables = {'MONGODB_USER': mongodb_user, 'MONGODB_PASS': mongodb_pass, 'MONGODB_HOST': mongodb_host}

        for var, val in required_variables.items():
            if not val:
                log.critical(f'{var} variable not found')
                raise ValueError(f'Set {var} variable')

        try:
            self.client = MongoClient(
                host=mongodb_host,
                port=27017,
                username=mongodb_user,
                password=mongodb_pass,
                authSource='admin',
                authMechanism='SCRAM-SHA-256'
            )
            self.db = self.client['TaskManagement']
        except Exception as e:
            log.critical(f'Failed to connect to the database: {e}')
            raise

    def close_connection(self):
        """
        Method in charge of closing connection to the DB.
        """
        if self.client:
            self.client.close()
