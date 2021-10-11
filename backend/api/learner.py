from flask import jsonify

from main import db
from api import auth
from model.Learner import Learner
from model.LoginSession import LoginSession

from api.error import throw_error


def getLearner(token: str):
    """
    Get a learner based on session token
    """
    isValid = auth.validateToken(token)

    if isValid["status"] == False:
        return throw_error("Learner", isValid["message"])

    session: LoginSession = LoginSession.query.filter_by(token=token).first()
    learner: Learner = Learner.query.filter_by(id=session.user_id).first()

    if learner == None:
        return throw_error("Learner", message="Invalid learner id")

    status_code = 200
    response = {
        "success": True,
        "result": {"type": "Learner", "records": [learner.serialise()]},
    }
    return jsonify(response), status_code
