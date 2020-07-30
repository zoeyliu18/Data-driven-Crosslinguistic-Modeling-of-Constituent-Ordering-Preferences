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

						pp1_lemma = []
						pp2_lemma = []

						for m in pp1_case:
							pp1_new.append(m[1])
							pp1_lemma.append(m[2])

						for m in pp2_case:
							pp2_new.append(m[1])
							pp2_lemma.append(m[2])

						pp1_len = len(pp1_new)
						pp2_len = len(pp2_new)


						new_sent = []
						for tok in sent[ : min1 - 1]:
							new_sent.append(tok[1])
						for tok in pp1_new:
							new_sent.append(tok)
						if max1 == min2 - 1:
							for tok in pp2_new:
								new_sent.append(tok)
							for tok in sent[max2 : ]:
								new_sent.append(tok[1])
						else:
							for tok in sent[max1 : min2 - 1]:
								new_sent.append(tok[1])
							for tok in pp2_new:
								new_sent.append(tok)
							for tok in sent[max2 : ]:
								new_sent.append(tok[1])
						new_sent.append('<eos>')

						reverse_sent = []
						for tok in sent[ : min1 - 1]:
							reverse_sent.append(tok[1])					
						for tok in pp2:
							reverse_sent.append(tok)
						if max1 == min2 - 1:
							for tok in pp1:
								reverse_sent.append(tok)
							for tok in sent[max2 : ]:
								reverse_sent.append(tok[1])
						else:
							for tok in sent[max1 : min2 - 1]:
								reverse_sent.append(tok[1])
							for tok in pp1:
								reverse_sent.append(tok)
							for tok in sent[max2 : ]:
								reverse_sent.append(tok[1])
						reverse_sent.append('<eos>')

						base_pp1 = []
						for tok in sent[ : min1 - 1]:
							base_pp1.append(tok[1])
						for tok in pp1_new:
							base_pp1.append(tok)
						if max1 == min2 - 1:
							for tok in sent[max2 : ]:
								base_pp1.append(tok[1])
						else:
							for tok in sent[max1 : min2 - 1]:
								base_pp1.append(tok[1])
							for tok in sent[max2 : ]:
								base_pp1.append(tok[1])
						base_pp1.append('<eos>')

						base_pp2 = []
						for tok in sent[ : min1 - 1]:
							base_pp2.append(tok[1])					
						for tok in pp2:
							base_pp2.append(tok)
						if max1 == min2 - 1:
							for tok in sent[max2 : ]:
								base_pp2.append(tok[1])
						else:
							for tok in sent[max1 : min2 - 1]:
								base_pp2.append(tok[1])
							for tok in sent[max2 : ]:
								base_pp2.append(tok[1])
						base_pp2.append('<eos>')

						if len(new_sent) != len(reverse_sent):
							print(' '.join(w for w in new_sent))

						distance1 = p1 - int(verb)
						distance2 = p2 - int(verb)

						vp = []
						vp.append(' '.join(tok for tok in new_sent))
						vp.append(' '.join(tok for tok in reverse_sent))
						vp.append(' '.join(tok for tok in pp1_new))
						vp.append(' '.join(tok for tok in pp2_new))
						vp.append(pp1_len)
						vp.append(pp2_len)
						vp.append(sent[int(verb) - 1])	

						vp.append(' '.join(tok for tok in base_pp1))
						vp.append(' '.join(tok for tok in base_pp2))

						vp.append(distance1)
						vp.append(distance2)		

						v = sent[int(verb) - 1]
						prep1 = sent[p1 - 1]
						pp1_lexical_head = sent[min(prep_head) - 1]
						prep2 = sent[p2 - 1]
						pp2_lexical_head = sent[max(prep_head) - 1]

						pp1_pro = 'nonpronominal'
						pp2_pro = 'nonpronominal'

						if pp1_lexical_head[3] == 'PRON':
							pp1_pro = 'pronominal'
						if pp2_lexical_head[3] == 'PRON':
							pp2_pro = 'pronominal'

						#### VERB_lemma, VERB_lexical, Prep1_lemma, Prep_lexical, PP_head_lemma, PP_head_lexical, PP_head_POS, VERB_id, Head_id #####
						vp.append([v[2], v[1], prep1[2], prep1[1], pp1_lexical_head[2], pp1_lexical_head[1], pp1_lexical_head[3], v[0], pp1_lexical_head[0]])
						vp.append([v[2], v[1], prep2[2], prep2[1], pp2_lexical_head[2], pp2_lexical_head[1], pp2_lexical_head[3], v[0], pp2_lexical_head[0]])

						vp.append(' '.join(tok for tok in pp1_lemma))
						vp.append(' '.join(tok for tok in pp2_lemma))

						vp.append(pp1_pro)
						vp.append(pp2_pro)
						vp.append(v[2])

						vp.append(' '.join(tok[1] for tok in sent))

						vp.append(sent[min(prep_head) - 1][7]) #dependent relation between lexical head of the PP and the verb
						vp.append(sent[max(prep_head) - 1][7])
						vp.append(sent[min(prep_head) - 1][3])
						vp.append(sent[max(prep_head) - 1][3])
						
						verb_phrase.append(vp)


			sent = conll_read_sentence(f)
	return verb_phrase

path = args.input
#path = '/Users/Silverlining/Desktop/test/'
os.chdir(path)

#pos = ['NOUN', 'NUM', 'PRON', 'PROPN'] 

for directory in glob.glob('*'):
	for files in os.listdir(directory):
		if files.endswith('-ud-train.conllu'):
			all_data = VP(files, directory)
			original = []
			variant = []
			pp1 = []
			pp2 = []
			pp_len = []
			base1 = []
			base2 = []
			distance_pp1 = []
			distance_pp2 = []
			tuples1 = []
			tuples2 = []
			pp1_lemmas = []
			pp2_lemmas = []
			pp1_pro = []
			pp2_pro = []
			verb = []
			full_sent = []


			for tok in VP(files,directory):
				if tok[-3] == 'obl' and tok[-4] == 'obl':
				#	if tok[-1] in pos and tok[-2] in pos and tok[-3] == 'obl' and tok[-4] == 'obl':
					original.append(tok[0])
					variant.append(tok[1])
					pp1.append(tok[2])
					pp2.append(tok[3])
					pp_len.append([tok[4], tok[5]])
					base1.append(tok[7])
					base2.append(tok[8])
#					distance_pp1.append(str(tok[9]))
#					distance_pp2.append(str(tok[10]))
					tuples1.append(tok[11])
					tuples2.append(tok[12])
					pp1_lemmas.append(tok[13])
					pp2_lemmas.append(tok[14])
					pp1_pro.append(tok[15])
					pp2_pro.append(tok[16])
					verb.append(tok[17])
					full_sent.append(tok[18])
		
			if len(original) >= 50:


#				with io.open(args.output + directory[3 : ] + '-zh-original.txt', 'w', encoding = 'utf-8') as f:
#					for tok in original:
#						f.write(tok + '\n')

#				with io.open(args.output + directory[3 : ] + '-zh-variant.txt', 'w', encoding = 'utf-8') as f:
#					for tok in variant:
#						f.write(tok + '\n')

#				with io.open(args.output + directory[3 : ] + '-zh-pp1.txt', 'w', encoding = 'utf-8') as f:
#					for tok in pp1:
#						f.write(tok + '\n')

#				with io.open(args.output + directory[3 : ] + '-zh-pp2.txt', 'w', encoding = 'utf-8') as f:
#					for tok in pp2:
#						f.write(tok + '\n')

#				with io.open(args.output + directory[3 : ] + '-zh-base1.txt', 'w', encoding = 'utf-8') as f:
#					for tok in base1:
#						f.write(tok + '\n')

#				with io.open(args.output + directory[3 : ] + '-zh-base2.txt', 'w', encoding = 'utf-8') as f:
#					for tok in base2:
#						f.write(tok + '\n')

#				with io.open(args.output + directory[3 : ] + '-zh-tuples1.txt', 'w', encoding = 'utf-8') as f:
#					f.write('\t'.join(w for w in ['VERB_lemma', 'VERB_lexical', 'Prep_lemma', 'Prep_lexical', 'PP_head_lemma', 'PP_head_lexical', 'PP_head_POS', 'VERB_id', 'Head_id']) + '\n')
#					for tok in tuples1:
#						f.write('\t'.join(w for w in tok) + '\n')

#				with io.open(args.output + directory[3 : ] + '-zh-tuples2.txt', 'w', encoding = 'utf-8') as f:
#					f.write('\t'.join(w for w in ['VERB_lemma', 'VERB_lexical', 'Prep_lemma', 'Prep_lexical', 'PP_head_lemma', 'PP_head_lexical', 'PP_head_POS', 'VERB_id', 'Head_id']) + '\n')
#					for tok in tuples2:
#						f.write('\t'.join(w for w in tok) + '\n')

#				with io.open(args.output + directory[3 : ] + '-zh-pp1-lemma.txt', 'w', encoding = 'utf-8') as f:
#					for tok in pp1_lemmas:
#						f.write(tok + '\n')

#				with io.open(args.output + directory[3 : ] + '-zh-pp2-lemma.txt', 'w', encoding = 'utf-8') as f:
#					for tok in pp2_lemmas:
#						f.write(tok + '\n')
				
#				with io.open(args.output + directory[3 : ] + '-zh-pro1.txt', 'w', encoding = 'utf-8') as f:
#					for tok in pp1_pro:
#						f.write(tok + '\n')

#				with io.open(args.output + directory[3 : ] + '-zh-pro2.txt', 'w', encoding = 'utf-8') as f:
#					for tok in pp2_pro:
#						f.write(tok + '\n')

#				with io.open(args.output + directory[3 : ] + '-zh-verb.txt', 'w', encoding = 'utf-8') as f:
#					for tok in verb:
#						f.write(tok + '\n')
				
				with io.open(args.output + directory[3 : ] + '-zh-full.txt', 'w', encoding = 'utf-8') as f:
					for tok in full_sent:
						f.write(tok + '\n')


#				with io.open(args.output + directory[3 : ] + '-en-distance1.txt', 'w', encoding = 'utf-8') as f:
#					for tok in distance_pp1:
#						f.write(tok + '\n')

#				with io.open(args.output + directory[3 : ] + '-en-distance2.txt', 'w', encoding = 'utf-8') as f:
#					for tok in distance_pp2:
#						f.write(tok + '\n')


'''
				all_short_closer = []
				all_longer_closer = [] 
				all_equal = []

				for i in range(1000000):
					sample = random.choices(pp_len, k=len(pp_len))

					short_closer = 0
					longer_closer = 0
					equal = 0

					for tok in sample:
						if tok[0] > tok[1]:
							short_closer += 1
						if tok[0] < tok[1]:
							longer_closer += 1
						if tok[0] == tok[1]:
							equal += 1

					total = short_closer + longer_closer + equal

					all_short_closer.append(short_closer * 100 / total)
					all_longer_closer.append(longer_closer * 100 / total)
					all_equal.append(equal * 100 / total)

				all_short_closer.sort()
				all_longer_closer.sort()
				all_equal.sort()

				with io.open('/Users/Silverlining/Desktop/PP-new/' + directory[3 : ] + '-zh-statistics.txt', 'w', encoding = 'utf-8') as f:
					f.write(str(round(statistics.mean(all_short_closer), 2)) + '\n')
					f.write(str(round(all_short_closer[25000], 2)) + '\n')
					f.write(str(round(all_short_closer[975000], 2)) + '\n')
				#	f.write(str(round(statistics.pstdev(all_short_closer), 2)) + '\n')
					f.write(str(round(statistics.mean(all_longer_closer), 2)) + '\n')
					f.write(str(round(all_longer_closer[25000], 2)) + '\n')
					f.write(str(round(all_longer_closer[975000], 2)) + '\n')
				#	f.write(str(round(statistics.pstdev(all_longer_closer), 2)) + '\n')
					f.write(str(round(statistics.mean(all_equal), 2)) + '\n')
					f.write(str(round(all_equal[25000], 2)) + '\n')
					f.write(str(round(all_equal[975000], 2)) + '\n')
				#	f.write(str(round(statistics.pstdev(all_equal), 2)) + '\n')


'''
