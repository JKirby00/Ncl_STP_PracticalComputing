"""Activity A - DICOM File Handling Functions

This activity asks you to implement functions related to DICOM file handling using the pydicom library

You need to complete tasks 3 and 5 to add DICOM reading functionality to the MiniPACs system.

Pre-requisites:
    Copy the pydicom example files to the import directory

1) Write a function that reads a DICOM file and prints the Patient Name and Patient ID. Diff 1.
2) Write a function that anonymises a DICOM file and saves the anonymised version to a specified output path. Diff 1.
3) Write a function that returns a list of full file paths for all DICOM files within a given folder. Diff 2.
4) Write a function that anonymises all DICOM files in a given folder and saves the anonymised copies to a specified 
    output folder. Diff 2.
5) Write a function that scans a folder of DICOM files and returns a list of dictionaries, each containing a patient's 
    MRN and Name, using the keys "MRN" and "Name". Diff 3.
6) Write a function that extracts demographic information and pixel data from a DICOM file and returns them in a 
    structured format. Diff 4.
7) Write a function that analyses all DICOM files in a folder and identifies the hierarchy of Patient → Study → Series, 
    returning a structured representation of this hierarchy. Diff 5.

Hints:
    pydicom.dcmread() is used to read a DICOM file.
    os.listdir() may be useful for getting a list of files in a folder.
    some_string.endswith(".dcm") may be useful for checking if a file is a DICOM file.
    os.path.join() is useful for creating file paths.
    os.basename() is useful for getting the filename from a file path.

"""
import pydicom as dcm
import os


def print_patient_info(dicom_filepath): #Diff 1
    ds = dcm.dcmread("import/pydicom_example_1.dcm")
    print( "Patient name is:", ds.PatientName, ", Patient ID is:", ds.PatientID)


def anonymise_dicom(dcm_file, output_file): # Diff 1
    ds = dcm.dcmread("import/CT_Anne_Dippet.dcm")
    ds.PatientName = "*********"
    ds.PatientBirthDate = "**********"
    ds.PatientID = "**********"
    ds.PatientSex = "**********"
    #print(ds)
    dcm.dcmwrite("annnonymise Anne", ds)
    print(ds)
    #output_file (str): The filename and path where the anonymised DICOM file will be saved


def get_dcm_filepaths(folder_path): #Diff 3
    list_filepaths = []
    filenames = os.listdir(folder_path)
    for file in filenames:
        if file.endswith(".dcm"):
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
    pass


def get_patient_mrns(file_paths): #Diff 3
    """5) Function to create a list of patient MRNs from DICOM files in a folder. Each list entry should be dictionary
    containing the keys "MRN" and "Name".

    Once complete, check the MiniPACS import functionality to check this is working.

    Inputs:
        folder_path (str): The folder containing DICOM files
    Outputs:
        pt_dicts (list): A list of dictionaries with patient MRNs and Names [{"MRN":..., "Name":...}]
    """
    mrns_found = []
    pt_dicts = []

    # Remove this following line when completing this task
    pt_dicts.append({"MRN":"Not Implemented", "Name":"Complete Task A3 and A5"})

    return pt_dicts


def scrape_dicom_data(input_filepaths): # Diff 4
    """6) Function to scrape demographics and pixel data from DICOM files.

    Inputs:
        input_filepaths (list): A list of file paths to the DICOM files to be scraped
    Outputs:
        scraped_data (list):  A list of dictionaries containing demographics and pixel data
    """
    scraped_data = []

    return scraped_data


def create_dicom_hierarchy(filepaths): # Diff 5
    """7) Function to search a folder containing DICOM files and identify the hierarchy of patient, study, and series.
    
    Inputs:
        filepaths (list): The list of DICOM file paths to be searched
    Outputs:
        hierarchy (dict): A nested dictionary representing the hierarchy of patient, study, and series. The structure is as follows:
            {
                patient_id: {
                    "PatientName": ...,
                    "PatientBirthDate": ...,
                    "PatientSex": ...,
                    "Study": {
                        study_uid: {
                            "StudyDate": ...,
                            "Series": {
                                series_uid: {
                                    "SeriesDate": ...,
                                    "PixelSpacing": ...,
                                    "SliceThickness": ...,
                                    "ImageData": {
                                        instance_number: pixel_array,
                                        ...
                                    }
                                },
                                ...
    """
    hierarchy = {}

    return hierarchy


if __name__ == "__main__":
    # Test each function
    dicom_file = r"./import/pydicom_example_1.dcm"    # r"path/to/dicom/file.dcm"
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
    hierarchy = create_dicom_hierarchy(dicom_filepaths)
    print("Task 7 - DICOM Hierarchy:")
    print(hierarchy)
    

