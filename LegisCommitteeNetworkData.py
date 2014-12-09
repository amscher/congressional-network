import json
import snap
import yaml
import Congressman
import CongressmenData as CD

def getEdgesFromCommittees(dgraph, ugraph):
  stream = open("data/committee-membership-current.yaml", 'r')
  y_stream = yaml.load(stream)

  for (k, v) in y_stream.iteritems():
    committeeId = k
    chairId = v[0]["thomas"]
    cochairId = v[1]["thomas"]
    # graph.AddEdge(int(cochairId), int(chairId))
    for i in range(2, len(v)):
      thomas = v[i]["thomas"]
      dgraph.AddEdge(int(thomas), int(chairId))
      dgraph.AddEdge(int(thomas), int(cochairId))

  for (k, v) in y_stream.iteritems():
    for i in range(len(v)):
      src = int(v[i]["thomas"])
      for j in range(i+1, len(v)):
        dst = int(v[j]["thomas"])
        ugraph.AddEdge(src, dst)


def getThomasStr(thomas):
  thomas = str(thomas)
  while (len(thomas) < 5):
    thomas = "0" + thomas
  return thomas


def addLegislatorNetworkData(thomas_data_map):
  stream = open("data/legislator-data.json", 'r')
  legData = json.load(stream)

  dgraph = snap.TNGraph.New()
  ugraph = snap.TUNGraph.New()
  for key in legData.iterkeys():
    dgraph.AddNode(int(key))
    ugraph.AddNode(int(key))

  getEdgesFromCommittees(dgraph, ugraph)
  snap.SaveEdgeList(dgraph, 'chair_member_graph.txt')
  snap.SaveEdgeList(ugraph, 'co-membership_graph.txt')


  thomas_pagerank_map = {}
  pRankH = snap.TIntFltH()
  snap.GetPageRank(dgraph, pRankH)
  for item in pRankH:
    pr = pRankH[item]
    thomas = getThomasStr(item)
    thomas_pagerank_map[thomas] = pr
    if (thomas_data_map):
      thomas_data_map[thomas].committee_pagerank = pr

  nodes = snap.TIntFltH()
  edges = snap.TIntPrFltH()
  snap.GetBetweennessCentr(ugraph, nodes, edges, 1.0)
  for node in nodes:
    btwnScore = nodes[node]
    thomas = getThomasStr(node)
    if (thomas_data_map):
      thomas_data_map[thomas].committee_btwnscore = btwnScore

if __name__ == '__main__':
  thomas_data_map = CD.dataMapFromFile()
  addLegislatorNetworkData(thomas_data_map)
  congressmanFile = open('data/legislator-data.json', 'w')
  json.dump(thomas_data_map, congressmanFile, cls=Congressman.Encoder, indent=2, separators=(',', ': '))
  print 'Total number of legislators is %d' % (len(thomas_data_map))

