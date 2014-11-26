'''Description of what each status means: https://github.com/unitedstates/congress/wiki/bills'''
SUCCESSFUL = [ 'ENACTED:SIGNED', 'PASSED:BILL', 'PASSED:SIMPLERES', 'PASSED:CONSTAMEND', 'PASSED:CONCURRENTRES', 'ENACTED:VETO_OVERRIDE', 'ENACTED:TENDAYRULE' ]
FAILED = [ 'FAIL:ORIGINATING:HOUSE', 'PROV_KILL:SUSPENSIONFAILED', 'PROV_KILL:CLOTUREFAILED', 'FAIL:ORIGINATING:SENATE', 'FAIL:SECOND:HOUSE', 'FAIL:SECOND:SENATE', 'PROV_KILL:PINGPONGFAIL', 'PROV_KILL:VETO', 'VETOED:POCKET' ]
IN_PROGRESS = [ 'INTRODUCED', 'REFERRED', 'PASS_OVER:SENATE', 'PASS_BACK:HOUSE', 'CONFERENCE:PASSED:SENATE', 'VETOED:OVERRIDE_FAIL_ORIGINATING:HOUSE', 'VETOED:OVERRIDE_FAIL_ORIGINATING:SENATE', 'VETOED:OVERRIDE_PASS_OVER:HOUSE', 'VETOED:OVERRIDE_PASS_OVER:SENATE', 'VETOED:OVERRIDE_FAIL_SECOND:HOUSE', 'VETOED:OVERRIDE_FAIL_SECOND:SENATE', 'REPORTED', 'PASS_OVER:HOUSE', 'PASS_BACK:SENATE', 'CONFERENCE:PASSED:HOUSE' ]
#neeral:~/Documents/cs224w/project/congressional-network/bills/hr$
#grep \"status\" hr*/data.json | grep -v REFERRED | grep -v REPORTED | grep -v PASS_OVER:HOUSE | grep -v ENACTED:SIGNED | grep -v PROV_KILL:SUSPENSIONFAILED | grep -v PASSED:BILL | grep -v PASS_BACK:SENATE | grep -v FAIL:ORIGINATING:HOUSE | grep -v CONFERENCE:PASSED:HOUSE

class Bill:
    'A class with all the attributes we need for a bill'
    def __init__(self, bill_type_id, bill_id, status, sponsor, cosponsors,introduced_at):
        self.bill_type_id = bill_type_id
        self.bill_id = bill_id
        self.status = status
        self.sponsor = sponsor # thomas id
        self.cosponsors = cosponsors
        self.introduced_month = int(introduced_at[5:6]) # month when the bill was introduced: "yyyy-MM-dd" -> MM
        self.num_voting_rounds = 0
        self.num_passed_rounds = 0

    def isSuccessful(self):
        return self.status in SUCCESSFUL

    def isFailed(self):
        return self.status in FAILED

    def isInProgress(self):
        return self.status in IN_PROGRESS

    def isOutOfCommittee(self):
        return self.status not in ['INTRODUCED', 'REFERRED']

    def addVotingRound(self, result):
        self.num_voting_rounds += 1
        if 'pass' == result:
            self.num_passed_rounds += 1


