from FormalLanguage import FormalLanguage
from LOTlib3.Grammar import Grammar
from pickle import load

class Braine66(FormalLanguage):
    """
    Language from Braine '66
    """

    def __init__(self):
        self.grammar = Grammar(start='S')
        
        self.grammar.add_rule('S', '%s', ['A'], 6.0)
        self.grammar.add_rule('S', '%s', ['PQ'], 3.0)
        self.grammar.add_rule('S', '%s%s', ['PQ', 'A'], 2.0)
        self.grammar.add_rule('S', '%s%s', ['A', 'PQ'], 1.0)
        # A phrases:
        # ob = b
        # ordem = d
        # remin = r
        # gice = g
        # kivil = k
        # noot = n
        # yarmo = f

        # PQ Phrases:
        # ged = G
        # mervo = m
        # yag = y
        # leck = l
        
        # som = s
        # eena = e
        # wimp = w
        
        self.grammar.add_rule('A', 'fbd', None, 1.0) # yarmo ob ordem
        self.grammar.add_rule('A', 'frg', None, 1.0)
        self.grammar.add_rule('A', 'fk', None, 1.0)
        self.grammar.add_rule('A', 'fn', None, 1.0)
        
        self.grammar.add_rule('PQ', 'Gms', None, 1.0)
        self.grammar.add_rule('PQ', 'Gys', None, 1.0)
        self.grammar.add_rule('PQ', 'Gls', None, 1.0)
        
        self.grammar.add_rule('PQ', 'Gme', None, 1.0)
        self.grammar.add_rule('PQ', 'Gye', None, 1.0)
        self.grammar.add_rule('PQ', 'Gle', None, 1.0)
        
        self.grammar.add_rule('PQ', 'Gmw', None, 1.0)
        self.grammar.add_rule('PQ', 'Gyw', None, 1.0)
        self.grammar.add_rule('PQ', 'Glw', None, 1.0)
        

    def terminals(self):
        return list('bdrgknfGmylsew')

    def all_strings(self):
        for g in self.grammar.enumerate():
            yield str(g)

# just for testing
if __name__ == '__main__':
    import json
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Generate language examples')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate (default: 11)')
    args = parser.parse_args()

    language = Braine66()
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
        "id": "Braine66",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/Braine66.json", "w") as f:
        json.dump(result, f, indent=2)
