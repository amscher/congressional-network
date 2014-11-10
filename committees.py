import yaml
import snap

def createNetwork(Nodes):
    G = snap.TUNGraph.New()
    for NId in Nodes:
        G.AddNode(int(NId))
    return G

def addCommitteeToNetwork(G, Members):
    for i in range(0, len(Members)):
        for j in range(i+1, len(Members)):
            G.AddEdge(int(Members[i]), int(Members[j]))

###### committees ######
stream = open("data/committees-current.yaml", 'r')
y_stream = yaml.load(stream)
#print y_stream
#print yaml.dump(y_stream)

thomas_id_to_committee_name_map = {}
num_committees = len(y_stream)

for i in range(0, num_committees):
    name = y_stream[i]["name"]
    thomas_id = y_stream[i]["thomas_id"]
    thomas_id_to_committee_name_map[thomas_id] = name

###### committee membership ######
stream = open("data/committee-membership-current.yaml", 'r')
y_stream = yaml.load(stream)

committee_to_members_map = {} # by thomas_id

for committee_thomas_id in thomas_id_to_committee_name_map:
    if committee_thomas_id in y_stream:
        members = []
        num_members = len(y_stream[committee_thomas_id])
        for i in range(0, num_members):
            members.append(y_stream[committee_thomas_id][i]["thomas"])
        committee_to_members_map[committee_thomas_id] = members

###### legislators ######
stream = open("data/legislators-current.yaml", 'r')
y_stream = yaml.load(stream)

thomas_to_member_map = {}
num_members = len(y_stream)

for i in range(0, num_members):
    thomas = y_stream[i]["id"]["thomas"]
    if "official_full" in y_stream[i]["name"]:
        name = y_stream[i]["name"]["official_full"]
        thomas_to_member_map[thomas] = name
    else:
        name = y_stream[0]["name"]["first"] + " " +  y_stream[0]["name"]["last"]
    # we ignore the one member who does not have an offical name


#################################
#### basic manipulation ####
#for thomas_id in committee_to_members_map:
#    print '\n', thomas_id_to_committee_name_map[thomas_id]
#    for thomas in committee_to_members_map[thomas_id]:
#        print '\t', thomas_to_member_map[thomas]

G = createNetwork(thomas_to_member_map.keys()) # creates network where a node is a legislator
for thomas_id in committee_to_members_map:
    addCommitteeToNetwork(G, committee_to_members_map[thomas_id])

print "Graph has %d nodes and %d edges" % (G.GetNodes(), G.GetEdges())
print "Its clustering co-efficient is %f" % (snap.GetClustCf(G))
