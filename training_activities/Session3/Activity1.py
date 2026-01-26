"""Activity - Databases

1) Write some simple SQL queries into the empty dictionary 'sql_queries' below to get the required information (diff=1-2)
2) Complete the query_database function to connect to the database, execute a query and return the results (diff=1)
3) Write functions to use your SQL queries and query_database function to return the results (diff=1)
4) Write the docstrings for the database query functions you have just created  (diff=1) 
5) Write tests for the database query functions: (diff=3)
    - Specified usual behaviour 
    - Specified edge cases 
    - Errors 
6) Review the practical from Session 2 and compile a list of specifications for one or more of the DICOM functions 
7) Turn the specifications into unit tests 
8) Review the mini-PACs application and compile a list of product specifications 
9) Turn the specifications into system tests 

"""
import sqlite3
import os
import pathlib

# Add your SQL queries into the empty strings below
sql_queries = {
    "get_all_patients": "SELECT * FROM Patients",
    "get_patient_by_mrn": "",
    "get_all_studies": "",
    "get_study_by_id": "",
    "get_all_series": "",
    "get_series_by_study_id": "",
    "get_images_by_id": "",
    "insert_new_patient": "",
    "insert_new_study": "",
    "insert_new_series": ""
}


def get_patients():
    pass


def query_database(query, params=()):
    '''
    Inputs:
        query (str): The SQL query to execute
        params (tuple): The parameters to use in the SQL query
    Outputs: 
    '''
    conn = None
    cursor = None
    db_path = os.path.join(pathlib.Path(__file__).parent.parent.parent.absolute(), "database", "Yr2PracticalComputingDb.db")


if __name__ == "__main__":
    query_result = query_database(sql_queries["get_all_patients"])
    print(query_result)

    query_result = query_database(sql_queries["get_patient_by_mrn"], ("123456",))
    print(query_result)