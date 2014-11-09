import snap
import fec_parser
from code.readBills import readBills
import readCandidateData
from matplotlib import pyplot

def getEdgeWeight(node1, node2, weightDict):
	edgeName = str(node1) + "," + str(node2)
	return weightDict[edgeName]

def setEdgeWeight(node1, node2, weightDict, edgeWeight):
	edgeName = str(node1) + "," + str(node2)
	weightDict[edgeName] = edgeWeight

def calculateCountOfStatuses(bills):
  count_successful  = 0
  count_failed      = 0
  count_in_progress = 0

  for key in bills:
    bill = bills[key]
    if bill.isSuccessful():
      count_successful += 1
    elif bill.isFailed():
      count_failed += 1
    elif bill.isInProgress():
      count_in_progress += 1
    else:
      print '*** ENCOUNTERED A NEW TYPE OF STATUS << %s >> - please categorise it ***' % (status)
  return (count_successful, count_failed, count_in_progress)

def find_next_x_value(cache, x):
    while x in cache:
        x += 1
    return x

c = fec_parser.readFECdata('FEC/')
print len(c)
print c.get('H4OK06056').name
print c.get('H4OK06056').displayCandidate()

G = snap.LoadEdgeList(snap.PUNGraph, 'co-membership_of_committees.txt')
print 'Loaded G with %d nodes and %d edges' % (G.GetNodes(), G.GetEdges())

snap.PrintInfo(G, "Python type PNGraph", "info-pngraph.txt", False)

DegToCntV = snap.TIntPrV()
snap.GetDegCnt(G, DegToCntV)
deg_distr_key = []
deg_distr_count = []
for item in DegToCntV:
    deg_distr_key.append(item.GetVal1())
    deg_distr_count.append(item.GetVal2())
# plot degree-distribution
pyplot.plot(deg_distr_key,deg_distr_count)
pyplot.title('plot of degree distribution of the graph of co-membership of committees')
pyplot.xlabel('degree / k')
pyplot.ylabel('count of nodes')
pyplot.show()


MxDegNId = snap.GetMxDegNId(G)
print 'The node with highest degree has %d edges.' % G.GetNI(MxDegNId).GetDeg()
print 'Fraction of nodes in the largest strongly connected component: %f' % snap.GetMxSccSz(G)
print 'Fraction of nodes in the largest weakly connected component: %f' % snap.GetMxWccSz(G)
print 'Is the graph connected? %s. It actually isn\'t as any isolated nodes aren\'t saved by snap.py' % (snap.IsConnected(G))
print 'The diameter of G is %d and its effective diameter is %f.' % (snap.GetBfsFullDiam(G, 20), snap.GetBfsEffDiam(G, 20))

bills_hr = readBills('code/', "hr")
bills_s = readBills('code/', "s")
bills_hjres = readBills('code/', "hjres")
bills_sjres = readBills('code/', "sjres")
bills = dict(bills_hr.items() + bills_s.items() + bills_hjres.items() + bills_sjres.items())
print 'Total number of bills is %d' % (len(bills))
print calculateCountOfStatuses(bills)

candidates = readCandidateData.readLegislators()
print 'Number of candidates from readCandidateData.readLegislators(): %d' % len(candidates)

for thomas_id in candidates.keys():
    if hasattr(candidates[thomas_id], 'FEC_Id'):
        FEC_Ids = candidates[thomas_id].FEC_Id
        for FEC_Id in FEC_Ids:
            if FEC_Id in c:
                c[FEC_Id].thomas_id = thomas_id
                candidates[thomas_id] = c[FEC_Id] #swap objects

for bill_id in bills.keys():
    bill = bills[bill_id]
    sponsor = bill.sponsor
    if sponsor not in candidates.keys():
        continue
    legislator = candidates[sponsor]
    if bill.isSuccessful():
        legislator.incrementSuccessfulCount()
    elif bill.isFailed():
        legislator.incrementFailedCount()
    else:
        legislator.incrementInProgressCount()
    legislator.num_voting_rounds += bill.num_voting_rounds
    legislator.num_passed_rounds += bill.num_passed_rounds
###############################################
# now we can plot $ against bills success:failed
plotData = {}
for thomas_id in candidates.keys():
    legislator = candidates[thomas_id]
    spending = legislator.amount
    completed_bills = legislator.failed + legislator.successful
    success_ratio = legislator.successful / float( 1 if completed_bills == 0 else completed_bills )
    if spending in plotData:
        # a hack against duplicate x-values
        spending = find_next_x_value(plotData, spending)
    plotData[spending] = success_ratio
print 'number of points to plot: %d' % len(plotData)
pyplot.plot(plotData.keys(), plotData.values(), '.')
###############################################
# taking into account In Progress bills too
plotData = {}
for thomas_id in candidates.keys():
    legislator = candidates[thomas_id]
    spending = legislator.amount
    completed_bills = legislator.failed + legislator.successful + legislator.inprogress
    success_ratio = legislator.successful / float( 1 if completed_bills == 0 else completed_bills )
    #print  'completed_bills:', completed_bills, 'success-ratio:', success_ratio, '#successful:', legislator.successful
    if spending in plotData:
        # a hack against duplicate x-values
        spending = find_next_x_value(plotData, spending)
    plotData[spending] = success_ratio
print 'number of points to plot: %d' % len(plotData)
pyplot.plot(plotData.keys(), plotData.values(), '.')
###############################################
# plotting each round of voting
plotData = {}
for thomas_id in candidates.keys():
    legislator = candidates[thomas_id]
    spending = legislator.amount
    success_ratio = legislator.num_passed_rounds / float( 1 if legislator.num_voting_rounds == 0 else legislator.num_voting_rounds )
    # a hack against duplicate x-values
    spending = find_next_x_value(plotData, spending)
    plotData[spending] = success_ratio
print 'number of points to plot: %d' % len(plotData)
pyplot.plot(plotData.keys(), plotData.values(), '.')

pyplot.title(['Plot of success-ratio of bils/in voting rounds\nfor each legislator against $ spend in campaign financing'])
pyplot.legend(['success-ratio', 'success-ratio including in-progress bills', 'success-ratio in voting rounds'])
pyplot.xlabel('Spend in $')
pyplot.ylabel('Fraction of successful bills/voting-rounds')
pyplot.show()

print calculateCountOfStatuses(bills)

