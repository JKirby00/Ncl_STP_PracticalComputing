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
    "get_all_patients": "SELECT * FROM Patients",
    "get_patient_by_mrn": "SELECT * FROM Patients WHERE MRN = ?",
    "get_all_studies": "SELECT * FROM Studies",
    "get_study_by_id": "SELECT * FROM Studies WHERE PatientDatabaseId = ?",
    "get_all_series": "SELECT * FROM Series",
    "get_series_by_study_id": "SELECT * FROM Series WHERE StudyId = ?",
    "get_images_by_id": "SELECT * FROM Images WHERE SeriesDbId = ?",
    "insert_new_patient": "INSERT INTO Patients (MRN, Name, DateOfBirth, Address) VALUES (?,?,?,?)",
    "insert_new_study": "INSERT INTO Studies (PatientDatabaseId, DateOfStudy, StudyType) VALUES (?,?,?)",
    "insert_new_series": "INSERT INTO Series (StudyId, Description, NumberOfSlices) VALUES (?,?,?)"
}

# For example:
def get_patients():
    '''
    Retrieve all patients from the database.

    Outputs:
        results: List of all patients
    '''
    return query_database(sql_queries["get_all_patients"])



def query_database(query, params=()):
    '''
    Connect and query the database.

    Inputs:
        query (str): The SQL query to execute
        params (tuple): The parameters to use in the SQL query
    Outputs: 
        results: The results of the query
    '''
    conn = None
    cursor = None
    try:
        db_path = os.path.join(pathlib.Path(__file__).parent.parent.parent.absolute(), "database", "Yr2PracticalComputingDb.db")
        conn = sqlite3.connect(db_path, timeout=30)
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()  
        conn.close()
        return results
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None


def insert_patient(mrn, name, dob, address):
    '''
    Insert a new patient into the database.

    Inputs:
        mrn (str): Medical Record Number
        name (str): Patient's name
        dob (str): Date of Birth
        address (str): Patient's address
    Outputs:
        result (bool): True if insertion was successful, False otherwise
    '''
    result = insert_into_database(sql_queries["insert_new_patient"], (mrn, name, dob, address))
    return result


def insert_into_database(query, params=()):
    '''
    Connect and insert into the database.

    Inputs:
        query (str): The SQL query to execute
        params (tuple): The parameters to use in the SQL query
    Outputs: 
        results: The results of the query
    '''
    conn = None
    cursor = None
    try:
        db_path = os.path.join(pathlib.Path(__file__).parent.parent.parent.absolute(), "database", "Yr2PracticalComputingDb.db")
        conn = sqlite3.connect(db_path, timeout=30)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()  
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False


if __name__ == "__main__":
    # Update the following to test your SQL queries
    query_result = query_database(sql_queries["get_all_patients"])
    print("Task2 query:", query_result)
    
    # Update the following to test your SQL queries requiring parameters
    query_result = query_database(sql_queries["get_patient_by_mrn"], ("123456B",))
    print("Task2 query:", query_result)
    
    # Update the following to test your SQL functions
    print("Task3 Query:", get_patients())

    # Update the following for inserting a new patient
    insert_result = insert_patient("654321", "John Doe", "01/01/1990", "404 Testing St")
    print("Insert Patient Result:", insert_result)
    print("Updated Patients List:", get_patients())