'''File for Session 1 Activity 9. In this task,
you are asked to write data to an excel spreadsheet.'''
import openpyxl

def WriteDataToExcel(pt_data, study_data, series_data):
    '''
    Function for you to edit to save the input data to and
    excel file in whatever format you think is best. You should
    save the file in the export directory of this repository.
    This function is called when the export button on the GUI
    is clicked.

    This example could probably be further brken down into units,
    and have additional formatting or linking of the data added.

    Args:
        pt_data (dict) = Dict of patient details of selected patient
        study_data (list) = List of dicts containing study details
            for selected patient
        series_data (list) = List of dicts containing series details
            for the selected patient and study

    returns nothing
    '''
    # create work book and set sheet title
    workbook  = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Exported Data"

    # just return if no patient is selected
    if pt_data is None:
        return
    
    # add the patient details
    pt_titles = [key for key in pt_data]
    pt_values = [pt_data[key] for key in pt_data]
    worksheet.append(pt_titles)
    worksheet.append(pt_values)

    # add he study information
    worksheet["A3"] = "Study Data:"

    if study_data is None:
        worksheet["A4"] = "No study is selected"
    else:
        if len(study_data) == 0:
            worksheet["A4"] = "No Studies found"
        else:
            study_titles = [key for key in study_data[0]]
            worksheet.append(study_titles)

            for study in study_data:
                study_values = [study[key] for key in study]
                worksheet.append(study_values)

        # add the series data (this will be for all
        # studies)
        worksheet.append([""])
        worksheet.append(["Series Data:"])

        if series_data is None:
            worksheet.append(["No study is selected"])
        else:
            if len(series_data) == 0:
                worksheet.append(["No series data found"])
            else:
                series_titles = [key for key in series_data[0]]
                worksheet.append(series_titles)
                for series in series_data:
                    series_values = [series[key] for key in series]
                    worksheet.append(series_values)

    # save the workbook - this will overwrite any pre-existing
    # export for the same patient
    workbook.save(rf"./export/Export_{pt_data['MRN']}.xlsx")