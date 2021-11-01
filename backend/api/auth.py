from flask import jsonify

from main import db
from model.Learner import Learner
from model.LoginSession import LoginSession
from controller.AuthController import AuthController


def login(username: str, password: str):
    """
    Checks if user record exists and if password is valid
    Returns:
      @success: return user record if username exists, and password is correct
      @error: status_code 500 if username does not exist or password is incorrect
    """
    session: LoginSession = AuthController.login(username=username, password=password)
    response = {
        "success": True,
        "result": {"type": "Login", "records": [session.serialise()]},
    }
    return jsonify(response), 200


def logout(token: str):
    """
    Invalidates a token by updating its expiry_date to now
    Returns:
      @success: success if expiry_date is updated
      @error: status_code 500 if failure
    """
    AuthController.logout(token)
    response = {
        "success": True,
        "result": {"type": "Logout", "message": "Success"},
    }
    return jsonify(response), 200
