'''File for Activity 6 in Session 1. This file
has not be written according to the style guide given
in the resource pack. Your task is to adapt the file so
that it aligns with the style guide.'''

from os import *

class file_info():
    '''A simple class hold basic information on a file'''
    def __init__(self):
        self.filename = None
        self.filetype = None

    def GetExtension(self, folder_path, fname):
        '''Method that extracts the extension and sets the filename.'''
        if path.isfile(path.join(folder_path, fname)) is False:
            return False
        
        self.filetype = fname.split(".")[-1]
        self.filename = fname
        return True


def get_file_names(FolderPath):
    '''Gets the file names'''
    FNames = listdir(FolderPath)
    return FNames


def createList_ofFileObjects(folderPath, fnames):
    '''Function that creates a list of file class objects
    for each file in the folder'''
    file_objects = []
    for fname in fnames:
        fileObject = file_info()
        success = fileObject.GetExtension(
            folder_path = folderPath,
            fname = fname
        )
        
        if success is True:
            file_objects.append(fileObject)

    return file_objects


if __name__ == "__main__":
    folder_path = r"./training_activities_examples/Session1"
    fnames = get_file_names(folder_path)

    objs = createList_ofFileObjects(
        folderPath = folder_path,
        fnames = fnames
    )

    print(f"{len(objs)} objects returned")
    for obj in objs:
        print(f"Filename: {obj.filename}  |  Extension: {obj.filetype}")