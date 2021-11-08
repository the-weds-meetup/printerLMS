from main import db

class Question(db.Model):
    __tablename__ = "question"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    question = db.Column(db.String())
    choices = db.Column(db.String())
    answer = db.Column(db.String())

    def __init__(
        self,
        question: str,
        choices: list,
        answer: str,
    ):
        self.question = question
        self.choices = choices
        self.answer = answer


    def __repr__(self):
        return "<id: {}, question: {}, choices: {}, answer: {}>".format(
            self.id, self.question, self.choices, self.answer
        )

    def to_dict(self):
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result