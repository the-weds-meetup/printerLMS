from main import db
from model.Learner import Learner
from model.LoginSession import LoginSession


class AuthController:
    def login(self, username: str, password: str):
        """Checks if user record exists and if password is valid"""
        learner = Learner.query.filter_by(email=username, password=password).first()

        if learner is None:
            raise Exception("Invalid Email or Password")

        session = LoginSession(learner.id)
        db.session.add(session)
        db.session.commit()
        return session

    def logout(self, token: str):
        """
        Invalidates a token by updating its expiry_date to now
        """
        session = self.return_login_session(token)

        if session is None:
            raise Exception("Invalid Token")

        session.expireToken()
        db.session.commit()

    def validate_token(self, token: str):
        """
        Validates a token by checking for expiry.
        Returns a boolean as it is meant to be used by other functions
        """
        session = self.return_login_session(token)

        if session is None:
            raise Exception("Token does not exist")

        if session.isExpired():
            raise Exception("Token has Expired")

        return True

    def return_login_session(self, token: str):
        """
        Returns a Login Session
        """
        loginSession: LoginSession = LoginSession.query.filter_by(token=token).first()
        return loginSession
