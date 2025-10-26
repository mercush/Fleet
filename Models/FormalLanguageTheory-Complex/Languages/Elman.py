
from FormalLanguage import FormalLanguage
from LOTlib3.Grammar import Grammar

class Elman(FormalLanguage):
    """
    From Saffran, Aslin, Newport studies.
    Strings consisting of               tupiro golabu bidaku padoti
    coded here with single characters:  tpr     glb    Bdk    PDT
    """
    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', '%s%s', ['T', 'S'], 2.0)
        self.grammar.add_rule('S', '%s',   ['T'], 1.0)
        self.grammar.add_rule('T', 'baa',    None, 1.0) # We are going to put a probability distribution on the words so that they can be evaluated reasonably, otherwise its hard to score uniform
        self.grammar.add_rule('T', 'dii',    None, 1.0)
        self.grammar.add_rule('T', 'guuu',    None, 1.0)

    def terminals(self):
        return list('badigu')

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

    language = Elman()
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
        "id": "Elman",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/Elman.json", "w") as f:
        json.dump(result, f, indent=2)
