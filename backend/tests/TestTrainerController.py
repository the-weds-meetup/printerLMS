import unittest
from unittest.mock import Mock, MagicMock, patch
import datetime
from freezegun import freeze_time
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../controller"))
)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../model")))


from tests.TestApp import TestApp
from controller import TrainerController
from model.Class import Class
from model.Learner import Learner


class TestTrainerController(TestApp):
    def test_hi(self):
        print(Learner.query.filter_by(id=3).first())
        shit = "hi"
        self.assertEqual("hi", shit)

    # @patch("TrainerController.datetime.datetime.now")
    @freeze_time("2021-10-22")
    def test_get_current_class(self):

        # set date to 2021-10-22 (YYYY-MM-DD)
        # datetime_mock.datetime.datetime.now.return_value = Mock(
        #     return_value=datetime.datetime(2021, 10, 22)
        # )
        self.assertListEqual(
            TrainerController.TrainerController().get_all_classes(2),
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
