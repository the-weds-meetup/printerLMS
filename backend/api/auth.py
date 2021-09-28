from model import Learner
from flask import jsonify

"""
Checks if user record exists and if password is valid
Returns:
  @success: return user record if username exists, and password is correct
  @error: status_code 500 if username does not exist or password is incorrect
"""


def login(username: str, password: str):
    learner = Learner.Learner.query.filter_by(email=username, password=password).first()

    if learner is None:
        error_type = "Login"
        message = "Invalid Email or Password"
        return throw_error(type=error_type, message=message)

    status_code = 200
    response = {
        "success": True,
        "result": {"type": "Login", "records": [learner.serialise()]},
    }

    return jsonify(response), status_code


"""
Throws an error status and message if something goes wrong during authentication
"""


def throw_error(
    type: str,
    message: str,
    status_code: int = 401,
):
    response = {
        "success": False,
        "result": {
            "type": type,
            "message": message,
        },
    }
    return jsonify(response), status_code
