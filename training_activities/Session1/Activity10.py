'''File for Activity 10 in Session 1. This activity is asking
you to create a PDF from some input data.'''


if __name__ == "__main__":
    # Below is the data that you need to transform into a nicely
    # readable PDF. It is intended to be some pretend QC data

    date = "01/05/2023"
    equipment_details = {
        "name":"Varian TrueBeam",
        "serial":12345,
        "energies":["6MV", "10MV", "10FFF"]
    }

    qc_tests = [
        {"test_number":1,
         "type":"mechanical",
         "title":"Laser Checks"},
         {"test_number":2,
          "type":"photon",
          "title":"6MV Output"},
          {"test_number":3,
          "type":"photon",
          "title":"10MV Output"},
          {"test_number":4,
          "type":"photon",
          "title":"10FFF Output"},
          {"test_number":5,
          "type":"imaging",
          "title":"CBCT SNR"}
        ]
    
    # the key in the results correspond to the test number
    results = {
        "1":{"result":"PASS"},
        "2":{"value":1.0, "result":"PASS"},
        "3":{"value":1.4, "result":"REMEDIAL"},
        "4":{"value":5.0, "result":"SUSPEND"},
        "5":{"value":1.05, "result":"PASS"}
    }

    qc_operator = "Joe Bloggs"