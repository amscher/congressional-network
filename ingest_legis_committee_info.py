# This file ingests all the information about current legislators, their terms served,
# leadership positions help, committee membership, and rank in committee
import json
import yaml
import Congressman
import Committee
import Bill

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

###### gets legislator's info ######
def ingestLegislators():
  stream = open("data/legislators-current.yaml", 'r')
  y_stream = yaml.load(stream)

  thomas_to_member_map = {}
  num_members = len(y_stream)

  for i in range(0, num_members):
    thomas = y_stream[i]["id"]["thomas"]
    thomas_to_member_map[thomas] = createLegislator(y_stream[i])

  return thomas_to_member_map


def ingestCommittees():
  stream = open("data/committees-current.yaml", 'r')
  y_stream = yaml.load(stream)

  thomas_committee_map = {}

  for i in range(len(y_stream)):
    thomas = y_stream[i]["thomas_id"]
    committee = Committee.Committee(thomas, y_stream[i]["name"])
    thomas_committee_map[thomas] = committee
  return thomas_committee_map


###### gets committee info for legislator ######
def ingestCommitteesForLegislator(thomas_member_map, thomas_committee_map):
  stream = open("data/committee-membership-current.yaml", 'r')
  y_stream = yaml.load(stream)

  for (k, v) in y_stream.iteritems():
    committeeId = k
    for i in range(len(v)):
      legInfo = v[i]
      thomas = legInfo["thomas"]
      legislator = thomas_member_map[thomas]
      legislator.committeesMap[committeeId] = legInfo["rank"]
      if "title" in legInfo and legInfo["title"] == "Chair":
        if not committeeId in thomas_committee_map:
          print "Couldn't find committee id ", committeeId
        else:
          thomas_committee_map[committeeId].chair = thomas


def ingestBillInfoForLegislator(thomas_member_map):
  stream = open("data/legislators-historical.yaml", 'r')
  y_stream = yaml.load(stream)
  stream = open("data/bill_data.json", 'r')
  data = json.load(stream)

  for (k,v) in data.iteritems():
    if not "sponsor" in v:
      continue
    billSponsorId = v["sponsor"]

    # If historical legislator... add to map
    if not billSponsorId in thomas_member_map:
      print "Sponsor is historic ", billSponsorId
      for index, item in enumerate(y_stream):
        if "thomas" in item["id"]:
          if item["id"]["thomas"] == billSponsorId:
            thomas_member_map[billSponsorId] = createLegislator(item)

    # if not thomas_member_map[billSponsorId]:

    thomas_member_map[billSponsorId].bills.append(k)
    if v["status"] in Bill.SUCCESSFUL:
      thomas_member_map[billSponsorId].num_success_bills += 1


def legislatorInfoMap():
  thomas_member_map = ingestLegislators()
  thomas_committee_map = ingestCommittees()
  ingestCommitteesForLegislator(thomas_member_map, thomas_committee_map)
  ingestBillInfoForLegislator(thomas_member_map)
  return thomas_member_map


if __name__ == '__main__':
  thomas_member_map = legislatorInfoMap()
  congressmanFile = open('data/legislator-data.json', 'w')
  json.dump(thomas_member_map, congressmanFile, cls=Congressman.Encoder, indent=2, separators=(',', ': '))
  print 'Total number of legislators is %d' % (len(thomas_member_map))

