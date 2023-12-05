import pandas as pd
import xlrd
import xlwings as xd


def read_file():
    wb = xd.Book(r"C:\Users\baisahu\Documents\TCAF FI\TCAF_AssessmentFramework_Enhancements.xlsx")
    sheet = wb.sheets['Test Monitoring and Control']

    # read the entire data present in sheet; comes as a list of lists
    sheet_in_list = sheet.used_range.value

    # get the column headers from the list
    column_header = sheet_in_list[0]
    sheet_in_list.pop(0)

    # create a dataframe from the list
    sheet_df = pd.DataFrame(sheet_in_list, columns=column_header)

    # drop rows where sl no is Nan
    df_without_na = sheet_df[sheet_df['S.No.'].notna()]

    # get questions, relevant to agile and user profiles in lists\
    serial_num = df_without_na['S.No.'].tolist()
    questions = df_without_na['Question'].tolist()
    relevant_to_agile = df_without_na['Relevant to Agile'].tolist()
    designation = df_without_na['User profile'].tolist()
    # print(serial_num)
    return serial_num, questions, relevant_to_agile, designation

# read_file()