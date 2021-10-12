from main import db
from typing import List
import dateutil.parser
import datetime
import pytz

from model.Class import Class


class Course(db.Model):
    tablename = "course"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    is_retired = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        is_retired: bool = False,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.is_retired = is_retired

    def __repr__(self):
        return "<id: {}, name: {}, description: {}, is retired: {}>".format(
            self.id, self.name, self.description, self.is_retired
        )

    def to_dict(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def get_class_enrolment(self):
        classes: List[Class] = Class.query.filter_by(course_id=self.id).all()
        enrolment_class: List[Class] = []
        time_now = datetime.datetime.now(pytz.utc)

        if len(classes) == 0:
            return classes

        # determine which classes are ongoing enrolment
        # ongoing enrolment start <= current time < ongoing enrolment end
        for a_class in classes:
            enrolment_start = dateutil.parser.parse(a_class.enrolment_start_date)
            enrolment_end = dateutil.parser.parse(a_class.enrolment_end_date)

            if time_now >= enrolment_start and time_now < enrolment_end:
                enrolment_class.append(a_class)

        return enrolment_class

    def get_class_ongoing(self):
        classes: List[Class] = Class.query.filter_by(course_id=self.id).all()
        ongoing_class: List[Class] = []
        time_now = datetime.datetime.now(pytz.utc)

        if len(classes) == 0:
            return classes

        # determine which classes are ongoing enrolment
        # ongoing class start <= current time < class end
        for a_class in classes:
            start_date = dateutil.parser.parse(a_class.class_start_date)
            end_date = dateutil.parser.parse(a_class.class_end_date)

            if time_now >= start_date and time_now < end_date:
                ongoing_class.append(a_class)

        return ongoing_class
