'''File to be used for activity 1. This activity
involves writing a function to print the patient
data to the console. Remember, call the function
PrintDataToConsole and get it to have a single argument
(input) called patient_details'''



if __name__ == "__main__":
    # This code will be run when you run this file directly
    # This can be very helpful for testing functions

    patient_dict = {
        "id":1,
        "MRN":"123456A",
        "Name":"Bob Duckworth",
        "DateOfBirth":"12/06/2001",
        "Address":"The Barn, Windy Street, Big Wood"
    }

    PrintDataToConsole(patient_details = patient_dict)
    
    #test


