import csv 
import numpy as np

evidence = [] 
labels = [] 

    # dictionary to map month names to numeric values
month_map = {
'Jan': 0,
'Feb': 1,
'Mar': 2,
'Apr': 3,
'May': 4,
'June': 5,
'Jul': 6,
'Aug': 7,
'Sep': 8,
'Oct': 9,
'Nov': 10,
'Dec': 11
}

to_int = [0, 2, 4, 10, 11, 12, 13, 14] 
to_float = [1, 3, 5, 6, 7, 8, 9] 

with open('shopping.csv') as f: 
    reader = csv.reader(f) 
    # skip header row 
    next(reader) 
    for row in reader:                 
        # convert Month 
        # convert month name to numeric value 
        month_numeric = month_map.get(row[10], None) 
        # replace month name with numeric value 
        row[10] = month_numeric 

        # convert VisitorType 
        if row[15] == "Returning_Visitor": 
            row[15] = 1
        elif row[15] == "New_Visitor": 
            row[15] = 0
        elif row[15] == "Other": 
            row[15] = 0

        # convert Weekend column 
        if row[16] == "TRUE": 
            row[16] = 1
        elif row[16] == "FALSE": 
            row[16] = 0

        # convert columns to either int or float 
        for int_index in to_int: 
            row[int_index] = int(row[int_index])
        for float_index in to_float: 
            row[float_index] = float(row[float_index])

        # append all rows 
        evidence.append(row[:14] + [row[15], row[16]]) 

        # convert Revenue column 
        if row[17] == "TRUE": 
            labels.append(1) 
        elif row[17] == "FALSE": 
            labels.append(0) 


# evidence_array = np.array(evidence) 
# print(type(evidence_array)) 
# print(evidence_array)

for row in labels:
    for value in row:
        if type(value) != int: 
            if type(value) != float: 
                print(value, type(value), row)