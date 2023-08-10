import csv
import sys

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
    labels = list()
    evidences = list()

    int_list = [0, 2, 4, 10, 11, 12, 13, 14, 15, 16]
    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader, None)  # skip file header row
        for row in reader:
            evidence = list()
            label = list()
            for i in range(0, 17):
                if i in int_list:
                    if i == 15:   # VisitorType
                        if row[i] == 'Returning_Visitor':
                            evidence.append(1)
                        else:
                            evidence.append(0)
                    elif i == 16:   # Weekend
                        if row[i] == 'TRUE':
                            evidence.append(1)
                        else:
                            evidence.append(0)
                    elif i == 10:   # Month
                        evidence.append(month_list.index(row[i]))
                    else:           
                        evidence.append(int(row[i]))
                else:       
                    evidence.append(float(row[i]))
                
            if row[17] == 'TRUE':   # Revenue
                labels.append(1)
            else:
                labels.append(0)
            #labels.append(label)
            evidences.append(evidence)
        
        ret_tuple = (evidences, labels)
        #print(ret_tuple[1][1])
        return ret_tuple


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    return KNeighborsClassifier(n_neighbors=1).fit(evidence, labels)


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
    sensivity = 0
    specificity = 0
    positive = 0
    negative = 0

    ret_tuple = tuple()

    for i in range(0, len(labels)):
        if labels[i] == 1:
            positive += 1
            if predictions[i] == labels[i]:
                sensivity += 1
        else:
            negative += 1
            if predictions[i] == labels[i]:
                specificity += 1

    ret_tuple = ((sensivity / positive), (specificity / negative))
    return ret_tuple


if __name__ == "__main__":
    main()
