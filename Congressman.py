class Congressman:
    'A class with all the attributes we need for a Congressman'
    def __init__(self):
        self.name =""
        self.thomas_id = ""
        self.num_terms = 0
        self.num_leader_roles = 0
        self.committeesMap = {} # thomas id of committee, and rank of congressman in that committee
        self.party = ""
        self.bills = []
        self.num_success_bills = 0

    def isRepublican(self):
        return self.part == "Republican"

from json import JSONEncoder
class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
