from main import db
import datetime


class Enrolment(db.Model):
    __tablename__ = "enrolment"
    __table_args__ = (db.UniqueConstraint("user_id", "class_id"),)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("learner.id"), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("class.id"), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    is_withdrawn = db.Column(db.Boolean, default=False)
    enrolment_date = db.Column(db.String(), nullable=False)
    course_progress = db.Column(db.Float, nullable=False, default=0)

    def __init__(
        self,
        user_id: int,
        class_id: int,
        is_approved: bool = False,
        course_progress: float = 0,
    ):
        dt = datetime.datetime.now()

        self.user_id = user_id
        self.class_id = class_id
        self.is_approved = is_approved
        self.course_progress = course_progress
        self.enrolment_date = dt.isoformat() + "Z"

    def serialise(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
