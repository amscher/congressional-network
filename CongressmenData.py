# This file has functions to ingests all the information about current legislators, their terms served,
# leadership positions help, committee membership, and rank in committee
import json
import yaml
import Congressman
import Committee
import Bill
import CommitteeNetworkData as NW
import CommitteeData


# Extracts one legislators number of terms, party, name, and id from data.
def createLegislator(info):
  legislator = Congressman.Congressman()
  thomas = info["id"]["thomas"]
  legislator.thomas_id = thomas
  legislator.num_terms = len(info["terms"])
  legislator.party = info["terms"][0]["party"]
  if "official_full" in info["name"]:
    legislator.name = info["name"]["official_full"]
  else:
    legislator.name = info["name"]["first"] + " " +  info["name"]["last"]
  if "leadership_roles" in info:
    legislator.num_leader_roles = len(info["leadership_roles"])
  return legislator


# Gets all of the legislator's personal info and adds to map.
def ingestLegislators():
  stream = open("data/legislators-current.yaml", 'r')
  y_stream = yaml.load(stream)

  thomas_to_data_map = {}
  num_members = len(y_stream)

  for i in range(0, num_members):
    thomas = y_stream[i]["id"]["thomas"]
    thomas_to_data_map[thomas] = createLegislator(y_stream[i])

  return thomas_to_data_map


# Gets committee info for legislator and adds to map.
def ingestCommitteesForLegislator(thomas_data_map, thomas_committee_map):
  stream = open("data/committee-membership-current.yaml", 'r')
  y_stream = yaml.load(stream)

  for (k, v) in y_stream.iteritems():
    committeeId = k
    for i in range(len(v)):
      legInfo = v[i]
      thomas = legInfo["thomas"]
      legislator = thomas_data_map[thomas]
      legislator.committeesMap[committeeId] = legInfo["rank"]
      if "title" in legInfo and legInfo["title"] == "Chair":
        if not committeeId in thomas_committee_map:
          print "Couldn't find committee id ", committeeId
        else:
          thomas_committee_map[committeeId].chair = thomas


# Gets bill information for each Congressman, i.e. bills they sponsored
# and success rate of the bills they've sponsored and adds it to the map.
def ingestBillInfoForLegislator(thomas_data_map):
  stream = open("data/legislators-historical.yaml", 'r')
  y_stream = yaml.load(stream)
  stream = open("data/bill-data.json", 'r')
  data = json.load(stream)

  for (k,v) in data.iteritems():
    if not "sponsor" in v:
      continue
    billSponsorId = v["sponsor"]

    # If historical legislator... add to map
    if not billSponsorId in thomas_data_map:
      print "Sponsor is historic ", billSponsorId
      for index, item in enumerate(y_stream):
        if "thomas" in item["id"]:
          if item["id"]["thomas"] == billSponsorId:
            thomas_data_map[billSponsorId] = createLegislator(item)

    thomas_data_map[billSponsorId].bills.append(k)
    if v["status"] in Bill.SUCCESSFUL:
      thomas_data_map[billSponsorId].num_success_bills += 1


# Builds the entire thomas to Congressman object map from scratch
def legislatorInfoMap():
  thomas_data_map = ingestLegislators()
  thomas_committee_map = CommitteeData.ingestCommittees()
  ingestCommitteesForLegislator(thomas_data_map, thomas_committee_map)
  ingestBillInfoForLegislator(thomas_data_map)
  # NW.addLegislatorNetworkData(thomas_data_map)
  return thomas_data_map


# Writes the thomas to Congressman object map to the legislator-data file.
def writeDataToFile(thomas_data_map):
  congressmanFile = open('data/legislator-data.json', 'w')
  json.dump(thomas_data_map, congressmanFile, cls=Congressman.Encoder, indent=2, separators=(',', ': '))
  print 'Total number of legislators is %d' % (len(thomas_data_map))


# Reads in legislator-data file and returns a map of thomas ids to
# Congressman objects.
def dataMapFromFile():
  stream = open("data/legislator-data.json", 'r')
  legData = json.load(stream)

  thomas_info_map = {}
  for (k, v) in legData.iteritems():
    cm = Congressman.Congressman()
    cm.name = v["name"]
    cm.thomas_id = v["thomas_id"]
    cm.num_leader_roles = v["num_leader_roles"]
    cm.num_terms = v["num_terms"]
    cm.committeesMap = v["committeesMap"]
    cm.party = v["party"]
    cm.bills = v["bills"]
    cm.num_success_bills = v["num_success_bills"]
    cm.committee_pagerank = v["committee_pagerank"]
    cm.committee_btwnscore = v["committee_btwnscore"]
    thomas_info_map[k] = cm

  return thomas_info_map


# Generates the legislor-data file.
if __name__ == '__main__':
  thomas_data_map = legislatorInfoMap()
  writeDataToFile(thomas_data_map)
  print 'Total number of legislators is %d' % (len(thomas_data_map))

