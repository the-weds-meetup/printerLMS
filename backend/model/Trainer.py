"""
Trainer.py
"""

from main import db


class Trainer(db.Model):
    __tablename__ = "trainer"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("learner.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
    class_id = db.Column(db.Integer, db.ForeignKey("class.class_id"))

    def __init__(
        self,
        user_id: int,
        course_id: int,
        class_id: int,
    ):
        self.user_id = user_id
        self.course_id = course_id
        self.class_id = class_id

    # learner = db.relationship(
    #     "Learner",
    #     primaryjoin="Trainer.user_id == Learner.id",
    #     backref="class",)

    # convert to json
    def serialise(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "course_id": self.course_id,
            "class_id": self.class_id,
        }

    # def get_name(self):
    #     return self.trainer_name


#db.create_all()