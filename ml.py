
"""
Using sklearn (scikit-learn) package which has library for performing Machine Learning. We want to classify a bill as passing (given that it is out of committee).

_Logistic Regression_
http://scikit-learn.org/stable/modules/linear_model.html#logistic-regression
http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression

_Support Vector Machines_
http://scikit-learn.org/stable/modules/svm.html
http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html#sklearn.svm.SVC
"""
import numpy
import sklearn.linear_model
import csv

import Bill
import readBills

def isEnacted(bill):
    return bill.isSuccessful()

def isOutOfCommittee(bill):
    return bill.isOutOfCommittee()

# shows how many bills passed to create dumb baseline if you always said No for your prediction
def calculateBaseline(bills, predicate):
    passed = 0
    for bill_id in bills:
        if predicate(bills[bill_id]):
            passed += 1
    proportion_passed =  passed / float(len(bills))
    print 'Successful bills: {0:.2f}% => baseline is {1:.2f}%'.format(100*proportion_passed, 100 * (1-proportion_passed))


# creates Feature matrix and Label vector and returns these as Python lists
# the features are a list of n-tuples
def prepareInputDataAfterCommitteeGettingEnacted():
    print 'running prepareInputDataAfterCommitteeGettingEnacted()'
    bills = readBills.readAllBills()
    bills = readBills.filterBillsOnlyOutOfCommittee(bills)
    print 'Number of bills out of committee: %d' % len(bills)
    calculateBaseline(bills, isEnacted)
    features = []
    labels = []
    for bill_id in bills:
        bill = bills[bill_id]
        features.append((1, len(bill.cosponsors), bill.introduced_month))
#        features.append((1, len(bill.cosponsors), bill.num_voting_rounds, bill.num_passed_rounds, bill.introduced_month))#, bill.sponsor))
        labels.append(1 if bill.isSuccessful() else 0)
    return (features, labels)

def prepareInputDataForGettingOutOfCommittee():
    print 'running prepareInputDataForGettingOutOfCommittee()'
    bills = readBills.readAllBills()
    print 'Number of bills (total): %d' % len(bills)
    calculateBaseline(bills, isOutOfCommittee)
    features = []
    labels = []
    for bill_id in bills:
        bill = bills[bill_id]
        features.append((1, len(bill.cosponsors), bill.introduced_month))
#        features.append((1, len(bill.cosponsors), bill.num_voting_rounds, bill.num_passed_rounds, bill.introduced_month))#, bill.sponsor))
        labels.append(1 if bill.isOutOfCommittee() else 0)
    return (features, labels)

def runML(prepareDatasetFunction):
    (features, labels) = prepareDatasetFunction()
    print ''
    X_train = numpy.array(features[:int(len(features)*.7)])
    y_train = numpy.array(labels[:int(len(labels)*.7)])
    print '%d training examples' % len(X_train)

    X_test = numpy.array(features[int(len(features)*.7):])
    y_test = numpy.array(labels[int(len(labels)*.7):]) 
    print '%d test samples' % len(X_test)

    score = doLogisticRegression(X_train, y_train, X_test, y_test)
    print '\nLogistic Regression score: {0:.2f}%'.format(100*score)
    score = doSVM(X_train, y_train, X_test, y_test)
    print 'SVM score: {0:.2f}%'.format(100*score)

def runML((features, labels)):
    X_train = numpy.array(features[:int(len(features)*.7)])
    y_train = numpy.array(labels[:int(len(labels)*.7)])
    print '%d training examples' % len(X_train)

    X_test = numpy.array(features[int(len(features)*.7):])
    y_test = numpy.array(labels[int(len(labels)*.7):]) 
    print '%d test samples' % len(X_test)

    score = doLogisticRegression(X_train, y_train, X_test, y_test)
    print '\nLogistic Regression score: {0:.2f}%'.format(100*score)
    score = doSVM(X_train, y_train, X_test, y_test)
    print 'SVM score: {0:.2f}%'.format(100*score)


def doLogisticRegression(X_train, y_train, X_test, y_test):
    # initialise model with some random parameters
    # extension would be to experiment with these
    clf_l2_LR = sklearn.linear_model.LogisticRegression(C=100, penalty='l2', tol=0.01)
    clf_l2_LR.fit(X_train, y_train)
    return clf_l2_LR.score(X_test, y_test)

def doSVM(X_train, y_train, X_test, y_test):
    clf = sklearn.svm.SVC()
    clf.fit(X_train, y_train)
    return clf.score(X_test, y_test)

# write data to a CSV file
# three columns: bill_id | # cosponsors | month it was introduced
def read_csv(file_path, bill_predicate):
    features = []
    labels = []
    print 'Reading from file %s' % file_path
    with open(file_path, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            bill_id = row[0]
            status = row[-1]
            del row[0]
            del row[-1]
            feature = tuple([int(round(float(item))) for item in row])
            if ('OutOfCommittee' == bill_predicate):
                label = 1 if status not in Bill.NOT_OUT_OF_COMMITTEE else 0
            else:
                if status in Bill.NOT_OUT_OF_COMMITTEE:
                    continue
                else:
                    label = 1 if status in Bill.SUCCESSFUL else 0
            features.append(feature)
            labels.append(label)
    print len(labels)
    return (features, labels)

if __name__ == '__main__':
    #(features, labels) = read_csv('./bill_combined_OutOfCommittee.csv', 'Enacted')
    #(features, labels) = read_csv('./bill_combined_All.csv', 'OutOfCommittee')
    # to find all CSV files: find . -maxdepth 2 -name '*.csv'

    #runML(prepareInputDataForGettingOutOfCommittee)
    print 'Predicting whether a bill will get out of committee'
    runML(read_csv('./bill_combined.csv', 'OutOfCommittee'))
    print '\n\nPredicting whether a bill will get enacted given it is out of committee'
    #runML(prepareInputDataAfterCommitteeGettingEnacted)
    runML(read_csv('./bill_combined.csv', 'Enacted'))


