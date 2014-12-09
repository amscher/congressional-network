from analysis import *
import legislators, votes, recommender, simulation
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    llist = list(legislators.load_legislators("/Users/travis/dev/cs224w/Project/legislators-current.csv"))
    vlist = [vote for vote in votes.read_votes("/Users/travis/dev/cs224w/Project/111/votes/2009","/Users/travis/dev/cs224w/Project/111/votes/2010","/Users/travis/dev/cs224w/Project/112/votes/2011","/Users/travis/dev/cs224w/Project/112/votes/2012","/Users/travis/dev/cs224w/Project/113/votes/2013","/Users/travis/dev/cs224w/Project/113/votes/2014") if vote.get_vote_type() == "passage"]
    print("Using %i votes" % len(vlist))
    r = recommender.create_vote_matrix(llist, vlist)
    
    print("Total number of individual votes cast: %d" % np.sum(np.logical_not(np.isnan(r))))
    print("Individual in favor: %d" % np.sum(r == 1))
    print("Individual votes against: %d" % np.sum(r== -1))
    
    test_set = get_sample(r, 0.15)
    r_p = remove_sample(r,test_set)
    
    legislator_features = legislators.get_legislator_features(llist)
    
    #compute some baseline metrics
    prob_aye = simulation.get_prob_aye(r)
    non_null_prob = [prob[0,0] for prob in prob_aye if not np.isnan(prob)]
    print("Number of voting legislators: %d" % len(non_null_prob))
    plt.hist(non_null_prob)
    plt.xlabel("Probability of voting \"Aye\"")
    plt.ylabel("Number of legislators")
    plt.savefig("aye_prob.png")
    plt.cla()

#     #try simulated random guessing
#     prob_aye = simulation.get_prob_aye(r_p)
#     random_predictions = simulation.simulate_votes(prob_aye, len(vlist))
#     #random_accuracy = compute_metrics(r, random_predictions)
#     random_sample_accuracy = sample_accuracy(r, random_predictions, test_set)
#     #print("Accuracy using random guessing: %f" % random_accuracy)
#     print("Accuracy using random guessing on test set: %f" % random_sample_accuracy)
    
    #try choosing most likely vote
    most_likely_votes = simulation.get_most_likely_votes(prob_aye, len(vlist))
    (mle_accuracy, mle_precision, mle_recall) = sample_accuracy(r, most_likely_votes, test_set)
    print("Accuracy using most likely guess on test set: %f" % mle_accuracy)
    print("Precision using most likely guess on test set: %f" % mle_precision)
    print("Recall using most likely guess on test set: %f" % mle_recall)
    
    #matrix factorization
    (p,q,bias,err) = recommender.run_factorization(r_p,40,2500,0.0002,legislator_features = legislator_features)
    (mfac_accuracy,mfac_precision,mfac_recall) = sample_accuracy(r, recommender.get_predictions(p*q.T+bias), test_set)
    plt.plot(err[1:])
    plt.xlabel("Iteration")
    plt.ylabel("Mean squared error")
    plt.savefig("mfac-mse.png")
    #accuracy = compute_metrics(r, p*q.T)
    print("Accuracy using matrix factorization on test set: %f" % mfac_accuracy)
    print("Precision using matrix factorization on test set: %f" % mfac_precision)
    print("Recall using matrix factorization on test set: %f" % mfac_recall)
    
    #plt.plot(err[1:])
    #plt.show()
    
    #matrix factorization by percentage votes tested
    percents = np.arange(0.025,1.01,0.025)
    num_tries = 3
    accuracies = []
    precisions = []
    recalls = []
    
    for percent_tested in percents:
        accuracy = 0
        precision = 0
        recall = 0
        
        for i in xrange(3):
            test_set = get_sample_billwise(r, 0.15, percent_tested)
            r_p = remove_sample(r,test_set)
            
            (p,q,bias,err) = recommender.run_factorization(r_p,40,2500,0.0002,legislator_features = legislator_features)
            (mfac_accuracy,mfac_precision,mfac_recall) = sample_accuracy(r, recommender.get_predictions(p*q.T+bias), test_set)
            accuracy += 0.3333333 * mfac_accuracy
            precision += 0.3333333 * mfac_precision
            recall += 0.3333333 * mfac_recall
            print("Metrics using %f percent of votes tested" % percent_tested)
            print("Accuracy using matrix factorization on test set: %f" % mfac_accuracy)
            print("Precision using matrix factorization on test set: %f" % mfac_precision)
            print("Recall using matrix factorization on test set: %f" % mfac_recall)
        accuracies.append(accuracy)
        precisions.append(precision)
        recalls.append(recall)
    
    plt.cla()
    plt.xlabel("Percent votes withheld and tested per bill")
    plt.ylabel("Metric value")
    plt.plot(percents, accuracies, 'b-', label='Accuracy')
    plt.plot(percents, precisions, 'g-', label='Precision')
    plt.plot(percents, recalls, 'r-', label='Recall')
    plt.legend(loc = 3)
    plt.savefig("withholding_graphs.png")
        