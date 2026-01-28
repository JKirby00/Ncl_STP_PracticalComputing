import unittest
from Activity1 import *

class TestDatabaseQueries(unittest.TestCase):

    def test_get_patients_retrieves_data_from_database(self):
        result = get_patients()
        # replace the assertion below with one that makes sense for this function, then add more
        self.skipTest("I have not written this test yet")

    def test_get_patients_retrieves_patient_details_from_database(self):
        self.skipTest("I have not written this test yet")

if __name__ == "__main__":
    unittest.main()