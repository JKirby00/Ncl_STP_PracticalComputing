'''
Module to sort the graphical user interface (GUI) to use
in the MiniPACS.
'''

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.QtWidgets import QDialog, QListWidgetItem, QMenu, QAction
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from pandas.plotting import register_matplotlib_converters
import sys
import pathlib
from os.path import join
from datetime import datetime

import DatabaseHandler
import ImportDicom
sys.path.append(join(pathlib.Path(__file__).parent.parent.absolute(), "training_activities_examples"))
from Session1 import Activity1, Activity2, Activity3, Activity7
from Session1 import Activity8, Activity9
from Session2 import ActivityB

class MainGui(QMainWindow):
    '''This is the class that defines the main PACS graphical window.'''
    def __init__(self):
        '''This function is called when the MainGui class is first
        initialised'''
        super(MainGui, self).__init__()
        uic.loadUi(r"./ui/pacs_home.ui" ,self)# loads the UI from .ui file
        self.showMaximized()
        self.pt_data = None
        self.study_list = None
        self.currentStudyRow = None
        self.series_list = None
        self.currentSeriesRow = None
        self.image_data = None
        self.current_patient_row = None
        self.import_dir = join(pathlib.Path(__file__).parent.parent.absolute(), "import")

        # create an instance of the database handler class
        self.DbClass = DatabaseHandler.PacsDatabaseClass()

        # update the patient table
        self.UpdatePatientTable()

        # connect up the actions on the GUI
        self.patientTable.cellClicked.connect(self.PatientRowClicked)
        self.importPatientBtn.clicked.connect(self.ImportBtnClicked)
        self.studiesTable.cellClicked.connect(self.StudyRowClicked)
        self.studiesTable.itemSelectionChanged.connect(self.OnStudiesSelectionChanged)
        self.seriesTable.cellClicked.connect(self.SeriesRowClicked)
        self.actionBMI_Calculator.triggered.connect(self.BmiBtnClicked)
        self.exportDataBtn.clicked.connect(self.ExportBtnClicked)

        self.seriesTable.setRowCount(0)
        self.studiesTable.setRowCount(0)
        self.seriesTable.setColumnWidth(0,150)

        # setup img viewer canvas
        self.img_viewer_canvas = FigureCanvas(Figure())
        self.viewerLayout.addWidget(self.img_viewer_canvas)
        self.img_viewer_canvas.mpl_connect('scroll_event',self.ScrollImage)

        # enable right-click context menu on the canvas
        self.img_viewer_canvas.setContextMenuPolicy(Qt.CustomContextMenu)
        self.img_viewer_canvas.customContextMenuRequested.connect(self.ShowWindowMenu)
        # remember the last selected window preset (default initially)
        self.current_window_preset = 'default'

    def ExportBtnClicked(self):
        '''The export button has been clicked, so send data
        to the Activity 9 function to save to Excel.'''
        
        if self.current_patient_row is None:
            pt_data = None
        else:
            pt_data = self.pt_data[self.current_patient_row]

        Activity9.WriteDataToExcel(
            pt_data = pt_data,
            study_data = self.study_list,
            series_data = self.series_list)

    def BmiBtnClicked(self):
        '''BMI Toolbar menu item has been selected so show
        the BMI dialog box'''
        bmi_dialog = BMIDialog()
        bmi_dialog.exec_()
        bmi_dialog.show()

    def ScrollImage(self, e):
        '''User has scroll on the image viewer so update slice shown'''
        if self.image_data is None:
            return
        max_instance_num = max(self.image_data["instance_ids"])
        min_instance_num = min(self.image_data["instance_ids"])

        if e.button == 'up':
            if self.current_instance_num == max_instance_num:
                return
            self.current_instance_num += 1
        else:
            if self.current_instance_num == min_instance_num:
                return
            self.current_instance_num -= 1

        self.PlotImage(self.current_instance_num)

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

    def UpdateStudyTable(self, study_list):
        '''A list of studies has been sent back from the thread so
        update the study table.'''
        self.study_list = study_list

        # loop through each study and add to the table
        for row_id in range(len(study_list)):
            self.studiesTable.insertRow(row_id)# create a row to add cells to
            col_id = -1
            for col_name in study_list[row_id]:
                if col_name == "id" or col_name == "PatientDatabaseId":
                    # ignore the id columns
                    continue
                elif col_name == "DateOfStudy":
                    # convert date into format required
                    time_string = datetime.strptime(study_list[row_id][col_name],
                        "%Y%m%d").strftime("%d/%m/%Y")
                    cell_item = QTableWidgetItem(time_string)
                    col_id += 1
                elif col_name == "StudyType":
                    # convert study type from id to text
                    conversion_dict = {
                        "1.2.840.10008.5.1.4.1.1.2":"CT",
                        "1.2.840.10008.5.1.4.1.1.2.1":"Enhanced CT",
                        "1.2.840.10008.5.1.4.1.1.4":"MRI"
                    }

                    if str(study_list[row_id][col_name]) in conversion_dict:
                        type_string = conversion_dict[str(study_list[row_id][col_name])]
                    else:
                        type_string = study_list[row_id][col_name]
                    cell_item = QTableWidgetItem(type_string)
                    col_id += 1

                # add to the table
                self.studiesTable.setItem(row_id, col_id, cell_item)

    def UpdateSeriesTable(self, series_list):
        '''A list of series has been sent back from the thread so
        update the series table.'''
        self.series_list = series_list

        # loop through each study and add to the table
        for row_id in range(len(series_list)):
            self.seriesTable.insertRow(row_id)# create a row to add cells to
            col_id = -1
            for col_name in series_list[row_id]:
                if col_name == "id" or col_name == "StudyId":
                    # ignore the id columns
                    continue
                else:
                    col_id += 1

                # add to the table
                cell_item = QTableWidgetItem(str(series_list[row_id][col_name]))
                self.seriesTable.setItem(row_id, col_id, cell_item)

        self.VolsThread = CalculateExternalVolumesThread(self.series_list)
        self.VolsThread.vol_calculated_sig.connect(self.UpdateExternalVol)
        self.VolsThread.start()

    def UpdateExternalVol(self, vol_data):
        '''Data has been sent back from the CalculateExternalVolumes
        Thread so update the series table with the volume data.
        
        Args:
            vol_data (dict) = Dict with keys: "table_row" and "content"    
        '''
        # create a new cell with the content and then add it to the table
        new_cell = QTableWidgetItem(vol_data["content"])
        self.seriesTable.setItem(vol_data["table_row"], 2, new_cell)

    def PatientRowClicked(self, row, col):
        '''User has clicked on a patient in the patient table so then
        update the study data and link to activity 1 to print the patient
        details to the console.'''
        self.current_patient_row = row
        try:
            Activity1.PrintDataToConsole(patient_details = self.pt_data[row])
        except:
            print("Activity 1 not yet completed")

        # update study and series tables
        # initially clearing them
        self.studiesTable.setRowCount(0)
        self.seriesTable.setRowCount(0)
        self.studythread = GetStudyInfoThread(self.pt_data[row]['id'])
        self.studythread.study_details_sig.connect(self.UpdateStudyTable)
        self.studythread.start()

    def OnStudiesSelectionChanged(self):
        """
        Triggered when the selection in seriesTable changes.
        Resets windowing and clears the image if the study list is repopulated.
        """
        self.ApplyWindowPreset("default")
        self.img_viewer_canvas.figure.clear()
        self.img_viewer_canvas.draw_idle()

    def StudyRowClicked(self, row, col):
        '''The user has clicked on a row of the study table
        so update the series table with data'''
        self.currentStudyRow = row
        self.seriesTable.setRowCount(0)
        self.seriesthread = GetSeriesInfoThread(self.study_list[row]['id'])
        self.seriesthread.series_details_sig.connect(self.UpdateSeriesTable)
        self.seriesthread.start()

    def SeriesRowClicked(self, row, col):
        '''The user has clicked on a row of the series table
        so get the image data and plot it.'''
        self.currentSeriesRow = row
        self.imagesthread = GetImageDataThread(self.series_list[row]['id'])
        self.imagesthread.image_data_sig.connect(self.SetImageData)
        self.imagesthread.start()

    def SetImageData(self, image_data):
        '''Image data has been sent back from the thread. Read
        this data and show it on the GUI'''
        self.image_data = image_data

        Activity3.GetSomeImageStats(image_data)

        self.current_instance_num = int(0.5*(max(image_data['instance_ids']) - min(image_data['instance_ids'])))
        self.PlotImage(self.current_instance_num)

    def PlotImage(self, instance_number):
        """Plot the image on the GUI for the specified instance number."""
        self.img_viewer_canvas.figure.clf()
        self._subplot = self.img_viewer_canvas.figure.subplots()
        img = self.image_data["images"][str(instance_number)]

        # Start with default values
        title_suffix = " (default)"
        display_img = img

        # Apply current window preset if not default
        if self.current_window_preset not in (None, 'default'):
            try:
                # Use preset if available, fallback to img if None
                display_img = ActivityB.window_image(img, self.current_window_preset) or img
                title_suffix = f" (window: {self.current_window_preset})"
            except Exception as e:
                print("Activity B isn't working yet!")
                print(repr(e))

        self._subplot.imshow(display_img, cmap='gray')
        self._subplot.set_title(f"Slice {instance_number}{title_suffix}")
        self.img_viewer_canvas.draw_idle()

    def ShowWindowMenu(self, pos):
        """
        Show a right-click context menu with windowing presets.

        Inputs:
            pos (QPoint): Position from the canvas where the menu should appear.
        Outputs:
            None: Displays the menu and triggers actions (side effect).
        """
        menu = QMenu(self)

        # Always include "Default"
        default_act = QAction("Default", menu)
        default_act.triggered.connect(lambda checked=False: self.ApplyWindowPreset("default"))
        menu.addAction(default_act)

        # Only add CT-specific presets if the current study is CT
        study = self.study_list[self.currentStudyRow]
        if study.get('StudyType') == "1.2.840.10008.5.1.4.1.1.2":
            ct_presets = [
                ("Lung (-600 / 1500)", "lung"),
                ("Soft Tissue (40 / 400)", "soft tissue"),
                ("Bone (300 / 1500)", "bone"),
            ]
            for text, key in ct_presets:
                act = QAction(text, menu)
                # Use a default arg to avoid late-binding of 'key'
                act.triggered.connect(lambda checked=False, k=key: self.ApplyWindowPreset(k))
                menu.addAction(act)

        # Show the menu at the cursor location
        global_pos = self.img_viewer_canvas.mapToGlobal(pos)
        menu.exec_(global_pos)

    def ApplyWindowPreset(self, preset):
        """
        Apply a window preset to the currently displayed slice and update the view.

        Inputs:
            preset (str): One of "default", "lung", "soft tissue", "bone".
        Outputs:
            None: Updates the canvas with the windowed image (side effect).
        """
        if self.image_data is None:
            return

        # Remember selection so it persists across scroll
        self.current_window_preset = preset
        # Re-plot the current slice with the selected window
        self.PlotImage(self.current_instance_num)

    def ImportBtnClicked(self):
        '''The user has clicked the import button so now get data
        on the patients in import directory.'''
        self.importPatientBtn.setText("Searching Import..")
        self.getptsthread = FindPatientsInImportThread(self.import_dir)
        self.getptsthread.pt_details_sig.connect(self.ImportPtsReturned)
        self.getptsthread.start()

    def ImportPtsReturned(self, pt_list):
        '''The list of patients has been returned so add this to the dialog
        so that the user can select which patient.'''
        self.importPatientBtn.setText("Import New Patient")
        dialog = PatientListDialog(pt_list, self.import_dir)
        dialog.exec_()
        dialog.show()

class BMIDialog(QDialog):
    '''This class defines the dialog that shows inputs
    for height and weight and a button for calculating BMI'''
    def __init__(self):
        '''This function is called when the dialog class
        is first initialised'''
        super(BMIDialog, self).__init__()
        uic.loadUi(r"./ui/bmi_dialog.ui", self)

        self.CalculateBtn.clicked.connect(self.CalculateBMI)

        self.show()

    def CalculateBMI(self):
        '''The calculate BMI button has been clicked. Call
        the function in Activity 7 Session 1 to get the value
        of the BMI'''
        height_input = self.HeightLineEdit.text()
        weight_input = self.WeightLineEdit.text()

        bmi = Activity7.CalculateBMI(
            height = height_input,
            weight = weight_input)
        
        self.BMIAnswerLabel.setText(str(bmi))

class PatientListDialog(QDialog):
    '''This is the class that defines the dialog that shows the
    user the list of patients in the import directory.'''
    def __init__(self, pt_list, import_dir):
        '''This function is called when the dialog class is first
        initialised'''
        super(PatientListDialog, self).__init__()
        uic.loadUi(r"./ui/pt_list_dialog.ui" ,self)
        self.import_dir = import_dir

        #clear and then populate the patient list
        self.ptListWidget.clear()
        for pt in pt_list:
            listItem = QListWidgetItem()
            listItem.setText(f"{pt['Name']} ({pt['MRN']})")
            self.ptListWidget.addItem(listItem)

        self.buttonBox.accepted.connect(self.ImportPatient)

        self.show()

    def ImportPatient(self):
        '''The user has selected a patient from the import directory so now
        we will call the thread that actually imports the data into the database'''
        selected_pt = self.ptListWidget.currentItem()
        if selected_pt is None:
            return
        
        progress = ProgressDialog()

        self.import_thread = ImportDicom.ImportPatientDataThread(
            self.import_dir, selected_pt.text().split("(")[-1].split(")")[0])
        self.import_thread.progress_sig.connect(progress.UpdateValue)
        self.import_thread.label_sig.connect(progress.UpdateLabel)
        self.import_thread.start()

        progress.exec_()
        progress.show()

class ProgressDialog(QDialog):
    '''This class is a generic progress bar dialog'''
    def __init__(self):
        super(ProgressDialog, self).__init__()
        uic.loadUi(r"./ui/progress_bar.ui" ,self)
        self.show()

    def UpdateValue(self, val):
        '''Update the value on the progress bar
        
        Args:
            val (int) = The new progress value
        returns nothing
        '''
        self.progressBarDialog.setValue(val)

    def UpdateLabel(self, new_string):
        '''Update the string shown on the label
        on the progress dialog.
        
        Args:
            new_string (str) = The string to show on the label
        Returns nothing    
        '''
        self.progressLabel.setText(new_string)

class FindPatientsInImportThread(QThread):
    '''Class to define the thread that identifies the patient
    data in the import directory. This is done as a thread to
    avoid locking the GUI.
    
    Args:
        import_dir (str) = The path of the import directory
    '''
    pt_details_sig = pyqtSignal(list)
    def __init__(self, import_dir):
        QThread.__init__(self)
        self.import_dir = import_dir

    def run(self):
        '''Code that is run when the thread is started'''
        pt_in_import = ImportDicom.GetPatientsInImport(
            import_dir = self.import_dir
        )
        self.pt_details_sig.emit(pt_in_import)

class GetStudyInfoThread(QThread):
    '''Class to define the thread that finds the study data
    associated with the clicked patient.
    
    Args:
        pt_dbid (int) = the database id of the patient
    '''
    study_details_sig = pyqtSignal(list)
    def __init__(self, pt_dbid):
        QThread.__init__(self)
        self.pt_dbid = pt_dbid

    def run(self):
        '''Code that is run when the thread is started'''
        db_handler = DatabaseHandler.PacsDatabaseClass()
        study_list = db_handler.GetStudyDetails(pt_id = self.pt_dbid)
        self.study_details_sig.emit(study_list)

class GetSeriesInfoThread(QThread):
    '''Class the define the thread that fiunds the series
    data associated with the clicked study.
    
    Args:
        study_dbid (int) = The database id of the study
    '''
    series_details_sig = pyqtSignal(list)
    def __init__(self, study_dbid):
        QThread.__init__(self)
        self.study_dbid = study_dbid

    def run(self):
        '''Code that is run when the thread is started'''
        db_handler = DatabaseHandler.PacsDatabaseClass()
        series_list = db_handler.GetSeriesDetails(study_id = self.study_dbid)
        self.series_details_sig.emit(series_list)

class GetImageDataThread(QThread):
    '''Class the define the thread that finds the image
    data associated with the clicked series.
    
    Args:
        series_dbid (int) = The database id of the series
    '''
    image_data_sig = pyqtSignal(dict)
    def __init__(self, series_dbid):
        QThread.__init__(self)
        self.series_dbid = series_dbid

    def run(self):
        '''Code that is run when the thread is started'''
        db_handler = DatabaseHandler.PacsDatabaseClass()
        image_data = db_handler.GetImageData(series_id = self.series_dbid)
        self.image_data_sig.emit(image_data)

class CalculateExternalVolumesThread(QThread):
    '''Class to define the thread that calls the function
    written as part of Activity 8 in session 1 to calculate
    the volume of the external.'''
    vol_calculated_sig = pyqtSignal(dict)
    def __init__(self, series_list):
        QThread.__init__(self)
        self.series_list = series_list
        self.PacsDatabaseClass = DatabaseHandler.PacsDatabaseClass()

    def run(self):
        '''Code to run when thread is started'''
        for i in range(len(self.series_list)):
            img_data = self.PacsDatabaseClass.GetImageData(
                series_id = self.series_list[i]["id"])
            
            try:
                vol = Activity8.EstimateExternalVolume(
                        px_arrs = img_data["images"],
                        slice_thickness = img_data["slice_thickness"],
                        row_px_spacing = img_data["row_pixel_spacing"],
                        col_px_spacing = img_data["col_pixel_spacing"],
                        instance_numbers = img_data["instance_ids"])
                
                self.vol_calculated_sig.emit({
                    "table_row":i,
                    "content":str(vol)}
                )
            except Exception as e:
                print(e)
                self.vol_calculated_sig.emit({
                    "table_row":i,
                    "content":"Error in function"}
                )


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