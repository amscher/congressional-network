import numpy as np

class Legislator(object):
	def __init__(self, last_name, first_name, bioguide_id,thomas_id,gender,party):
		self.last_name = last_name
		self.first_name = first_name
		self.bioguide_id = bioguide_id
		self.thomas_id = thomas_id
		self.party = party.lower()
		self.gender = gender.lower()

	def get_bioguide_id(self):
		return self.bioguide_id

	def get_thomas_id(self):
		return self.thomas_id

	def get_name(self):
		return "{0} {1}".format(self.first_name, self.last_name)
	
	def get_party(self):
		return self.party

	def get_gender(self):
		return self.gender

def load_legislators(filename):
	with open(filename) as legislator_file:
		headers = legislator_file.readline().strip().split(',')
		line = legislator_file.readline()
		while (line is not None and line != ""):
			split_line = line.strip().split(',')
			if len(split_line) != len(headers):
				#TODO: Fix case for quoted commas
				print("Error: expected length %i, received length %i", len(headers), len(split_line))
				print(split_line)
			else:
				row = dict(zip(headers,split_line))
				yield Legislator(row["last_name"],row["first_name"],row["bioguide_id"],row["thomas_id"],row["gender"],row["party"])
			line = legislator_file.readline()

def build_id_map(legislators):
	id_map = {}
	for legislator in legislators:
		id_map[legislator.get_bioguide_id()] = legislator
		id_map[legislator.get_thomas_id()] = legislator
	return id_map

def get_legislator_features(llist):
	legislator_features = np.zeros((len(llist), 4))
	for i in xrange(len(llist)):
		if llist[i].get_gender() == "m":
			legislator_features[i,0] = 1
			legislator_features[i,1] = 0
		else:
			legislator_features[i,1] = 1
			legislator_features[i,0] = 0
			
		if llist[i].get_party() == "republican":
			legislator_features[i,2] = 1
			legislator_features[i,3] = 0
		else:
			legislator_features[i,3] = 1
			legislator_features[i,2] = 0
	return legislator_features