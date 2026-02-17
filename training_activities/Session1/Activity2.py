'''File to be used for activity 2. This activity asks
you to write a function called CalculateAgeFromDob
that calulates the patient's age given the date of birth
given to the function as a string.'''

import datetime

def CalculateAgeFromDob(dob):
    Date_Of_Birth = datetime.datetime.strptime(dob, "%d/%m/%Y") # parse the date of birth from input string
    Today_Date = datetime.datetime.today()   #Gets today's time in epoch time

    Time_Delta = Today_Date - Date_Of_Birth # Check seconds between the dates

    Age_in_Years = int(Time_Delta.days / 365.245) # The years in Time_Delta
    return Age_in_Years

if __name__ == "__main__":
    date_of_birth = str(input("Enter DoB in dd/mm/yyyy"))

    example_age = CalculateAgeFromDob(date_of_birth)

    print(example_age)