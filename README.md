# text-inductor
An experiment in stochastic context-free grammar optimization.  The grammars define are used to generate random words intended for a specific purpose, e.g. "Generate words that would make good names for Harry Potter spells".  Given a grammar with a vector of probabilities for each rule, the goal is to "learn" better probabilities, i.e. probabilities that make the grammar generate words that better fit this overall criterion.  Right now, very simple optimization techniques are used, but this may change in the future.

## Overview

The central data structure behind all of text-inductor is the Grammar class, which is defined in grammar.py.  A grammar can be created manually in Python, or imported using the grammar_from_file() function in grammar.py.

spell.txt gives an example of how to format grammar rules.  Here is an excerpt:

     4: L -> EXX
    *2: L -> EXs
    *3: L -> io
    
The number represents the weight of a rule.  These numbers are normalized in code, so there is no need for all of the weights for a nonterminal to add up to 1.

Capital letters represent nonterminal symbols.  These will be used to generate more characters.

Lowercase letters represent terminal symbols.  These form the letters of the final word that is generated.

The asterisk turns a rule into a wildcard rule.  These rules' probabilities will be changed during the optimization phase.  Rules without this wildcard will not be affected.
