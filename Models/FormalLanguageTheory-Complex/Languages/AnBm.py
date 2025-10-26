import itertools
from LOTlib3.Miscellaneous import partitions
from FormalLanguage import FormalLanguage
from LOTlib3.Grammar import Grammar
from random import random

class AnBm(FormalLanguage):
    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', 'a%s', ['S'], 2.0)
        self.grammar.add_rule('S', 'a%s', ['T'], 1.0)
        self.grammar.add_rule('T', 'b%s',  ['T'], 2.0)
        self.grammar.add_rule('T', 'b',    None, 1.0)

    def terminals(self):
        return list('ab')

class AnBmA2n(FormalLanguage):
    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', 'a%s', ['S'], 2.0)
        self.grammar.add_rule('S', 'a%s', ['T'], 1.0)
        self.grammar.add_rule('T', 'b%s',  ['T'], 2.0)
        self.grammar.add_rule('T', 'b',    None, 1.0)
        
    def sample_string(self):
        s = str(self.grammar.generate())
        return s + 'a'*(s.count("a")*2)

    def terminals(self):
        return list('ab')

class AnBmCm(FormalLanguage):

    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', 'a%s', ['S'], 2.0)
        self.grammar.add_rule('S', 'a%s', ['T'], 1.0)
        self.grammar.add_rule('T', 'b%s',  ['T'], 2.0)
        self.grammar.add_rule('T', 'b',    None, 1.0)

    def terminals(self):
        return list('abc')
    
    def sample_string(self):
        s = str(self.grammar.generate())
        return s + ('c'*s.count('b'))

class AnBmCnpm(FormalLanguage):

    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', 'a%s', ['S'], 2.0)
        self.grammar.add_rule('S', 'a%s', ['T'], 1.0)
        self.grammar.add_rule('T', 'b%s',  ['T'], 2.0)
        self.grammar.add_rule('T', 'b',    None, 1.0)

    def terminals(self):
        return list('abc')
    
    def sample_string(self):
        s = str(self.grammar.generate())
        return s + ('c'*(s.count('a') + s.count('b')))

class AnBmCnm(FormalLanguage):

    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', 'a%s', ['S'], 2.0)
        self.grammar.add_rule('S', 'a%s', ['T'], 1.0)
        self.grammar.add_rule('T', 'b%s',  ['T'], 2.0)
        self.grammar.add_rule('T', 'b',    None, 1.0)

    def terminals(self):
        return list('abc')
    
    def sample_string(self):
        s = str(self.grammar.generate())
        return s + ('c'*(s.count('a')*s.count('b')))
    

class AnBk(FormalLanguage):
    """
    A^n B^k, k>n, with n, k-n sampled from a geometric
    """

    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', 'a%sb', ['S'], 2.0)
        self.grammar.add_rule('S', 'ab',    None, 1.0)

    def terminals(self):
        return list('ab')

    def sample_string(self): # fix that this is not CF
        s = str(self.grammar.generate()) # from a^n b^n

        mmn=1
        while random() < (2./3.):
            mmn += 1

        s = s+'b'*mmn

        return s

    def all_strings(self):
        for r in itertools.count(1):
            for n,m in partitions(r, 2, 1): # partition into two groups (NOTE: does not return both orders)
                if m>n:
                    yield 'a'*n + 'b'*m
                if n>m:
                    yield 'a'*m + 'b'*n
    
# just for testing
if __name__ == '__main__':
    import json
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Generate language examples')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate (default: 11)')
    args = parser.parse_args()

    language = AnBm()
    data_output = language.sample_data(args.num_examples)

    # Extract strings from Counter and create example list
    counter = data_output[0].output
    examples = []
    for string, count in counter.items():
        for _ in range(count):
            examples.append({"i": [], "o": [string]})
            if len(examples) >= args.num_examples:
                break
        if len(examples) >= args.num_examples:
            break

    # Create JSON structure
    result = {
        "canary": "",
        "id": "AnBm",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/AnBm.json", "w") as f:
        json.dump(result, f, indent=2)
