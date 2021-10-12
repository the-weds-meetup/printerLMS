from flask import Flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
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


@app.route("/api/auth/logout", methods=["POST"])
def logout():
    request_data = request.get_json()

    try:
        session = request_data["token"]
        return auth.logout(session)

    except Exception as e:
        print(e)
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
        print(e)
        return auth.throw_error(type="Course", message=str(e), status_code=400)


@app.route("/api/course/<int:course_id>", methods=["GET", "POST"])
def get_course(course_id):
    if request.method == "GET":
        try:
            return course.get_course(course_id=course_id)

        except Exception as e:
            print(e)
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
            print(e)
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
        print(e)
        return auth.throw_error(type="course_status", message=str(e), status_code=400)


@app.route("/api/learner", methods=["POST"])
def get_learner():
    request_data = request.get_json()
    try:
        session = request_data["token"]
        return learner.get_learner(token=session)

    except Exception as e:
        print(e)
        return auth.throw_error(type="Learner", message=str(e), status_code=400)


@app.route("/api/enroll/<int:class_id>", methods=["POST"])
def enroll_learner(class_id):
    request_data = request.get_json()
    try:
        session = request_data["token"]
        isValid = auth.validateToken(session)
        if isValid["status"] == False:
            return auth.throw_error("enroll_class", isValid["message"])
        else:
            return enrolment.add_enrolment(token=session, class_id=class_id)

    except Exception as e:
        print(e)
        return auth.throw_error(type="enroll_class", message=str(e), status_code=400)

@app.route("/api/class/all")
def get_all_class():
    try:
        return class_list.get_all_class()
    except Exception as e:
        print(e)
        return auth.throw_error(type="Class", message=str(e), status_code=400)


@app.route("/api/class", methods=['POST'])
def add_class():
    request_data = request.get_json()
    return classes.add_class(request_data)

@app.route("/api/model/class")
def classes():
    class_list = Class.query.all()
    return jsonify(
        {
            "data": [Class.to_dict()
                     for Class in class_list]
        }
    ), 200


@app.route("/api/model/class", methods=['POST'])
def create_class():
    data = request.get_json()
    if not all(key in data.keys() for
               key in ('course_id', 'class_id',
                       'start_date', 'end_date',
                        'enrolment_start_date','enrolment_end_date')):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 500


if __name__ == "__main__":
    from api import *

    db.create_all()
    app.run(debug=True, host="0.0.0.0")
