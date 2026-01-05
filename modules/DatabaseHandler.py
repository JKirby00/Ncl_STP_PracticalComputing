'''This module is designed to deal with the communication
with the SQlite database which will contain the basic patient 
data to show in our test pacs system.'''

import sqlite3
import pathlib
from os.path import join

class PacsDatabaseClass:
    '''
    Class to deal with database connections to the sqlite database
    that contains test patient data for the pacs system.
    '''
    def __init__(self):
        self.Conn = None
        self.ExceptionList = []

    def CreateDatabaseConnection(self):
        '''
        Connect to the database at the path specified.
        Set self.Conn to the connection if successful.

        Args: None
        Returns: True if connected, False if not
        '''
        db_path = join(pathlib.Path(__file__).parent.parent.absolute(),
            "database", "Yr2PracticalComputingDb.db")
        if self.Conn == None:
            try:
                self.Conn = sqlite3.connect(db_path, timeout=30)
                return True
            except Exception as e:
                self.Conn = None
                self.ExceptionList.append(e)
                return False

    def CloseDatabaseConnection(self):
        '''
        If a connection is present on the class, close the connection.

        Args: None
        Returns True or Faslse depending on whether it is a success
            or not.
        '''
        if self.Conn != None:
            try:
                self.Conn.close()
                self.Conn = None
                return True
            except:
                return False

    def GetPatientDetails(self):
        '''Function to retrieve the list of patient data
        from the patients table.
        
        Args: None
        Returns:
            List of dicts where the keys are the column names and each
            dictionary is for a different patient record
        '''
        self.CreateDatabaseConnection()

        # complate the query to get all patients
        cursor = self.Conn.cursor()
        cursor.execute("SELECT * FROM Patients")
        patients = cursor.fetchall()

        self.CloseDatabaseConnection()

        # get the column names
        col_names = [desc[0] for desc in cursor.description]
        
        # convert the result to a list of dictionaries
        pt_dicts = []
        for row in patients:
            row_dict = {}
            for i in range(len(col_names)):
                row_dict[col_names[i]] = row[i]
            pt_dicts.append(row_dict)
        
        return pt_dicts

if __name__ == "__main__":
    test = PacsDatabaseClass()
    test.GetPatientDetails()
    