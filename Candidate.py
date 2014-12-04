class Candidate:
    def __init__(self):
        '''Initialise all number fields to zero'''
        self.amount = 0
        self.successful = 0
        self.failed = 0
        self.inprogress = 0
        self.num_voting_rounds = 0
        self.num_passed_rounds = 0

    def displayCandidate(self):
        return "FEC Id:", self.FEC_Id, "Name:", self.name, "Amount:", self.amount, "Party:", self.party

    def incrementSuccessfulCount(self):
        self.successful += 1

    def incrementFailedCount(self):
        self.failed += 1

    def incrementInProgressCount(self):
        self.inprogress += 1

    def getTotalNumberOfBills(self):
        return self.successful + self.failed + self.inprogress
