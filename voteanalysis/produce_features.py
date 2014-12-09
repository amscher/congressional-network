import votes, legislators, recommender
import readBills
import numpy as np
import csv

def read_all_bills(base_directory):
    bills_hr = readBills.readBills(base_directory, "hr")
    bills_s = readBills.readBills(base_directory, "s")
    bills_hjres = readBills.readBills(base_directory, "hjres")
    bills_sjres = readBills.readBills(base_directory, "sjres")
    bills = dict(bills_hr.items() + bills_s.items() + bills_hjres.items() + bills_sjres.items())
    return bills

if __name__ == '__main__':
    #Load legislators
    llist = list(legislators.load_legislators("/Users/travis/dev/cs224w/Project/legislators-current.csv"))
    #Load votes
    vlist = list(vote for vote in \
            votes.read_votes("/Users/travis/dev/cs224w/Project/111/votes/2009","/Users/travis/dev/cs224w/Project/111/votes/2010","/Users/travis/dev/cs224w/Project/112/votes/2011","/Users/travis/dev/cs224w/Project/112/votes/2012","/Users/travis/dev/cs224w/Project/113/votes/2013","/Users/travis/dev/cs224w/Project/113/votes/2014") \
             #votes.read_votes("/Users/travis/dev/cs224w/Project/113/votes/2013","/Users/travis/dev/cs224w/Project/113/votes/2014") \
            if vote.get_vote_type() == "passage")
    #Map legislator IDs to legislators
    legislator_id_map = legislators.build_id_map(llist)
    #Create vote matrix
    r = recommender.create_vote_matrix(llist, vlist)
    # Map legislators to rows
    legislator_row_map = {llist[l_i].get_thomas_id(): l_i for l_i in xrange(len(llist))}
    #Load bills
    bills = read_all_bills("/Users/travis/dev/cs224w/Project/113/").values()

    #Map bills to columns
    bill_column_map = {bill.bill_id:\
                       [v_i for v_i in xrange(len(vlist)) \
                        if vlist[v_i].get_full_bill_id() == bill.bill_id] \
                     for bill in bills}
    
    #randomly shuffle bills
    np.random.shuffle(bills)
    group_size = int(np.floor(0.05 * float(len(bills))))
    groups = np.arange(0,len(bills),group_size)
    
    #Iterate bill groups; produce features and compute metrics
    tp = fp = tn = fn = 0
    
    with open("bill_vote_features.csv",'w') as csvfile:
        feature_writer = csv.writer(csvfile, delimiter = ',')
        
        for i in groups:
            print("Processing bills %i to %i" % (i,i+group_size))
            #Get set of target bills
            target_bills = bills[i:i+group_size]
            #Remove corresponding columns from the matrix
            bill_columns = []
            for bill in target_bills:
                target_bill_columns = bill_column_map[bill.bill_id]
                bill_columns += target_bill_columns
            r_p = r[:,[i for i in xrange(len(vlist)) if i not in bill_columns]]
            #Add new columns for each target bill
            column_offset = r_p.shape[1]
            column_stack = [r_p]
            for bill in target_bills:
                vote = np.nan * np.ones((len(llist),1))
                known_voter_ids = bill.cosponsors + [bill.sponsor]
                for thomas_id in known_voter_ids:
                    if thomas_id in legislator_row_map:
                        vote[legislator_row_map[thomas_id]] = 1
                column_stack.append(vote)
            r_p = np.hstack(column_stack)
            #Run matrix factorization
            (p,q,bias,err) = recommender.run_factorization(r_p,40,2500,0.0002)
            #Get predicted votes on bill
            r_hat = p*q.T + bias
            for i in xrange(len(target_bills)):
                bill = target_bills[i]
                predicted_votes = np.array([vote[0,0] for vote in r_hat[:,column_offset + i]])
                mean = np.mean(predicted_votes)
                sd = np.std(predicted_votes)
                hist = list(np.percentile(predicted_votes, [10,25,50,75,90]))
                feature_writer.writerow([bill.bill_id, mean, sd] + hist)
                #compute accuracy metrics
                if (bill.bill_id in bill_column_map and len(bill_column_map[bill.bill_id]) > 0):
                    actual_vote_column = bill_column_map[bill.bill_id][-1]
                    actual_votes = np.array([vote[0,0] for vote in r[:,actual_vote_column]])
                    tp += np.sum(np.logical_and(actual_votes == 1, predicted_votes > 0))
                    tn += np.sum(np.logical_and(actual_votes == -1, predicted_votes < 0))
                    fp += np.sum(np.logical_and(actual_votes == -1, predicted_votes > 0))
                    fn += np.sum(np.logical_and(actual_votes == 1, predicted_votes < 0))
                
    print("Accuracy: %f" % (float(tp + tn)/float(tp + tn + fp + fn)) )
    print("Precision: %f" % (float(tp)/float(tp + fp)) )
    print("Recall: %f" % (float(tp)/float(tp+fn)) )
#         for bill in bills.values():
#             print("Generating features for bill %s" % bill.bill_id)
#             #Remove all votes relate to that bill
#             bill_columns = bill_column_map[bill.bill_id]
#             r_p = r[:,[i for i in xrange(len(vlist)) if i not in bill_columns]]
#             #Add a new column in which only legislators vote
#             vote = np.nan * np.ones((len(llist),1))
#             known_voter_ids = bill.cosponsors + [bill.sponsor]
#             for thomas_id in known_voter_ids:
#                 if thomas_id in legislator_row_map:
#                     vote[legislator_row_map[thomas_id]] = 1
#             r_p = np.hstack([r_p, vote])
#             
#             #Run matrix factorization
#             (p,q,err) = recommender.run_factorization(r_p,40,2500,0.0002)
#             #Get predicted votes on bill
#             r_hat = p*q.T
#             predicted_votes = [vote[0,0] for vote in r_hat[:,-1]]
#             mean = np.mean(predicted_votes)
#             median = np.median(predicted_votes)
#             sd = np.std(predicted_votes)
#             feature_writer.writerow([bill.bill_id, median, mean, sd])
        
        