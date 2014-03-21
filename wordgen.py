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
from grammar import Rule, Grammar, grammar_from_file

MAX_STEPS = 200
DEFAULT_NUM_WORDS = 10
DEFAULT_SEED = None

def get_nonterms(string):
	nonterms = []
	# returns list of 2-tuples (nonterminal value, position in string)
	for pos, char in list(enumerate(string)):
		if char.isupper():
			nonterms.append((char, pos))
			
	return nonterms
	
# weighted random selection from list of nonterminal rules
def choose_rule(rules, total_weight):
	randnum = rand.randint(1, total_weight)
	currtotal = 0
	for rule in rules:
		currtotal += rule.weight
		if currtotal >= randnum:
			return rule
			
	print "Error: choosing rule from list {0} with weight total {1} resulted in invalid choice".format(
			rules, total_weight)
	raise Exception
	

def generate_word(grammar, n = 1, seed = None):
	if seed != None:
		rand.seed(seed)

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
		
	for i in range(n):
		# begin forming generated string
		genstr = grammar.start
		
		# choose random nonterminal to expand
		nonterms = get_nonterms(genstr)
		numsteps = 0
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
	
		#print "Final string {0}: {1}".format(i, genstr)
		print genstr
		
		if numsteps == MAX_STEPS:
			print "Error: generation exceeded maximum number of steps ({0})".format(MAX_STEPS)
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
		



	