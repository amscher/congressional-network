import json
import Bill
import os

def readBills(directory_prefix, bill_type):
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
    if data["cosponsors"]:
      for i in range(len(data["cosponsors"])):
        cosponsors.append(data["cosponsors"][i]["thomas_id"])
    if data["sponsor"]:
        sponsor = data["sponsor"]["thomas_id"]
        cosponsors.append(sponsor)
    if data["status"]:
        raw_status = data["status"]
    bill_object = Bill.Bill(bill_type, directory, raw_status, sponsor, cosponsors)

    if data["actions"]:
        for action in data['actions']:
            if "vote" == action['type']:
                bill_object.addVotingRound(action['result'])
    bills[directory] = bill_object
  return bills



if __name__ == '__main__':
    bills = readBills('', "hr")
    print 'Total number of bills is %d' % (len(bills))



