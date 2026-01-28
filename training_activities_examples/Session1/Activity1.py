'''File to be used for activity 1. This activity
involves writing a function to print the patient
data to the console.'''

def PrintDataToConsole(patient_details):
    '''
    Functon to print out the patient details to the console.
    
    Args:
        patient_details (dict) = A dict of patient details with
            keys: id, MRN, Name, DateOfBirth and Address

    Returns nothing
    '''
    print("_")
    print("The following patient has been clicked on by the user:")
    print(f"Name: {patient_details['Name']} ({patient_details['MRN']})")
    print(f"Date of birth: {patient_details['DateOfBirth']}")
    print(f"Address: {patient_details['Address']}")