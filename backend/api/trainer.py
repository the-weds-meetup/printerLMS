from main import db
from model.Learner import Learner
from model.Trainer import Trainer
from model.LearnerCourseCompletion import LearnerCourseCompletion
from flask import jsonify


def get_trainers(department_id):
    learner_list = Learner.query.filter_by(department_id=2)
    if learner_list:
        return jsonify({"data": [learner.serialise() for learner in learner_list]}), 200
    return jsonify({"message": "There are no learners"}), 404


def get_trainers_by_id(id):
    learner_list = Learner.query.filter_by(id=id).all()
    if len(learner_list):
        return jsonify({"data": [learner.serialise() for learner in learner_list]}), 200
    return jsonify({"message": "There are no learners"}), 404


def assign_trainer(user_id: int, course_id: int, class_id: int):
    # for checking if trainer has already been assigned to the course
    assigned_trainer = Trainer.query.filter_by(
        user_id=user_id, course_id=course_id, class_id=class_id
    ).first()

    if assigned_trainer:
        return jsonify({"message": "Trainer is already assigned to the course"}), 500

    trainer = Trainer(user_id, course_id, class_id)
    db.session.add(trainer)
    db.session.commit()

    response = {
        "success": True,
        "message": "Trainer record is successfully created",
        "result": {"type": "Trainer", "records": [trainer.serialise()]},
    }
    return jsonify(response), 201
