import Congressman
import Bill


def getNId(billId):
  billId.replace("hjres", "1")
  billId.replace("hr", "2")
  billId.replace("sjres", "3")
  billId.replace("s", "4")
  return int(billId)

def billGraph():
  stream = open("data/legislator-data.json", 'r')
  legData = json.load(stream)
  stream2 = open("data/bill-data.json", 'r')
  billData = json.load(stream2)

  graph = snap.TUNGraph.New()
  for key in billData.iterkeys():
    ugraph.AddNode(getNId(key))

  # Add edges
  for v in legData.itervalues():
    bills = v["bills"]
    for i in range(len(bills)):
      bill = bills[b]
