#usr/bin/env python3
import io, csv, os

path = '/Users/Silverlining/Desktop/dlm/'
os.chdir(path)

header = ['Language', 'Len', 'CI', 'Std']

vprep = []
vprep_language = []

for file in os.listdir(path):
	if file.endswith('-en-statistics.txt'):
		with io.open(file, encoding = 'utf-8') as f:
			data = []
			for line in f:
				tok = line.split()[0]
				data.append(tok)
			
			vprep.append([file.split('-')[0], 'Shorter PP closer', data[0], data[1], data[2]])
			vprep.append([file.split('-')[0], 'Longer PP closer', data[3], data[4], data[5]])
			vprep.append([file.split('-')[0], 'Equal length', data[6], data[7], data[8]])
			vprep_language.append(file.split('-')[0])


postpv = []
postpv_language = []

for file in os.listdir(path):
	if file.endswith('-ja-statistics.txt'):
		with io.open(file, encoding = 'utf-8') as f:
			data = []
			for line in f:
				tok = line.split()[0]
				data.append(tok)
			
			postpv.append([file.split('-')[0], 'Shorter PP closer', data[0], data[1], data[2]])
			postpv.append([file.split('-')[0], 'Longer PP closer', data[3], data[4], data[5]])
			postpv.append([file.split('-')[0], 'Equal length', data[6], data[7], data[8]])
			postpv_language.append(file.split('-')[0])

prepv = []
prepv_language = []

for file in os.listdir(path):
	if file.endswith('-zh-statistics.txt'):
		with io.open(file, encoding = 'utf-8') as f:
			data = []
			for line in f:
				tok = line.split()[0]
				data.append(tok)
			
			prepv.append([file.split('-')[0], 'Shorter PP closer', data[0], data[1], data[2]])
			prepv.append([file.split('-')[0], 'Longer PP closer', data[3], data[4], data[5]])
			prepv.append([file.split('-')[0], 'Equal length', data[6], data[7], data[8]])
			prepv_language.append(file.split('-')[0])


vprep_only_language = []

for tok in set(vprep_language):
	if tok not in set(prepv_language):
		vprep_only_language.append(tok)


with io.open('/Users/Silverlining/Desktop/dlm/dlm-prepv-new.csv', 'w', encoding = 'utf-8') as data:
	writer = csv.writer(data)
	writer.writerow(header)
	for tok in prepv:
		if tok[0] not in vprep_language:
			writer.writerow(tok)


with io.open('/Users/Silverlining/Desktop/dlm/dlm-vprep-new.csv', 'w', encoding = 'utf-8') as data:
	writer = csv.writer(data)
	writer.writerow(header)
	for tok in vprep:
		if tok[0] in vprep_only_language:
			writer.writerow(tok)

with io.open('/Users/Silverlining/Desktop/dlm/dlm-mix-vprep-new.csv', 'w', encoding = 'utf-8') as data:
	writer = csv.writer(data)
	writer.writerow(header)
	for tok in vprep:
		if tok[0] in prepv_language:
			writer.writerow(tok)

with io.open('/Users/Silverlining/Desktop/dlm/dlm-mix-prepv-new.csv', 'w', encoding = 'utf-8') as data:
	writer = csv.writer(data)
	writer.writerow(header)
	for tok in prepv:
		if tok[0] in vprep_language:
			writer.writerow(tok)


with io.open('/Users/Silverlining/Desktop/dlm/dlm-postpv-new.csv', 'w', encoding = 'utf-8') as data:
	writer = csv.writer(data)
	writer.writerow(header)
	for tok in postpv:
		writer.writerow(tok)


