# This file ingests all the information about current legislators, their terms served,
# leadership positions help, committee membership, and rank in committee

import yaml
import Congressman

###### gets a map of legislators with fec ids ######
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


def ingestCommitteesForLegislator():