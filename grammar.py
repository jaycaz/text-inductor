#####################################
# Word Generator using Text Grammar #
#####################################
# Jordan Cazamias                   #
# 2014                              #
#####################################

import re

CHAR_SPACE = 0.2
DX = 1 + CHAR_SPACE
COMMENT = "#"
ARROW = "->"
SYMBOLNAME = "_5by5"
LIBNAME = "i_pix.cfdg"
TERM = "term"

class Rule:
	def __init__(self, lhs, rhs, weight):
		self.lhs = lhs
		self.rhs = rhs
		self.weight = weight
		
	def __repr__(self):
		return "{0} : {1} {2} {3}".format(self.weight, self.lhs, ARROW, self.rhs)

class Grammar:
	def __init__(self, nonterminals, terminals, rules, start):
		self.nonterminals = nonterminals
		self.terminals = terminals
		self.rules = rules
		self.start = start
		

def term(symbol):
	return "{0}{1}".format(symbol.upper(), TERM)
	
# Splits
def splitrule(rule):
	ruleparts = re.findall(r"[^: ]+", rule)
	ruleparts = filter(lambda a: a != ARROW, ruleparts)
	if len(ruleparts) == 2:
			ruleparts.insert(0, 1)
	if len(ruleparts) != 3:		
		print "Error: malformed rule {0}".format(rule)
		raise Exception
	return ruleparts
	
def getweight(rule):
	ruleparts = splitrule(rule)
	return ruleparts[0]
	
def getlhs(rule):
	ruleparts = splitrule(rule)
	return ruleparts[1]
	
def getrhs(rule):
	ruleparts = splitrule(rule)
	return ruleparts[2]

def parse_grammar_file(filename):
	# Open input grammar file for parsing
	print "Opening {0}...".format(filename)
	try:
		infile = open(filename, 'r')
	except IOError:
		print "Error: {0} could not be found".format(filename)
		sys.exit(-1)
		
	#find starting shape
	while True:
		firstline = infile.readline()
		if firstline != "\n" and firstline[0:len(COMMENT)] != COMMENT:
			break
	
	#parse starting shape
	if not("start" in firstline.lower()):
		print "Error: start symbol could not be found"
		raise Exception
	else:
		startsymbol = firstline.split()[-1]
		if not startsymbol.isupper():
			print "Error: start symbol {0} must be a nonterminal (i.e. capital letter)"
			raise Exception
		
	rulelines = infile.readlines()
	rulelines = filter(lambda r: r != "\n", rulelines)
	rulelines = [r.strip() for r in rulelines]
	
	nonterminals = []
	terminals = []
	rules = []
	
	# parse rules for correct syntax and find all symbols
	for line in rulelines:
		lhs = getlhs(line)
		rhs = getrhs(line)
		weight = getweight(line)
	
		#print("({0} | {1} | {2})".format(rule.weight, rule.lhs, rule.rhs))
		
		if not str(weight).isdigit():
			print "Error: rule '{0}' has an invalid/NaN weight".format(line)
			raise Exception
		
		if len(lhs) != 1:
			print "Error: rule '{0}' has a malformed left-hand side".format(line)
			raise Exception
		
		if not (lhs in nonterminals):
			nonterminals.append(lhs)
		
		for symbol in rhs:
			if not (symbol.isupper()) and not(symbol in terminals):
				terminals.append(symbol)
				
		r = Rule(lhs, rhs, int(weight))
		rules.append(r)
		
	print "Nonterminals: {0}".format(nonterminals)
	print "Terminals: {0}".format(terminals)
	print "Start Symbol: {0}".format(startsymbol)
	print "Rules: ["
	for rule in rules:
		print str(rule)
	print "]"
	
	grammar = Grammar(nonterminals, terminals, rules, startsymbol)
	return grammar
	
		
def import_rules(filename):
		# Open input grammar file for parsing
		print "Opening {0}...".format(filename)
		try:
			infile = open(filename, 'r')
		except IOError:
			print "Error: {0} could not be found".format(filename)
			sys.exit(-1)
			
		# Open output grammar file for writing
		try:
			outfilename = filename.replace(".txt", ".cfdg")
			outfile = open(outfilename, 'w')
		except IOError:
			print "Error: {0} could not be opened for writing".format(outfilename)
			sys.exit(-1)

	
	