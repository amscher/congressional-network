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
            #votes.read_votes("/Users/travis/dev/cs224w/Project/111/votes/2009","/Users/travis/dev/cs224w/Project/111/votes/2010","/Users/travis/dev/cs224w/Project/112/votes/2011","/Users/travis/dev/cs224w/Project/112/votes/2012","/Users/travis/dev/cs224w/Project/113/votes/2013","/Users/travis/dev/cs224w/Project/113/votes/2014") \
            votes.read_votes("/Users/travis/dev/cs224w/Project/113/votes/2013","/Users/travis/dev/cs224w/Project/113/votes/2014") \
            if vote.get_vote_type() == "passage")
    
    bills = read_all_bills("/Users/travis/dev/cs224w/Project/113/")
    
    voted_bills = set("%s%s" % (v.get_bill_type(),v.get_bill_id()) for v in vlist)
    successful_bills = set(b.bill_id for b in bills.values() if b.isSuccessful())
    successful_voted_bills = voted_bills.intersection(successful_bills)
    
    print("Total number of bills voted on: %d" % len(voted_bills))
    print("Total number of bills: %d" % len(bills))
    print("Percentage of success of voted bills: %f" % (float(len(successful_voted_bills))/float(len(voted_bills))) )
    print("Percentage success of all bills: %f" % (float(len(successful_bills))/float(len(bills))) )
    
    