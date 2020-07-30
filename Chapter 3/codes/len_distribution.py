########## This script calculates the length differences between two PPs ###########

#usr/bin/env python3
import csv, os, io, random, statistics, argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type = str, help = 'path to length difference data')
parser.add_argument('--output', type = str, help = 'path to output')

args = parser.parse_args()


path = args.input
os.chdir(path)

features = [['Language', 'position', 'diff', 'Mean', 'CI25', 'CI975']]

for file in os.listdir(path):
	if file.endswith('-len-diff.txt'):
		print(file)
		with io.open(file, encoding = 'utf-8') as f:

			diff = []
			diff_1_prob = []
			diff_24_prob = []
			diff_56_prob = []
			diff_7_prob = []

			for line in f:
				if line.startswith('original') is False:
					toks = line.split()
					diff.append(int(toks[5]) - int(toks[4]))
			
			for i in range(10000):
				sample = random.choices(diff, k = len(diff))

				diff_1 = 0
				diff_24 = 0
				diff_56 = 0
				diff_7 = 0

				for d in sample:
					if abs(d) == 1:
						diff_1 += 1
					if abs(d) >= 2 and abs(d) <= 4:
						diff_24 += 1
					if abs(d) >= 5 and abs(d) <= 6:
						diff_56 += 1
					if abs(d) >= 7:
						diff_7 += 1

				total = diff_1 + diff_24 + diff_56 + diff_7

				diff_1_prob.append(round(diff_1 * 100 / total, 2))
				diff_24_prob.append(round(diff_24 * 100 / total, 2))
				diff_56_prob.append(round(diff_56 * 100 / total, 2))
				diff_7_prob.append(round(diff_7 * 100 / total, 2))

			diff_1_prob.sort()
			diff_24_prob.sort()
			diff_56_prob.sort()
			diff_7_prob.sort()

			features.append([file[ : -16], file[-15 : -13], 1, statistics.mean(diff_1_prob), round(diff_1_prob[250],2), round(diff_1_prob[9750],2)])

			features.append([file[ : -16], file[-15 : -13], '2-4', statistics.mean(diff_24_prob), round(diff_24_prob[250],2), round(diff_24_prob[9750],2)])

			features.append([file[ : -16], file[-15 : -13], '5-6', statistics.mean(diff_56_prob), round(diff_56_prob[250],2), round(diff_56_prob[9750],2)])

			features.append([file[ : -16], file[-15 : -13], 'larger than 7', statistics.mean(diff_7_prob), round(diff_7_prob[250],2), round(diff_7_prob[9750],2)])
 

with io.open(args.output, 'w', newline = '', encoding = 'utf-8') as f:
	writer = csv.writer(f)
	for tok in features:
		writer.writerow(tok)
