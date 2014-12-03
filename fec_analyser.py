'''This is similar to neeral_analyse_graph.py except it now buckets the contribution amounts and also has levels of success.
The buckets are defined in $10,000 intervals.
The levels of success is borrowed from Montana's work.
'''

import csv
import math
import fec_parser
import readBills
import readCandidateData
from matplotlib import pyplot


# adapted from montana/bills-status.py
status_map = {
  "FAILED" : 0, # not a real state
  "INTRODUCED" : 1,
  "REFERRED" : 2,
  "REPORTED" : 3,
  "PASS_OVER:SENATE": 4,
  "PASS_OVER:HOUSE": 4,
  "PASS_BACK:SENATE": 4.5,
  "PASS_BACK:HOUSE": 4.5,
  "SUCCESSFUL" : 5 # not a real state
}
max_score = 5.0
BUCKET_SIZE = 5000

def roundup(x):
    return math.ceil(x/float(BUCKET_SIZE))*BUCKET_SIZE


# read FEC data on contributions to candidates
c = fec_parser.readFECdata('FEC/')
print 'Number of candidates read in from FEC data file: %d' %len(c)
print 'Candidate[H4OK06056] =', c.get('H4OK06056').displayCandidate()

# read the bills
bills = readBills.readAllBills()

# read the legislators files
candidates = readCandidateData.readLegislators()
print 'Number of candidates from readCandidateData.readLegislators(): %d' % len(candidates)

# merge candidates from the FEC data and YAML Legislators file
for thomas_id in candidates.keys():
    if hasattr(candidates[thomas_id], 'FEC_Id'):
        FEC_Ids = candidates[thomas_id].FEC_Id
        for FEC_Id in FEC_Ids:
            if FEC_Id in c:
                c[FEC_Id].thomas_id = thomas_id
                candidates[thomas_id] = c[FEC_Id] #swap objects

# populate statistics on the success of a legislator's bills
# and how their bill fared in voting rounds
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

# bucket the status
for bill_id in bills.keys():
    bill = bills[bill_id]
    status = bill.status
    if bill.isSuccessful():
        score = status_map['SUCCESSFUL'] # 1
    elif bill.isFailed():
        score = status_map['FAILED']     # 0
    else:
        score = status_map[status]
    setattr(bill, 'bucket_status', score / max_score)

# bucket the financial contribution
for bill_id in bills.keys():
    bill = bills[bill_id]
    sponsor = bill.sponsor
    if sponsor in candidates:
        spending = candidates[sponsor].amount
        num_bills = candidates[sponsor].getTotalNumberOfBills()
        setattr(bill, 'amount', spending/float(num_bills))
        setattr(bill, 'bucket_amount', roundup(spending/float(num_bills)))
    for cosponsor in bill.cosponsors:
        amount = getattr(bill, 'amount', 0)
        if cosponsor in candidates:
            spending = candidates[cosponsor].amount
            num_bills = candidates[cosponsor].getTotalNumberOfBills()
            if num_bills == 0:
                continue
            amount += spending/float(num_bills)
        setattr(bill, 'co-amount', amount)
        setattr(bill, 'bucket_co-amount', roundup(amount))
    
    

# aggregating the bills into their buckets
plotData = {}
co_plotData = {}
for bill_id in bills.keys():
    bill = bills[bill_id]
    spending = getattr(bill, 'bucket_amount', 0)
    co_spending = getattr(bill, 'bucket_co-amount', 0)
    status = getattr(bill, 'bucket_status')
    if (spending, status) not in plotData:
        plotData[(spending, status)] = 0
    if (co_spending, status) not in co_plotData:
        co_plotData[(co_spending, status)] = 0
    plotData[(spending, status)] = plotData[(spending, status)] + 1
    co_plotData[(co_spending, status)] = co_plotData[(co_spending, status)] + 1

# plotting $ spend against success per bill
x = [] # spending/$
y = [] # success/status
s = [] # size/count
for (spending, status) in plotData.keys():
    x.append(spending)
    y.append(status)
    s.append(plotData[(spending, status)])
print 'number of points to plot: %d' % len(plotData)
print 'highest spend = $%d' % max(x)
pyplot.scatter(x, y, s=s)

pyplot.title('Plot of success-ratio of bills against spending per bill - both are buckets')
pyplot.xlabel('Spend in $')
pyplot.ylabel('Successfulness of bills')
pyplot.xlim([0, 2000000])
pyplot.ylim([0, 1])
pyplot.show()


# plotting co-sponsors $ spend against success per bill
x = [] # co-sponsors spending/$
y = [] # success/status
s = [] # size/count
for (co_spending, status) in co_plotData.keys():
    x.append(co_spending)
    y.append(status)
    s.append(co_plotData[(co_spending, status)])
print 'number of points to plot: %d' % len(co_plotData)
print 'highest spend = $%d' % max(x)
pyplot.scatter(x, y, s=s)

pyplot.title('Plot of success-ratio of bills against spending per bill - both are buckets')
pyplot.xlabel('Spend of all cosponsors of a bill in $')
pyplot.ylabel('Successfulness of bills')
pyplot.xlim([0, 4000000])
pyplot.ylim([0, 1])
pyplot.show()


# write data to a CSV file
def write_csv(file_path, bills):
    print 'Writing to file %s' % file_path
    csv_file = csv.writer(open('file_path', 'wb+'))
    with open(file_path, 'wb+') as fin:
        csv_file = csv.writer(fin)
        csv_file.writerow(['bill_id', 'intercept_term', 'num_cosponsors', 'introduced_month', 'num_voting_rounds', 'num_passed_rounds', 'amount', 'bucket_amount', 'status', 'bucket_status', 
])
        for bill_id in bills.keys():
            bill = bills[bill_id]
            csv_file.writerow(
                [bill_id,
                1,
                len(bill.cosponsors),
                bill.introduced_month,
                bill.num_voting_rounds,
                bill.num_passed_rounds,
                getattr(bill, 'amount', 0),
                getattr(bill, 'bucket_amount', 0),
                bill.status,
                getattr(bill, 'bucket_status')])

#write_csv('./bill_static_and_funding_All.csv',bills)
#bills = readBills.filterBillsOnlyOutOfCommittee(bills)
#write_csv('./bill_static_and_funding_OutOfCommittee.csv', bills)
print 'Done'
