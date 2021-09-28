from model import Learner


def get_user_full_name(user_id):
    learner = Learner.Learner.query.filter_by(id=user_id).first()
    return learner.fullName()
