from main import db
from model.Administrator import Administrator


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
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "full_name": self.fullName(),
            "department_id": self.department_id,
            "is_admin": self.isAdmin(),
        }

    def fullName(self):
        if self.middle_name != None:
            return "{} {} {}".format(self.first_name, self.middle_name, self.last_name)
        return "{} {}".format(self.first_name, self.last_name)

    def isAdmin(self):
        admin = Administrator.query.filter_by(user_id=self.id)
        if admin == None:
            return False
        return True
