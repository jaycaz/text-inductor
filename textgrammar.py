###################################
# Text Grammar to CFDG conversion #
###################################
# Jordan Cazamias #     2014      #
###################################

# Grammar Syntax Definitions #
# <Grammar> := 
	# <Startline>
	#
	# <Rule>+
	
# <Startline> := start <StartSymbol>
# <Rule> := <Weight>? : <Nonterminal> -> <Nonterminal | Terminal>*

# The rule weight is optional.  If no weight is specified, a weight of 1 is used.

import sys
import re

CHAR_SPACE = 0.2
DX = 1 + CHAR_SPACE
ARROW = "->"
SYMBOLNAME = "_5by5"
LIBNAME = "i_pix.cfdg"
TERM = "term"

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

def convert(infile, outfile):
	while True:
		firstline = infile.readline()
		if(firstline != "\n"):
			break
	
	#parse starting shape
	if not("start" in firstline.lower()):
		print "Error: start symbol could not be found"
		raise Exception
	else:
		startsymbol = firstline.split()[-1]
		if not startsymbol.isupper():
			print "Error: start symbol {0} must be a capital letter"
			raise Exception
		
	rules = infile.readlines()
	rules = filter(lambda r: r != "\n", rules)
	rules = [r.strip() for r in rules]
	
	nonterminals = []
	terminals = []
	
	# parse rules for correct syntax and find all symbols
	for rule in rules:
		weight = getweight(rule)
		lhs = getlhs(rule)
		rhs = getrhs(rule)
		
		print("({0} | {1} | {2})".format(weight, lhs, rhs))
		
		if not str(weight).isdigit():
			print "Error: rule '{0}' has an invalid/NaN weight".format(rule)
			raise Exception
		
		if len(lhs) != 1:
			print "Error: rule '{0}' has a malformed left-hand side".format(rule)
			raise Exception
		
		if not (lhs in nonterminals):
			nonterminals.append(lhs)
		
		for symbol in rhs:
			if not (symbol.isupper()) and not(symbol in terminals):
				terminals.append(symbol)
		
	print "Start: {0}".format(startsymbol)
	print "Nonterminals: {0}".format(nonterminals)
	print "Terminals: {0}".format(terminals)
	
	outfile.write("startshape {0}\n".format(startsymbol))
	outfile.write("import {0}\n\n".format(LIBNAME))
	
	# generate nonterminal rules
	for nonterminal in nonterminals:
		print "Finding all rules matching '{0}'".format(nonterminal)
		outfile.write("shape {0}\n".format(nonterminal))
		for rule in filter(lambda r: getlhs(r) == nonterminal, rules):
			weight = getweight(rule)
			weightstr = '' if weight == 1 else str(weight)
			outfile.write("rule {0}\n{{\n".format(weightstr))
			rhs = getrhs(rule)
			print "\t{0}".format(rule)
			for offset, symbol in list(enumerate(rhs)):
				if symbol.isupper():
					write = "\t{0} [x {1}]\n".format(symbol, offset * DX)
				else:
					write = "\t{0} [x {1}]\n".format(term(symbol), offset * DX)
				print write
				outfile.write(write)
			outfile.write("}\n")
		outfile.write("\n")
		
	outfile.write("\n")	
	
	# generate terminal rules
	for terminal in terminals:
		outfile.write("shape {0}\n{{\n".format(term(terminal)))
		outfile.write("\t{0}{1} []\n".format(terminal.upper(), SYMBOLNAME))
		outfile.write("}\n\n")
	
		
if __name__ == "__main__":
	if len(sys.argv) < 2:
		filename = raw_input("Enter a file name to convert: ")
	else:
		filename = sys.argv[1]
		
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
		
	#perform conversion
	try:
		convert(infile, outfile)
		print "Output CFDG grammar saved to {0}".format(outfilename)
	finally:
		infile.close()
		outfile.close()
	
	