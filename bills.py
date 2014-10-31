import json
import snap

bill_sponsors_map = {}
sponsor_bills_map = {}

def addBillEdgesToNetwork(graph, sponsors):
  for i in range(0, len(sponsors)):
    for j in range(i+1, len(sponsors)):
      graph.AddEdge(int(sponsors[i]), int(sponsors[j]))

def createNetwork(Nodes):
  graph = snap.TUNGraph.New()
  for NId in Nodes:
    graph.AddNode(NId)
  return graph

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
getBills("hjres", 1)
createSponsorToBillsMap()
for key in sponsor_bills_map:
  print "%s : " % (key),
  bills = sponsor_bills_map[key]
  for i in range(len(bills)):
    print "%d, " % (bills[i]),
  print "\n"

graph = createNetwork(bill_sponsors_map.keys()) # creates network where a node is a bill
for thomas_id in sponsor_bills_map:
    addBillEdgesToNetwork(graph, sponsor_bills_map[thomas_id])

print "Graph has %d nodes and %d edges" % (graph.GetNodes(), graph.GetEdges())
print "Its clustering co-efficient is %f" % (snap.GetClustCf(graph))
print "Its effective diameter is %d" % (snap.GetBfsEffDiam(graph, 20, False))
DegToCntV = snap.TIntPrV()
snap.GetDegCnt(graph, DegToCntV)
for item in DegToCntV:
    print "%d nodes with degree %d" % (item.GetVal2(), item.GetVal1())

