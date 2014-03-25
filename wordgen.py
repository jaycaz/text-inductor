#####################################
# Word Generator using Text Grammar #
#####################################
# Jordan Cazamias                   #
# 2014                              #
#####################################

import sys
import re
import string
import random as rand
import types
from grammar import Rule, Grammar, grammar_from_file

MAX_STEPS = 200
DEFAULT_NUM_WORDS = 10
DEFAULT_SEED = None

def gen_words_file(grammarlist, outfilename, numwords = 1, seed = None):
	if type(grammarlist) != types.ListType:
		grammarlist = [grammarlist]
	
	# try to open file for writing
	try:
		outfile = open(outfilename, 'w')
	except IOError as err:
		print "Error: could not open '{0}' for writing".format(outfilename)
		raise err
	
	wordmat = []
	print wordmat
	
	# create words lists
	for grammar in grammarlist:
		wordmat.append(gen_words(grammar, numwords, seed))
	
	for i in range(len(grammarlist)):
		outfile.write("Grammar {0},Score {0},".format(i))
	outfile.write("\n")
	
	for i in range(numwords):
		for j in range(len(grammarlist)):
			outfile.write("{0},,".format(wordmat[j][i]))
		outfile.write("\n")
		
	outfile.close()
	
	return wordmat
	

def gen_words(grammar, numwords = 1, seed = None):
	if seed != None:
		rand.seed(seed)

	words = []
		
	# generate map of nonterminals to rules
	rulemap = {}
	for nonterm in grammar.nonterminals:
		rulemap[nonterm] = []		
	for rule in grammar.rules:
		rulemap[rule.lhs].append(rule)
	
	# generate map of nonterminals to total weights
	weighttotals = {}
	for nonterm in grammar.nonterminals:
		weighttotals[nonterm] = 0
	for rule in grammar.rules:
		weighttotals[rule.lhs] += rule.weight
		
	for i in range(numwords):
		# begin forming generated string
		genstr = grammar.start
		
		# choose random nonterminal to expand
		nonterms = get_nonterms(genstr)
		numsteps = 0
		#print "--------------------"
		while len(nonterms) != 0 and numsteps < MAX_STEPS:
			#print genstr
			next_nonterm, next_pos = rand.choice(nonterms)
			
			# choose among the nonterminal's rules (weighted)
			next_rule = choose_rule(rulemap[next_nonterm], weighttotals[next_nonterm])
			
			# apply rule to string
			chars = list(genstr)
			chars.pop(next_pos)
			chars.insert(next_pos, next_rule.rhs)
			genstr = string.join(chars, '')
			
			nonterms = get_nonterms(genstr)
			numsteps += 1
		
		words.append(genstr)
		#print genstr
		#print "--------------------"
		
		if numsteps == MAX_STEPS:
			print "Error: generation exceeded maximum number of steps ({0})".format(MAX_STEPS)
			raise Exception
			
	return words
		
def get_nonterms(string):
	nonterms = []
	# returns list of 2-tuples (nonterminal value, position in string)
	for pos, char in list(enumerate(string)):
		if char.isupper():
			nonterms.append((char, pos))
			
	return nonterms
	
# weighted random selection from list of nonterminal rules
def choose_rule(rules, total_weight):
	randnum = rand.uniform(0, total_weight) - sys.float_info.epsilon
	randnum = max(0, randnum)
	currtotal = 0
	for rule in rules:
		currtotal += rule.weight
		if currtotal >= randnum:
			return rule
			
	print "Error: choosing rule from list {0} with weight total {1} resulted in invalid choice".format(
			rules, total_weight)
	raise Exception
	
	
if __name__ == "__main__":
	if len(sys.argv) < 2:
		filename = raw_input("Enter a file name to convert: ")
	else:
		filename = sys.argv[1]
		
	if len(sys.argv) < 3:
		numwords = DEFAULT_NUM_WORDS
	else:
		try:
			numwords = int(sys.argv[2])
		except:
			numwords = DEFAULT_NUM_WORDS
	
	if len(sys.argv) < 4:
		seed = DEFAULT_SEED
	else:
		try:
			seed = int(sys.argv[3])
		except:
			seed = DEFAULT_SEED
			
	gram = grammar_from_file(filename)
	generate_word(gram, numwords, seed)
		



	