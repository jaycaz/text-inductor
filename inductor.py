#####################################
# Word Generator using Text Grammar #
#####################################
# Jordan Cazamias                   #
# 2014                              #
#####################################

# Induction strategy:
#----------------------
# 1. Determine how many iterations to perform (i)
# 2. For each iteration:
#	a. Generate j grammar variants
#	b. For each grammar variant:
#		i. Generate k exemplars
#		ii. Rate each exemplar on a 1 to RATE_MAX
#		iii. Average the score and map the exemplar to the score
#	

# The std dev for the grammar variant random variables will decrease
# with each iteration, representing simulated annealing

import random as rand
import copy
import math

MAX_WEIGHT = 100
START_STD_DEV = 2
DEFAULT_ITERATIONS = 5
RATE_MAX = 5


def optimal_grammar(grammar_score_map):
	maxitem = reduce(lambda a,b: a if a[1] > b[1] else b, grammar_score_map.items())
	return maxitem[0]

# simulated annealing adjustment
# std dev should decrease to 0 when iteration == iterations
def weight_std_dev(iteration = 1, iterations = DEFAULT_ITERATIONS):
	if iterations == 1:
		return START_STD_DEV
	s = START_STD_DEV * (1 - (float(iteration - 1) / (iterations - 1)))
	return max(0, s)

# generates a new rule weight
# lognormal distribution centered around <center>
def gen_weight(center, iteration = 1, iterations = DEFAULT_ITERATIONS):
	s = weight_std_dev(iteration, iterations)
	r = rand.lognormvariate(math.log(center), s) 
	return min(r, MAX_WEIGHT) 

# takes grammar and generates n iterations
def gen_grammar_variants(grammar, n, iteration = 1, iterations = DEFAULT_ITERATIONS, seed = None):
	if seed != None:
		rand.seed(seed)

	variants = []
	for i in range(n):	
		newgrammar = copy.deepcopy(grammar)
		for rule in newgrammar.rules:
			if rule.fixed:
				continue
			oldweight = rule.weight
			rule.weight = gen_weight(oldweight, iteration, iterations)
			print "{0} -> {1}".format(oldweight, rule.weight)
		variants.append(newgrammar)
	return variants