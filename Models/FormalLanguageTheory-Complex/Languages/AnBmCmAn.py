import itertools
from LOTlib3.Miscellaneous import partitions
from FormalLanguage import FormalLanguage
from LOTlib3.Grammar import Grammar

class AnBmCmAn(FormalLanguage):
    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', 'a%sa', ['S'], 2.0)
        self.grammar.add_rule('S', 'a%sa', ['T'], 1.0)
        self.grammar.add_rule('T', 'b%sc', ['T'], 2.0)
        self.grammar.add_rule('T', 'bc',    None, 1.0)

    def terminals(self):
        return list('abcd')

    def sample_string(self):
        return str(self.grammar.generate())

    def all_strings(self):
        for r in itertools.count(1):
            for n,m in partitions(r, 2, 1): # partition into two groups (NOTE: does not return both orders)
                yield 'a'*n + 'b'*m + 'c'*m + 'a'*n
                if n != m:
                    yield 'a'*m + 'b'*n + 'c'*n + 'a'*m

# just for testing
if __name__ == '__main__':
    import json
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Generate language examples')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate (default: 11)')
    args = parser.parse_args()

    language = AnBmCmAn()
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
        "id": "AnBmCmAn",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/AnBmCmAn.json", "w") as f:
        json.dump(result, f, indent=2)
