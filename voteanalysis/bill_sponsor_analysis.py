import votes, legislators, recommender
import readBills
import numpy as np
import csv
import matplotlib.pyplot as plt

def read_all_bills(base_directory):
    bills_hr = readBills.readBills(base_directory, "hr")
    bills_s = readBills.readBills(base_directory, "s")
    bills_hjres = readBills.readBills(base_directory, "hjres")
    bills_sjres = readBills.readBills(base_directory, "sjres")
    bills = dict(bills_hr.items() + bills_s.items() + bills_hjres.items() + bills_sjres.items())
    return bills

if __name__ == '__main__':
    bills = read_all_bills("/Users/travis/dev/cs224w/Project/113/")
    cosponsor_counts = [len(b.cosponsors)+1 for b in bills.values()]
    print("Mean number of cosponsors: %f" % np.mean(cosponsor_counts))
    print("Median: %f" % np.median(cosponsor_counts))
    print("SD: %f" % np.std(cosponsor_counts))
    
    plt.cla()
    plt.hist(cosponsor_counts)
    plt.xlabel("Number of cosponsors")
    plt.savefig("cosponsor_distribution.png")
    
    