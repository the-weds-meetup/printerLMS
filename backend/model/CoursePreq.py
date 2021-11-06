from main import db
from model.Course import Course


class CoursePreq(db.Model):
    __tablename__ = "course_prerequisite"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    prerequisite_course_id = db.Column(
        db.Integer, db.ForeignKey("course.id"), nullable=False
    )
    is_active = db.Column(db.Boolean, default=True)

    def __init__(
        self,
        course_id: int,
        prerequisite_course_id: int,
        is_active: bool = True,
    ):
        self.course_id = course_id
        self.prerequisite_course_id = prerequisite_course_id
        self.is_active = is_active

    def serialise(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def get_course(self):
        course: Course = Course.query.filter_by(id=self.course_id).first()
        return course

    def get_prereq_course(self):
        course: Course = Course.query.filter_by(id=self.prerequisite_course_id).first()
        return course
