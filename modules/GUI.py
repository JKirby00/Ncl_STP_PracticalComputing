'''
Module to sort the graphical user interface (GUI) to use
in the MiniPACS.
'''

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
import sys
import pathlib
from os.path import join
sys.path.append(join(pathlib.Path(__file__).parent.parent.absolute(), "training_activities"))
import DatabaseHandler
import Activity1, Activity2

class MainGui(QMainWindow):
    '''This is the class that defines the main PACS graphical window.'''
    def __init__(self):
        '''This function is called when the MainGui class is first
        initialised'''
        super(MainGui, self).__init__()
        uic.loadUi(r"./ui/pacs_home.ui" ,self)# loads the UI from .ui file
        self.showMaximized()
        self.pt_data = None

        # create an instance of the database handler class
        self.DbClass = DatabaseHandler.PacsDatabaseClass()

        # update the patient table
        self.UpdatePatientTable()

        # connect up the actions on the GUI
        self.patientTable.cellClicked.connect(self.PatientRowClicked)

    def UpdatePatientTable(self):
        '''Function to update the patient table data by querying
        the database and then updating the table with the results.
        
        Args: Nothing
        Returns Nothing
        '''
        # first get the patient data
        self.pt_data = self.DbClass.GetPatientDetails()
        
        # then remove existing rows in table
        self.patientTable.setRowCount(0)

        # loop through each patient and add to the table
        for row_id in range(len(self.pt_data)):
            self.patientTable.insertRow(row_id)# create a row to add cells to
            col_id = -1
            for col_name in self.pt_data[row_id]:
                if col_name == "id":
                    # ignore the id column
                    continue
                elif col_name == "Address":
                    # if col is address, jump two columns for id to skip the age column
                    col_id += 2
                else:
                    # for all other columns add one to the column id
                    col_id += 1

                # create the table cell widget and then add to the table
                cell_item = QTableWidgetItem(self.pt_data[row_id][col_name])
                self.patientTable.setItem(row_id, col_id, cell_item)

            # add in the calculated age of the patient (will work once activity 2
            # has been successfully completed)
            try:
                # call age calculating function and then set to table cell
                age = Activity2.CalculateAgeFromDob(dob = self.pt_data[row_id]["DateOfBirth"])
                cell_item = QTableWidgetItem(str(age))
                self.patientTable.setItem(row_id, 3, cell_item)
            except:
                # just add ?? for now as not able to set age
                cell_item = QTableWidgetItem("??")
                self.patientTable.setItem(row_id, 3, cell_item)
            
    def PatientRowClicked(self, row, col):
        '''User has clicked on a patient in the patient table so then
        update the study data and link to activity 1 to print the patient
        details to the console.'''
        try:
            Activity1.PrintDataToConsole(patient_details = self.pt_data[row])
        except:
            print("Activity 1 not yet completed")
        


def ShowGui():
    '''
    Very simple function that shows the main PACS GUI
    by creating a PyQt application, creates an instance of our
    UI class and then executes the QApplication.

    Args: Nothing
    Returns: Nothing
    '''
    app = QApplication([])
    window = MainGui()
    app.exec_()


if __name__ == "__main__":
    ShowGui()