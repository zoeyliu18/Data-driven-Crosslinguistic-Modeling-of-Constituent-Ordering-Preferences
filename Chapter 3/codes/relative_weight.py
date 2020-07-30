########## This script calculates the extent of DLM given length differences between two PPs ###########


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
			for line in f:
				if line.startswith('original') is False:
					toks = line.split()
					diff.append(int(toks[5]) - int(toks[4]))
			diff_1 = []
			diff_24 = []
			diff_56 = []
			diff_7 = []
			for d in diff:
				if abs(d) == 1:
					diff_1.append(d)
				if abs(d) >= 2 and abs(d) <= 4:
					diff_24.append(d)
				if abs(d) >= 5 and abs(d) <= 6:
					diff_56.append(d)
				if abs(d) >= 7:
					diff_7.append(d)

		   ########### 1 ############
			
			diff_1_short_closer = []

			for i in range(10000):
				sample = random.choices(diff_1, k = len(diff_1))

				short_closer = 0
				longer_closer = 0

				for tok in sample:
					if tok > 0:
						short_closer += 1
					if tok < 0:
						longer_closer += 1

				total = short_closer + longer_closer 

				diff_1_short_closer.append(short_closer * 100 / total)

			diff_1_short_closer.sort()

			features.append([file[ : -16], file[-15 : -13], 1, statistics.mean(diff_1_short_closer), round(diff_1_short_closer[250],2), round(diff_1_short_closer[9750],2)])

           ########### 2 - 4 ############

			diff_24_short_closer = []

			for i in range(10000):
				sample = random.choices(diff_24, k = len(diff_24))

				short_closer = 0
				longer_closer = 0

				for tok in sample:
					if tok > 0:
						short_closer += 1
					if tok < 0:
						longer_closer += 1

				total = short_closer + longer_closer

				diff_24_short_closer.append(short_closer * 100 / total)

			diff_24_short_closer.sort()

			features.append([file[ : -16], file[-15 : -13], '2-4', statistics.mean(diff_24_short_closer), round(diff_24_short_closer[250],2), round(diff_24_short_closer[9750],2)])
 
 		########### 5 - 6 ############

			diff_56_short_closer = []

			for i in range(10000):
				sample = random.choices(diff_56, k = len(diff_56))

				short_closer = 0
				longer_closer = 0

				for tok in sample:
					if tok > 0:
						short_closer += 1
					if tok < 0:
						longer_closer += 1

				total = short_closer + longer_closer

				diff_56_short_closer.append(short_closer * 100 / total)

			diff_56_short_closer.sort()

			features.append([file[ : -16], file[-15 : -13], '5-6', statistics.mean(diff_56_short_closer), round(diff_56_short_closer[250],2), round(diff_56_short_closer[9750],2)])

		######### >= 7 ########

			diff_7_short_closer = []

			for i in range(10000):
				sample = random.choices(diff_7, k = len(diff_7))

				short_closer = 0
				longer_closer = 0

				for tok in sample:
					if tok > 0:
						short_closer += 1
					if tok < 0:
						longer_closer += 1

				total = short_closer + longer_closer

				diff_7_short_closer.append(short_closer * 100 / total)

			diff_7_short_closer.sort()

			features.append([file[ : -16], file[-15 : -13], 'larger than 7', statistics.mean(diff_7_short_closer), round(diff_7_short_closer[250],2), round(diff_7_short_closer[9750],2)])
 

with io.open(args.output, 'w', newline = '', encoding = 'utf-8') as f:
	writer = csv.writer(f)
	for tok in features:
		writer.writerow(tok)
