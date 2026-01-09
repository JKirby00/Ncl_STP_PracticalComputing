"""Activity A - DICOM File Handling Functions

This activity asks you to implement three functions related to DICOM file handling using the pydicom library

TODO Add easier tasks 

1)  Write a function that creates a list of file paths from a folder containing DICOM files.

2)  Write a function that anonymises a set of DICOM files and saves them at a specified location.

3)  Write a function that scrapes some data (demographics + pixel data) from some DICOM files and returns it 
    (so that a pre-written function can save this data to a database).

4)  Write a function that searches a folder containing DICOM files and identifies the hierarchy of the patient, 
    study and series for each. These are returned as a dictionary. 

Hints:
    os.listdir() may be useful for getting a list of files in a folder.
    os.path.join() is useful for creating file paths.
    os.basename() is useful for getting the filename from a file path.
    pydicom.dcmread() is used to read a DICOM file.

"""
import pydicom
import os


def create_list_filepaths(folder_path): #Diff 3?
    """Function to create a list of file paths from a folder containing DICOM files.

    Inputs:
        folder_path (str): The folder containing DICOM files
    Outputs:
        list_filepaths (list): A list of file paths to the DICOM files
    """    
    list_filepaths = []
    filenames = os.listdir(folder_path)
    for file in filenames:
        if file.endswith(".dcm"):
            filepath = os.path.join(folder_path, file)
            list_filepaths.append(filepath)
    return list_filepaths


def anonymise_and_save_dicom(input_filepaths, output_folder): # Diff 2?
    """Function to anonymise a set of DICOM files and save them at a specified location.
    
    Inputs:
        input_filepaths (list): A list of file paths to the DICOM files to be anonymised
        output_folder (str): The folder where the anonymised DICOM files will be saved

    Outputs:
        None: The anonymised DICOM files are saved to the specified output folder
    """
    for filepath in input_filepaths:
        ds = pydicom.dcmread(filepath)
        
        # Anonymise patient information
        ds.PatientName = "Anonymised"
        ds.PatientID = "Anonymised"
        ds.PatientBirthDate = ""
        ds.PatientSex = ""
        
        # Create output filepath + filename
        filename = os.path.basename(filepath)
        output_filepath = os.path.join(output_folder, filename)
        
        # Save anonymised DICOM file
        ds.save_as(output_filepath)


def scrape_dicom_data(input_filepaths): # Diff 3?
    """Function to scrape demographics and pixel data from DICOM files.

    Inputs:
        input_filepaths (list): A list of file paths to the DICOM files to be scraped
    Outputs:
        scraped_data (list):  A list of dictionaries containing demographics and pixel data
    """
    scraped_data = []
    for filepath in input_filepaths:
        ds = pydicom.dcmread(filepath)
        
        # Extract demographics (this is just an example of the types of information to change)
        demographics = {
            "PatientName": ds.PatientName,
            "PatientID": ds.PatientID,
            "PatientBirthDate": ds.PatientBirthDate,
            "PatientSex": ds.PatientSex,
        }
        
        # Extract pixel data
        pixel_data = ds.pixel_array if "PixelData" in ds else None # account for files without pixel data
        
        scraped_data.append({
            "demographics": demographics,
            "pixel_data": pixel_data
        })
    return scraped_data


def search_dicom_hierarchy(filepaths): # Diff 4?
    """Function to search a folder containing DICOM files and identify the hierarchy of patient, study, and series.
    
    Inputs:
        filepaths (list): The list of DICOM file paths to be searched
    Outputs:
        hierarchy (dict): A nested dictionary representing the hierarchy of patients, studies, and series
    """
    hierarchy = {}
    for filepath in filepaths:
        ds = pydicom.dcmread(filepath)
        
        patient_id = ds.PatientID                   #patient_id = ds.get("PatientID", "Unknown") TODO would this be better?
        study_instance_uid = ds.StudyInstanceUID    #study_instance_uid = ds.get("StudyInstanceUID", "Unknown")
        series_instance_uid = ds.SeriesInstanceUID  #series_instance_uid = ds.get("SeriesInstanceUID", "Unknown")

        if patient_id not in hierarchy:
            hierarchy[patient_id] = {}
        if study_instance_uid not in hierarchy[patient_id]:
            hierarchy[patient_id][study_instance_uid] = {}
        if series_instance_uid not in hierarchy[patient_id][study_instance_uid]:
            hierarchy[patient_id][study_instance_uid][series_instance_uid] = []

        hierarchy[patient_id][study_instance_uid][series_instance_uid].append(filepath)
    return hierarchy


if __name__ == "__main__":
    # Test each function
    filepaths = create_list_filepaths("./import/")
    print("Original Filepaths", filepaths)
    anon_filepath = "./anonymised/"
    os.makedirs(anon_filepath, exist_ok=True)
    anonymise_and_save_dicom(filepaths, anon_filepath)

    anon_paths = create_list_filepaths("./anonymised/") # Checking the anonymised file paths
    print("Anonymised Filepaths", anon_paths)

    scraped_data = scrape_dicom_data(filepaths)
    print("Scraped Data", scraped_data)

    hierarchy = search_dicom_hierarchy(filepaths)
    print("Hierarchy", hierarchy)