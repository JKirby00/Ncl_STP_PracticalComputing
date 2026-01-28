'''File for Activity 6 in Session 1. This file
has not be written according to the style guide given
in the resource pack. Your task is to adapt the file so
that it aligns with the style guide.'''

from os import path, listdir

class FileInfo():
    '''A simple class hold basic information on a file'''
    def __init__(self):
        self.filename = None
        self.filetype = None

    def GetExtension(self, folder_path, fname):
        '''Method that extracts the extension and sets the filename.
        
        Args:
            folder_path (str) = The path to the folder files are in
            fname (str) = The name of the file

        Returns True/False depending on whether fname is a file
        '''
        if path.isfile(path.join(folder_path, fname)) is False:
            return False
        
        self.filetype = fname.split(".")[-1]
        self.filename = fname
        return True


def GetFileNames(folder_path):
    '''Function that gets the file names of files within
    a given folder path

    Args:
        folder_path (str) = The path tot he folder to search
    
    returns list of filenames
    '''
    f_names = listdir(folder_path)
    return f_names


def CreateListOfFileObjects(folder_path, fnames):
    '''Function that creates a list of file class objects
    for each file in the folder
    
    Args:
        folder_path (str) = The path to the folder containing files
        fnames (list) = A list of filenames

    returns a list of FileInfo class objects for each file
        in the folder.
    '''
    file_objects = []
    for fname in fnames:
        file_object = FileInfo()
        success = file_object.GetExtension(
            folder_path = folder_path,
            fname = fname
        )

        if success is True:
            file_objects.append(file_object)

    return file_objects


if __name__ == "__main__":
    folder_path = r"./training_activities_examples/Session1"
    fnames = GetFileNames(folder_path)

    objs = CreateListOfFileObjects(
        folder_path = folder_path,
        fnames = fnames
    )

    print(f"{len(objs)} objects returned")
    for obj in objs:
        print(f"Filename: {obj.filename}  |  Extension: {obj.filetype}")