#usr/bin/env python3
import sys, glob, os, io, random, statistics, argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--input', type = str, help = 'path to UD data')
parser.add_argument('--output', type = str, help = 'path to output PP data')

args = parser.parse_args()

def conll_read_sentence(file_handle):
	sent = []
	for line in file_handle:
		toks = line.split()
		if len(toks) == 0:
			return sent ### when it reads an empty list (end of sentence) it stops
		else:
			if toks[0].isdigit() == True:

				sent.append(toks)

	return None

# return index of all the verbs that have a P directly following it
def verb_list(sentence):
	verbs = []
	for tok in sentence:
		if tok[3] == 'VERB':
			verbs.append(tok[0])

	return verbs

def dependents(index, sentence):
	dependent = []
	for tok in sentence:
		if tok[6] == index:
			dependent.append(tok[0])

	return dependent

def head(index, sentence):
	if int(index) - 1 >=0:
		head = sentence[int(index) - 1][6]
		return head
	else: 
		return None

#get the index of all the preposition dependents of each verb
#make sure it's a PP, not just a P, which means the P has to have at least one dependent
#the output PP index list will give PP, so if length is larger than 2, not consider
def prep_heads(verb_index, sentence): 
	preps = []
	preps_head = []
	for tok in sentence:
		if tok[3] == 'ADP':
			if tok[7] == 'case':

				if int(tok[0]) < int(verb_index): #the PP appears before the verb
					if head(tok[0], sentence) != None:
						if int(tok[6]) > int(tok[0]):

							if head(head(tok[0], sentence), sentence) == verb_index:
								preps_head.append(head(tok[0], sentence))

	if len(set(preps_head)) == 2:
		if len(preps_head) == 2:

			return preps_head

	return None

def prep(head_index, sentence):
	all_dependents = dependents(head_index, sentence)
	pos = []
	preps = []
	for i in all_dependents:
		if sentence[int(float(i)) - 1][3] == 'ADP':
			if sentence[int(i) - 1][7] == 'case':
				preps.append(sentence[int(i) - 1][0])

	if len(preps) > 0:
		a = []
		for tok in preps:
			a.append(int(tok))
		return min(a)
	else: 
		return None

def first_dependent(index, sentence):
	min_de = int(index)
	for tok in sentence:
		if tok[6] == index:
			if tok[7] != 'punct':
				if int(tok[0]) < min_de:
					min_de = int(tok[0])
	return min_de

def object_order(index, sentence):
	for tok in sentence:
		if tok[6] == index:
			if tok[7] == 'obj':
				if int(tok[0]) < int(index):
					return 'OV'
				else:
					return 'VO'
	return 'V'

# generate V PP...PP...
def VP(file_handle, directory):
	with io.open(directory + '/' + file_handle, encoding='utf-8') as f:
		verb_phrase = []
		sent = conll_read_sentence(f)
		
		while sent is not None:	
			verbs = verb_list(sent)
			if len(verbs) != 0:

				for verb in verbs:					
					preps = prep_heads(verb, sent)

					if preps is not None:
						prep_head = []
						for i in preps:
							prep_head.append(int(i))
											
						idxlist1 = [str(min(prep_head))]			
						min1 = len(sent)
						max1 = 0
						while len(idxlist1) != 0:
							i = idxlist1.pop()
							if int(i) < min1:
								min1 = int(i)
							if int(i) > max1:
								max1 = int(i)
							
							if dependents(i,sent) is not None:
								for j in dependents(i, sent):
									idxlist1.append(j)

						p1 = prep(str(min(prep_head)), sent)

						idxlist2 = [str(max(prep_head))] #convert to a list so pop can be used
						min2 = len(sent)
						max2 = 0
						while len(idxlist2) != 0:
							i = idxlist2.pop()
							if int(i) < min2:
								min2 = int(i)
							if int(i) > max2:
								max2 = int(i)

							if dependents(i, sent) is not None:
								for j in dependents(i, sent):
									idxlist2.append(j)

						p2 = prep(str(max(prep_head)), sent)
						
						pp1_case = []
						pp2_case = []

						for tok in sent[min1 - 1: max1]:
							if tok[7] != 'punct':
								pp1_case.append(tok)

						for tok in sent[min2 - 1: max2]:
							if tok[7] != 'punct':
								pp2_case.append(tok)

						pp1 = []
						pp2 = []

						if pp1_case[0][1][0].isupper() == True:
							pp1.append(pp1_case[0][1].lower())
							pp2.append(pp2_case[0][1].capitalize())

						else:
							pp1.append(pp1_case[0][1])
							pp2.append(pp2_case[0][1])

						for tok in pp1_case[1 : ]:
							pp1.append(tok[1])

						for tok in pp2_case[1 : ]:
							pp2.append(tok[1])


						pp1_new = []
						pp2_new = []

						for m in pp1_case:
							pp1_new.append(m[1])

						for m in pp2_case:
							pp2_new.append(m[1])

						pp1_len = len(pp1_new)
						pp2_len = len(pp2_new)

						v_idx = int(verb)
						pp1_lexical_head_idx = min(prep_head)
						pp2_lexical_head_idx = max(prep_head)

						pp1_function_head_idx = p1 
						pp2_function_head_idx = p2

						original_content = v_idx - pp1_lexical_head_idx + v_idx - pp2_lexical_head_idx 
						variant_content = v_idx - pp1_lexical_head_idx - pp2_len + v_idx - pp2_lexical_head_idx + pp1_len

						original_content_hudson = v_idx - pp1_lexical_head_idx - 1 + v_idx - pp2_lexical_head_idx - 1
						variant_content_hudson = v_idx - pp1_lexical_head_idx - pp2_len - 1 + v_idx - pp2_lexical_head_idx + pp1_len - 1

						original_function = v_idx - pp1_function_head_idx + v_idx - pp2_function_head_idx
						variant_function = v_idx - pp1_function_head_idx - pp2_len + v_idx - pp2_function_head_idx + pp1_len

						original_function_hudson = v_idx - pp1_function_head_idx - 1 + v_idx - pp2_function_head_idx - 1
						variant_function_hudson = v_idx - pp1_function_head_idx - pp2_len - 1 + v_idx - pp2_function_head_idx + pp1_len - 1

						vp = []

						vp.append(pp1_len)
						vp.append(pp2_len)
						vp.append(original_content)
						vp.append(variant_content)	
						vp.append(original_content_hudson)
						vp.append(variant_content_hudson)
						vp.append(original_function)
						vp.append(variant_function)
						vp.append(original_function_hudson)
						vp.append(variant_function_hudson)

						vp.append(sent[min(prep_head) - 1][7]) #dependent relation between lexical head of the PP and the verb
						vp.append(sent[max(prep_head) - 1][7])
						
						verb_phrase.append(vp)

			sent = conll_read_sentence(f)
	return verb_phrase

path = args.input
#path = '/Users/Silverlining/Desktop/test/'
os.chdir(path)

for directory in glob.glob('*'):
	for files in os.listdir(directory):
		if files.endswith('-ud-train.conllu'):
			all_data = VP(files, directory)
			pp1_len = []
			pp2_len = []
			diff = []
			content_diff = []
			content_hudson_diff = []
			function_diff = []
			function_hudson_diff = []

			for tok in VP(files,directory):
				if tok[-2] == 'obl' and tok[-1] == 'obl':
					pp1_len.append(tok[0])
					pp2_len.append(tok[1])
					diff.append([tok[2], tok[3], tok[4], tok[5], tok[6], tok[7], tok[8], tok[9]])
					content_diff.append([tok[2], tok[3]])
					content_hudson_diff.append([tok[4], tok[5]])
					function_diff.append([tok[6], tok[7]])
					function_hudson_diff.append([tok[8], tok[9]])

			if len(pp1_len) >= 50:

########## Bootstrapping for comparisons of DLM based on content head, measured with absolute index values #############

				content_short_closer = []
				content_longer_closer = [] 
				content_equal = []

				for i in range(1000000):
					sample = random.choices(content_diff, k = len(pp1_len))

					short_closer = 0
					longer_closer = 0
					equal = 0

					for tok in sample:
						if tok[0] < tok[1]:
							short_closer += 1
						if tok[0] > tok[1]:
							longer_closer += 1
						if tok[0] == tok[1]:
							equal += 1

					total = short_closer + longer_closer + equal

					content_short_closer.append(short_closer * 100 / total)
					content_longer_closer.append(longer_closer * 100 / total)
					content_equal.append(equal * 100 / total)

				content_short_closer.sort()
				content_longer_closer.sort()
				content_equal.sort()

########## Bootstrapping for comparisons of DLM based on content head, measured based on Hudson (1995) #############

				content_hudson_short_closer = []
				content_hudson_longer_closer = [] 
				content_hudson_equal = []

				for i in range(1000000):
					sample = random.choices(content_hudson_diff, k = len(pp1_len))

					short_closer = 0
					longer_closer = 0
					equal = 0

					for tok in sample:
						if tok[0] < tok[1]:
							short_closer += 1
						if tok[0] > tok[1]:
							longer_closer += 1
						if tok[0] == tok[1]:
							equal += 1

					total = short_closer + longer_closer + equal

					content_hudson_short_closer.append(short_closer * 100 / total)
					content_hudson_longer_closer.append(longer_closer * 100 / total)
					content_hudson_equal.append(equal * 100 / total)

				content_hudson_short_closer.sort()
				content_hudson_longer_closer.sort()
				content_hudson_equal.sort()


########## Bootstrapping for comparisons of DLM based on function head, measured with absolute index values #############
				
				function_short_closer = []
				function_longer_closer = [] 
				function_equal = []

				for i in range(1000000):
					sample = random.choices(function_diff, k = len(pp1_len))

					short_closer = 0
					longer_closer = 0
					equal = 0

					for tok in sample:
						if tok[0] < tok[1]:
							short_closer += 1
						if tok[0] > tok[1]:
							longer_closer += 1
						if tok[0] == tok[1]:
							equal += 1

					total = short_closer + longer_closer + equal

					function_short_closer.append(short_closer * 100 / total)
					function_longer_closer.append(longer_closer * 100 / total)
					function_equal.append(equal * 100 / total)

				function_short_closer.sort()
				function_longer_closer.sort()
				function_equal.sort()


########## Bootstrapping for comparisons of DLM based on function head, measured based on Hudson (1995) #############

				function_hudson_short_closer = []
				function_hudson_longer_closer = [] 
				function_hudson_equal = []

				for i in range(1000000):
					sample = random.choices(function_hudson_diff, k = len(pp1_len))

					short_closer = 0
					longer_closer = 0
					equal = 0

					for tok in sample:
						if tok[0] < tok[1]:
							short_closer += 1
						if tok[0] > tok[1]:
							longer_closer += 1
						if tok[0] == tok[1]:
							equal += 1

					total = short_closer + longer_closer + equal

					function_hudson_short_closer.append(short_closer * 100 / total)
					function_hudson_longer_closer.append(longer_closer * 100 / total)
					function_hudson_equal.append(equal * 100 / total)

				function_hudson_short_closer.sort()
				function_hudson_longer_closer.sort()
				function_hudson_equal.sort()


				with io.open(args.output + directory[3 : ] + '-zh-content-statistics.txt', 'w', encoding = 'utf-8') as f:
					f.write(str(round(statistics.mean(content_short_closer), 2)) + '\n')
					f.write(str(round(content_short_closer[25000], 2)) + '\n')
					f.write(str(round(content_short_closer[975000], 2)) + '\n')
					f.write(str(round(statistics.mean(content_longer_closer), 2)) + '\n')
					f.write(str(round(content_longer_closer[25000], 2)) + '\n')
					f.write(str(round(content_longer_closer[975000], 2)) + '\n')
					f.write(str(round(statistics.mean(content_equal), 2)) + '\n')
					f.write(str(round(content_equal[25000], 2)) + '\n')
					f.write(str(round(content_equal[975000], 2)) + '\n')

				with io.open(args.output + directory[3 : ] + '-zh-content-hudson-statistics.txt', 'w', encoding = 'utf-8') as f:
					f.write(str(round(statistics.mean(content_hudson_short_closer), 2)) + '\n')
					f.write(str(round(content_hudson_short_closer[25000], 2)) + '\n')
					f.write(str(round(content_hudson_short_closer[975000], 2)) + '\n')
					f.write(str(round(statistics.mean(content_hudson_longer_closer), 2)) + '\n')
					f.write(str(round(content_hudson_longer_closer[25000], 2)) + '\n')
					f.write(str(round(content_hudson_longer_closer[975000], 2)) + '\n')
					f.write(str(round(statistics.mean(content_hudson_equal), 2)) + '\n')
					f.write(str(round(content_hudson_equal[25000], 2)) + '\n')
					f.write(str(round(content_hudson_equal[975000], 2)) + '\n')

				with io.open(args.output + directory[3 : ] + '-zh-function-statistics.txt', 'w', encoding = 'utf-8') as f:
					f.write(str(round(statistics.mean(function_short_closer), 2)) + '\n')
					f.write(str(round(function_short_closer[25000], 2)) + '\n')
					f.write(str(round(function_short_closer[975000], 2)) + '\n')
					f.write(str(round(statistics.mean(function_longer_closer), 2)) + '\n')
					f.write(str(round(function_longer_closer[25000], 2)) + '\n')
					f.write(str(round(function_longer_closer[975000], 2)) + '\n')
					f.write(str(round(statistics.mean(function_equal), 2)) + '\n')
					f.write(str(round(function_equal[25000], 2)) + '\n')
					f.write(str(round(function_equal[975000], 2)) + '\n')

				with io.open(args.output + directory[3 : ] + '-zh-function-hudson-statistics.txt', 'w', encoding = 'utf-8') as f:
					f.write(str(round(statistics.mean(function_hudson_short_closer), 2)) + '\n')
					f.write(str(round(function_hudson_short_closer[25000], 2)) + '\n')
					f.write(str(round(function_hudson_short_closer[975000], 2)) + '\n')
					f.write(str(round(statistics.mean(function_hudson_longer_closer), 2)) + '\n')
					f.write(str(round(function_hudson_longer_closer[25000], 2)) + '\n')
					f.write(str(round(function_hudson_longer_closer[975000], 2)) + '\n')
					f.write(str(round(statistics.mean(function_hudson_equal), 2)) + '\n')
					f.write(str(round(function_hudson_equal[25000], 2)) + '\n')
					f.write(str(round(function_hudson_equal[975000], 2)) + '\n')

				header = ['original_content', 'variant_content', 'original_content_hudson', 'variant_content_hudson', 'original_function', 'variant_function', 'original_function_hudson', 'variant_function_hudson']
				with io.open(args.output + directory[3 : ] + '-zh-len-diff.txt', 'w', encoding = 'utf-8') as f:
					f.write(' '.join(tok for tok in header) + '\n')
					for tok in diff:
						f.write(' '.join(str(w) for w in tok) + '\n')

