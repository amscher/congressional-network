import json
import Congressman
import Committee
import Bill
import matplotlib
import matplotlib.pyplot as plt


def getLowestRank(item):
  lowestRank = 20
  for (id, rank) in item["committeesMap"].iteritems():
    if rank < lowestRank:
      lowestRank = rank
  return lowestRank

def getAvgRank(item):
  rankSum = 0
  numCommittees = 0
  for (id, rank) in item["committeesMap"].iteritems():
    rankSum += rank
    numCommittees += 1
  if numCommittees == 0:
    return 30
  else:
    return float(rankSum)/float(numCommittees)

def getSuccessRate(item):
  if len(item["bills"]) == 0:
    return 0
  else:
    # billsPerTerm = /float(item["num_terms"])
    return float(item["num_success_bills"])/float(len(item["bills"]))

def plot(title, xlabel, ylabel, xVals, yVals, filename, ymax=1, xlog=False):
  fig1 = plt.figure()
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.ylim(ymax=ymax)
  ax = fig1.add_subplot(111)
  if xlog:
    ax.set_xscale('log')
  plot = ax.plot(xVals, yVals, 'bo', mec='b', markersize=5, alpha=0.3, label="chart")
  ax.legend(loc='upper right')
  fig1.savefig('plotting/' + filename + '.png')

def readAndPlotData():
  stream = open("data/legislator-data.json", 'r')
  data = json.load(stream)

  ranks = [0 for i in range(0, 31)]
  numRanks = [1 for i in range(0, 31)]
  for value in data.itervalues():
    rank = getAvgRank(value)
    successRate = getSuccessRate(value)
    index = int(round(rank))
    ranks[index] += successRate
    numRanks[index] += 1


  plot("Time in Office vs Bill Success Rate", "Time in Office", "Bill Success Rate",
    [v["num_terms"] for v in data.itervalues()],
    [getSuccessRate(v) for v in data.itervalues()], "timeinoffice_v_success")

  plot("Number of Leadership Roles vs Bill Success Rate", "Number Leadership Roles", "Bill Success Rate",
    [v["num_leader_roles"] for v in data.itervalues()],
    [getSuccessRate(v) for v in data.itervalues()], "numLeaderRoles_v_success")

  plot("Page Rank in Committee Graph vs Bill Success Rate", "Page Rank in Committee Graph", "Bill Success Rate",
    [v["committee_pagerank"] for v in data.itervalues()],
    [getSuccessRate(v) for v in data.itervalues()], "pageRank_v_success", 1)

  plot("Btwn Score in Committee Graph vs Bill Success Rate", "Btwn Score in Committee Graph", "Bill Success Rate",
    [v["committee_btwnscore"] for v in data.itervalues()],
    [getSuccessRate(v) for v in data.itervalues()], "btwnScore_v_success", 0.6)

  plot("avg.Rank vs Bill Success Rate", "avg.Rank", "Bill Success Rate",
    [getAvgRank(v) for v in data.itervalues()],
    [getSuccessRate(v) for v in data.itervalues()], "avgLegislatorRank_v_success")

  plot("Lowest Rank vs Bill Success Rate", "Lowest Rank", "Bill Success Rate",
    [getLowestRank(v) for v in data.itervalues()],
    [getSuccessRate(v) for v in data.itervalues()], "legislatorRank_v_success")

  plot("Group Rank vs Bill Success Rate", "Group Rank", "Bill Success Rate",
    [i for i in range(len(ranks))],
    [float(ranks[i])/float(numRanks[i]) for i in range(len(ranks))], "legislatorGroupRank_v_success")


def getNumCICForBill(legData, thomas, bill):
  numCosponsorsInCommittee = 0
  for cosponsor in bill["cosponsors"]:
    if not cosponsor in legData:
      continue
    for committee in bill["committees"]:
      if committee in legData[cosponsor]["committeesMap"].keys():
        numCosponsorsInCommittee += 1
        break
        # if legData[cosponsor]["committeesMap"][committee] == 1:
  value = 0 if len(bill["committees"]) == 0 else float(numCosponsorsInCommittee)/float(len(bill["cosponsors"]))
  value = round(value, 2)
  value = value - (value % 0.04)
  return value

def plotNumConsponsorsVBillSuccess():
  stream1 = open("data/legislator-data.json", 'r')
  legData = json.load(stream1)
  stream2 = open("data/bill-data.json", 'r')
  billData = json.load(stream2)

 # key = number of cosponsors in referred committee | value = [number of bills,
 # number of successfull bills, number of out of committee bills]
  numcic_map = {}
  for (thomas, bill) in billData.iteritems():
    value = getNumCICForBill(legData, thomas, bill)
    if not numcic_map.has_key(value):
      numcic_map[value] = [1, 0, 0]
    else:
      numcic_map[value][0] += 1
    if bill["status"] not in Bill.NOT_OUT_OF_COMMITTEE:
      numcic_map[value][1] += 1
    if bill["status"] in Bill.SUCCESSFUL:
      numcic_map[value][2] += 1

  plot("Number of Cosponsors in referred Committee vs. Bill Reported Out Rate", "Num Cosponsors",
      "Bill Reported Out of Committee Rate", numcic_map.keys(),
      [float(v[1])/float(v[0]) for v in numcic_map.values()],
      "numCosponsorsInComm_v_billReported", 1)

  plot("Number of Cosponsors in referred Committee vs. Bill Success", "Num Cosponsors",
      "Bill Success", numcic_map.keys(),
      [float(v[2])/float(v[0]) for v in numcic_map.values()],
      "numCosponsorsInComm_v_billSuccess", .6)


plotNumConsponsorsVBillSuccess()
readAndPlotData()




