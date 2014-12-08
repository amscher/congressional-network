import json
import Bill
import generate_leg_success_plots as Legislator

file = open("csv/legislator-info.csv", 'w')

def createCsv():
  stream1 = open("data/legislator-data.json", 'r')
  legData = json.load(stream1)
  stream2 = open("data/bill-data.json", 'r')
  billData = json.load(stream2)

  file.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}\n".format(
      "bill_id", 1, "numTerms", "avgRank", "lowestRank", "percentCIC", "bill_status"))

  for (bill_id, bill) in billData.iteritems():
    numTerms = 0
    avgRank = 0
    lowestRank = 0
    numCIC = float(Legislator.getNumCICForBill(legData, bill_id, bill))/float(len(bill["cosponsors"]))

    if "sponsor" in bill:
      sponsor = bill["sponsor"]
      sponsorInfo = legData[sponsor]
      numTerms = sponsorInfo["num_terms"]
      avgRank = Legislator.getAvgRank(sponsorInfo)
      lowestRank = Legislator.getLowestRank(sponsorInfo)
    file.write("{0},{1},{2},{3},{4},{5},{6}\n".format(
        bill_id, 1, numTerms, avgRank, lowestRank, numCIC, bill["status"]))


createCsv()


