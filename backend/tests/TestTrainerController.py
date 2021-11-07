"""
TestTrainerController.py
Authored by: Amos Tan
"""

import unittest
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

    # Test if classes are returned as expected
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

    @freeze_time("2021-10-22")
    def test_get_trainer_future_classes(self):
        self.assertEqual(
            len(TrainerController.TrainerController().get_future_classes(2)),
            2,
        )

    @freeze_time("2021-10-22")
    def test_get_trainer_past_classes(self):
        self.assertEqual(
            len(TrainerController.TrainerController().get_past_classes(2)),
            2,
        )

    # Test if classes taught by Trainer is empty
    @freeze_time("2021-10-22")
    def test_get_trainer_all_classes_empty(self):
        self.assertEqual(
            len(TrainerController.TrainerController().get_all_classes(3)),
            0,
        )

    @freeze_time("2021-10-22")
    def test_get_trainer_current_classes_empty(self):
        self.assertEqual(
            len(TrainerController.TrainerController().get_current_classes(3)),
            0,
        )

    @freeze_time("2021-10-22")
    def test_get_trainer_future_classes_empty(self):
        self.assertEqual(
            len(TrainerController.TrainerController().get_future_classes(3)),
            0,
        )

    @freeze_time("2021-10-22")
    def test_get_trainer_past_classes_empty(self):
        self.assertEqual(
            len(TrainerController.TrainerController().get_past_classes(3)),
            0,
        )

    # Test Exceptions
    def test_get_trainer_get_all_classes_exception(self):
        with self.assertRaises(Exception):
            TrainerController.TrainerController().get_all_classes("string")

    @freeze_time("2021-10-22")
    def test_get_trainer_get_current_classes_exception(self):
        with self.assertRaises(Exception):
            TrainerController.TrainerController().get_current_classes("string")

    @freeze_time("2021-10-22")
    def test_get_trainer_future_classes_exception(self):
        with self.assertRaises(Exception):
            TrainerController.TrainerController().get_future_classes("string")

    @freeze_time("2021-10-22")
    def test_get_trainer_past_classes_exception(self):
        with self.assertRaises(Exception):
            TrainerController.TrainerController().get_future_classes("string")

    # Test if learners are trainers
    def test_is_trainer_true(self):
        self.assertTrue(TrainerController.TrainerController().is_trainer(2))

    def test_is_trainer_false(self):
        self.assertFalse(TrainerController.TrainerController().is_trainer(3))


if __name__ == "__main__":
    unittest.main()
