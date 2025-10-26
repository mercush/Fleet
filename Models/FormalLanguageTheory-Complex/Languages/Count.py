import itertools
from FormalLanguage import FormalLanguage
from LOTlib3.Grammar import Grammar

class Count(FormalLanguage):
    """

    The language ababbabbbabbbb etc

    """

    def __init__(self):
        # This grammar is just a proxy, it gets replaced in sample
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', 'a%s', ['S'], 1.5) # if we make this 2, then we end up with things that are waay too long
        self.grammar.add_rule('S', 'a',    None, 1.0)

    def sample_string(self):
        proxy = str(self.grammar.generate())
        out = ''
        for i in range(len(proxy)):
            out = out+'a' + 'b'*(i+1)
        return out

    def terminals(self):
        return list('ab')

    def all_strings(self):
        for n in itertools.count(0):
            out = ''
            for i in range(n):
                out = out + 'a' + 'b' * (i + 1)
            yield out

# just for testing
if __name__ == '__main__':
    import json
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Generate language examples')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate (default: 11)')
    args = parser.parse_args()

    language = Count()
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
        "id": "Count",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/Count.json", "w") as f:
        json.dump(result, f, indent=2)
