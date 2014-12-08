import yaml
import json
import snap
import Bill
import generate_leg_success_plots as plots
import Committee

# Reads in committees-data file and returns a map of thomas ids to
# Committee objects.
def dataMapFromFile():
  stream = open("data/committees-data.json", 'r')
  data = json.load(stream)

  thomas_info_map = {}
  for (k, v) in data.iteritems():
    ct = Committee.Committee(v["name"], v["thomas_id"])
    ct.chair = v["chair"]
    ct.btwnness_score = v["btwnness_score"]
    ct.bill_success_rate = v["bill_success_rate"]
    ct.bill_outcomm_rate = v["bill_outcomm_rate"]
    ct.numbills = v["numbills"]
    thomas_info_map[k] = ct
  return thomas_info_map


def writeDataToFile(thomas_data_map):
  committeeFile = open('data/committees-data.json', 'w')
  json.dump(thomas_data_map, committeeFile, cls=Committee.Encoder, indent=2, separators=(',', ': '))
  print 'Total number of committees is %d' % (len(thomas_data_map))


def ingestCommittees(shouldWrite=False):
  stream = open("data/committees-current.yaml", 'r')
  y_stream = yaml.load(stream)

  thomas_committee_map = {}
  for i in range(len(y_stream)):
    committeeData = y_stream[i]
    thomas = committeeData["thomas_id"]
    committee = Committee.Committee(thomas, committeeData["name"])
    thomas_committee_map[thomas] = committee
    if "subcommittees" not in committeeData:
      continue
    for j in range(len(committeeData["subcommittees"])):
      sub = committeeData["subcommittees"][j]
      subId = sub["thomas_id"]
      subName = sub["name"]
      subcommittee = Committee.Committee((thomas + subId), subName)
      thomas_committee_map[thomas + subId] = subcommittee
  if shouldWrite:
    writeDataToFile(thomas_committee_map)
  return thomas_committee_map


def getNId(committeeId):
  nId = abs(hash(committeeId)) % (10 ** 8)
  return nId


def committeeGraph(committeeData):
  stream = open("data/committee-membership-current.yaml", 'r')
  committeeData = yaml.load(stream)
  graph = snap.TUNGraph.New()
  for k in committeeData.iterkeys():
    graph.AddNode(getNId(k))

  for (k, v) in legData.iteritems():
    committees = v["committeesMap"].keys()
    for i in range(len(committees)):
      for j in range(i+1, len(committees)):
        srcId = getNId(committees[i])
        dstId = getNId(committees[j])
        graph.AddEdge(srcId, dstId)
  snap.SaveEdgeList(graph, 'committee_graph.txt')
  return graph


def committeeBtwnCentrMap():
  graph = snap.LoadEdgeList(snap.PUNGraph, 'committee_graph.txt', 0, 1, '\t')
  nodes = snap.TIntFltH()
  edges = snap.TIntPrFltH()
  snap.GetBetweennessCentr(graph, nodes, edges, 1.0)
  id_btwn_map = {}
  for node in nodes:
    id_btwn_map[node] = nodes[node]
  return id_btwn_map


def addDataToCommitteeInfo():
  committeeData = dataMapFromFile()
  stream2 = open("data/bill-data-112.json", 'r')
  billData = json.load(stream2)
  id_btwn_map = committeeBtwnCentrMap()

  numbills_map = {}
  for (thomas, bill) in billData.iteritems():
    for committeeId in bill["committees"]:
      if not numbills_map.has_key(committeeId):
        numbills_map[committeeId] = [1, 0, 0]
      else:
        numbills_map[committeeId][0] += 1
      if bill["status"] not in Bill.NOT_OUT_OF_COMMITTEE:
        numbills_map[committeeId][1] += 1
      if bill["status"] in Bill.SUCCESSFUL:
        numbills_map[committeeId][2] += 1

  print "Num committees with bills ", len(numbills_map)

  for (committeeId, committee) in committeeData.iteritems():
    if not committeeId in numbills_map:
      continue
    values = numbills_map[committeeId]
    successRate = float(values[2])/float(values[0])
    outCommRate = float(values[1])/float(values[0])
    committee.numbills = values[0]
    committee.bill_success_rate = successRate
    committee.bill_outcomm_rate = outCommRate
    committee.btwnness_score = id_btwn_map[getNId(committeeId)]
    print "out of committee: %f , total: %d" % (outCommRate, committee.numbills)
  writeDataToFile(committeeData)


def genBillCommitteeCsv():
  stream2 = open("data/bill-data.json", 'r')
  billData = json.load(stream2)
  committeeData = dataMapFromFile()
  csv = open("csv/committee-historical.csv", 'w')
  for (bill_id, bill) in billData.iteritems():
    success = 0
    outcomm = 0
    for committeeId in bill["committees"]:
      committee = committeeData[committeeId]
      success = committee.bill_success_rate if committee.bill_success_rate > success else success
      outcomm = committee.bill_outcomm_rate if committee.bill_outcomm_rate > outcomm else outcomm
    csv.write("{0},{1},{2},{3},{4}\n".format(
      bill_id, 1, success, outcomm, bill["status"]))


if __name__ == '__main__':
  addDataToCommitteeInfo()
  genBillCommitteeCsv()




# Plots the committess probability of reporting/bill sucess rate vs its btwnness score
def plotCommitteeSuccessVBtwnScore():
  stream = open("data/committees-current.yaml", 'r')
  committeeData = yaml.load(stream)
  stream2 = open("data/bill-data.json", 'r')
  billData = json.load(stream2)
  id_btwn_map = committeeBtwnCentrMap()

 # key = btwnness score | value = [number of bills,
 # number of successfull bills, number of out of committee bills]
  btwn_numbills_map = {}
  for (thomas, bill) in billData.iteritems():
    value = 0
    for committeeId in bill["committees"]:
      value += id_btwn_map[getNId(committeeId)]
    value = value / 10
    if not btwn_numbills_map.has_key(value):
      btwn_numbills_map[value] = [1, 0, 0]
    else:
      btwn_numbills_map[value][0] += 1
    if bill["status"] not in Bill.NOT_OUT_OF_COMMITTEE:
      btwn_numbills_map[value][1] += 1
    if bill["status"] in Bill.SUCCESSFUL:
      btwn_numbills_map[value][2] += 1

  plots.plot("Btwnness Score of Referred Committee vs. Bill Reported Out Rate", "Btwnness Centr Score",
      "Bill Reported Out of Committee Rate", btwn_numbills_map.keys(),
      [float(v[1])/float(v[0]) for v in btwn_numbills_map.values()],
      "committeeBtwnness_v_billReported", 1)

  plots.plot("Btwnness Score of Referred Committee vs. Bill Success", "Btwnness Centr Score",
      "Bill Success", btwn_numbills_map.keys(),
      [float(v[2])/float(v[0]) for v in btwn_numbills_map.values()],
      "committeeBtwnness_v_billSuccess", 1)









