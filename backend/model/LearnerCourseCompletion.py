"""
LearnerCouseCompletion.py
"""

from main import db


class LearnerCourseCompletion(db.Model):
    __tablename = "learner_course_completion"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("learner.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
    class_id = db.Column(db.Integer, db.ForeignKey("class.class_id"))
    completion_date = db.Column(db.String(), nullable=False)

    def __init__(
        self,
        user_id: int,
        course_id: int,
        class_id: int,
        completion_date: str,
    ):
        self.user_id = user_id
        self.course_id = course_id
        self.class_id = class_id
        self.completion_date = completion_date
        

    def serialise(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "course_id": self.course_id,
            "class_id": self.class_id,
            "completion_date": self.completion_date,
        }
