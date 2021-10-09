from flask import jsonify

from main import db
from model.Learner import Learner
from model.LoginSession import LoginSession
from api.error import throw_error


def login(username: str, password: str):
    """
    Checks if user record exists and if password is valid
    Returns:
      @success: return user record if username exists, and password is correct
      @error: status_code 500 if username does not exist or password is incorrect
    """
    learner = Learner.query.filter_by(email=username, password=password).first()

    if learner is None:
        error_type = "Login"
        message = "Invalid Email or Password"
        return throw_error(type=error_type, message=message)

    session = LoginSession(learner.id)
    db.session.add(session)
    db.session.commit()

    status_code = 200
    response = {
        "success": True,
        "result": {"type": "Login", "records": [session.serialise()]},
    }

    return jsonify(response), status_code


"""
Invalidates a token by updating its expiry_date to now
Returns:
  @success: success if expiry_date is updated
  @error: status_code 500 if failure
"""


def logout(token: str):
    session: LoginSession = LoginSession.query.filter_by(token=token).first()

    if session is None:
        error_type = "Logout"
        message = "Invalid token"
        return throw_error(type=error_type, message=message)

    session.expireToken()
    db.session.commit()

    status_code = 200
    response = {
        "success": True,
        "result": {"type": "Logout", "message": "Success"},
    }
    return jsonify(response), status_code


"""
Validates a token by checking for expiry.
Returns a boolean as it is meant to be used by other functions
Returns:
  @success: TRUE if token is valid (aka, not expired)
  @error: FALSE if token does not exist or is expired
"""


def validateToken(token: str):
    session: LoginSession = LoginSession.query.filter_by(token=token).first()

    if session is None:
        return {"status": False, "message": "Token does not exist"}

    if session.isExpired():
        return {"status": False, "message": "Token is Expired"}

    return {"status": True, "message": "OK"}


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
