from LOTlib3.Grammar import Grammar
from FormalLanguage import FormalLanguage


class AnABAn(FormalLanguage):

    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', 'a%saba', ['S'], 2.0)
        self.grammar.add_rule('S', 'aaba',    None, 1.0)

    def terminals(self):
        return list('ab')

    def all_strings(self):
        n=1
        while True:
            yield 'a'*n + 'aba'*(n)
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

    language = AnABAn()
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
        "id": "AnABAn",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/AnABAn.json", "w") as f:
        json.dump(result, f, indent=2)
