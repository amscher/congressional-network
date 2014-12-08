import json
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

score_map = {
  "INTRODUCED" : 0,
  "REFERRED" : 1,
  "REPORTED" : 2,
  "PASS_OVER:SENATE": 3,
  "PASS_OVER:HOUSE": 3,
  "PASSED:BILL": 4,
  "ENACTED:SIGNED" : 5
}

status_map = {
  "INTRODUCED" : 0,
  "REFERRED" : 1,
  "REPORTED" : 2,
  "PASS_OVER:SENATE": 3,
  "PASS_OVER:HOUSE": 4,
  "ENACTED:SIGNED" : 5
}

bill_status_score = {}
bill_status_map = {}

def getBills(bill_type):
  for i in range(10000):
    bill_name = "%s%d" % (bill_type, i)
    try:
      filename = "113/bills/%s/%s/data.json" % (bill_type, bill_name)
      stream = open(filename, 'r')
    except IOError, e:
      # print "Can't open file: ", filename
      continue
    data = json.load(stream)

    bill_info = {}
    bill_info["status"] = data["status"]
    bill_info["status_at"] = data["status_at"]
    bill_info["introduced_at"] = data["introduced_at"]

    bill_status_map[bill_name] = bill_info

getBills("hr")
getBills("hjres")
getBills("s")

date_billcount_map = {}

def plotBillsAgainstTime():
  bill_scores = open("billscores.tab", 'w')

  for key in bill_status_map.keys():
    status = bill_status_map[key]["status"]
    score = -1
    if (status_map.has_key(status)):
      score = status_map[status]
    else:
      print status
      continue
    time = bill_status_map[key]["introduced_at"].strip()

    if date_billcount_map.has_key(time):
      date_billcount_map[time][score] += 1
    else:
      date_billcount_map[time] = [0 for i in range(6)]
      date_billcount_map[time][score] = 1
    bill_scores.write('{0} {1}\n'.format(time, score))

plotBillsAgainstTime()


def getCCDF(keys, countMap, ccdfMap):
  runningSum = [0 for i in range(7)]
  i = len(keys) - 1
  while i > 0:
    key = keys[i]
    ccdfMap[key] = [0 for y in range(7)]
    for x in range(6):
      runningSum[x] += countMap[key][x]
      ccdfMap[key][x] = runningSum[x]
    runningSum[6] += sum(countMap[key])
    ccdfMap[key][6] = runningSum[6]
    i -= 1

count_ccdf_map = {}
dates = date_billcount_map.keys()
dates.sort()
getCCDF(dates, date_billcount_map, count_ccdf_map)

score_ccdf_map = {}

for i in range(6):
  bill_counts = open("count/billcount{0}.tab".format(i), 'w')
  for key in count_ccdf_map.keys():
    value = count_ccdf_map[key][i]
    total = count_ccdf_map[key][6]
    # print "%s [%f]" % (key, value)
    bill_counts.write('{0} {1}\n'.format(key, float(value)/float(total)))


dates = count_ccdf_map.keys()
dates.sort()
datesFile = open("dates.tab", 'w')
for i in range(len(dates)):
  datesFile.write('{0}  1\n'.format(dates[i]))

def getArray(column):
  counts = []
  for i in range(len(dates)):
    key = dates[i]
    counts.append(date_billcount_map[key][column])
  return counts

print "Number Referred ", sum(getArray(1))
print "Number Reported",  sum(getArray(2))
print "Number Passed by House", sum(getArray(3))
print "Number Passed by Senate", sum(getArray(4))
print "Number Enacted", sum(getArray(5))




# y = np.row_stack((getArray(1), getArray(2), getArray(3), getArray(4), getArray(5)))
# days, count = np.loadtxt("dates.csv", unpack=True,
#         converters={0: mdates.strpdate2num('%Y-%m-%d')})
# x = np.array(days)

# y_stack = np.cumsum(y, axis=0)

# fig = plt.figure()
# ax = fig.add_subplot(111)

# ax.fill_between(x, 0, y_stack[0,:], facecolor="#CC6666", alpha=.7)
# ax.fill_between(x, y_stack[0,:], y_stack[1,:], facecolor="#1DACD6", alpha=.7)
# ax.fill_between(x, y_stack[1,:], y_stack[2,:], facecolor="#6E5160")
# ax.fill_between(x, y_stack[2,:], y_stack[3,:], facecolor="#5CD5CD")
# ax.fill_between(x, y_stack[3,:], y_stack[4,:], facecolor="#D55CD5")

# plt.show()



