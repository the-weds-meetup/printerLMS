from main import db
import datetime
from model.Class import Class
from model.Course import Course


class LearnerCourseCompletion(db.Model):
    __tablename__ = "learner_course_completion"
    __table_args__ = (db.UniqueConstraint("user_id", "class_id"),)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("learner.id"), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("class.id"), nullable=False)
    completion_date = db.Column(db.String(), nullable=False)

    def __init__(self, user_id: int, class_id: int, completion_date=None):
        dt = datetime.datetime.now()
        self.user_id = user_id
        self.class_id = class_id

        if completion_date is None:
            self.completion_date = dt.isoformat() + "Z"
        else:
            self.completion_date = completion_date

    def serialise(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def get_course(self):
        current_class: Class = Class.query.filter_by(id=self.class_id).first()
        return current_class.get_course()
