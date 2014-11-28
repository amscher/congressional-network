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

def remove_sample(r, sample):
    r_p = r.copy()
    for (i,j) in sample:
        r_p[i,j] = np.NAN
    return r_p

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
    return accuracy


