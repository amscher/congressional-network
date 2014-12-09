import json
import math
from numpy import mean, median, std
from scipy import stats

def readAndPlotData():
  stream = open("data/legislator-data.json", 'r')
  data = json.load(stream)

  numBills = []
  numTerms = []
  numCommittees = []
  numChairPos = []
  numLeadershipRoles = []
  for v in data.itervalues():
    numBills.append(len(v["bills"]))
    numTerms.append(v["num_terms"])
    numCommittees.append(len(v["committeesMap"]))
    chairs = 0
    for i in v["committeesMap"].values():
      if i == 1:
        chairs += 1
    numChairPos.append(chairs)
    numLeadershipRoles.append(v["num_leader_roles"])

  print "__STATS"
  print "--------------------- MEAN -------- MEDIAN -------- STD ----- [MIN, MAX] "
  print "Number of bills:      %.2f         %.2f         %.2f       (%d, %d)" % (round(mean(numBills),2), round(median(numBills),2), round(std(numBills),2), min(numBills), max(numBills))
  print "Number of terms:      %.2f          %.2f          %.2f        (%d, %d)" % (round(mean(numTerms),2), round(median(numTerms),2), round(std(numTerms),2), min(numTerms), max(numTerms))
  print "Number of comms:      %.2f          %.2f          %.2f        (%d, %d)" % (round(mean(numCommittees),2), round(median(numCommittees),2), round(std(numCommittees),2), min(numCommittees), max(numCommittees))
  print "Number of chairs:     %.2f          %.2f          %.2f        (%d, %d)" % (round(mean(numChairPos),2), round(median(numChairPos),2), round(std(numChairPos),2), min(numChairPos), max(numChairPos))
  print "Number of leader:     %.2f          %.2f          %.2f        (%d, %d)" % (round(mean(numLeadershipRoles),2), round(median(numLeadershipRoles),2), round(std(numLeadershipRoles),2), min(numLeadershipRoles), max(numLeadershipRoles))


readAndPlotData()