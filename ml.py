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

import readBills

# shows how many bills passed to create dumb baseline if you always said No for your prediction
def calculateBaseline(bills):
    passed = 0
    for bill_id in bills:
        if bills[bill_id].isSuccessful():
            passed += 1
    proportion_passed =  passed / float(len(bills))
    print 'Successful bills: {0:.2f}% => baseline is {1:.2f}%'.format(100*proportion_passed, 100 * (1-proportion_passed))


# creates Feature matrix and Label vector and returns these as Python lists
# the features are a list of n-tuples
def prepareInputData():
    bills = readBills.readAllBills()
    bills = readBills.filterBillsOnlyOutOfCommittee(bills)
    print 'Number of bills out of committee: %d' % len(bills)
    calculateBaseline(bills)
    features = []
    labels = []
    for bill_id in bills:
        bill = bills[bill_id]
        features.append((1, len(bill.cosponsors), bill.introduced_month))
#        features.append((1, len(bill.cosponsors), bill.num_voting_rounds, bill.num_passed_rounds, bill.introduced_month))#, bill.sponsor))
        labels.append(1 if bill.isSuccessful() else 0)
    return (features, labels)

def runML():
    (features, labels) = prepareInputData()
    print ''
    # initialise model with some random parameters
    # extension would be to experiment with these
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

if __name__ == '__main__':
    runML()
