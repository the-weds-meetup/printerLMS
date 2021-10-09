from flask import Flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from model import Learner


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
        return auth.throw_error(type="Login", message=str(e), status_code=400)

@app.route("/api/learners")
def learners():
    search_first_name = request.args.get('first_name')
    if search_first_name:
        learner_list = Learner.Learner.query.filter(Learner.Learner.name.contains(search_first_name))
    else:
        learner_list = Learner.Learner.query.all()
    
    
    return jsonify(
        {
            "data": [learner.to_dict() for learner in learner_list]
        }
    ), 200



if __name__ == "__main__":
    from api import *

    db.create_all()
    app.run(debug=True, host="0.0.0.0")
