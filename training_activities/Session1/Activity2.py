'''File to be used for activity 2. This activity asks
you to write a function called CalculateAgeFromDob
that calulates the patient's age given the date of birth
given to the function as a string.'''


    


def CalculateAgeFromDob(dob):
    from datetime import date, datetime
    today = datetime.today()
    birthdate = datetime.strptime(dob, "%d/%m/%Y")
    age = today.year - birthdate.year
    return age


