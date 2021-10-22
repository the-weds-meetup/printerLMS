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


# get all courses that aren't retired
@app.route("/api/course/get_courses")
def courses():
    is_retired = request.args.get("is_retired", default="False")
    return course.get_courses(is_retired)


# get all classes
@app.route("/api/classes/get_classes")
def classes():
    return classes.get_classes()


# get classes by course
@app.route("/api/classes/get_classes_by_course/<int:course_id>")
def classes_by_course(course_id):
    return classes.get_classes_by_course(course_id)


# get all trainers (department id 2)
# for now: assume you can put any learner in the trainer role
@app.route("/api/learners/get_trainers/<int:department_id>")
def learners(department_id):
    return trainer.get_trainers(department_id)


@app.route("/api/learners/get_trainers_by_id/<int:id>")
def learners_by_user_id(id):
    return trainer.get_trainers_by_id(id)


@app.route("/api/learners/get_trainers_by_id/<int:user_id>")
def assigned_trainers(user_id):
    return trainer.get_assigned_trainer(user_id)


@app.route("/api/trainer/assign_trainer", methods=["POST"])
def assign_trainer():
    data = request.get_json()

    try:
        user_id = data["user_id"]
        course_id = data["course_id"]
        class_id = data["class_id"]
        return trainer.assign_trainer(user_id, course_id, class_id)
    except Exception:
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Error occured, unable to commit to database",
                }
            )
        ), 500


@app.route("/api/learnercompletion/get_learners_by_course/<int:course_id>")
def learners_by_course(course_id):
    return learnercompletion.get_learners_by_course(course_id)


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
        return error.throw_error(type="Login", message=str(e), status_code=400)


@app.route("/api/course/add", methods=["POST"])
def add_course():
    request_data = request.get_json()
    token = request_data["token"]
    isValid = auth.validateToken(token)

    if isValid["status"] == False:
        return auth.throw_error("course_add", isValid["message"])
    else:
        return course.add_course(request_data)


@app.route("/api/course/all")
def get_course_all():
    # get is_retired 'True' or 'False' so that we can display the data accordingly
    is_retired = request.args.get("is_retired", default="False")
    try:
        return course.get_all_courses(is_retired)
    except Exception as e:
        print(e)
        return auth.throw_error(type="Course", message=str(e), status_code=400)


@app.route("/api/course/<int:course_id>")
def get_course(course_id):
    try:
        return course.get_course(course_id=course_id)

    except Exception as e:
        print(e)
        return auth.throw_error(type="Course", message=str(e), status_code=400)


@app.route("/api/auth/logout", methods=["POST"])
def logout():
    request_data = request.get_json()

    try:
        session = request_data["token"]
        return auth.logout(session)

    except Exception as e:
        print(e)
        return auth.throw_error(type="Logout", message=str(e), status_code=400)


@app.route("/api/learner", methods=["POST"])
def get_learner():
    request_data = request.get_json()
    try:
        session = request_data["token"]
        return learner.get_learner(token=session)

    except Exception as e:
        print(e)
        return auth.throw_error(type="Learner", message=str(e), status_code=400)


if __name__ == "__main__":
    from api import *

    db.create_all()
    app.run(debug=True, host="0.0.0.0")
