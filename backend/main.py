from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask_cors import CORS
from os import environ

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://{}:{}@{}/{}".format(
    environ["DB_USER"],
    environ["DB_PASSWORD"],
    environ["DB_HOST"],
    environ["DB_NAME"],
)
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_size": 100, "pool_recycle": 280}

db = SQLAlchemy(app)
CORS(app)


@app.route("/")
@app.route("/api")
def index():
    return "Hello World!"


# get all courses
@app.route("/courses")
def courses():
    course_list = Course.Course.query.all()
    if len(course_list):
        return jsonify(
            {"code": 200, "data": [course.serialise() for course in course_list]}
        )
    return jsonify({"code": 404, "message": "There are no courses"}), 404


# get all classes
@app.route("/classes")
def classes():
    class_list = Class.Class.query.all()
    if len(class_list):
        return jsonify(
            {
                "code": 200,
                "data": [each_class.serialise() for each_class in class_list],
            }
        )
    return jsonify({"code": 404, "message": "There are no classes"}), 404


# get classes by course
@app.route("/classes/<int:course_id>")
def classes_by_course(course_id):
    class_list = Class.Class.query.filter_by(course_id=course_id)
    if class_list:
        return jsonify(
            {
                "code": 200,
                "data": [each_class.serialise() for each_class in class_list],
            }
        )
    return jsonify({"code": 404, "message": "There are no classes"}), 404


# get all trainers (department id 2)
# for now: assume you can put any learner in the trainer role
@app.route("/learners/<int:department_id>")
def learners(department_id):
    learner_list = Learner.Learner.query.filter_by(department_id=2)
    if learner_list:
        return jsonify(
            {"code": 200, "data": [learner.serialise() for learner in learner_list]}
        )
    return jsonify({"code": 404, "message": "There are no learners"}), 404


# get a specific trainer
@app.route("/learner/<int:id>")
def get_trainer(id):
    learner = Learner.Learner.query.filter_by(id=id).first()

    if learner:
        return jsonify({"code": 200, "data": learner.serialise()})
    return jsonify({"code": 404, "message": "There is no such trainer"}), 404


@app.route("/trainer", methods=["POST"])
def assign_trainer():
    data = request.get_json()
    if not all(key in data.keys() for key in ("user_id", "course_id", "class_id")):
        return jsonify({"message": "Incorrect JSON object provided."}), 500

    # create record in Trainer table
    trainer = Trainer.Trainer(**data)

    try:
        db.session.add(trainer)
        db.session.commit()
        return trainer.serialise(), 201
    except Exception:
        return jsonify({"message": "Unable to commit to database."}), 500

@app.route("/api/test/user/<int:user_id>")
def get_user(user_id):
    return test.get_user_full_name(user_id)


@app.route("/api/auth/login", methods=["POST"])
def login():
    request_data = request.get_json()

    try:
        email = request_data["email"]
        password = request_data["password"]
        return auth.login(email, password)

    except Exception as e:
        print(e)
        return auth.throw_error(type="Login", message=str(e), status_code=400)



if __name__ == "__main__":
    from api import *
    from model import *

    db.create_all()
    app.run(debug=True, host="0.0.0.0")
