# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 09:35:49 2023

@author: AL27397
"""
import pandas as pd
import os

#Import function to import numbers from a single column from excel.
#The input contains the filepath, the sheet name in excel, the column indicator
#and the start and end position of the column of numbers you want to import.
def import_col(location, filename, sheetname, col_name, start_row, end_row):
    filepath = os.path.join(location, filename)
    df = pd.read_excel(filepath, sheet_name=sheetname, usecols=col_name, skiprows=range(1, start_row-1), nrows=(end_row - start_row + 1))
    X = df.values
    return X