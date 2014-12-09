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
    return float(item["num_outcomm_bills"])/float(len(item["bills"]))

def plot(title, xlabel, ylabel, xVals, yVals, filename, ymax=1, xlog=False, markersize=5):
  fig1 = plt.figure()
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.ylim(ymax=ymax)
  ax = fig1.add_subplot(111)
  if xlog:
    ax.set_xscale('log')
  plot = ax.plot(xVals, yVals, 'bo', mec='b', markersize=markersize, alpha=0.3, label="chart")
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

  timebills_map = {}
  for value in data.itervalues():
    time = value["num_terms"]
    if not timebills_map.has_key(time):
      timebills_map[time] = [len(value["bills"]), 1]
    else:
      timebills_map[time][0] += len(value["bills"])
      timebills_map[time][1] += 1

  plot("Time in Office vs Bill Out of Committee Rate", "Time in Office", "Bill Out of Committee Rate",
    [v["num_terms"] for v in data.itervalues()],
    [getSuccessRate(v) for v in data.itervalues()], "timeinoffice_v_outcomm")

  plot("Number of Leadership Roles vs Bill Out of Committee Rate", "Number Leadership Roles", "Bill Out of Committee Rate",
    [v["num_leader_roles"] for v in data.itervalues()],
    [getSuccessRate(v) for v in data.itervalues()], "numLeaderRoles_v_outcomm")

  plot("Page Rank in Committee Graph vs Bill Out of Committee Rate", "Page Rank in Committee Graph", "Bill Out of Committee Rate",
    [v["committee_pagerank"] for v in data.itervalues()],
    [getSuccessRate(v) for v in data.itervalues()], "pageRank_v_outcomm", 1)

  plot("Btwn Score in Committee Graph vs Bill Out of Committee Rate", "Btwn Score in Committee Graph", "Bill Out of Committee Rate",
    [v["committee_btwnscore"] for v in data.itervalues()],
    [getSuccessRate(v) for v in data.itervalues()], "btwnScore_v_outcomm", 1)

  plot("avg.Rank vs Bill Out of Committee Rate", "avg.Rank", "Bill Out of Committee Rate",
    [getAvgRank(v) for v in data.itervalues()],
    [getSuccessRate(v) for v in data.itervalues()], "avgLegislatorRank_v_outcomm")

  plot("Lowest Rank vs Bill Out of Committee Rate", "Lowest Rank", "Bill Out of Committee Rate",
    [getLowestRank(v) for v in data.itervalues()],
    [getSuccessRate(v) for v in data.itervalues()], "legislatorRank_v_outcomm")

  plot("Group Rank vs Bill Out of Committee Rate", "Group Rank", "Bill Out of Committee Rate",
    [i for i in range(len(ranks))],
    [float(ranks[i])/float(numRanks[i]) for i in range(len(ranks))], "legislatorGroupRank_v_outcomm")

  plot("PR Rank vs Avg. Bill Out of Committee Rate", "PR Rank", "Avg. Bill Out of Committee Rate",
    [k for k in pr_map.iterkeys()],
    [float(v[0])/float(v[1]) for v in pr_map.itervalues()], "pageRank_v_avgOutcomm", 1, False, 7)

  plot("Btwn Score vs Avg. Bill Out of Committee Rate", "Btwn Score", "Avg. Bill Out of Committee Rate",
    [k for k in btwn_map.iterkeys()],
    [float(v[0])/float(v[1]) for v in btwn_map.itervalues()], "btwnScore_v_avgOutcomm", 1, False, 7)

  plot("Terms In Office vs Avg. Bill Out of Committee Rate", "Terms In Office", "Avg. Bill Out of Committee Rate",
    [k for k in timeio_map.iterkeys()],
    [float(v[0])/float(v[1]) for v in timeio_map.itervalues()], "termsInOffice_v_avgOutComm", 1, False, 7)

  plot("Terms In Office vs Number of Bills", "Terms In Office", "Number of Bills",
    [k for k in timebills_map.iterkeys()],
    [float(v[0])/float(v[1]) for v in timebills_map.itervalues()], "avgNumBills_v_timeInOffice", 80, False, 7)

readAndPlotData()




