import logging
import azure.functions as func
import pandas as pd
from io import StringIO
import re

def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    blob_data = myblob.read().decode('utf-8')
    test_data = StringIO(blob_data)
    df = pd.read_csv(test_data, sep=",")
    test_result,error = validateCSV(df)
    if test_result:
        if error is None:
            logging.info("SUCCESS")
        else:
            logging.info("WARNING: " + error)
    else:
        logging.info("ERROR: " + error)

def validateCSV(df):

    # TODO: Add as many validation methods here...
    # Add as many validation steps here
    result,error = validateDates(df) 
    if result:
        if error is None:
            return validateStructure(df)  
    return result,error 
    
def validateDates(df):
    # 1: Check for valid date formats
    error1 = "Invalid date format"
    error2 = "Duplicate dates"
    try:
        pd.to_datetime(df['date'], format='%m/%d/%Y', errors='raise')

        # 2: Check if all the dates are unique
        dates = df["date"]
        if True in dates.duplicated():
            return False,error2
        else:
            return True
    except ValueError:
        return False,error1

def validateStructure(df):
    error1 = "No inflows/outflows"
    error2 = "Invalid format for inflow/outflow columns"
    error3 = "Missing date column"
    error4 = "Missing Totals column"

    columns = df.columns.values
    if not 'date' in columns:
        return False,error3

    r_total = re.compile("total_*")
    totals_column = list(filter(r_total.match,columns))
    if len(totals_column) == 0:
        return True,error4
    
    # Validate inflows and outflows column structure
    r_inflow = re.compile("inflows_\d")
    r_outflow = re.compile("outflows_\d")
    inflow_list = list(filter(r_inflow.match,columns))
    outflow_list = list(filter(r_outflow.match,columns))
    if len(inflow_list) == 0 or len(outflow_list) == 0:
        return False,error1
    else:
        for item in columns:
            if item == 'date' or re.match("inflows_\d",item) or re.match("outflows_\d",item) or item == 'total_inflows' or item == 'total_outflows':
                continue
            else:
                return False,error2
    
    return True

    
    

