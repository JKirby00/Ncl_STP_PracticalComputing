"""Activity - Databases

1) Write some simple SQL queries to obtain data, and then add these into pre-written python functions that query the database (diff=2) 

2) Write the docstrings for the database query functions you just updated 

3) Write tests for the database query functions: 

    - Specified usual behaviour 
    - Specified edge cases 
    - Errors 

4) Review the practical from Session 2 and compile a list of specifications for one or more of the DICOM functions 

5) Turn the specifications into unit tests 

6) Review the mini-PACs application and compile a list of product specifications 

7) Turn the specifications into system tests 


"""
import sqlite3
import os
import pathlib

# Add your SQL queries here
sql_queries = {
    "get_all_patients": "",
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


if __name__ == "__main__":
    query_result = query_database(sql_queries["get_all_patients"])
    print(query_result)

    query_result = query_database(sql_queries["get_patient_by_mrn"], ("123456",))
    print(query_result)