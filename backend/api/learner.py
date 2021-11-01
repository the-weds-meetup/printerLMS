from flask import jsonify
from model.Learner import Learner

from controller.LearnerController import LearnerController


def get_learner(token: str):
    """
    Get a learner based on session token
    """
    learner: Learner = LearnerController().get_learner(token)

    response = {
        "success": True,
        "result": {"type": "Learner", "records": [learner.serialise()]},
    }
    return jsonify(response), 200
