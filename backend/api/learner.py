from flask import jsonify

from main import db
from api import auth
from model.Learner import Learner
from model.LoginSession import LoginSession

from api.error import throw_error


def get_learner(token: str):
    """
    Get a learner based on session token
    """
    isValid = auth.validateToken(token)

    if isValid["status"] == False:
        return throw_error("Learner", isValid["message"])

    session: LoginSession = LoginSession.query.filter_by(token=token).first()
    learner: Learner = session.get_learner()

    if learner == None:
        return throw_error("Learner", message="Invalid learner id")

    response = {
        "success": True,
        "result": {"type": "Learner", "records": [learner.serialise()]},
    }
    return jsonify(response), 200
