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
from controller import LearnerController


class TestLearnerController(TestApp):
    def test_get_learner_from_id(self):
        learner = LearnerController.LearnerController().get_learner_from_id(1)
        self.assertEqual(learner.fullName(), "Phris Coskitt")