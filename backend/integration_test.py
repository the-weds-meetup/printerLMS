import unittest
from tests import *

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(
    loader.loadTestsFromTestCase(TestTrainerController.TestTrainerController)
)

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
<<<<<<< HEAD


# if __name__ == "__main__":


# suites = unittest.TestSuite(
#     [
#         TestTrainerController.suite(),
#     ]
# )
# suites.run()
=======
>>>>>>> 9c82e49aa9812ad82518bee6c2adca9257a0932a
