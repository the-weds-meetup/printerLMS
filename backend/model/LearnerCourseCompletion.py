from main import db
import datetime


class LearnerCourseCompletion(db.Model):
    __tablename__ = "learner_course_completion"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("learner.id"), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("class.id"), nullable=False)
    completion_date = db.Column(db.String(), nullable=False)

    def __init__(
        self,
        user_id: int,
        class_id: int,
    ):
        dt = datetime.datetime.now()
        self.user_id = user_id
        self.class_id = class_id
        self.completion_date = dt.isoformat() + "Z"

    def serialise(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
