import itertools
from LOTlib3.Miscellaneous import partitions
from FormalLanguage import FormalLanguage
from LOTlib3.Grammar import Grammar

class AnBmCnDm(FormalLanguage):
    def __init__(self):
        self.grammarA = Grammar(start='A')
        self.grammarA.add_rule('A', 'a%s', ['A'], 2.0)
        self.grammarA.add_rule('A', 'a',   None, 1.0)

        self.grammarB = Grammar(start='B')
        self.grammarB.add_rule('B', 'b%s', ['B'], 2.0)
        self.grammarB.add_rule('B', 'b',   None, 1.0)

    def terminals(self):
        return list('abcd')

    def sample_string(self):
        a = str(self.grammarA.generate())
        b = str(self.grammarB.generate())
        return a+b+('c'*len(a))+('d'*len(b))

    def all_strings(self):
        for r in itertools.count(1):
            for n,m in partitions(r, 2, 1): # partition into two groups (NOTE: does not return both orders)
                yield 'a'*n + 'b'*m + 'c'*n + 'a'*m
                if n != m:
                    yield 'a'*m + 'b'*n + 'c'*m + 'a'*n

# just for testing
if __name__ == '__main__':
    import json
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Generate language examples')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate (default: 11)')
    args = parser.parse_args()

    language = AnBmCnDm()
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
        "id": "AnBmCnDm",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/AnBmCnDm.json", "w") as f:
        json.dump(result, f, indent=2)
