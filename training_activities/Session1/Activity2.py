'''File to be used for activity 2. This activity asks
you to write a function called CalculateAgeFromDob
that calulates the patient's age given the date of birth
given to the function as a string.'''

from datetime import datetime

def CalculateAgeFromDob(dob):
    # convert dob string to datetime object
    date_of_birth = datetime.strptime(dob.split()[0], "%d/%m/%Y").date()
    today = datetime.today().date()

    # calculate age from dob, -1 if today is before birthday in year
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    return(age)

if __name__ == "__main__":
    # This code will be run when you run this file directly
    # This can be very helpful for testing functions

    birthday = "19/06/1993"

    print(CalculateAgeFromDob(dob = birthday))

