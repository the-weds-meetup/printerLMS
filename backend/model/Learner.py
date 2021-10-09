"""
Learner.py
"""

from main import db


class Learner(db.Model):
    __tablename__ = "learner"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    first_name = db.Column(db.String(), nullable=False)
    middle_name = db.Column(db.String(), nullable=True)
    last_name = db.Column(db.String(), nullable=False)
    department_id = db.Column(db.Integer, nullable=False)

    def __init__(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        department_id: int,
        middle_name: str = None,
    ):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.department_id = department_id

        if middle_name != None:
            self.middle_name = middle_name

    def __repr__(self):
        return "<id: {}, firstName: {}>".format(self.id, self.first_name)

    def serialise(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "department_id": self.department_id,
        }

    def fullName(self):
        if self.middle_name != None:
            return "{} {} {}".format(self.first_name, self.middle_name, self.last_name)
        return "{} {}".format(self.first_name, self.last_name)


    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

