from model import Learner


def test(user_id):
    learner = Learner.Learner.query.filter_by(id=user_id).first()
    return learner.fullName()
