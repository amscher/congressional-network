import Candidate

def readFile(filename):
    f = open(filename, 'r')
    return f.read().splitlines()

# returns a map: CAND_ID->Total Amount
def readContributionsFile(prefix, candidates):
    # this is for 'Contributions to Candidates from Committees '
    headers = readFile(prefix + 'pas2_header_file.csv')
    headers = headers[0].split(',')
    # simple version, we will only extract candidate Ids and transaction amounts
    TRANSACTION_AMT = headers.index('TRANSACTION_AMT')
    CAND_ID = headers.index('CAND_ID')
    ENTITY_TP = headers.index('ENTITY_TP')
    TO_CANDIDATE = 'CAN' # for entity type

    lines = readFile(prefix + 'itpas2.txt')
    contributions = {}
    for line in lines:
        line = line.split('|')
        if not line[ENTITY_TP] == TO_CANDIDATE:
            continue
        candidateId = line[CAND_ID]
        amount = int(line[TRANSACTION_AMT])
        if (candidateId == ""):
            print line
        if candidateId in contributions:
            contributions[candidateId] += amount
        else:
            contributions[candidateId] = amount
        if candidateId not in candidates:
            print '%s not in candidates' % candidateId
        else:
            (candidates[candidateId]).amount += amount
    return contributions

# returns a map: CAND_ID->Candidate objects
def readCandidateFile(prefix):
    headers = readFile(prefix + 'cn_header_file.csv')[0].split(',')
    CAND_ID = headers.index('CAND_ID')
    CAND_NAME = headers.index('CAND_NAME')
    CAND_PTY_AFFILIATION = headers.index('CAND_PTY_AFFILIATION')

    lines = readFile(prefix + 'cn.txt')
    candidates = {}
    for line in lines:
        line = line.split('|')
        candidateId = line[CAND_ID]
        name = line[CAND_NAME]
        party = line[CAND_PTY_AFFILIATION]
        candidates[candidateId] = Candidate.Candidate(candidateId, name, party)
    return candidates

def readFECdata(prefix, verbose=False):
    candidates = readCandidateFile(prefix)
    contributions = readContributionsFile(prefix, candidates)
    if verbose:
        for candidateId in candidates:
            print candidateId, candidates[candidateId].name, candidates[candidateId].amount
    return candidates

if __name__ =='__main__':
    readFECdata('', True)