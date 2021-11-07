import unittest
from unittest.mock import Mock, MagicMock, patch
from freezegun import freeze_time
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../controller"))
)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../model")))


from tests.TestApp import TestApp
from controller import TrainerController


class TestTrainerController(TestApp):
    @freeze_time("2021-10-22")
    def test_get_trainer_all_classes(self):
        self.assertEqual(
            len(TrainerController.TrainerController().get_all_classes(2)),
            6,
        )

    @freeze_time("2021-10-22")
    def test_get_trainer_current_classes(self):
        self.assertEqual(
            len(TrainerController.TrainerController().get_current_classes(2)),
            2,
        )


def suite():
    """This defines all the tests of a module"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestTrainerController))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
