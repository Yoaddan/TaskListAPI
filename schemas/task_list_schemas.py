from marshmallow import fields, validates, ValidationError

class TaskListSchema:
    """
    Class in charge of validations.
    """
    _id = fields.String(required=True)
