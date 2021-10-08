from main import db
from model.Learner import Learner
from model.Trainer import Trainer
from flask import jsonify


def get_trainers(department_id):
    learner_list = Learner.query.filter_by(department_id=2)
    if learner_list:
        return jsonify(
            {"code": 200, "data": [learner.serialise() for learner in learner_list]}
        )
    return jsonify({"code": 404, "message": "There are no learners"}), 404


def assign_trainer(user_id: int, course_id: int, class_id: int):
    trainer = Trainer(user_id, course_id, class_id)
    db.session.add(trainer)
    db.session.commit()

    status_code = 201
    response = {
        "success": True,
        "message": "Trainer record is successfully created",
        "result": {"type": "Trainer", "records": [trainer.serialise()]},
    }
    return jsonify(response), status_code
