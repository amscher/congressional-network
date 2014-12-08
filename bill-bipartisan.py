import snap
import yaml
from readBills import readBills
import Bill
import matplotlib
import matplotlib.pyplot as plt

score_map = {
  "INTRODUCED" : 0,
  "REFERRED" : 1,
  "REPORTED" : 2,
  "PASS_OVER:SENATE": 3,
  "PASS_OVER:HOUSE": 3,
  "PASSED:BILL": 4,
  "ENACTED:SIGNED" : 5
}

def plot(title, xlabel, ylabel, xVals, yVals, filename, ymax=1):
  fig1 = plt.figure()
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.ylim(ymax=ymax)
  ax = fig1.add_subplot(111)
  plot = ax.plot(xVals, yVals, 'bo', mec='b', markersize=5, alpha=0.3, label="chart")
  fig1.savefig('plotting/' + filename + '.png')

score_numcosponsor_map = {}
bipartisan_score_count_map = {}
score_status_map = {}

def plotBiPartisanVSuccess():
  stream = open("data/bill-data.json", 'r')
  bills = yaml.load(stream)

  bill_id_to_score_file = open("csv/bill-bipartisan_2.csv", 'w')

  for bill_id in bills.iterkeys():
    bill = bills[bill_id]
    status = bill["status"]
    bipartisanScore = bill["bipartisan_score"]
    binnedScore = round(bipartisanScore, 2)
    binnedScore = binnedScore - (binnedScore % 0.04)
    bill_id_to_score_file.write("{0}, {1}, {2}, {3}\n".format(bill_id, binnedScore, bipartisanScore, status))

    if score_map.has_key(status):
      # Used for calculating the percantage of enacted bills per bipartisan score
      if bipartisan_score_count_map.has_key(binnedScore):
        bipartisan_score_count_map[binnedScore][0] += 1
      else:
        bipartisan_score_count_map[binnedScore] = [1, 0, 0]
      if status in Bill.SUCCESSFUL:
        bipartisan_score_count_map[binnedScore][1] += 1
      if status not in Bill.NOT_OUT_OF_COMMITTEE:
        bipartisan_score_count_map[binnedScore][2] += 1

      # creates score vs status data
      score_status_map[bipartisanScore] = score_map[status]

      numCosponsors = len(bill["cosponsors"]) / 5
      if score_numcosponsor_map.has_key(numCosponsors):
        score_numcosponsor_map[numCosponsors][0] += 1
      else:
        score_numcosponsor_map[numCosponsors] = [1, 0]
      if status in Bill.SUCCESSFUL:
        score_numcosponsor_map[numCosponsors][1] += 1

plotBiPartisanVSuccess()

plot("Percent Republican vs Bill Success", "Percent Republican", "Bill Success",
    [k for k in score_status_map.iterkeys()],
    [v for v in score_status_map.itervalues()], "bill-bipartisan", 6)

plot("Percent Republican vs Bill Success", "Percent Republican", "Bill Success",
    [k for k in bipartisan_score_count_map.iterkeys()],
    [float(v[1])/float(v[0]) for v in bipartisan_score_count_map.itervalues()], "bill-bipartisan-count", 0.2)

plot("Number Cosponsors vs Bill Success", "Number Cosponsors", "Bill Success",
    [k for k in score_numcosponsor_map.iterkeys()],
    [float(v[1])/float(v[0]) for v in score_numcosponsor_map.itervalues()], "bill-numbercosponsors", 1.1)







