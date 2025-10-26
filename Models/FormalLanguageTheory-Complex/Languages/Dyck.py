import itertools
from FormalLanguage import FormalLanguage
from LOTlib3.Grammar import Grammar

def dyck_at_depth(n):
    if n == 1:
        yield '()'
    else:
        for k in dyck_at_depth(n-1):
            yield '()' + k
            yield '('+k+')'

class Dyck(FormalLanguage):

    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', '(%s)', ['S'], 1.0)
        self.grammar.add_rule('S', '()%s', ['S'], 1.0)
        self.grammar.add_rule('S', '()',    None, 1.0)

    def terminals(self):
        return list(')(')

    def all_strings(self):
        for n in itertools.count(1):
            for s in dyck_at_depth(n):
                yield s



# just for testing
if __name__ == '__main__':
    import json
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Generate language examples')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate (default: 11)')
    args = parser.parse_args()

    language = Dyck()
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
        "id": "Dyck",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/Dyck.json", "w") as f:
        json.dump(result, f, indent=2)
