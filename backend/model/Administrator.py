from main import db


class Administrator(db.Model):
    __tablename__ = "administrator"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("learner.id"), nullable=False)

    def __init__(self, user_id):
        self.user_id = user_id

    def serialise(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }
