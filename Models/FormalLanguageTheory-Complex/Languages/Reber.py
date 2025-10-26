
from FormalLanguage import FormalLanguage
from LOTlib3.Grammar import Grammar

class Reber(FormalLanguage):
    """
    From Reber, 1967
    """
    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', 'T%s', ['S1'], 1.0)
        self.grammar.add_rule('S', 'V%s', ['S3'], 1.0)

        self.grammar.add_rule('S1', 'P%s', ['S1'], 1.0)
        self.grammar.add_rule('S1', 'T%s', ['S2'], 1.0)

        self.grammar.add_rule('S3', 'X%s', ['S3'], 1.0)
        self.grammar.add_rule('S3', 'V%s', ['S4'], 1.0)

        self.grammar.add_rule('S2', 'X%s', ['S3'], 1.0)
        self.grammar.add_rule('S2', 'S',   None, 1.0)

        self.grammar.add_rule('S4', 'P%s', ['S2'], 1.0)
        self.grammar.add_rule('S4', 'S',   None, 1.0)

    def terminals(self):
        return list('PSTVX')

    def all_strings(self):
        for g in self.grammar.enumerate():
            yield str(g)



# just for testing
if __name__ == '__main__':
    import json
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Generate language examples')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate (default: 11)')
    args = parser.parse_args()

    language = Reber()
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
        "id": "Reber",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/Reber.json", "w") as f:
        json.dump(result, f, indent=2)
