#usr/bin/env python3
import io, sys

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

def count_adp(file_handle):
	with io.open(file_handle, encoding = 'utf-8') as f:
		adp_list = []
		sent = conll_read_sentence(f)
		while sent is not None:
			for tok in sent:
				if tok[7] == 'obl':
					for tok_x in sent:
						if tok_x[6] == tok[0] and tok_x[3] == 'ADP' and tok_x[7] == 'case' and int(tok_x[0]) > int(tok[0]):
							adp_list.append(tok_x[1])
			sent = conll_read_sentence(f)
	return adp_list

def count_verbal_adp(file_handle):
	preverbal_list = 0
	postverbal_list = 0
	with io.open(file_handle, encoding = 'utf-8') as f:
		adp_list = []
		sent = conll_read_sentence(f)
		while sent is not None:
			for t in sent:
				if t[3] == 'VERB':				
					for tok in sent:
						if tok[7] == 'obl' and tok[6] == t[0]:
							for tok_x in sent:
								if tok_x[6] == tok[0] and tok_x[3] == 'ADP' and tok_x[7] == 'case' and int(tok_x[0]) < int(tok[0]):
									adp_list.append(tok_x[1])

									if int(tok[0]) > int(t[0]):
										postverbal_list += 1
									if int(tok[0]) < int(t[0]):
										preverbal_list += 1
			sent = conll_read_sentence(f)
	return adp_list, preverbal_list, postverbal_list

adp, preverbal, postverbal= count_verbal_adp(sys.argv[1])
print(len(set(adp)))
print(preverbal)
print(postverbal)



''''

#### Dealing with preposition and postpositions in Mandarin #####

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


# generate V PP...PP...
def VP(file_handle):
	with io.open(file_handle, encoding='utf-8') as f:
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

						pp1_lexical_head = sent[min(prep_head) - 1][1]
						pp2_lexical_head = sent[max(prep_head) - 1][1]

						exceptions = 0

						for tok_x in sent:
							if tok_x[6] == sent[min(prep_head) - 1][0] and tok_x[3] == 'ADP' and tok_x[7] == 'acl':
								exceptions += 1

							if tok_x[6] == sent[max(prep_head) - 1][0] and tok_x[3] == 'ADP' and tok_x[7] == 'acl':
								exceptions += 1

						if exceptions == 0:	
							vp = []
							vp.append(' '.join(tok for tok in pp1_new))
							vp.append(' '.join(tok for tok in pp2_new))
							print(pp1_new)
							vp.append(pp1_len)
							vp.append(pp2_len)		

							vp.append(sent[min(prep_head) - 1][7]) #dependent relation between lexical head of the PP and the verb
							vp.append(sent[max(prep_head) - 1][7])
							vp.append(sent[min(prep_head) - 1][3])
							vp.append(sent[max(prep_head) - 1][3])
						
							verb_phrase.append(vp)	

			sent = conll_read_sentence(f)
	return verb_phrase

zh_adp = VP(sys.argv[1])


short_closer = 0
long_closer = 0
equal = 0


for tok in zh_adp:
	if tok[-3] == 'obl' and tok[-4] == 'obl':
		if tok[2] > tok[3]:
			short_closer += 1
		if tok[2] < tok[3]:
			long_closer += 1
		if tok[2] == tok[3]:
			equal += 1

total = short_closer + long_closer + equal

print(round(short_closer * 100 / total, 2))
print(round(long_closer * 100 / total, 2))
print(round(equal * 100 / total, 2))
print(total)

'''