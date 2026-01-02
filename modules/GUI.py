'''
Module to sort the graphical user interface (GUI) to use
in the MiniPACS.
'''

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

class MainGui(QMainWindow):
    '''This is the class that defines the main PACS graphical window.'''
    def __init__(self):
        '''This function is called when the MainGui class is first
        initialised'''
        super(MainGui, self).__init__()
        uic.loadUi(r"./ui/pacs_home.ui" ,self)# loads the UI from .ui file
        self.showMaximized()


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