import itertools
from FormalLanguage import FormalLanguage, compute_all_strings
from LOTlib3.Grammar import Grammar



class AB(FormalLanguage):

    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', 'a%s', ['S'], 2.0)
        self.grammar.add_rule('S', 'b%s', ['S'], 2.0)
        self.grammar.add_rule('S', 'a', None, 1.0)
        self.grammar.add_rule('S', 'b', None, 1.0)

    def terminals(self):
        return list('ab')

    def all_strings(self):
        for l in itertools.count(1):
            for s in compute_all_strings(l, alphabet='ab'):
                yield s
                
class aABb(FormalLanguage):

    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', 'a%sb', ['T'], 2.0)
        self.grammar.add_rule('T', 'a%s', ['T'], 2.0)
        self.grammar.add_rule('T', 'b%s', ['T'], 2.0)
        self.grammar.add_rule('T', 'a', None, 1.0)
        self.grammar.add_rule('T', 'b', None, 1.0)

    def terminals(self):
        return list('ab')

    def all_strings(self):
        raise NotImplementedError

class ABaaaAB(FormalLanguage):

    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', '%saaa%s', ['T', 'T'], 2.0)
        self.grammar.add_rule('T', 'a%s', ['T'], 2.0)
        self.grammar.add_rule('T', 'b%s', ['T'], 2.0)
        self.grammar.add_rule('T', 'a', None, 1.0)
        self.grammar.add_rule('T', 'b', None, 1.0)

    def terminals(self):
        return list('ab')

    def all_strings(self):
        raise NotImplementedError
if __name__ == '__main__':
    import json
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Generate language examples')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate (default: 11)')
    args = parser.parse_args()

    language = AB()
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
        "id": "AB",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/AB.json", "w") as f:
        json.dump(result, f, indent=2)
