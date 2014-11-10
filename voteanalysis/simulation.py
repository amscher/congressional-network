import legislators, votes, recommender
import numpy as np

def get_prob_aye(r):
    row_sum = np.sum(abs(np.nan_to_num(r)),1)
    aye_votes = np.sum(r == 1,1)
    p = np.divide(aye_votes, row_sum)
    return p
    
def simulate_votes(p,n):
    votes = np.matrix(np.random.rand(len(p),n))
    for i in xrange(len(p)):
        for j in xrange(n):
            if(np.isnan(p[i])):
                votes[i,j] = np.nan
            elif votes[i,j] <= p[i]:
                votes[i,j] = 1
            else:
                votes[i,j] = -1
    return votes

def get_most_likely_votes(p,n):
    votes = np.matrix(np.zeros((len(p),n)))
    for i in xrange(len(p)):
        if np.isnan(p[i]):
            votes[i,:] = np.nan
        elif p[i] >= 0.5:
            votes[i,:] = 1
        else:
            votes[i,:] = -1
    return votes
