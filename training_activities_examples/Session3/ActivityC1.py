import unittest
from Activity1 import *

class TestDatabaseQueries(unittest.TestCase):

    def test_get_patients_retrieves_data_from_database(self):
        result = get_patients()
        self.assertIsInstance(result, list)
        first_result = result[0]
        self.assertIsInstance(first_result, tuple)
        self.assertEqual(len(first_result), 5)

    # this test will break if the content of the database is altered!
    def test_get_patients_retrieves_patient_details_from_database(self):
        result = get_patients()
        # if you insert any new patients into the database, this count will fail
        self.assertEqual(len(result), 5)
        first_result = result[0]
        self.assertEqual(first_result, ("First", "patient", "details"))
        # any new patients will be added at the end, so this will also fail
        last_result = result[-1]
        self.assertEqual(last_result, ("Last", "patient", "details"))

    # integration failure
    def test_get_patients_cannot_retrieve_data_from_database_if_not_connected(self):
        # you could move or rename the database file, but only manually!
        self.skipTest("Cannot disconnect the database automatically")

if __name__ == "__main__":
    unittest.main()