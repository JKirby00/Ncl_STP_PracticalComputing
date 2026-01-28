import unittest

def CalculateBMI(height=None, weight=None):
    """Function to calculate BMI.
    
    Args:
        height (str) = The input height in metres
        width (str) = The input weight in kg

    Returns: The calculated BMI as a float
    """
    if height is None or weight is None:
        return "Both weight and height need to be entered"

    # first check that the height and weight can be converted to a float 
    try:
        height = float(height)
        weight = float(weight)
    except:
        return "Height or weight given is not a number"
    
    # then check that they are within range (as per NHS BMI calculator)
    if height < 1.397 or height > 2.438:
        return "Height must be between 1.397 m and 2.438 m"

    if weight < 25.4 or weight > 317.5:
        return  "Weight must be between 25.4 kg and 317.5 kg"

    # calculate BMI
    bmi = weight / (height**2)

    return bmi

class TestCalculateBMI(unittest.TestCase):

    def test_calculation_is_correct(self):
        self.assertEqual(CalculateBMI(1.50, 45), 20)
        self.assertEqual(CalculateBMI(1.50, 90), 40)
        self.assertEqual(CalculateBMI(1.50, 50), 22.22222222222222)

    def test_float_input_is_accepted(self):
        self.assertEqual(CalculateBMI(1.50, 45.0), 20)

    def test_integer_input_is_accepted(self):
        self.assertEqual(CalculateBMI(2, 80), 20)

    def test_numeric_string_input_is_accepted(self):
        self.assertEqual(CalculateBMI("1.5", "45"), 20)

    def test_result_is_float(self):
        self.assertIsInstance(CalculateBMI(1.50, 45), float)

    def test_input_that_is_not_numeric_returns_a_message(self):
        self.assertEqual(CalculateBMI("not" , "numeric"), "Height or weight given is not a number")
        self.assertEqual(CalculateBMI("" , ""), "Height or weight given is not a number")

    # What are sensible ranges for height and weight? This is not a software development question!
    # Ideally you would identify a reputable expert source. We will use the same limits as the 
    # official NHS BMI calculator 
    # https://www.nhs.uk/health-assessment-tools/calculate-your-body-mass-index/calculate-bmi-for-adults
    def test_height_must_be_within_the_accepted_range(self):
        self.assertEqual(CalculateBMI(1.35, 45), "Height must be between 1.397 m and 2.438 m")
        self.assertEqual(CalculateBMI(2.55, 45), "Height must be between 1.397 m and 2.438 m")

    def test_weight_must_be_within_the_accepted_range(self):
        self.assertEqual(CalculateBMI(1.75, 25), "Weight must be between 25.4 kg and 317.5 kg")
        self.assertEqual(CalculateBMI(1.75, 320), "Weight must be between 25.4 kg and 317.5 kg")

    # we may decide that the function should NEVER raise an exception, instead only returning
    # a message. In that case, we will udpate the test to make a different assertion.
    # Note that this isn't always best practice! In many cases raising errors is the correct choice.
    def test_two_inputs_must_be_provided(self):
        self.assertEqual(CalculateBMI(), "Both weight and height need to be entered")
        self.assertEqual(CalculateBMI(None, None), "Both weight and height need to be entered")

if __name__ == "__main__":
    unittest.main()