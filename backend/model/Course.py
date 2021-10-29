from main import db
from typing import List


class Course(db.Model):
    __tablename__ = "course"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    is_retired = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(
        self,
        name: str,
        description: str,
        is_retired: bool = False,
    ):
        self.name = name
        self.description = description
        self.is_retired = is_retired

    def get_course_name(self):
        return self.name

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

    def get_class_past(self):
        classes: List[Class] = Class.query.filter_by(course_id=self.id).all()
        past_class: List[Class] = []
        time_now = datetime.datetime.now(pytz.utc)

        if len(classes) == 0:
            return classes

        for a_class in classes:
            start_date = dateutil.parser.parse(a_class.class_start_date)
            end_date = dateutil.parser.parse(a_class.class_end_date)

            if time_now >= end_date:
                past_class.append(a_class)

        return past_class

