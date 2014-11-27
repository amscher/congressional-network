import snap
import yaml
from readBills import readBills
from matplotlib import pyplot
from math import log

score_map = {
  "INTRODUCED" : 0,
  "REFERRED" : 1,
  "REPORTED" : 2,
  "PASS_OVER:SENATE": 3,
  "PASS_OVER:HOUSE": 3,
  "PASSED:BILL": 4,
  "ENACTED:SIGNED" : 5
}

stream = open("data/legislators-current.yaml", 'r')
y_stream = yaml.load(stream)

thomas_to_wing_map = {}
num_members = len(y_stream)

for i in range(0, num_members):
    thomas = y_stream[i]["id"]["thomas"]
    party = y_stream[i]["terms"][0]["party"]
    thomas_to_wing_map[thomas] = party

bills = readBills('./montana/113/', "hr")
# bills_s = readBills('./montana/112/', "s")
# bills_hjres = readBills('./montana/112/', "hjres")
# bills_sjres = readBills('./montana/112/', "sjres")
# bills = dict(bills_hr.items() + bills_s.items() + bills_hjres.items() + bills_sjres.items())


score_number_file = open("bill-numbercosponsors.tab", 'w')
score_status_file = open("bill-bipartisan.tab", 'w')
score_status_count_file = open("bill-bipartisan-count.tab", 'w')
bill_id_to_score_file = open("bill-bipartisan.csv", 'w')
score_number_map = {}

bipartisan_score_count_map = {}

for bill_id in bills.keys():
    bill = bills[bill_id]
    sponsor = bill.sponsor
    cosponsors = bill.cosponsors
    total = len(cosponsors)
    repCount = 0
    for i in range(len(cosponsors)):
      if not thomas_to_wing_map.has_key(cosponsors[i]):
        print "No congressman ", cosponsors[i]
        continue
      party = thomas_to_wing_map[cosponsors[i]]
      if party == "Republican":
        repCount += 1
    print "republicans: %d, total: %d" % (repCount, total)
    if score_map.has_key(bill.status):
      bipartisanScore = float(repCount)/float(total)

      binnedScore = round(bipartisanScore, 1)
      bill_id_to_score_file.write("{0}, {1}\n".format(bill_id, binnedScore))

      # Used for calculating the percantage of enacted bills per bipartisan score
      if bipartisan_score_count_map.has_key(binnedScore):
        bipartisan_score_count_map[binnedScore][1] += 1
      else:
        bipartisan_score_count_map[binnedScore] = [0, 1]
      if bill.status == "ENACTED:SIGNED":
        bipartisan_score_count_map[binnedScore][0] += 1

      # creates score vs status data
      score_status_file.write("{0} {1}\n".format(binnedScore, score_map[bill.status]))

      # Creates number of cosponsor data
      # score_number_file.write("{0} {1}\n".format(len(cosponsors), score_map[bill.status]))
      numCosponsors = len(cosponsors) / 15
      if score_number_map.has_key(numCosponsors):
        score_number_map[numCosponsors][1] += 1
      else:
        score_number_map[numCosponsors] = [0, 1]
      if bill.status == "ENACTED:SIGNED":
        score_number_map[numCosponsors][0] += 1

for key in bipartisan_score_count_map.keys():
  success = bipartisan_score_count_map[key][0]
  total = bipartisan_score_count_map[key][1]
  score_status_count_file.write("{0} {1}\n".format(key, float(success)/float(total)))

for key in score_number_map.keys():
  success = score_number_map[key][0]
  total = score_number_map[key][1]
  score_number_file.write("{0} {1}\n".format(key, float(success)/float(total)))











