"""
LoginSession.py
"""

from main import db
from uuid import uuid4
import dateutil.parser
import datetime


class LoginSession(db.Model):
    __tablename__ = "login_session"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    token = db.Column(db.String(), unique=True, nullable=False)
    creation_date = db.Column(db.String(), nullable=False)
    expiry_date = db.Column(db.String(), nullable=False)

    def __init__(
        self,
        user_id: int,
    ):
        dt = datetime.datetime.now()
        expiry_time = 3 * 60 * 60

        self.user_id = user_id
        self.token = uuid4()
        self.creation_date = dt.isoformat() + "Z"

        # token will expiry in 3 hours from creation_date
        self.expiry_date = (
            dt + datetime.timedelta(seconds=expiry_time)
        ).isoformat() + "Z"

    def serialise(self):
        return {
            "token": self.token,
            "expiry_date": self.expiry_date,
        }

    """
    Checks if token is expired
    """

    def isExpired(self):
        diff = datetime.datetime.now() - dateutil.parser.parse(self.expiry_date)

        # less than 0 ms, current time is bigger than expiry_date
        return diff.microseconds <= 0

    """
    Set token as expired when user signs out
    """

    def expireToken(self):
        self.expiry_date = datetime.datetime.now().isoformat() + "Z"
