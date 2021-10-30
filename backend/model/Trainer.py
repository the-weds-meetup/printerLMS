from main import db


class Trainer(db.Model):
    __tablename__ = "trainer"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("learner.id"), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("class.id"), nullable=False)

    def __init__(self, user_id, class_id):
        self.user_id = user_id
        self.class_id = class_id

    def serialise(self):
        return {
            "user_id": self.user_id,
            "class_id": self.class_id,
        }
