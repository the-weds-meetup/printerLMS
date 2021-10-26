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


@app.route("/api/class/<int:class_id>")
def get_class(class_id):
    try:
        return classes.get_class(class_id=class_id)

    except Exception as e:
        print(e)
        return auth.throw_error(type="Course", message=str(e), status_code=400)


@app.route("/api/trainer/add", methods=["POST"])
def add_trainer():
    data = request.get_json()

    try:
        user_id = data["user_id"]
        class_id = data["class_id"]
        return classes.add_trainer(user_id, class_id)
    except Exception as e:
        return auth.throw_error(type="Trainer", message=str(e), status_code=400)


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
