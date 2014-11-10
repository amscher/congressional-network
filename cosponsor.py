import json
import snap

bill_sponsors_map = {}
sponsor_bills_map = {}
sponsors = []

def addBillEdgesToNetwork(graph, bills):
  for i in range(0, len(bills)):
    for j in range(i+1, len(bills)):
      if (graph.IsEdge(bills[j], bills[i]) == False or graph.IsEdge(bills[i], bills[j]) == False):
        graph.AddEdge(bills[i], bills[j])

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
    if len(sponsors) > 5:
      continue
    for i in range(len(sponsors)):
      sponsor = sponsors[i]
      if sponsor in sponsor_bills_map:
        sponsor_bills_map[sponsor].append(key)
      else:
        sponsor_bills_map[sponsor] = [key]

getBills("s", "1")
# getBills("hjres", "2")
createSponsorToBillsMap()
print "Number of sponsers = ", len(sponsor_bills_map)

getBills("hr", "1")

graph = createNetwork(sponsor_bills_map.keys()) # creates network where a node is a bill
for thomas_id in sponsor_bills_map:
    addBillEdgesToNetwork(graph, sponsor_bills_map[thomas_id])


maxDegNId = snap.GetMxDegNId(graph)
numDeg = graph.GetNI(maxDegNId).GetDeg()
print "Max degree [%d] :: legislator %s with %d bills" % (numDeg, maxDegNId, len(bill_sponsors_map[maxDegNId]))
print "Graph has %d nodes and %d edges" % (graph.GetNodes(), graph.GetEdges())
print "Its clustering co-efficient is %f" % (snap.GetClustCf(graph))
print "Its effective diameter is %d" % (snap.GetBfsEffDiam(graph, 50, False))