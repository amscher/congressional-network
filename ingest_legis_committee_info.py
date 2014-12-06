# This file ingests all the information about current legislators, their terms served,
# leadership positions help, committee membership, and rank in committee

import yaml
import Congressman
import Committee
import Bill

###### gets legislator's info ######
def ingestLegislators():
  stream = open("data/legislators-current.yaml", 'r')
  y_stream = yaml.load(stream)

  thomas_to_member_map = {}
  num_members = len(y_stream)

  for i in range(0, num_members):
    legislator = Congressman.Congressman()

    thomas = y_stream[i]["id"]["thomas"]
    legislator.thomas_id = thomas
    legislator.num_terms = len(y_stream[i]["terms"])
    legislator.party = y_stream[i]["terms"][0]["party"]

    thomas_to_member_map[thomas] = legislator

  return thomas_to_member_map


def ingestCommittees():
  stream = open("data/committees-current.yaml", 'r')
  y_stream = yaml.load(stream)

  thomas_committee_map = {}

  for i in range(len(y_stream)):
    committee = Committee.Committee()
    thomas = y_stream[i]["thomas_id"]
    committee.thomas_id = thomas
    committee.name = y_stream[i]["name"]
    thomas_committee_map[thomas] = committee


###### gets committee info for legislator ######
def ingestCommitteesForLegislator(thomas_member_map, thomas_committee_map):
  stream = open("data/committee-membership-current.yaml", 'r')
  y_stream = yaml.load(stream)

  for (k, v) in y_stream:
    committeeId = k
    for i in range(len(v)):
      legInfo = v[i]
      legislator = thomas_member_map[legInfo["thomas"]]
      legislator.committeesMap[committeeId] = legInfo["rank"]
      if legInfo["title"] == "Chair":
        thomas_committee_map[committeeId].chair = legInfo["thomas"]


def ingestBillInfoForLegislator(thomas_member_map):
  stream = open("data/bill_data.json", 'r')
  data = json.load(stream)

  for (k,v) in data:
    if not v["sponsor"]:
      continue
    billSponsorId = v["sponsor"]
    thomas_member_map[billSponsorId].bills.append(k)
    if v["status"] in Bill.SUCCESSFUL:
      thomas_member_map[billSponsorId] += 1


def legislatorInfoMap():
  thomas_member_map = ingestLegislators()
  thomas_committee_map = ingestCommittees()
  ingestCommitteesForLegislator(thomas_member_map, thomas_committee_map)
  return thomas_member_map


if __name__ == '__main__':
    thomas_member_map = legislatorInfoMap()
    print 'Total number of legislators is %d' % (len(thomas_member_map))

