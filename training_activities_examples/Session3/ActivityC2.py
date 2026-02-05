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
        self.assertEqual(len(result), 7)
        first_result = result[0]
        self.assertEqual(first_result, (1, "123456B", "John Smith", "22/03/1956", "221B Baker Street, London"))
        # any new patients will be added at the end, so this will also fail
        last_result = result[-1]
        self.assertEqual(last_result, (7, "654321", "John Doe", "01/01/1990", "404 Testing St"))

    # integration failure
    def test_get_patients_cannot_retrieve_data_from_database_if_not_connected(self):
        # you could move or rename the database file, but only manually!
        self.skipTest("Cannot disconnect the database automatically")

    def test_query_database_can_execute_sql_queries(self):
        q = query_database("SELECT * FROM Patients")
        self.assertEqual(len(q), 7)
        q = query_database("SELECT MRN FROM Patients")
        self.assertEqual(len(q), 7)

    def test_query_database_can_execute_sql_queries_with_parameters(self):
        q = query_database("SELECT * FROM Patients WHERE MRN = ?", ("123456B",))
        self.assertEqual(len(q), 1)
        q = query_database("SELECT * FROM Series WHERE NumberOfSlices > ?", (10,))
        self.assertEqual(len(q), 4)

    def test_query_database_returns_None_if_query_is_not_valid(self):
        q = query_database("THIS IS NOT VALID SQL")
        self.assertIsNone(q)
        q = query_database("SELECT * FROM Series WHERE StudyNumber = ?", (1,))
        self.assertIsNone(q)

if __name__ == '__main__':
    unittest.main()