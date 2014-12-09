import csv,sys

def combine_features(*args):
    features = {}
    input_filenames = args[:-1]
    output_filename = args[-1]
    
    for filename in input_filenames:
        with open(filename, 'r') as csvfile:
            featurereader = csv.reader(csvfile)
            for row in featurereader:
                bill = row[0]
                bill_features = row[1:]
                if bill not in features:
                    features[bill] = list()
                features[bill] += bill_features
                
    feature_counts = [len(f) for f in features.values()]
    feature_count_counts = {}
    for c in feature_counts:
        if c not in feature_count_counts:
            feature_count_counts[c] = 0
        feature_count_counts[c] += 1
        
    most_common_length = max(feature_count_counts.items(), key = lambda x: x[1])[0]
                
    with open(output_filename, 'w') as output_file:
        outputwriter = csv.writer(output_file, delimiter = ',')
        for (bill, features) in features.items():
            if len(features) == most_common_length:
                outputwriter.writerow([bill] + features[:-4] + [features[-1]])
            
if __name__ == '__main__':
    combine_features(*sys.argv[1:])
            