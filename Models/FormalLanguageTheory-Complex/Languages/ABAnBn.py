import itertools
from FormalLanguage import FormalLanguage, compute_all_strings
from LOTlib3.Grammar import Grammar

class ABAnBn(FormalLanguage):
    """
    An AB language followed by AnBn
    """
    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', 'a%s', ['S'], 1.0)
        self.grammar.add_rule('S', 'b%s', ['S'], 1.0)
        self.grammar.add_rule('S', '%s', ['Q'], 2.0)
        
        self.grammar.add_rule('Q', 'a%sb', ['Q'], 2.0)
        self.grammar.add_rule('Q', 'ab',   None, 1.0)

    def terminals(self):
        return list('ab')

    def sample_string(self):
        while True:
            x = str(self.grammar.generate())
            y = str(self.grammar.generate())
            if x != y:
                return x+y

    def all_strings(self):
        assert False


# just for testing
if __name__ == '__main__':
    import json
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Generate language examples')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate (default: 11)')
    args = parser.parse_args()

    language = ABAnBn()
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
        "id": "ABAnBn",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/ABAnBn.json", "w") as f:
        json.dump(result, f, indent=2)
