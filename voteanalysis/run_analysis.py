from analysis import *
import legislators, votes, recommender, simulation
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    llist = list(legislators.load_legislators("/Users/travis/dev/cs224w/Project/legislators-current.csv"))
    vlist = [vote for vote in votes.read_votes("/Users/travis/dev/cs224w/Project/113/votes/2013","/Users/travis/dev/cs224w/Project/113/votes/2014") if vote.get_vote_type() == "passage"]
    print("Using %i votes" % len(vlist))
    r = recommender.create_vote_matrix(llist, vlist)
    test_set = get_sample(r, 0.15)
    r_p = remove_sample(r,test_set)
    
    #compute some baseline metrics
    prob_aye = simulation.get_prob_aye(r)
    non_null_prob = [prob[0,0] for prob in prob_aye if not np.isnan(prob)]
    print("Number of voting legislators: %d" % len(non_null_prob))
    plt.hist(non_null_prob)
    plt.xlabel("Probability of voting \"Aye\"")
    plt.ylabel("Number of legislators")
    plt.savefig("aye_prob.png")
    plt.cla()

    #try simulated random guessing
    prob_aye = simulation.get_prob_aye(r_p)
    random_predictions = simulation.simulate_votes(prob_aye, len(vlist))
    #random_accuracy = compute_metrics(r, random_predictions)
    random_sample_accuracy = sample_accuracy(r, random_predictions, test_set)
    #print("Accuracy using random guessing: %f" % random_accuracy)
    print("Accuracy using random guessing on test set: %f" % random_sample_accuracy)
    
    #try choosing most likely vote
    most_likely_votes = simulation.get_most_likely_votes(prob_aye, len(vlist))
    most_likely_accuracy = sample_accuracy(r, most_likely_votes, test_set)
    print("Accuracy using most likely guess on test set: %f" % most_likely_accuracy)
    
    #matrix factorization
    (p,q,err) = recommender.run_factorization(r_p,40,2500,0.0002)
    mfac_accuracy = sample_accuracy(r, recommender.get_predictions(p*q.T), test_set)
    plt.plot(err[1:])
    plt.xlabel("Iteration")
    plt.ylabel("Mean squared error")
    plt.savefig("mfac-mse.png")
    #accuracy = compute_metrics(r, p*q.T)
    print("Accuracy using matrix factorization on test set: %f" % mfac_accuracy)
    
    #plt.plot(err[1:])
    #plt.show()