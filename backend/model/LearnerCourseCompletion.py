"""
LearnerCouseCompletion.py
"""

from main import db


class LearnerCourseCompletion(db.Model):
    __tablename = "learner_course_completion"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("learner.id"))
    class_id = db.Column(db.Integer, db.ForeignKey("class.id"))
    completion_date = db.Column(db.String(), nullable=False)

    def __init__(
        self,
        user_id: int,
        class_id: int,
        completion_date: str,
    ):
        self.user_id = user_id
        self.class_id = class_id
        self.completion_date = completion_date

    def to_dict(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)

        return result
