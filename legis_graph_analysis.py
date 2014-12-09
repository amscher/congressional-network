import snap

def getStats(G, degreeFileName, description):
  MxDegNId = snap.GetMxDegNId(G)
  print 'The node with highest degree has %d edges.' % G.GetNI(MxDegNId).GetDeg()
  print 'Fraction of nodes in the largest strongly connected component: %f' % snap.GetMxSccSz(G)
  print 'Fraction of nodes in the largest weakly connected component: %f' % snap.GetMxWccSz(G)
  print 'Is the graph connected? %s. It actually isn\'t as any isolated nodes aren\'t saved by snap.py' % (snap.IsConnected(G))
  print 'The diameter of G is %d and its effective diameter is %f.' % (snap.GetBfsFullDiam(G, 20), snap.GetBfsEffDiam(G, 20))
  print 'Its clustering coefficient is %f' % (snap.GetClustCf(G))
  snap.PlotInDegDistr(G, degreeFileName, description)


def analyze():
  committeeG = snap.LoadEdgeList(snap.PUNGraph, 'co-membership_of_committees.txt', 0, 1, '\t')
  memberG = snap.LoadEdgeList(snap.PUNGraph, 'co-membership_graph.txt', 0, 1, '\t')
  chairG = snap.LoadEdgeList(snap.PUNGraph, 'chair_member_graph.txt', 0, 1, '\t')

  print "-------- COMMITTEE GRAPH ----------"
  getStats(committeeG, "commitee_graph_dd", "Undirected Graph - Committees as Nodes, shared members as edges - Degree Distribution")

  print "-------- MEMBER GRAPH ----------"
  getStats(memberG, "co-membership_graph_dd", "Undirected Graph - Legislator as Nodes, co-membership defines edges - Degree Distribution")

  print "-------- CHAIR GRAPH ----------"
  getStats(chairG, "chair-member_graph_dd", "Directed Graph - Legislator as Nodes, edges from members to committee chair/co-chair - Degree Distribution")

analyze()