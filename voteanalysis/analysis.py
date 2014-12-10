import legislators, votes, recommender, simulation
import numpy as np

def compute_metrics(r,r_hat):
    threshold = np.vectorize(lambda x: 1 if x >= 0 else -1)
    predictions = threshold(r_hat)
    tp = tn = fp = fn = 0
    for i in xrange(r.shape[0]):
        for j in xrange(r.shape[1]):
            if np.isnan(r[i,j]):
                continue
            actual = r[i,j]
            prediction = predictions[i,j]
            if (actual == prediction):
                if (actual == 1):
                    tp += 1
                else:
                    tn += 1
            else:
                if (actual == 1):
                    fn += 1
                else:
                    fp += 1
    accuracy = float(tp + tn)/float(tp + tn + fp + fn)
    return accuracy

def get_sample(m, p):
    population = [(i,j) for i in xrange(m.shape[0]) for j in xrange(m.shape[1]) if not np.isnan(m[i,j])]
    sample = np.random.choice(xrange(len(population)), np.ceil(p*len(population)), replace = False)
    return [population[i] for i in sample]

def get_sample_rowwise(m, p):
    sample = []
    for i in xrange(m.shape[0]):
        population = [j for j in xrange(m.shape[1]) if not np.isnan(m[i,j])]
        if len(population) == 0:
            continue
        column_selection = np.random.choice(population, np.ceil(p*len(population)), replace = False)
        for j in column_selection:
            sample.append((i,j))
    return sample

def get_sample_billwise(m, percent_bills, percent_votes_tested):
    sample = []
    bill_population = [i for i in xrange(m.shape[1]) if not np.all(np.isnan(m[:,i]))]
    bill_sample = np.random.choice(bill_population, np.ceil(percent_bills*m.shape[1]), replace = False)
    for bill_column in bill_sample:
        pool = [l_row for l_row in xrange(m.shape[0]) if not np.isnan(m[l_row, bill_column])]
        if len(pool) == 0:
            continue
        legislator_bill_sample = np.random.choice(pool, np.ceil(percent_votes_tested*len(pool)), replace = False)
        for legislator_row in legislator_bill_sample:
            sample.append((legislator_row, bill_column))
    return sample

def remove_sample(r, sample):
    r_p = r.copy()
    for (i,j) in sample:
        r_p[i,j] = np.NAN
    return r_p

def get_rowwise_accuracy(r, predictions, sample):
    accuracies = []
    
    predictions_only = np.nan * np.ones(r.shape)
    (rows, columns) = zip(*sample)
    predictions_only[rows,columns] = predictions[rows,columns]
    
    for i in xrange(r.shape[0]):
        #tp = tn = fp = fn = 0
        actual_row = r[i,:]
        
        if np.all(np.isnan(actual_row)):
            continue
        
        predicted_row = predictions_only[i,:]

        tp = np.sum(np.logical_and(actual_row == 1, predicted_row > 0))
        tn = np.sum(np.logical_and(actual_row == -1, predicted_row < 0))
        fp = np.sum(np.logical_and(actual_row == -1, predicted_row > 0))
        fn = np.sum(np.logical_and(actual_row == 1, predicted_row < 0))
        accuracies.append(float(tp + tn)/float(tp + tn + fp + fn))
        
    return accuracies

def sample_accuracy(r, predictions, sample):
    tp = tn = fp = fn = 0
        
    for (i,j) in sample:
        actual = r[i,j]
        prediction = predictions[i,j]
        if (actual == prediction):
            if (actual == 1):
                tp += 1
            else:
                tn += 1
        else:
            if (actual == 1):
                fn += 1
            else:
                fp += 1
    accuracy = float(tp + tn)/float(tp + tn + fp + fn)
    precision  = float(tp)/float(tp + fp)
    recall = float(tp)/float(tp+fn) 
    return (accuracy,precision,recall)


