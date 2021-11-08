import unittest
from tests import *

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(
    [
        loader.loadTestsFromTestCase(TestCoursePreqModel.TestCoursePreq),
        loader.loadTestsFromTestCase(TestTrainerController.TestTrainerController),
    ]
)

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)

if result.wasSuccessful():
    exit(0)
else:
    exit(1)
