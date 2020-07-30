import sys, io, csv

likelihood = []

with io.open(sys.argv[1] + '-' + sys.argv[2] + '-prob_likelihood.txt', encoding = 'utf-8') as f:
	for line in f:
		toks = line.split()
	#	likelihood.append(str(round(float(toks[0]), 2)))
		likelihood.append(toks[0])

pp1_len = []
pp2_len = []
with io.open(sys.argv[1] + '-' + sys.argv[2] + '-pp1.txt', encoding = 'utf-8') as f:
	for line in f:
		pp1_len.append(len(line.split()))

with io.open(sys.argv[1] + '-' + sys.argv[2] + '-pp2.txt', encoding = 'utf-8') as f:
	for line in f:
		pp2_len.append(len(line.split()))

len_diff = []


for i in range(len(pp1_len)):
	if sys.argv[2] == 'en':
#		if pp2_len[i] > pp1_len[i]:
#			len_diff.append(1)
#		if pp2_len[i] < pp1_len[i]:
#			len_diff.append(-1)
#		if pp2_len[i] == pp1_len[i]:
#			len_diff.append(0)
		len_diff.append(pp2_len[i] - pp1_len[i])
	if sys.argv[2] in ['ja', 'zh']:
		len_diff.append(pp1_len[i] - pp2_len[i])

a = 0
b = 0
c = 0
for i in range(len(len_diff)):
	if float(likelihood[i]) < 1:
		if len_diff[i] > 0:
			a += 1
		if len_diff[i] < 0:
			b += 1
		if len_diff[i] == 0:
			c += 1

total = a + b 
print(a * 100 / total)
print(b * 100 / total)
#print(c * 100 / total)



header = ['Likelihood', 'Len_diff']
with io.open(sys.argv[1] + '-' + sys.argv[2] + '-freedom.csv', 'w', encoding = 'utf-8') as f:
	writer = csv.writer(f)
	writer.writerow(header)
	for i in range(len(pp1_len)):
		feature = [likelihood[i], str(len_diff[i])]
		writer.writerow(feature)
