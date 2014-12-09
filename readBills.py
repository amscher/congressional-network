import json
import Bill
import os
import CongressmenData as CD
import Date

def getBiPartisanScore(bill, congressmen):
  cosponsors = bill.cosponsors
  repCount = 0
  total = len(cosponsors)
  for i in range(len(cosponsors)):
    if cosponsors[i] not in congressmen:
      print "Can't find congressman ", cosponsors[i]
      continue
    congressman = congressmen[cosponsors[i]]
    if congressman.isRepublican():
      repCount += 1
  bipartisanScore = float(repCount)/float(total)
  return bipartisanScore

# Checks to see if a sufficient time has passed since the last action taken on
# on the bill, or a definitive action has taken place.
def isComplete(bill):
  lastUpdate = bill["status_at"]
  if bill["status"] in Bill.SUCCESSFUL or bill["status"] in Bill.FAILED:
    return True
  if Date.monthdelta(Date.get(lastUpdate), Date.now()) > 5:
    return True
  else:
    return False

def readBills(directory_prefix, bill_type):
  numInComplete = 0
  # MAKE SURE THIS FILE EXISTS
  congressmen = CD.dataMapFromFile()
  bills = {} # map from id-->Bill object

  bill_dir = '%sbills/%s/' % (directory_prefix, bill_type)
  for directory in os.listdir(bill_dir):
    try:
      filename = '%s%s/data.json' % (bill_dir, directory)
      stream = open(filename, 'r')
    except IOError, e:
      print "Can't open file: ", filename
      continue
    data = json.load(stream)

    sponsor = None
    cosponsors = []

    if not isComplete(data):
      numInComplete += 1
      continue

    if data["cosponsors"]:
      for i in range(len(data["cosponsors"])):
        cosponsors.append(data["cosponsors"][i]["thomas_id"])
    if data["sponsor"]:
      sponsor = data["sponsor"]["thomas_id"]
      cosponsors.append(sponsor)
    if data["status"]:
      raw_status = data["status"]
    if data["introduced_at"]:
      introduced_at = data["introduced_at"]
    bill_object = Bill.Bill(bill_type, directory, raw_status, sponsor, cosponsors, introduced_at)
    if data["actions"]:
      for action in data['actions']:
        if "vote" == action['type']:
          bill_object.addVotingRound(action['result'])
    if data["committees"]:
      for committee in data["committees"]:
        bill_object.committees.append(committee["committee_id"])
    bill_object.bipartisan_score = getBiPartisanScore(bill_object, congressmen)
    bills[directory] = bill_object

  print "Number still in action: ", numInComplete
  return bills

def readAllBills():
    bills_hr = readBills('./bill_files/113/', "hr")
    bills_s = readBills('./bill_files/113/', "s")
    bills_hjres = readBills('./bill_files/113/', "hjres")
    bills_sjres = readBills('./bill_files/113/', "sjres")
    bills = dict(bills_hr.items() + bills_s.items() + bills_hjres.items() + bills_sjres.items())
    print 'Total number of bills is %d' % (len(bills))
    return bills

def filterBillsOnlyOutOfCommittee(bills):
    out_of_committee_bills = {}
    for bill_id in bills.keys():
        if bills[bill_id].isOutOfCommittee():
            out_of_committee_bills[bill_id] = bills[bill_id]
    return out_of_committee_bills

if __name__ == '__main__':
    bills = readAllBills()
    billFile = open('data/bill-data.json', 'w')
    json.dump(bills, billFile, cls=Bill.Encoder, indent=2, separators=(',', ': '))
    print 'Total number of bills is %d' % (len(bills))



