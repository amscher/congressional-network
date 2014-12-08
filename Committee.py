class Committee:
    'A class with all the attributes we need for a Committee'
    def __init__(self, thomas_id, name):
        self.thomas_id = thomas_id
        self.chair = ""
        self.name = name
        self.btwnness_score = 0
        self.bill_success_rate = 0
        self.bill_outcomm_rate = 0
        self.numbills = 0


from json import JSONEncoder
class Encoder(JSONEncoder):
  def default(self, o):
    if not isinstance(o, Committee):
      return {}
    return o.__dict__