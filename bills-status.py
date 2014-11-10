import json

status_map = {
  "INTRODUCED" : 0,
  "REFERRED" : 0.2,
  "REPORTED" : 0.4,
  "PASS_OVER:SENATE": 0.6,
  "PASS_OVER:HOUSE": 0.8,
  "ENACTED:SIGNED" : 1.0
}

bill_status_score = {}
bill_status_map = {}

def getBills(bill_type):
  for i in range(1000):
    bill_name = "%s%d" % (bill_type, i)
    try:
      filename = "bills/%s/%s/data.json" % (bill_type, bill_name)
      stream = open(filename, 'r')
    except IOError, e:
      # print "Can't open file: ", filename
      continue
    data = json.load(stream)

    bill_info = {}
    bill_info["status"] = data["status"]
    bill_info["status_at"] = data["status_at"]
    bill_info["introduced_at"] = data["introduced_at"]

    bill_status_map[bill_name] = bill_info

getBills("hr")
getBills("hjres")
getBills("s")

def plotBillsAgainstTime():
  bill_scores = open("billscores.tab", 'w')

  for key in bill_status_map.keys():
    status = bill_status_map[key]["status"]
    score = 0
    if (status_map.has_key(status)):
      score = status_map[status]
    else:
      print status
      continue
    time = bill_status_map[key]["introduced_at"].replace("-", "")
    time = time.replace("2013", "")
    time = int(time.replace("2014", ""))
    print "%d -- %f" % (time, score)
    bill_scores.write('{0} {1}\n'.format(time, score))

plotBillsAgainstTime()