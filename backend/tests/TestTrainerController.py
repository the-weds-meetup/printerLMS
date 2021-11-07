import unittest
from unittest.mock import Mock, MagicMock, patch
import datetime
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../controller"))
)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../model")))

from controller import TrainerController
from model.Class import Class
from main import app, db

basedir = os.path.abspath(os.path.dirname(__file__))


class TestTrainerController(unittest.TestCase):
    def setUp(self):
        self.db_uri = "sqlite:///" + os.path.join(basedir, "database.db")
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {}
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = self.db_uri
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_hi(self):
        shit = "hi"
        self.assertEqual("hi", shit)

    @patch("TrainerController.datetime")
    def test_get_current_class(self, datetime_mock):

        # set date to 2021-10-22 (YYYY-MM-DD)
        datetime_mock.datetime.now = Mock(return_value=datetime.datetime(2021, 10, 22))
        self.assertListEqual(
            TrainerController.TrainerController().get_current_classes(5),
            [
                Class(
                    1,
                    2,
                    20,
                    "2021-10-22T16:00:00.000Z",
                    "2021-11-05T16:00:00.000Z",
                    "2021-10-04T00:00:00.000Z",
                    "2021-11-15T04:00:00.000Z",
                ),
                # class-id-11
                Class(
                    2,
                    3,
                    20,
                    "2021-10-22T16:00:00.000Z",
                    "2021-11-05T16:00:00.000Z",
                    "2021-10-04T00:00:00.000Z",
                    "2021-11-15T04:00:00.000Z",
                ),
                # class-id-14
                Class(
                    4,
                    3,
                    20,
                    "2021-11-01T16:00:00.000Z",
                    "2021-11-05T16:00:00.000Z",
                    "2021-10-04T00:00:00.000Z",
                    "2021-11-01T08:00:00.000Z",
                ),
            ],
        )


def suite():
    """This defines all the tests of a module"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestTrainerController))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
