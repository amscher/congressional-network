import json
import snap

maxSponsors = 30

bill_sponsors_map = {}
sponsor_bills_map = {}

def addEdgesToNetwork(graph, nodes):
  for i in range(0, len(nodes)):
    for j in range(i+1, len(nodes)):
      if (graph.IsEdge(int(nodes[j]), int(nodes[i])) == False):
        graph.AddEdge(int(nodes[i]), int(nodes[j]))

def createNetwork(nodes):
  graph = snap.TUNGraph.New()
  for nId in nodes:
    graph.AddNode(int(nId))
  return graph

def getBills(bill_type, bill_type_id):
  for i in range(10000):
    bill_name = "%s%d" % (bill_type, i)
    try:
      filename = "112/bills/%s/%s/data.json" % (bill_type, bill_name)
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
      if len(sponsors) > maxSponsors:
        continue
      if sponsor in sponsor_bills_map:
        sponsor_bills_map[sponsor].append(key)
      else:
        sponsor_bills_map[sponsor] = [key]

getBills("hr", "1")
getBills("s", "2")
createSponsorToBillsMap()
print "Number of sponsers = ", len(sponsor_bills_map)
# for key in sponsor_bills_map:
#   print "%s : " % (key),
#   bills = sponsor_bills_map[key]
#   for i in range(len(bills)):
#     print "%d, " % (bills[i]),
#   print "\n"

def createGraphsWithData(nodeMap, edgeMap, limit):
  graph = createNetwork(nodeMap.keys())
  for node in edgeMap:
    edges = edgeMap[node]
    if limit and len(edges) > maxSponsors:
      continue
    addEdgesToNetwork(graph, edges)
  snap.PrintInfo(graph)


  maxDegNId = snap.GetMxDegNId(graph)
  numDeg = graph.GetNI(maxDegNId).GetDeg()
  print "Graph has %d nodes and %d edges" % (graph.GetNodes(), graph.GetEdges())
  print "Its clustering co-efficient is %f" % (snap.GetClustCf(graph))
  print "Its effective diameter is %d" % (snap.GetBfsFullDiam(graph, 5, False))
  return graph



print "/* BILL <--[cosponsors]--> BILL */"
billGraph = createGraphsWithData(bill_sponsors_map, sponsor_bills_map, False)
maxDegNId = snap.GetMxDegNId(billGraph)
numDeg = billGraph.GetNI(maxDegNId).GetDeg()
snap.PlotOutDegDistr(billGraph, "billGraph", "billGraph- out-degree Distribution")
print "Max degree [%d] :: bill hr%d with %d co-sponsors" % (numDeg, maxDegNId, len(bill_sponsors_map[maxDegNId]))


print "/* LEGISLATOR <--[cosponsors]--> LEGISLATOR */"
sponsorGraph = createGraphsWithData(sponsor_bills_map, bill_sponsors_map, True)
snap.PlotOutDegDistr(sponsorGraph, "sponsorGraph", "sponsorGraph- out-degree Distribution")

