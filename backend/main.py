from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS, cross_origin
from sqlalchemy.pool import NullPool

isDebug = True if environ.get("FLASK_ENV", "") == "development" else False
isProduction = True if environ.get("FLASK_ENV", "") == "production" else False

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

if isDebug is True:
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://{}:{}@{}/{}".format(
        environ.get("DB_USER", ""),
        environ.get("DB_PASSWORD", ""),
        environ.get("DB_HOST", ""),
        environ.get("DB_NAME", ""),
    )
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_size": 100, "pool_recycle": 300}

if isProduction is True:
    # fix heroku using postgres (unsupported) instead of postgresql
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DATABASE_URL").replace(
        "://", "ql://", 1
    )
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "poolclass": NullPool,
    }


CORS(app)
db = SQLAlchemy(app)


@app.route("/")
@app.route("/api")
def index():
    return "Hello World!"


@app.route("/api/auth/login", methods=["POST"])
def login():
    request_data = request.get_json()

    try:
        email = request_data["email"]
        password = request_data["password"]
        response = auth.login(email, password)

    except Exception as e:
        print(e, flush=True)
        response = error.throw_error(type="Login", message=str(e), status_code=400)

    finally:
        db.session.remove()
        return response


@app.route("/api/auth/logout", methods=["POST"])
def logout():
    request_data = request.get_json()

    try:
        session = request_data["token"]
        response = auth.logout(session)

    except Exception as e:
        print(e, flush=True)
        response = error.throw_error(type="Logout", message=str(e), status_code=500)

    finally:
        db.session.remove()
        return response


@app.route("/api/course/add", methods=["POST"])
def add_course():
    request_data = request.get_json()
    token = request_data["token"]

    try:
        AuthController.AuthController().validate_token(token)
        response = course.add_course(request_data)

    except Exception as e:
        print(e, flush=True)
        response = error.throw_error(type="course_add", message=str(e), status_code=500)

    finally:
        db.session.remove()
        return response


@app.route("/api/course/all")
def get_course_all():
    # get is_retired 'True' or 'False' so that we can display the data accordingly
    is_retired = request.args.get("is_retired", default="False")
    try:
        response = course.get_all_courses(is_retired)
    except Exception as e:
        print(e, flush=True)
        response = error.throw_error(type="Course", message=str(e), status_code=400)

    finally:
        db.session.remove()
        return response


@app.route("/api/course/enrol")
def get_course_enrolling():
    try:
        response = classes.response_get_all_enrollable_classes()
    except Exception as e:
        print(e, flush=True)
        response = error.throw_error(
            type="course_enrolling", message=str(e), status_code=400
        )
    finally:
        db.session.remove()
        return response


@app.route("/api/course/<int:course_id>", methods=["GET", "POST"])
def get_course(course_id):
    if request.method == "GET":
        try:
            response = course.get_course(course_id=course_id)

        except Exception as e:
            print(e, flush=True)
            response = error.throw_error(type="Course", message=str(e), status_code=400)

        finally:
            db.session.remove()
            return response

    if request.method == "POST":
        request_data = request.get_json()
        session = request_data["token"]

        try:
            AuthController.AuthController().validate_token(session)
            loginSession = AuthController.AuthController().return_login_session(session)
            response = enrolment.check_learners_class_enrolment_status(
                loginSession.get_learner().id, course_id
            )

        except Exception as e:
            print(e, flush=True)
            response = error.throw_error(
                type="course_enrolement_valid", message=str(e), status_code=400
            )
        finally:
            db.session.remove()
            return response


@app.route("/api/class/<int:class_id>/status", methods=["POST"])
def get_course_enrolment_status(class_id):
    request_data = request.get_json()
    session = request_data["token"]

    try:
        AuthController.AuthController().validate_token(session)
        loginSession = AuthController.AuthController().return_login_session(session)
        response = enrolment.learner_class_enrolment_status(
            learner_id=loginSession.get_learner().id, class_id=class_id
        )

    except Exception as e:
        print(e, flush=True)
        response = error.throw_error(
            type="course_status", message=str(e), status_code=400
        )

    finally:
        db.session.remove()
        return response


@app.route("/api/class/<int:class_id>/nonlearners")
def get_class_nonlearners(class_id):
    try:
        response = classes.response_get_non_enrolled_learners(class_id)

    except Exception as e:
        print(e, flush=True)
        response = error.throw_error(
            type="class_non_enroled", message=str(e), status_code=400
        )

    finally:
        db.session.remove()
        return response


@app.route("/api/class/<int:class_id>/learners")
def get_class_learners(class_id):
    try:
        response = classes.response_get_class_learners(class_id)

    except Exception as e:
        print(e, flush=True)
        response = error.throw_error(
            type="class_learners", message=str(e), status_code=400
        )

    finally:
        db.session.remove()
        return response


@app.route("/api/class/<int:class_id>/waiting-list")
def get_class_awaiting_learners(class_id):
    try:
        response = classes.response_get_all_waiting_learners(class_id)

    except Exception as e:
        print(e, flush=True)
        response = error.throw_error(
            type="class_waiting_list", message=str(e), status_code=400
        )

    finally:
        db.session.remove()
        return response


@app.route("/api/class/<int:class_id>")
def get_class(class_id):
    try:
        response = classes.response_get_class_details(class_id=class_id)

    except Exception as e:
        print(e, flush=True)
        response = error.throw_error(type="Class", message=str(e), status_code=400)

    finally:
        db.session.remove()
        return response


@app.route("/api/class/<int:class_id>", methods=["POST"])
def get_class_post(class_id):
    try:
        request_data = request.get_json()
        session = request_data["token"]
        AuthController.AuthController().validate_token(session)
        loginSession = AuthController.AuthController().return_login_session(session)
        response = classes.response_get_all_class_details(
            learner_id=loginSession.get_learner().id, class_id=class_id
        )

    except Exception as e:
        print(e, flush=True)
        response = error.throw_error(type="Class_POST", message=str(e), status_code=400)

    finally:
        db.session.remove()
        return response


@app.route("/api/me/classes", methods=["POST"])
def get_all_learner_classes():
    try:
        request_data = request.get_json()
        session = request_data["token"]
        AuthController.AuthController().validate_token(session)
        loginSession = AuthController.AuthController().return_login_session(session)
        response = classes.get_all_learner_classes(user_id=loginSession.user_id)
    except Exception as e:
        print(e, flush=True)
        response = error.throw_error(type="me_class", message=str(e), status_code=400)

    finally:
        db.session.remove()
        return response


@app.route("/api/course/<int:course_id>/learners/completed")
def get_course_completed_learners(course_id):
    try:
        response = course.response_get_completed_learners(course_id)

    except Exception as e:
        print(e)
        response = error.throw_error(
            type="course_learners", message=str(e), status_code=400
        )

    finally:
        db.session.remove()
        return response


@app.route("/api/trainer/add", methods=["POST"])
def add_trainer():
    data = request.get_json()

    try:
        user_id = data["user_id"]
        class_id = data["class_id"]
        response = classes.add_trainer_response(user_id, class_id)
    except Exception as e:
        response = error.throw_error(type="Trainer", message=str(e), status_code=400)

    finally:
        db.session.remove()
        return response


@app.route("/api/learner", methods=["POST"])
def get_learner():
    request_data = request.get_json()
    try:
        session = request_data["token"]
        response = learner.get_learner(token=session)

    except Exception as e:
        print(e, flush=True)
        response = error.throw_error(type="Learner", message=str(e), status_code=400)

    finally:
        db.session.remove()
        return response


@app.route("/api/enrolment/approved", methods=["POST"])
def get_approved_courses():
    request_data = request.get_json()
    session = request_data["token"]

    try:
        AuthController.AuthController().validate_token(session)
        loginSession = AuthController.AuthController().return_login_session(session)

        response = enrolment.response_get_approved_enrolments(
            learner_id=loginSession.get_learner().id
        )

    except Exception as e:
        print(e)
        response = error.throw_error(type="Class", message=str(e), status_code=400)

    finally:
        db.session.remove()
        return response


@app.route("/api/enroll/self/<int:class_id>", methods=["POST"])
def self_enroll_learner(class_id):
    request_data = request.get_json()
    session = request_data["token"]

    try:
        AuthController.AuthController().validate_token(session)
        loginSession = AuthController.AuthController().return_login_session(session)

        response = enrolment.response_self_enrolment(
            learner_id=loginSession.get_learner().id, class_id=class_id
        )

    except Exception as e:
        print(e, flush=True)
        response = error.throw_error(
            type="enroll_class", message=str(e), status_code=400
        )

    finally:
        db.session.remove()
        return response


@app.route("/api/enroll/manual/<int:class_id>", methods=["POST"])
def manual_enroll_learner(class_id):
    request_data = request.get_json()
    try:
        session = request_data["token"]
        learner_id_list = request_data["learners"]
        AuthController.AuthController().validate_token(session)
        loginSession = AuthController.AuthController().return_login_session(session)

        if loginSession.get_learner().isAdmin() == False:
            response = error.throw_error(
                type="Authorisation", message="Not Authorised", status_code=403
            )
            db.session.remove()
            return response

        if learner_id_list == None:
            raise Exception("Missing Learners List")

        response = enrolment.response_manual_enrolment(class_id, learner_id_list)

    except Exception as e:
        print(e, flush=True)
        response = error.throw_error(
            type="enroll_class", message=str(e), status_code=400
        )

    finally:
        db.session.remove()
        return response


@cross_origin(origins="http://localhost:8080")
@app.route("/api/class/add", methods=["POST"])
def add_class():
    request_data = request.get_json()
    try:
        session = request_data["token"]
        AuthController.AuthController().validate_token(session)
        loginSession = AuthController.AuthController().return_login_session(session)

        if loginSession.get_learner().isAdmin() == False:
            response = error.throw_error(
                type="Authorisation", message="Not Authorised", status_code=403
            )
            db.session.remove()
            return response

        response = classes.add_class(request_data)

    except Exception as e:
        print(e, flush=True)
        response = error.throw_error(
            type="create_class", message=str(e), status_code=400
        )

    finally:
        db.session.remove()
        return response


@cross_origin(origins="http://localhost:8080")
@app.route("/api/class/edit", methods=["POST"])
def edit_class():
    request_data = request.get_json()
    try:
        session = request_data["token"]
        AuthController.AuthController().validate_token(session)
        response = classes.edit_class(request_data)

    except Exception as e:
        print(e, flush=True)
        response = error.throw_error(
            type="create_class", message=str(e), status_code=400
        )

    finally:
        db.session.remove()
        return response


@app.route("/api/quiz/add", methods=["POST"])
def add_quiz():
    return auth.throw_error(type="quiz", message="Work In Progress", status_code=500)
    # request_data = request.get_json()
    # try:
    #     response = quiz.add_quiz(request_data)
    # except Exception as e:
    #     print(e, flush=True)
    #     response = auth.throw_error(type="create_quiz", message=str(e), status_code=400)
    # finally:
    #     db.session.remove()
    #     return response


if __name__ == "__main__":
    from api import *
    from controller import *

    db.create_all()
    app.run(debug=isDebug, host="0.0.0.0", port=environ.get("PORT", 5000))
