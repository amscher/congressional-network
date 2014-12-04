import csv

import Bill
import ml

def ForwardSearch(file_path, bill_predicate):
    for col in range(1,7):
        print '\n\n\t\tColumn %d' % col
        features = []
        labels = []
        with open(file_path, 'rb') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                bill_id = row[0]
                status = row[-1]
                del row[0]
                del row[-1]
                feature = (float(row[0]), float(row[2]), float(row[col]))
                if ('OutOfCommittee' == bill_predicate):
                    label = 1 if status not in Bill.NOT_OUT_OF_COMMITTEE else 0
                else:
                    if status in Bill.NOT_OUT_OF_COMMITTEE:
                        continue
                    else:
                        label = 1 if status in Bill.SUCCESSFUL else 0
                features.append(feature)
                labels.append(label)
        ml.runML((features, labels))

if __name__ == '__main__':
    ForwardSearch('./bill_combined.csv', 'Enacted')
