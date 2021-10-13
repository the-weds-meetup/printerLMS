from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://{}:{}@{}/{}".format(
    environ["DB_USER"],
    environ["DB_PASSWORD"],
    environ["DB_HOST"],
    environ["DB_NAME"],
)
db = SQLAlchemy(app)


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


@app.route("/api/course/catalog")
def get_course_catalog():
    # get is_retired 'True' or 'False' so that we can display the data accordingly
    is_retired = request.args.get("is_retired", default="False")

    try:
        return course.getCourseCatalog(is_retired == "True")

    except Exception as e:
        print(e)
        return auth.throw_error(type="Course", message=str(e), status_code=400)


@app.route("/api/course/<int:course_id>")
def get_course(course_id):
    try:
        return course.getCourse(course_id=course_id)

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
def getLearner():
    request_data = request.get_json()
    try:
        session = request_data["token"]
        return learner.getLearner(token=session)

    except Exception as e:
        print(e)
        return auth.throw_error(type="Learner", message=str(e), status_code=400)


if __name__ == "__main__":
    from api import *

    db.create_all()
    app.run(debug=True, host="0.0.0.0")
