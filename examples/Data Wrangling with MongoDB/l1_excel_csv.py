# -*- coding: utf-8 -*-
# Find the time and value of max load for each of the regions
# COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
# and write the result out in a csv file, using pipe character | as the delimiter.
# An example output can be seen in the "example.csv" file.
import xlrd
import os
import csv
from zipfile import ZipFile
datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = []
    # YOUR CODE HERE
    # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
    # Excel date to Python tuple of (year, month, day, hour, minute, second)
    
    for col in range(sheet.ncols - 1):
        values = sheet.col_values(col+1, start_rowx=1, end_rowx=None) 
        maxval = float(max(values))
        maxindex = values.index(maxval) + 1   
        maxdate = sheet.cell_value(maxindex, 0)
        realmaxdate = xlrd.xldate_as_tuple(maxdate, 0)
        data.append([sheet.cell_value(0,col+1), realmaxdate, maxval])
        
    return data

def save_file(data, filename):
    # YOUR CODE HERE
    with open(filename, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter = '|')
        spamwriter.writerow(['Station','Year','Month','Day','Hour','Max Load'])
        for line in data:
            spamwriter.writerow([line[0],
                                 line[1][0],
                                 line[1][1],
                                 line[1][2],
                                 line[1][3],
                                 line[2]])
    return csvfile

    
def test():
    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    ans = {'FAR_WEST': {'Max Load': "2281.2722140000024", 'Year': "2013", "Month": "6", "Day": "26", "Hour": "17"}}
    
    fields = ["Year", "Month", "Day", "Hour", "Max Load"]
    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            s = line["Station"]
            if s == 'FAR_WEST':
                for field in fields:
                    assert ans[s][field] == line[field]

        
test()