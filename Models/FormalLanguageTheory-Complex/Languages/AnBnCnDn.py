from FormalLanguage import FormalLanguage
from LOTlib3.Grammar import Grammar

class AnBnCnDn(FormalLanguage):

    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', 'a%sb', ['S'], 2.0)
        self.grammar.add_rule('S', 'ab',    None, 1.0)

    def terminals(self):
        return list('abcd')

    def sample_string(self): # fix that this is not CF
        s = str(self.grammar.generate())
        return s + 'c'*(len(s)//2) + 'd'*(len(s)//2)

    def all_strings(self):
        n=1
        while True:
            yield 'a'*n + 'b'*n + 'c'*n + 'd'*n
            n += 1

# just for testing
if __name__ == '__main__':
    import json
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Generate language examples')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate (default: 11)')
    args = parser.parse_args()

    language = AnBnCnDn()
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
        "id": "AnBnCnDn",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/AnBnCnDn.json", "w") as f:
        json.dump(result, f, indent=2)
