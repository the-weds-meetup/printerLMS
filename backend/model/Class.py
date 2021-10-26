from main import db
from model.Trainer import Trainer
from model.Learner import Learner


class Class(db.Model):
    __tablename__ = "class"
    __table_args__ = (db.UniqueConstraint("course_id", "class_id"),)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    class_id = db.Column(db.Integer, nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    class_start_date = db.Column(db.String(), nullable=False)
    class_end_date = db.Column(db.String(), nullable=False)
    enrolment_start_date = db.Column(db.String(), nullable=False)
    enrolment_end_date = db.Column(db.String(), nullable=False)

    def __init__(
        self,
        course_id: int,
        class_id: int,
        max_capacity: int,
        class_start_date: str,
        class_end_date: str,
        enrolment_start_date: str,
        enrolment_end_date: str,
    ):
        self.course_id = course_id
        self.class_id = class_id
        self.max_capacity = max_capacity
        self.class_start_date = class_start_date
        self.class_end_date = class_end_date
        self.enrolment_start_date = enrolment_start_date
        self.enrolment_end_date = enrolment_end_date

    def __repr__(self):
        return "<id: {}, course_id: {}, class_id: {}, max_capacity: {}>".format(
            self.id, self.course_id, self.class_id, self.max_capacity
        )

    def serialise(self):
        trainer = self.get_trainer()
        if trainer == None:
            trainer_name = None
        else:
            learner: Learner = Learner.query.filter_by(id=trainer.user_id).first()
            trainer_name = learner.fullName()

        return {
            "course_id": self.course_id,
            "class_id": self.class_id,
            "max_capacity": self.max_capacity,
            "class_start_date": self.class_start_date,
            "class_end_date": self.class_end_date,
            "enrolment_start_date": self.enrolment_start_date,
            "enrolment_end_date": self.enrolment_end_date,
            "trainer": trainer_name,
        }

    def to_dict(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def get_trainer(self):
        trainer: Trainer = Trainer.query.filter_by(class_id=self.id).first()

        return trainer

    def add_trainer(self, user_id):
        trainer: Trainer = Trainer.query.filter_by(class_id=self.id).first()

        if trainer == None:
            # record dont exist, we shall add it
            trainer = Trainer(user_id, self.id)
        else:
            # else overwrite
            trainer.user_id = user_id

        db.session.add(trainer)
        db.session.commit()

        response = {
            "success": True,
            "message": "Trainer record is successfully created",
            "result": {"type": "Trainer", "records": [trainer.serialise()]},
        }

        return response
