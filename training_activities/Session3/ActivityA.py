"""Activity - Databases

Pre-requisite:
    Either install SQLite Viewer from VSCode extensions or view the database in SQLite DBBrowser

1) Write some simple SQL queries into the empty dictionary 'sql_query' below to retrieve the required information (diff=1-2)
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
sql_query = {
    "get_all_patients": "SELECT Name, MRN, DateOfBirth, Address FROM patients", # this query adds functionality to MiniPACs
    "get_patient_by_mrn": "SELECT MRN FROM patients WHERE mrn = ?",
    "get_all_studies": "SELECT * FROM studies",
    "get_study_by_id": "SELECT ID FROM studies WHERE id = ?",
    "get_all_series": "SELECT * FROM series",
    "get_series_by_study_id": "SELECT * FROM series WHERE study_id = ?",
    "get_images_by_id": "SELECT * FROM images WHERE series_id = ?",
    "insert_new_patient": "INSERT INTO patients (MRN, NAME, DateOfBirth, Address) VALUES (?, ?, ?, ?)" # this query adds functionality to MiniPACs
}
def get_patients():
    return query_database(sql_query["get_all_patients"])

def query_database(query, params=()):
    db_path = r"C:\Users\c4073711\Desktop\Ncl_STP_PracticalComputing\database\Yr2PracticalComputingDb.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results


def insert_patient(MRN, NAME, DateOfBirth, Address):
    insert_into_database(sql_query["insert_new_patient"], (MRN, NAME, DateOfBirth, Address))
    db_path = r"C:\Users\c4073711\Desktop\Ncl_STP_PracticalComputing\database\Yr2PracticalComputingDb.db"
    query = "INSERT INTO patients (MRN, NAME, DateOfBirth, Address) VALUES (?, ?, ?, ?)"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor() 
    cursor.execute(query, (MRN, NAME, DateOfBirth, Address))
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results




def insert_into_database(query, params=()):
    db_path = r"C:\Users\c4073711\Desktop\Ncl_STP_PracticalComputing\database\Yr2PracticalComputingDb.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor() 
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results


if __name__ == "__main__":
    # Update the following to test your SQL queries
    query_result = query_database(sql_query["get_all_patients"])
    print("Task2 query:", query_result)
    
    # Update the following to test your SQL queries requiring parameters
    query_result = query_database(sql_query["get_patient_by_mrn"], ("123456B",))
    print("Task2 query:", query_result)
    
    # Update the following to test your SQL functions
    print("Task3 query:", get_patients())

    # Update the following for inserting a new patient
    print("Task4 Insert:")
    insert_result = insert_patient("654321", "John Doeeeeeeee", "01/01/1990", "404 Testing St")
    print("Insert Patient Result:", insert_result)
    print("Updated Patients List:", get_patients())