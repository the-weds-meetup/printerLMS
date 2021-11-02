from main import db


class Department(db.Model):
    __tablename__ = "department"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    name = db.Column(db.String(), nullable=False)

    def __init__(self, name: str):
        self.name = name

    def serialise(self):
        return {
            "id": self.id,
            "name": self.name,
        }
