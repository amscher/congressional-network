import yaml
import code.Candidate as Candidate

###### legislators ######
def readLegislators():
    stream = open("/home/neeral/Documents/cs224w/project/legislators-current.yaml", 'r')
    y_stream = yaml.load(stream)

    thomas_to_member_map = {}
    num_members = len(y_stream)

    for i in range(0, num_members):
        legislator = Candidate.Candidate()

        thomas = y_stream[i]["id"]["thomas"]
        legislator.thomasId = thomas

        if "official_full" in y_stream[i]["name"]:
            legislator.name = y_stream[i]["name"]["official_full"]
        else:
            # the one member who does not have an offical name
            legislator.name = y_stream[0]["name"]["first"] + " " +  y_stream[0]["name"]["last"]
        
        if "fec" in y_stream[i]["id"]:
            legislator.FEC_Id = y_stream[i]["id"]["fec"]
        thomas_to_member_map[thomas] = legislator

    return thomas_to_member_map

