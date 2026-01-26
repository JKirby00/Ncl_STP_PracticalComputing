"""Activity A - DICOM File Handling Functions

This activity asks you to implement functions related to DICOM file handling using the pydicom library

1) Write a function that will print Patient Name and Patient ID from a DICOM file. Diff 1.
2) Write a function that will anonymise a DICOM file and save it to a specified file. Diff 1.
3) *Write a function that creates a list of file paths from a folder containing DICOM files. Diff 3.
4) Write a function that anonymises a set of DICOM files and saves them to a specified location. Diff 2.
5) *Write a function that creates a list of patient MRNs from DICOM files in a folder. Each list entry should be dictionary
    containing the keys "MRN" and "Name". Diff 3.
6) Write a function that scrapes demographics and pixel data from DICOM files. Diff 4.
7) Write a function that searches a folder containing DICOM files and identifies the hierarchy of patient, study, and series. Diff 5.

Hints:
    os.listdir() may be useful for getting a list of files in a folder.
    some_string.endswith(".dcm") may be useful for checking if a file is a DICOM file.
    os.path.join() is useful for creating file paths.
    os.basename() is useful for getting the filename from a file path.
    pydicom.dcmread() is used to read a DICOM file.

"""
import pydicom
import os


def print_patient_info(dicom_filepath): #Diff 1
    """1) Function to print Patient Name and Patient ID from a DICOM file.

    Inputs:
        dicom_filepath (str): The file path to the DICOM file
    Outputs:
        None: The function prints the Patient Name and Patient ID
    """
    ds = pydicom.dcmread(dicom_filepath)
    print(f"Patient Name: {ds.PatientName}")
    print(f"Patient ID: {ds.PatientID}")


def anonymise_dicom(dcm_file, output_file): # Diff 1
    """2) Function to anonymise a DICOM file and save it as a new DICOM file.
    
    Inputs:
        dcm_file (list): A file path to a DICOM file to be anonymised
        output_file (str): The filename and path where the anonymised DICOM file will be saved

    Outputs:
        None: The anonymised DICOM files are saved to the specified output folder
    """
    ds = pydicom.dcmread(dcm_file)
    
    # Anonymise patient information
    ds.PatientName = "Anonymised"
    ds.PatientID = "Anonymised"
    ds.PatientBirthDate = ""
    ds.PatientSex = ""
    
    # Save anonymised DICOM file
    ds.save_as(output_file)


def get_dcm_filepaths(folder_path): #Diff 3
    """3) Function to create a list of file paths from a folder containing DICOM files.

    Inputs:
        folder_path (str): The folder to check for DICOM files
    Outputs:
        list_filepaths (list): A list of file paths to the DICOM files
    """
    list_filepaths = []
    filenames = os.listdir(folder_path)
    
    # Loop through files in the folder and add DICOM file paths to the list
    for file in filenames:
        # Check if the file is a DICOM file (assuming .dcm extension)
        if file.endswith(".dcm"):
            # Create full file path
            filepath = os.path.join(folder_path, file)
            list_filepaths.append(filepath)
    return list_filepaths


def anonymise_dicom_folder(input_filepaths, output_folder): # Diff 2
    """4) Function to anonymise a set of DICOM files and save them at a specified location.
    
    Inputs:
        input_filepaths (list): A list of file paths to the DICOM files to be anonymised
        output_folder (str): The folder where the anonymised DICOM files will be saved

    Outputs:
        None: The anonymised DICOM files are saved to the specified output folder
    """
    for filepath in input_filepaths:        
        # Create output filepath + filename
        filename = os.path.basename(filepath)
        output_filepath = os.path.join(output_folder, filename)
        anonymise_dicom(filepath, output_filepath)


def get_patient_mrns(file_paths): #Diff 3
    """5) Function to create a list of patient MRNs from DICOM files in a folder. Each list entry should be dictionary
    containing the keys "MRN" and "Name".

    Inputs:
        folder_path (str): The folder containing DICOM files
    Outputs:
        pt_dicts (list): A list of dictionaries with patient MRNs and Names [{"MRN":..., "Name":...}]
    """
    mrns_found = []
    pt_dicts = []

    for fpath in file_paths:
        ds = pydicom.dcmread(fpath)
        if ds.PatientID in mrns_found:
            # ignore files with same MRN as one we've already found
            continue
        mrns_found.append(ds.PatientID)
        pt_dicts.append({"MRN":ds.PatientID, "Name":ds.PatientName})
    return pt_dicts


def scrape_dicom_data(input_filepaths): # Diff 4
    """6) Function to scrape demographics and pixel data from DICOM files.

    Inputs:
        input_filepaths (list): A list of file paths to the DICOM files to be scraped
    Outputs:
        scraped_data (list):  A list of dictionaries containing demographics and pixel data
    """
    scraped_data = []
    for filepath in input_filepaths:
        ds = pydicom.dcmread(filepath)
        
        # Extract demographics (this is just an example of the types of information to scrape)
        demographics = {
            "PatientName": ds.PatientName,
            "PatientID": ds.PatientID,
            "PatientBirthDate": ds.PatientBirthDate,
            "PatientSex": ds.PatientSex,
        }
        
        # Extract pixel data
        pixel_data = ds.pixel_array if "PixelData" in ds else None # account for files without pixel data

        # Append to scraped data list
        scraped_data.append({
            "demographics": demographics,
            "pixel_data": pixel_data
        })
    return scraped_data


def search_dicom_hierarchy(filepaths): # Diff 5
    """7) Function to search a folder containing DICOM files and identify the hierarchy of patient, study, and series.
    
    Inputs:
        filepaths (list): The list of DICOM file paths to be searched
    Outputs:
        hierarchy (dict): A nested dictionary representing the hierarchy of patients, studies, and series
    """
    hierarchy = {}
    for filepath in filepaths:
        ds = pydicom.dcmread(filepath)

        # Extract relevant identifiers
        patient_id = ds.PatientID                   #patient_id = ds.get("PatientID", "Unknown") # Alternatively we can check for 
        study_instance_uid = ds.StudyInstanceUID    #study_instance_uid = ds.get("StudyInstanceUID", "Unknown")
        series_instance_uid = ds.SeriesInstanceUID  #series_instance_uid = ds.get("SeriesInstanceUID", "Unknown")

        # Create nested dictionary structure based on whether the keys already exist
        if patient_id not in hierarchy:
            hierarchy[patient_id] = {}
        if study_instance_uid not in hierarchy[patient_id]:
            hierarchy[patient_id][study_instance_uid] = {}
        if series_instance_uid not in hierarchy[patient_id][study_instance_uid]:
            hierarchy[patient_id][study_instance_uid][series_instance_uid] = []

        # Append the filepath to the appropriate series
        hierarchy[patient_id][study_instance_uid][series_instance_uid].append(filepath)
    return hierarchy


if __name__ == "__main__":
    # Test each function
    dicom_file = r"./import/example.dcm"    # r"path/to/dicom/file.dcm"
    folder_path = r"./import/"              # r"path/to/dicom/folder"
    output_folder = r"./export/"            # r"path/to/output/folder"

    # Test function 1 and 2
    print("Task 1 - Patient Info:")
    print_patient_info(dicom_file)
    print("Task 2 - Anonymising DICOM file...")
    anonymise_dicom(dicom_file, os.path.join(output_folder, "anonymised_file.dcm"))

    # Test function 3
    print("Task 3 - List of DICOM file paths:")
    dicom_filepaths = get_dcm_filepaths(folder_path)
    print(dicom_filepaths)
    
    # Test function 4
    anonymise_dicom_folder(dicom_filepaths, output_folder)
    print("Task 4 - Anonymised DICOM files saved.")
    
    # Test function 5
    patient_mrns = get_patient_mrns(dicom_filepaths)
    print("Task 5 - Patient MRNs:")
    print(patient_mrns)

    # Test function 6
    scraped_data = scrape_dicom_data(dicom_filepaths)
    print("Task 6 - Scraped DICOM Data:")
    print(scraped_data)

    # Test function 7
    hierarchy = search_dicom_hierarchy(dicom_filepaths)
    print("Task 7 - DICOM Hierarchy:")
    print(hierarchy)
    

