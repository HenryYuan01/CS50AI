import csv
import sys
import numpy as np 

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
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
    'Dec': 11}

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
    # labels_array = np.array(labels)
    return evidence, labels



def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=7)
    model.fit(evidence, labels)
    return model 


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    size = len(labels) 
    positives = 0 
    true_positives = 0 
    negatives = 0 
    true_negatives = 0 
    
    for i in range(size):

        if labels[i] == 0:
            negatives += 1
            if labels[i] == predictions[i]:
                true_negatives += 1
        else:
            positives += 1
            if labels[i] == predictions[i]:
                true_positives += 1

    # True Positive Rate        
    sensitivity = true_positives / positives

    # True Negative Rate
    specificity = true_negatives / negatives   

    return sensitivity, specificity 


if __name__ == "__main__":
    main()
