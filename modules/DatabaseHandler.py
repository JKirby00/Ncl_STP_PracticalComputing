'''This module is designed to deal with the communication
with the SQlite database which will contain the basic patient 
data to show in our test pacs system.'''

import sqlite3
import pathlib
from os.path import join
import numpy as np

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

    def GetDatabaseIdFromMRN(self, MRN):
        '''Get the primary key for a patient with a given MRN.
        Arguably this is unecessary if the MRN is unique.'''
        self.CreateDatabaseConnection()

        cursor = self.Conn.cursor()
        cursor.execute("SELECT id FROM Patients WHERE MRN = ?", (MRN,))
        mrn = cursor.fetchone()[0]
        self.CloseDatabaseConnection()

        return mrn

    def InsertNewPatientData(self, data):
        '''Take the dictionary of scraped data and insert this into
        the database'''
        # ad the patient to the database if they don't exist
        first_study_uid = [key for key in data.keys()][0]
        try:
            id = self.GetDatabaseIdFromMRN(MRN = data[first_study_uid]["MRN"])
        except:
            self.CreateDatabaseConnection()
            cursor = self.Conn.cursor()
            sql_string = """INSERT INTO Patients (MRN,
                Name, DateOfBirth, Address) VALUES (?,?,?,?)
            """
            
            variables = (data[first_study_uid]["MRN"],
                str(data[first_study_uid]["Name"]),
                data[first_study_uid]["DOB"],
                "")

            cursor.execute(sql_string, variables)
            self.Conn.commit()
            self.CloseDatabaseConnection()

        for study_uid in data:
            # get the database id for the MRN
            id = self.GetDatabaseIdFromMRN(MRN = data[study_uid]["MRN"])

            # add the study
            self.CreateDatabaseConnection()
            cursor = self.Conn.cursor()

            sql_string = """INSERT INTO Studies (PatientDatabaseId,
                DateOfStudy, StudyType) VALUES (?,?,?)
            """
            variables = (id, data[study_uid]["StudyDate"], data[study_uid]["Type"])

            cursor.execute(sql_string, variables)
            self.Conn.commit()
            lastrowid = cursor.lastrowid
            self.CloseDatabaseConnection()

            # get the database id for the study based on the lastrowid
            self.CreateDatabaseConnection()
            cursor = self.Conn.cursor()
            cursor.execute("SELECT id FROM Studies WHERE ROWID = ?", (lastrowid,))
            study_db_id = cursor.fetchone()[0]
            self.CloseDatabaseConnection()

            # now add each series
            for series_uid in data[study_uid]["Series"]:
                self.CreateDatabaseConnection()
                cursor = self.Conn.cursor()
            
                sql_string = """INSERT INTO Series (StudyId,
                    Description, NumberOfSlices) VALUES (?,?,?)
                """
                variables = (study_db_id,
                    data[study_uid]["Series"][series_uid]["Description"],
                    len(data[study_uid]["Series"][series_uid]["ImageData"]))

                cursor.execute(sql_string, variables)
                self.Conn.commit()
                series_lastrowid = cursor.lastrowid
                self.CloseDatabaseConnection()

                # get the database id for the series based on the lastrowid
                self.CreateDatabaseConnection()
                cursor = self.Conn.cursor()
                cursor.execute("SELECT id FROM Series WHERE ROWID = ?", (series_lastrowid,))
                series_db_id = cursor.fetchone()[0]
                self.CloseDatabaseConnection()

                # loop through all the images and store this data
                for instance_number in data[study_uid]["Series"][series_uid]["ImageData"]:
                    # flatten the pixel array and convert to bytes
                    img_arr = data[study_uid]["Series"][series_uid]["ImageData"][instance_number]
                    img_arr = np.ascontiguousarray(img_arr)
                    shape = img_arr.shape
                    img_bytes = img_arr.ravel().tobytes()

                    self.CreateDatabaseConnection()
                    cursor = self.Conn.cursor()
                
                    sql_string = """INSERT INTO Images (InstanceNumber,
                        PixelData, SeriesDbId, Shape1, Shape2) VALUES (?,?,?,?,?)
                    """
                    variables = (instance_number,
                        sqlite3.Binary(img_bytes),
                        series_db_id,
                        int(shape[0]),
                        int(shape[1]))

                    cursor.execute(sql_string, variables)
                    self.Conn.commit()
                    self.CloseDatabaseConnection()




if __name__ == "__main__":
    test = PacsDatabaseClass()
    test.GetPatientDetails()
    