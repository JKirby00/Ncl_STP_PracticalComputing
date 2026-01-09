"""Activity A - DICOM File Handling Functions

This activity asks you to implement functions related to DICOM file handling using the pydicom library

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
    pass

def anonymise_and_save_dicom(input_filepaths, output_folder): # Diff 2?
    """Function to anonymise a set of DICOM files and save them at a specified location.
    
    Inputs:
        input_filepaths (list): A list of file paths to the DICOM files to be anonymised
        output_folder (str): The folder where the anonymised DICOM files will be saved

    Outputs:
        None: The anonymised DICOM files are saved to the specified output folder
    """
    pass


def scrape_dicom_data(input_filepaths): # Diff 3?
    """Function to scrape demographics and pixel data from DICOM files.

    Inputs:
        input_filepaths (list): A list of file paths to the DICOM files to be scraped
    Outputs:
        scraped_data (list):  A list of dictionaries containing demographics and pixel data
    """
    pass


def search_dicom_hierarchy(filepaths): # Diff 4?
    """Function to search a folder containing DICOM files and identify the hierarchy of patient, study, and series.
    
    Inputs:
        filepaths (list): The list of DICOM file paths to be searched
    Outputs:
        hierarchy (dict): A nested dictionary representing the hierarchy of patients, studies, and series
    """
    pass


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