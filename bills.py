import json
import snap

bill_sponsors_map = {}

def addBillEdgesToNetwork(G, sponsors):
  for i in range(0, len(sponsors)):
    for j in range(i+1, len(sponsors)):
      G.AddEdge(int(sponsors[i]), int(sponsors[j]))

def createNetwork(Nodes):
  G = snap.TUNGraph.New()
  for NId in Nodes:
    G.AddNode(NId)
  return G

def getBills(bill_type, bill_type_id):
  for i in range(1000):
    bill_name = "%s%d" % (bill_type, i)
    try:
      filename = "bills/%s/%s/data.json" % (bill_type, bill_name)
      stream = open(filename, 'r')
    except IOError, e:
      print "Can't open file: ", filename
      continue
    data = json.load(stream)

    cosponsors = []
    if data["cosponsors"]:
      for i in range(len(data["cosponsors"])):
        cosponsors.append(data["cosponsors"][i]["thomas_id"])

    if data["sponsor"]:
      cosponsors.append(data["sponsor"]["thomas_id"])

    bill_id = bill_name.strip(bill_type)
    bill_id = "%s%s" % (bill_type_id, bill_id)
    bill_sponsors_map[int(bill_id)] = cosponsors

sponsor_bills_map = {}

def createSponsorToBillsMap():
  for key in bill_sponsors_map:
    sponsors = bill_sponsors_map[key]
    for i in range(len(sponsors)):
      sponsor = sponsors[i]
      if sponsor in sponsor_bills_map:
        sponsor_bills_map[sponsor].append(key)
      else:
        sponsor_bills_map[sponsor] = [key]

getBills("hr", 0)
createSponsorToBillsMap()

G = createNetwork(bill_sponsors_map.keys()) # creates network where a node is a bill
for thomas_id in sponsor_bills_map:
    addBillEdgesToNetwork(G, sponsor_bills_map[thomas_id])

print "Graph has %d nodes and %d edges" % (G.GetNodes(), G.GetEdges())
print "Its clustering co-efficient is %f" % (snap.GetClustCf(G))


