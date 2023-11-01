from datetime import datetime, timedelta

from flask import request, jsonify, logging
from werkzeug.exceptions import BadRequest


def validate_request_data(data, required_fields):
    for field in required_fields:
        if field not in data:
            error_message = f"Missing required field: {field}."
            logging.error(error_message)
            raise BadRequest(description=error_message)



