import os, json

class VoteType(object):
	Passage = "passage"
	Other = "other"

class VoteResponse(object):
	Aye = "Aye"
	No = "No"
	NotVoting = "Not Voting"
	Present = "Present"
	Other = "Other"
	Map = {}

def parse_vote_type(s):
	if s.lower() == "Passage":
		return VoteType.Passage
	else:
		return VoteType.Other

def parse_vote_response(s):
	if s.lower() == "aye":
		return VoteResponse.Aye
	elif s.lower() == "no":
		return VoteResponse.No
	elif s.lower() == "not voting":
		return VoteResponse.NotVoting
	elif s.lower() == "present":
		return VoteResponse.Present
	else:
		return VoteResponse.Other

def read_votes(*args):
	for directory in args:
		subdirectories = os.listdir(directory)
		for subdirectory in subdirectories:
			filepath = os.path.sep.join([directory, subdirectory, "data.json"])
			if not os.path.isfile(filepath):
				continue
			else:
				with open(filepath) as json_file:
					json_doc = json.load(json_file)
					yield Vote(json_doc)


class Vote(object):
	def __init__(self, parsed_json):
		self.data = parsed_json

	def get_vote_type(self):
		if self.data["category"] == "passage":
			return VoteType.Passage
		else:
			return VoteType.Other

	def _get_vote_id_pairs(self):
		for vote_response in self.data["votes"]:
			vote_response_type = parse_vote_response(vote_response)
			for vote in self.data["votes"][vote_response]:
				yield (vote["id"], vote_response_type)

	def get_legislator_vote_map(self, legislator_id_map):
		vote_map = {}
		for (legislator_id, vote_type) in self._get_vote_id_pairs():
			if legislator_id not in legislator_id_map:
				continue
			vote_map[legislator_id_map[legislator_id]] = vote_type
		return vote_map
	
	def get_bill_type(self):
		if "bill" in self.data:
			return self.data["bill"]["type"]
		else:
			return None
		
	def get_bill_id(self):
		if "bill" in self.data:
			return self.data["bill"]["number"]