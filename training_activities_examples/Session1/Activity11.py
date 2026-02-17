'''File for Activity 11 in Session 1. This activity gets your
to write a simple logger that logs the username of the logged in
person to a file and the MRN of the patient that has been clicked on.
You will find the bare bones of the function already there.'''

import logging
from os import getlogin

def CustomLogger(logger_path, logger_name, level = logging.DEBUG, format_string = None,
                    logger_path_is_full_path = False):
    '''
    Method to return a custom logger with the given name and debug level.

    Inputs:
        logger_path = path to where log file will be saved
        logger_name = name of the logger
        level = level of logging. The default is debug logging

    Returns:
        logger = the logger object
    '''
    #get logger of the specified name and set the level
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    #create the format string and then set it on the logger
    if format_string is None:
        format_string = ("%(asctime)s — %(levelname)s || %(message)s")
    log_format = logging.Formatter(format_string)

    #create a file handler that will append to the log
    if logger_path_is_full_path is False:
        file_handler = logging.FileHandler(logger_path + "\\" + logger_name, mode='a')
    else:
        file_handler = logging.FileHandler(logger_path, mode='a')

    #set the formatter and the handler
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    return logger


def LogAccess(patient_mrn):
    '''Function to log the access to a patient. You
    need to add the logic to do the logging. Keep the function
    name and arguments the same.

    Args:
        patient_mrn (str) = The MRN of the patient

    returns nothing
    '''

    mylogger = CustomLogger("./export", "access_log")
    mylogger.info(f"Patient {patient_mrn} accessed by {getlogin()}")

    for handler in mylogger.handlers:
        mylogger.removeHandler(handler)
        handler.close()


if __name__ == "__main__":
    LogAccess(patient_mrn = "test")