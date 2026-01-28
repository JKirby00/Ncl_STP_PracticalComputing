import unittest

def CalculateBMI(height, weight):
    """Function to calculate BMI.
    
    Args:
        height (str) = The input height in metres
        width (str) = The input weight in kg

    Returns: The calculated BMI as a float
    """
    # Note: Additional validation logic could be added to this
    # to check for whether height or weight are sensible values

    # first check that the height and weight can be converted to a float 
    try:
        height = float(height)
        weight = float(weight)
    except:
        return "Height or weight given is not a number"
    
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

    def test_result_is_float(self):
        self.assertIsInstance(CalculateBMI(1.50, 45), float)

    def test_input_that_is_not_numeric_returns_a_message(self):
        self.assertEqual(CalculateBMI("not" , "numeric"), "Height or weight given is not a number")

    def test_two_inputs_must_be_provided(self):
        with self.assertRaises(TypeError):
            CalculateBMI()

if __name__ == "__main__":
    unittest.main()