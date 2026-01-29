'''File to be used for activity 2. This activity asks
you to write a function called CalculateAgeFromDob
that calulates the patient's age given the date of birth
given to the function as a string.'''

from datetime import date, datetime

def CalculateAgeFromDob(dob):
    '''Function to calculate the age from the
    given date of birth
    
    '''
    # convert the date of birth to a datetime
    dob = datetime.strptime(dob, "%d/%m/%Y")
    
    today = date.today()# get todays date

    # identify if today is before the birthday this year
    before_birthday = ((today.month, today.day) < (dob.month, dob.day))

    # find years since birth year and then subtract one if not yet had birthday 
    age = today.year - dob.year - before_birthday
    return age