from flask import Flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from os import environ
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
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
        print(e, flush=True)
        return error.throw_error(type="Login", message=str(e), status_code=400)


@app.route("/api/auth/logout", methods=["POST"])
def logout():
    request_data = request.get_json()

    try:
        session = request_data["token"]
        return auth.logout(session)

    except Exception as e:
        print(e, flush=True)
        return auth.throw_error(type="Logout", message=str(e), status_code=400)


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
        print(e, flush=True)
        return auth.throw_error(type="Course", message=str(e), status_code=400)


@app.route("/api/course/<int:course_id>", methods=["GET", "POST"])
def get_course(course_id):
    if request.method == "GET":
        try:
            return course.get_course(course_id=course_id)

        except Exception as e:
            print(e, flush=True)
            return auth.throw_error(type="Course", message=str(e), status_code=400)

    if request.method == "POST":
        request_data = request.get_json()
        try:
            session = request_data["token"]
            isValid = auth.validateToken(session)
            if isValid["status"] == False:
                return auth.throw_error("course_enrolement_valid", isValid["message"])
            else:
                return enrolment.check_learner_course_valid(
                    token=session, course_id=course_id
                )

        except Exception as e:
            print(e, flush=True)
            return auth.throw_error(
                type="course_enrolement_valid", message=str(e), status_code=400
            )


@app.route("/api/class/<int:class_id>/status", methods=["POST"])
def get_course_enrolment_status(class_id):
    request_data = request.get_json()
    session = request_data["token"]

    try:
        isValid = auth.validateToken(session)
        if isValid["status"] == False:
            return auth.throw_error("class_enrolment_status", isValid["message"])
        else:
            return enrolment.class_enrolment_status(token=session, class_id=class_id)

    except Exception as e:
        print(e, flush=True)
        return auth.throw_error(type="course_status", message=str(e), status_code=400)


@app.route("/api/class/<int:class_id>/nonlearners")
def get_class_nonlearners(class_id):
    try:
        return classes.response_get_non_enrolled_learners(class_id)

    except Exception as e:
        print(e, flush=True)
        return auth.throw_error(type="course_status", message=str(e), status_code=400)


@app.route("/api/class/<int:class_id>/learners")
def get_class_learners(class_id):
    try:
        return classes.response_get_class_learners(class_id)

    except Exception as e:
        print(e, flush=True)
        return auth.throw_error(type="course_status", message=str(e), status_code=400)


@app.route("/api/class/<int:id>")
def get_class(id):
    try:
        return classes.get_class(id=id)

    except Exception as e:
        print(e)
        return auth.throw_error(type="Class", message=str(e), status_code=400)


@app.route("/api/course/<int:course_id>/learners/completed")
def get_course_completed_learners(course_id):
    try:
        return course.response_get_completed_learners(course_id)

    except Exception as e:
        print(e)
        return auth.throw_error(type="course_learners", message=str(e), status_code=400)


@app.route("/api/trainer/add", methods=["POST"])
def add_trainer():
    data = request.get_json()

    try:
        user_id = data["user_id"]
        class_id = data["class_id"]
        return classes.add_trainer(user_id, class_id)
    except Exception as e:
        return auth.throw_error(type="Trainer", message=str(e), status_code=400)


@app.route("/api/learner", methods=["POST"])
def get_learner():
    request_data = request.get_json()
    try:
        session = request_data["token"]
        return learner.get_learner(token=session)

    except Exception as e:
        print(e, flush=True)
        return auth.throw_error(type="Learner", message=str(e), status_code=400)


@app.route("/api/enrolment/<int:user_id>")
def get_approved_courses(user_id):
    try:
        return enrolment.get_approved_enrolments(user_id=user_id)

    except Exception as e:
        print(e)
        return auth.throw_error(type="Class", message=str(e), status_code=400)


@app.route("/api/enroll/self/<int:class_id>", methods=["POST"])
def self_enroll_learner(class_id):
    request_data = request.get_json()
    try:
        session = request_data["token"]
        isValid = auth.validateToken(session)

        if isValid["status"] == True:
            loginSession = auth.return_login_session(session)
            return enrolment.response_self_enrolment(
                learner_id=loginSession.get_learner().id, class_id=class_id
            )

        return auth.throw_error("enroll_class", isValid["message"])

    except Exception as e:
        print(e, flush=True)
        return auth.throw_error(type="enroll_class", message=str(e), status_code=400)


@app.route("/api/enroll/manual/<int:class_id>", methods=["POST"])
def manual_enroll_learner(class_id):
    request_data = request.get_json()

    try:
        session = request_data["token"]
        learner_id = request_data["learners"]
        isValid = auth.validateToken(session)

        if isValid["status"] == True:
            loginSession = auth.return_login_session(session)

            if loginSession.get_learner().isAdmin() == False:
                return auth.throw_error(
                    type="Authorisation", message="Not Authorised", status_code=403
                )

            if learner_id == None:
                return auth.throw_error(
                    type="enroll_class", message="Missing Variables", status_code=403
                )

            return enrolment.response_manual_enrolment(
                class_id=class_id, learner_id_list=learner_id
            )

        return auth.throw_error("enroll_class", isValid["message"])

    except Exception as e:
        print(e, flush=True)
        return auth.throw_error(type="enroll_class", message=str(e), status_code=400)


@cross_origin(origins="http://localhost:8080")
@app.route("/api/class", methods=["GET"])
def get_all_class():
    try:
        return classes.get_all_class()
    except Exception as e:
        print(e, flush=True)
        return auth.throw_error(type="Class", message=str(e), status_code=400)


@cross_origin(origins="http://localhost:8080")
@app.route("/api/class/add", methods=["POST"])
def add_class():
    request_data = request.get_json()
    try:
        token = request_data["token"]
        tokenValid = auth.validateToken(token)

        if tokenValid["status"]:
            return classes.add_class(request_data)
        else:
            return auth.throw_error("create_class", tokenValid["message"])

    except Exception as e:
        print(e, flush=True)
        return auth.throw_error(type="create_class", message=str(e), status_code=400)


@cross_origin(origins="http://localhost:8080")
@app.route("/api/class/edit", methods=["POST"])
def edit_class():
    request_data = request.get_json()
    try:
        token = request_data["token"]
        tokenValid = auth.validateToken(token)

        if tokenValid["status"]:
            return classes.edit_class(request_data)
        else:
            return auth.throw_error("create_class", tokenValid["message"])

    except Exception as e:
        print(e, flush=True)
        return auth.throw_error(type="create_class", message=str(e), status_code=400)


if __name__ == "__main__":
    from api import *

    db.create_all()
    app.run(debug=True, host="0.0.0.0")
