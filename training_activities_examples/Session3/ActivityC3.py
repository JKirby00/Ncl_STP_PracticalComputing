import unittest
from Activity1 import *
# from Activity1 import sql_queries

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

    def test_query_database_can_execute_sql_queries(self):
        q = query_database("SELECT * FROM Patients")
        self.assertEqual(len(q), 5)
        q = query_database("SELECT MRN FROM Patients")
        self.assertEqual(len(q), 5)

    def test_query_database_can_execute_sql_queries_with_parameters(self):
        q = query_database("SELECT * FROM Patients WHERE MRN = ?", ('12345'))
        self.assertEqual(len(q), 1)
        q = query_database("SELECT * FROM Series WHERE NumberOfSlices > ?", (10))
        self.assertEqual(len(q), 5)

    def test_query_database_returns_None_if_query_is_not_valid(self):
        q = query_database("THIS IS NOT VALID SQL")
        self.assertIsNone(q)
        q = query_database("SELECT * FROM Series WHERE StudyId = ? AND NumberOfSlices = ?", (1))
        self.assertIsNone(q)

    def test_insert_patient_can_add_a_patient_to_the_database(self):
        before_add = get_patients()
        add = insert_patient("87654321", "Gytha Ogg", "1938-05-21", "Lancre")
        self.assertTrue(add)
        after_add = get_patients()
        # by checking the number of patients before and after, we don't have
        # to hardcode the expected number (which will go up every time we run!)
        self.assertEqual(len(before_add) + 1, len(after_add))
        last_patient = after_add[-1]
        self.assertEqual(last_patient, ("87654321", "Gytha Ogg", "1938-05-21", "Lancre"))

    def test_insert_patient_does_not_add_a_patient_to_the_database_if_the_input_is_invalid(self):
        # this does NOT fail as the db has no constraints
        before_add = get_patients()
        add = insert_patient("", "Sam Vimes", "1951-55-55", "Ankh-Mopork")
        self.assertFalse(add)
        after_add = get_patients()
        # no patients added: length is the same before and after
        self.assertEqual(len(before_add), len(after_add))
        before_add = get_patients()
        # calling a function without all its non-optional arguments raises a TypeError
        with self.assertRaises(TypeError):
            insert_patient()
        after_add = get_patients()
        # check that nothing was added to the database
        self.assertEqual(len(before_add), len(after_add))

if __name__ == "__main__":
    unittest.main()