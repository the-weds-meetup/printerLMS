from main import db

class Question(db.model):
    __tablename__="questions"
    qid = db.Column(db.Integer, primary_key=True)
    question =db.Column(db.String, nullable=False)
    option1 = db.Column(db.String, nullable=True)
    option2 = db.Column(db.String, nullable=True)
    option3 = db.Column(db.String, nullable=True)
    option4 = db.Column(db.String, nullable=True)
    answer = db.Column(db.Integer, nullable=True 
