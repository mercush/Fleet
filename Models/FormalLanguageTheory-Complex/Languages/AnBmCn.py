import itertools
from LOTlib3.Miscellaneous import partitions
from FormalLanguage import FormalLanguage
from LOTlib3.Grammar import Grammar
from random import random

class AnBmCn(FormalLanguage):
    """
    Anything in AnBmCn
    """

    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', 'a%sc', ['S'], 2.0)
        self.grammar.add_rule('S', 'a%sc', ['T'], 1.0)
        self.grammar.add_rule('T', 'b%s',  ['T'], 2.0)
        self.grammar.add_rule('T', 'b',    None, 1.0)

    def terminals(self):
        return list('abc')

            
            
# just for testing
if __name__ == '__main__':
    import json
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Generate language examples')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate (default: 11)')
    args = parser.parse_args()

    language = AnBmCn()
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
        "id": "AnBmCn",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/AnBmCn.json", "w") as f:
        json.dump(result, f, indent=2)
