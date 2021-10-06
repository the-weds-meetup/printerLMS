"""
Class.py
"""

from main import db


class Class(db.Model):
    __tablename__ = "class"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
    class_id = db.Column(db.Integer, nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    current_capacity = db.Column(db.String(), nullable=False)
    class_start_date = db.Column(db.String(), nullable=False)
    class_end_date = db.Column(db.String(), nullable=False)
    enrolment_start_date = db.Column(db.String(), nullable=False)
    enrolment_end_date = db.Column(db.String(), nullable=False)

    def __init__(
        self,
        course_id: int,
        class_id: int,
        max_capacity: int,
        current_capacity: int,
        class_start_date: str,
        class_end_date: str,
        enrolment_start_date: str,
        enrolment_end_date: str,
    ):
        self.course_id = course_id
        self.class_id = class_id
        self.max_capacity = max_capacity
        self.current_capacity = current_capacity
        self.class_start_date = class_start_date
        self.class_end_date = class_end_date
        self.enrolment_start_date = enrolment_start_date
        self.enrolment_end_date = enrolment_end_date

    # course = db.relationship(
    #     "Course",
    #     primaryjoin="Class.course_id == Course.id",
    #     backref="class",
    # )

    # this method caused an recursion depth error
    # def __repr__(self):
    #     return "<id: {}, class start date: {}>".format(self.id, self.class_start_date)

    def serialise(self):
        return {
            "id": self.id,
            "course_id": self.course_id,
            "class_id": self.class_id,
            "max_capacity": self.max_capacity,
            "current_capacity": self.current_capacity,
            "class_start_date": self.class_start_date,
            "class_end_date": self.class_end_date,
            "enrolment_start_date": self.enrolment_start_date,
            "enrolment_end_date": self.enrolment_end_date,
        }

    def class_max_capacity(self):
        return "{}".format(self.max_capacity)

    def get_start_date(self):
        return self.class_start_date

    def get_end_date(self):
        return self.class_end_date


#db.create_all()