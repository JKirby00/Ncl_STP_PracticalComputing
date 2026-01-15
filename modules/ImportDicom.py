'''This module contains a collection of functions for 
importing data from DICOM files into the database'''
import pydicom
import sys
from os import listdir
from os.path import join
import pathlib
from PyQt5.QtCore import QThread, pyqtSignal
import DatabaseHandler
from datetime import datetime

sys.path.append(join(pathlib.Path(__file__).parent.parent.absolute(), "training_activities_examples"))
from Session2 import ActivityA

def GetPatientsInImport(import_dir):
    '''Function to obtain a list of patients that currently
    have data in the import directory. This function only searches
    the import directory and does not recursively search the child
    folders
    
    Args:
        import_dir (str) = the import directory path

    Returns:
        List of dictionaries where each dict has keys: "MRN" and "Name"    
    '''
    # loop through each file in the import directory
    fpaths = ActivityA.create_list_filepaths(import_dir)
    # return a list of dictionaries with patient MRNs and Names
    pt_dicts = ActivityA.list_patient_mrns(fpaths)
    
    if pt_dicts is None:
        pt_dicts = []

    return pt_dicts

class ImportPatientDataThread(QThread):
    '''Class to define the thread that imports all of the image
    data found in the import directory for that patient
    
    Args:
        import_dir (str) = The path of the import directory
        mrn (str) = The patient MRN
    '''
    progress_sig = pyqtSignal(int)
    label_sig = pyqtSignal(str)
    def __init__(self, import_dir, mrn):
        QThread.__init__(self)
        self.import_dir = import_dir
        self.mrn = mrn
        self.data = {}# to store the data before saving to database
        self.fnames_scraped = []

    def run(self):
        '''Code to run when the trhead is started'''
        self.progress_sig.emit(0)
        self.label_sig.emit(f"Starting import for MRN: {self.mrn}")

        all_fnames = listdir(self.import_dir)

        # loop through files in import directory
        for i in range(len(all_fnames)):
            if ".dcm" not in all_fnames[i].lower():
                # if not a dicom file just mark file as processed
                # and then move on
                progress = int(((i+1)*100)/len(all_fnames))
                self.progress_sig.emit(progress)
                self.label_sig.emit(f"Processed {i+1}/{len(all_fnames)} files")
                continue

            f = pydicom.dcmread(join(self.import_dir, all_fnames[i]))
            if f.PatientID == self.mrn:
                study_uid = f.StudyInstanceUID
                if study_uid not in self.data:
                    self.data[study_uid] = {
                        "StudyDate": (f.StudyDate if getattr(f, "StudyDate", None) else "19000101"),
                        "Type":f.SOPClassUID,
                        "MRN":self.mrn,
                        "Name":f.PatientName,
                        "DOB":datetime.strptime(f.PatientBirthDate, "%Y%m%d").strftime("%d/%m/%Y"),
                        "Series":{}
                    }
                
                series_uid = f.SeriesInstanceUID
                if series_uid not in self.data[study_uid]["Series"]:
                    self.data[study_uid]["Series"][series_uid] = {
                        "SeriesNumber":f.SeriesNumber,
                        "Description":f.ProcedureCodeSequence[0].CodeMeaning,
                        "PixelSpacing":f.PixelSpacing,
                        "ImageData":{}
                    }

                # Convert pixel data to HU for CT, leave MR unchanged
                if hasattr(f, "Modality") and f.Modality.upper() == "CT":
                    slope = getattr(f, "RescaleSlope", 1)
                    intercept = getattr(f, "RescaleIntercept", 0)
                    img_array = (f.pixel_array * slope) + intercept
                else:
                    img_array = f.pixel_array  # MR or other modalities: keep raw values

                self.data[study_uid]["Series"][series_uid]["ImageData"][f.InstanceNumber] = img_array

            progress = int(((i+1)*100)/len(all_fnames))
            self.progress_sig.emit(progress)
            self.label_sig.emit(f"Processed {i+1}/{len(all_fnames)} files")

        self.label_sig.emit(f"Now saving data to database")
        self.progress_sig.emit(95)
        db_handler = DatabaseHandler.PacsDatabaseClass()
        db_handler.InsertNewPatientData(data = self.data)

        self.label_sig.emit(f"Import Complete")
        self.progress_sig.emit(100)

if __name__ == "__main__":
    import pathlib
    p = join(pathlib.Path(__file__).parent.parent.absolute(), "import", "CT1.3.12.2.1107.5.2.51.182900.30000025112810444972500000006.dcm")
    f = pydicom.dcmread(p)