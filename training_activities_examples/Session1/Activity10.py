'''File for Activity 10 in Session 1. This activity is asking
you to create a PDF from some input data.'''

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Spacer
from reportlab.platypus.tables import Table, TableStyle
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

def CreatePDF(date, operator, equipment_details, qc_tests, results):
    '''This function creates a simple PDF of the QC test result data
    provided to it.

    Args:
        date (str) = The date of the QC tests
        operator (str) = The name of the operator
        equipment_details (dict) = Dict outling basic machine parameters
            with keys: name, serial, energies
        qc_tests (dict) = Dict defining the tests to be performed. The
            keys are test_number, type, title
        results (dict) = The results of each test where the keys of the
            dict relate to the test numbers. Each result is a dict
            with an optional key called value and a mandatory key
            called result.

    Returns:
        Nothing
    '''
    # create the simple template to use at A4 size and state location/filename
    doc= SimpleDocTemplate(f"./export/qc_results.pdf", pagesize = A4)
    styles = getSampleStyleSheet()

    # create an empty list to add document elements to
    elements = []

    # add some basic text info
    elements.append(Paragraph(("QC Results"), styles["Title"]))
    elements.append(Paragraph((f"Date of tests: {date}"), styles["Normal"]))
    elements.append(Paragraph((f"QC operator: {operator}"), styles["Normal"]))
    elements.append(Spacer(1, 1*cm))

    # convert the energy list into a human readable string
    energy_list = ""
    for energy in equipment_details['energies']:
        energy_list = energy_list + "," + energy

    # create the data for the table containing machine info
    data= [
        ['Equipment Name', 'Serial No.', 'Energies'],
        [equipment_details['name'], equipment_details['serial'],
            energy_list]
    ]

    # add that machine data to the table and add some styling
    equip_table = Table(data)
    equip_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ('INNERGRID',(0,0), (-1,-1), 0.25, colors.black),
        ('BACKGROUND',(0,0), (-1,0), colors.grey)
    ]))

    elements.append(equip_table)
    elements.append(Spacer(1, 1*cm))

    # now do similarly for the test data and associated results
    test_data = [["No.", "Test Type", "Test Title", "Value", "Result"]]
    for qc_test in qc_tests:
        row = [qc_test['test_number'],
            qc_test['type'],
            qc_test['title']
            ]

        result = results[str(qc_test['test_number'])]
        if 'value' in result:
            row.append(result['value'])
        else:
            # if value is missing we want to say not applicable
            row.append("N/A")

        row.append(result['result'])

        test_data.append(row)

    results_table = Table(test_data)

    results_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ('INNERGRID',(0,0), (-1,-1), 0.25, colors.black),
        ('BACKGROUND',(0,0), (-1,0), colors.grey)
    ]))

    elements.append(results_table)

    # now build all the elements
    doc.build(elements)



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


    CreatePDF(
        date = date,
        operator = qc_operator,
        equipment_details = equipment_details,
        qc_tests = qc_tests,
        results = results
    )