#####################################
# Word Generator using Text Grammar #
#####################################
# Jordan Cazamias                   #
# 2014                              #
#####################################

# Grammar Syntax Definitions:
# <Grammar> := 
# 	<Startline>
# 	<Rule>+
#	
# <Startline> := start <StartSymbol>
# <StartSymbol> is a symbol in the set of nonterminals
# <Rule> := <Weight>? : <Nonterminal> -> <String>
# <String> := <Nonterminal | Terminal>* | <Empty>
# <Empty> := defined below
#
# The rule weight is optional.  If no weight is specified, a weight of 1 is used.
# As shown above, a rule may have an empty string as the RHS, indicated by the empty symbol (defined below)

import re

CHAR_SPACE = 0.2
DX = 1 + CHAR_SPACE
COMMENT = "#"
ARROW = "->"
EMPTY = "~"
WILDCARD = "*"
SYMBOLNAME = "_5by5"
LIBNAME = "i_pix.cfdg"
TERM = "term"


class Rule:
	def __init__(self, lhs, rhs, weight, fixed = True):
		self.lhs = lhs
		self.rhs = rhs
		self.weight = weight
		self.fixed = fixed
		
	def __repr__(self):
		fixedstr = "" if self.fixed else "*"
		return "{0} {1} : {2} {3} {4}".format(
			fixedstr, self.weight, self.lhs, ARROW, self.rhs)

class Grammar:
	def __init__(self, nonterminals, terminals, rules, start):
		self.nonterminals = nonterminals
		self.terminals = terminals
		self.rules = rules
		self.start = start
	
	def __repr__(self):
		string = "Grammar \n{\n"
		string += "Nonterminals: {0}\n".format(self.nonterminals)
		string += "Terminals: {0}\n".format(self.terminals)
		string += "Start Symbol: {0}\n".format(self.start)
		string += "Rules: [\n"
		for rule in self.rules:
			string += str(rule) + "\n"
		string += "]\n}\n"
		return string
		

# Creates a Grammar instance from a specification in a grammar file
def grammar_from_file(filename):
	# Open input grammar file for parsing
	print "Opening {0}...".format(filename)
	try:
		infile = open(filename, 'r')
	except IOError as err:
		print "Error: {0} could not be found".format(filename)
		raise err
		
	try:
		grammar = parse_grammar_file(infile)
	except Exception as err:
		infile.close()
		raise err
	
	infile.close()		
	return grammar
		
	# # Open output grammar file for writing
	# try:
		# outfilename = filename.replace(".txt", ".cfdg")
		# outfile = open(outfilename, 'w')
	# except IOError:
		# print "Error: {0} could not be opened for writing".format(outfilename)
		# sys.exit(-1)

def term(symbol):
	return "{0}{1}".format(symbol.upper(), TERM)
	
# Splits
def splitrule(rule):
	ruleparts = re.findall(r"[^: ]+", rule)
	ruleparts = filter(lambda a: a != ARROW and a != WILDCARD, ruleparts)
	if len(ruleparts) == 2:
			ruleparts.insert(0, "1")
	if len(ruleparts) != 3:		
		print "Error: malformed rule {0}".format(rule)
		raise Exception
	return ruleparts
	
def getfixed(rule):
	return rule.lstrip()[0: len(WILDCARD)] != WILDCARD
	
def getweight(rule):
	ruleparts = splitrule(rule)
	weight = ruleparts[0].replace(WILDCARD, "")
	return weight
	
def getlhs(rule):
	ruleparts = splitrule(rule)
	return ruleparts[1]
	
def getrhs(rule):
	ruleparts = splitrule(rule)
	rhs = ruleparts[2]
	if rhs == EMPTY:
		return ''
	else:
		return rhs

			
def parse_grammar_file(file):		
	#find starting shape
	while True:
		firstline = file.readline()
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
		
	rulelines = file.readlines()
	rulelines = filter(lambda r: r != "\n", rulelines)
	rulelines = [r.strip() for r in rulelines]
	
	nonterminals = []
	terminals = []
	rules = []
	
	# parse rules for correct syntax and find all symbols
	for line in rulelines:
		if line.lstrip()[0] == COMMENT:
			continue
		lhs = getlhs(line)
		rhs = getrhs(line)
		weightstr = getweight(line)
		fixed = getfixed(line)
	
		#print "({0} | {1} | {2})".format(rule.weight, rule.lhs, rule.rhs)
		
		try:
			weight = float(weightstr)
		except ValueError as err:
			print "Error: rule '{0}' has an invalid/NaN weight".format(line)
			raise err
		
		if len(lhs) != 1:
			print "Error: rule '{0}' has a malformed left-hand side".format(line)
			raise Exception
		
		if not (lhs in nonterminals):
			nonterminals.append(lhs)
		
		for symbol in rhs:
			if not ((symbol == EMPTY) or (symbol.isupper()) or(symbol in terminals)):
				terminals.append(symbol)
				
		r = Rule(lhs, rhs, weight, fixed)
		rules.append(r)
		
	#print grammar
	
	grammar = Grammar(nonterminals, terminals, rules, startsymbol)
	return grammar
	
		