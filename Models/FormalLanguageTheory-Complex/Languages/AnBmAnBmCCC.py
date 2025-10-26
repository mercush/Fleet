import itertools
from LOTlib3.Miscellaneous import partitions
from FormalLanguage import FormalLanguage
from LOTlib3.Grammar import Grammar

class AnBmAnBm(FormalLanguage):
    def __init__(self):
        self.grammarA = Grammar(start='A')
        self.grammarA.add_rule('A', 'a%s', ['A'], 2.0)
        self.grammarA.add_rule('A', 'a',   None, 1.0)

        self.grammarB = Grammar(start='B')
        self.grammarB.add_rule('B', 'b%s', ['B'], 2.0)
        self.grammarB.add_rule('B', 'b',   None, 1.0)

    def terminals(self):
        return list('ab')

    def sample_string(self):
        a = str(self.grammarA.generate())
        b = str(self.grammarB.generate())
        return a+b+a+b
		
    def all_strings(self):
        raise NotImplementedError
    

class AnBmAnBmCCC(FormalLanguage):
    def __init__(self):
        self.grammarA = Grammar(start='A')
        self.grammarA.add_rule('A', 'a%s', ['A'], 2.0)
        self.grammarA.add_rule('A', 'a',   None, 1.0)

        self.grammarB = Grammar(start='B')
        self.grammarB.add_rule('B', 'b%s', ['B'], 2.0)
        self.grammarB.add_rule('B', 'b',   None, 1.0)

    def terminals(self):
        return list('abc')

    def sample_string(self):
        a = str(self.grammarA.generate())
        b = str(self.grammarB.generate())
        return a+b+a+b+'ccc'
		
    def all_strings(self):
        raise NotImplementedError
    

# just for testing
if __name__ == '__main__':
    import json
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Generate language examples')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate (default: 11)')
    args = parser.parse_args()

    language = AnBmAnBmCCC()
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
        "id": "AnBmAnBmCCC",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/AnBmAnBmCCC.json", "w") as f:
        json.dump(result, f, indent=2)
