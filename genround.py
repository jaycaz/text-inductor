# Jordan Cazamias
# Generates a round of code

import os
import wordgen as gen
import inductor as ind
import sys
import pickle

NUM_ROUNDS = 8
NUM_VARIANTS = 10
NUM_EXEMPLARS = 25

SEED = 1

def gen_round(grammar, roundnum):
	grams = ind.gen_grammar_variants(grammar, NUM_VARIANTS, roundnum, NUM_ROUNDS, SEED)
	wordmat = gen.gen_words_file(grams, "Round-{0}.csv".format(roundnum), NUM_EXEMPLARS)
	
	datfilename = "Round-{0}.data".format(roundnum)	
	bakfilename = "Round-{0}.bak".format(roundnum)
	
	f = open(datfilename, "w")
	pickle.dump(grams, f)
	f.close()
	
	if not os.path.isfile(bakfilename):
		fbak = open(bakfilename, "w")
		pickle.dump(grams, fbak)
		fbak.close()

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Error: enter round number"
		raise Exception
		
	gram = gen.grammar_from_file("spell.txt")
	