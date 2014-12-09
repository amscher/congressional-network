import json
import Congressman
import Committee
import Bill
import numpy
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
    return round(float(rankSum)/float(numCommittees))

def getSuccessRate(item):
  if len(item["bills"]) == 0:
    return 0
  else:
    # billsPerTerm = /float(item["num_terms"])
    return float(item["num_success_bills"])/float(len(item["bills"]))

def plot(title, xlabel, ylabel, xVals, yVals, filename, ymax=1, xlog=False, markersize=5, alpha=0.3):
  fig1 = plt.figure()
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.ylim(ymax=ymax)
  ax = fig1.add_subplot(111)
  plot = ax.plot(xVals, yVals, 'go', mec='g', markersize=markersize, alpha=alpha, label="chart")
  fig1.savefig('plotting/' + filename + '.png')


def scatterplot(title, xlabel, ylabel, xVals, yVals, filename, ymax=1, xlog=False, data={}):
  fig1 = plt.figure()
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.ylim(ymax=ymax)
  ax = fig1.add_subplot(111)
  plot = ax.scatter(xVals, yVals, marker='o', c='b', s=data, label='the data')
  fig1.savefig('plotting/' + filename + '.png')


def getArrayFromMulti(index, arr):
  array = []
  for i in range(len(arr)):
    array.append(arr[i][index])
  return array


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

  pr_map = {}
  for value in data.itervalues():
    pr = value["committee_pagerank"]
    pr = round(pr, 3)
    if not pr_map.has_key(pr):
      pr_map[pr] = [getSuccessRate(value), 1]
    else:
      pr_map[pr][0] += getSuccessRate(value)
      pr_map[pr][1] += 1

  btwn_map = {}
  for value in data.itervalues():
    btwn = value["committee_btwnscore"]
    btwn = round(btwn, -2)
    if not btwn_map.has_key(btwn):
      btwn_map[btwn] = [getSuccessRate(value), 1]
    else:
      btwn_map[btwn][0] += getSuccessRate(value)
      btwn_map[btwn][1] += 1

  timeio_map = {}
  for value in data.itervalues():
    time = value["num_terms"] / 5
    if not timeio_map.has_key(time):
      timeio_map[time] = [getSuccessRate(value), 1]
    else:
      timeio_map[time][0] += getSuccessRate(value)
      timeio_map[time][1] += 1

  avgRank_map = {}
  for value in data.itervalues():
    rank = getAvgRank(value)
    if not avgRank_map.has_key(rank):
      avgRank_map[rank] = [getSuccessRate(value), 1]
    else:
      avgRank_map[rank][0] += getSuccessRate(value)
      avgRank_map[rank][1] += 1

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
    [getSuccessRate(v) for v in data.itervalues()], "avgLegislatorRank_v_success", 1.1)

  plot("Lowest Rank vs Bill Success Rate", "Lowest Rank", "Bill Success Rate",
    [getLowestRank(v) for v in data.itervalues()],
    [getSuccessRate(v) for v in data.itervalues()], "legislatorRank_v_success")

  plot("Group Rank vs Bill Success Rate", "Group Rank", "Bill Success Rate",
    [i for i in range(len(ranks))],
    [float(ranks[i])/float(numRanks[i]) for i in range(len(ranks))], "legislatorGroupRank_v_success", 0.2, False, 7, 1)

  plot("PR Rank vs Avg. Bill Success Rate", "PR Rank", "Avg. Bill Success Rate",
    [k for k in pr_map.iterkeys()],
    [float(v[0])/float(v[1]) for v in pr_map.itervalues()], "pageRank_v_avgSuccess", 0.2, False, 7, 1)

  plot("Btwn Score vs Avg. Bill Success Rate", "Btwn Score", "Avg. Bill Success Rate",
    [k for k in btwn_map.iterkeys()],
    [float(v[0])/float(v[1]) for v in btwn_map.itervalues()], "btwnScore_v_avgSuccess", 0.2, False, 7, 1)

  plot("Avg. Rank vs Avg. Bill Success Rate", "Avg. Rank", "Avg. Bill Success Rate",
    [k for k in avgRank_map.iterkeys()],
    [float(v[0])/float(v[1]) for v in avgRank_map.itervalues()], "avgRank_v_avgSuccess", 1.1, False, 7)

  plot("Terms In Office vs Avg. Bill Success Rate", "Terms In Office", "Avg. Bill Success Rate",
    [k*5 for k in timeio_map.iterkeys()],
    [float(v[0])/float(v[1]) for v in timeio_map.itervalues()], "termsInOffice_v_avgSuccess", 0.2, False, 7)


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
      "numCosponsorsInComm_v_billReported", 0.6, False, 6, 1)

  plot("Number of Cosponsors in referred Committee vs. Bill Success", "Num Cosponsors",
      "Bill Success", numcic_map.keys(),
      [float(v[2])/float(v[0]) for v in numcic_map.values()],
      "numCosponsorsInComm_v_billSuccess", .2, False, 6, 1)


plotNumConsponsorsVBillSuccess()
readAndPlotData()




