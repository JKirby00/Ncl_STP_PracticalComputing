"""Activity - Databases

Pre-requisite:
    Either install SQLite Viewer from VSCode extensions or view the database in SQLite DBBrowser

1) Write some simple SQL queries into the empty dictionary 'sql_queries' below to retrieve the required information (diff=1-2)
2) Complete the query_database function to connect to the database, execute a query and return the results (diff=1)
3) Write functions to use your SQL queries and query_database function to return the results (diff=1)
4) Write a function to add a new patient to the database (diff=3)
5) Write the docstrings for the database query functions you have just created  (diff=1) 

Some helper code for testing has been included in the block at the end of the script.

"""
import sqlite3
import os
import pathlib

# Add your SQL queries into the empty strings below
sql_queries = {
    "get_all_patients": "Replace this with your SQL query",
    "get_patient_by_mrn": "",
    "get_all_studies": "",
    "get_study_by_id": "",
    "get_all_series": "",
    "get_series_by_study_id": "",
    "get_images_by_id": "",
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


def insert_patient(mrn, name, date_of_birth, address):
    pass


def insert_into_database(query, params=()):
    conn = None
    cursor = None
    db_path = os.path.join(pathlib.Path(__file__).parent.parent.parent.absolute(), "database", "Yr2PracticalComputingDb.db")
    pass


if __name__ == "__main__":
    # Update the following to test your SQL queries
    query_result = query_database(sql_queries["get_all_patients"])
    print("Task2 query:", query_result)
    
    # Update the following to test your SQL queries requiring parameters
    query_result = query_database(sql_queries["get_patient_by_mrn"], ("123456B",))
    print("Task2 query:", query_result)
    
    # Update the following to test your SQL functions
    print("Task3 query:", get_patients())

    # Update the following for inserting a new patient
    print("Task4 Insert:")
    insert_result = insert_patient("654321", "John Doe", "01/01/1990", "404 Testing St")
    print("Insert Patient Result:", insert_result)
    print("Updated Patients List:", get_patients())