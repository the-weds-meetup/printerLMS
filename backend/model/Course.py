"""
Course.py
"""

from main import db


class Course(db.Model):
    __tablename__ = "course"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    is_retired = db.Column(db.Boolean(), nullable=False)

    def __init__(self, name: str, description: str, is_retired: bool):
        self.name = name
        self.description = description
        self.is_retired = is_retired

    # def __repr__(self):
    #     return "<id: {}, name: {}>".format(self.id, self.name)

    def serialise(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_retired": self.is_retired,
        }

    def get_course_name(self):
        return self.name


#db.create_all()
