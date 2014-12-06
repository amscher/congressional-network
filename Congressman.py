class Congressman:
    'A class with all the attributes we need for a Congressman'
    def __init__(self, thomas_id, num_terms, leadership_positions, committees, party):
        self.thomas_id = thomas_id
        self.num_terms = num_terms
        self.leadership_positions = leadership_positions
        self.committeesMap = {} # thomas id of committee, and rank of congressman in that committee
        self.party = party
        self.bills = []
        self.num_success_bills = 0

    def isRepublican(self):
        return self.part == "Republican"