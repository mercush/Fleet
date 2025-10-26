from FormalLanguage import FormalLanguage
from LOTlib3.Grammar import Grammar
from pickle import load

class English(FormalLanguage):
    """
    A fancier English language with a few kinds of recursion all at once
    """

    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', '%s%s', ['NP', 'VP'], 5.0)
        self.grammar.add_rule('NP', 'd%sn', ['AP'], 1.0)
        self.grammar.add_rule('NP', 'dn', None, 1.0)
        self.grammar.add_rule('NP', 'n', None, 1.0)
        self.grammar.add_rule('AP', 'a%s', ['AP'], 1.0)
        self.grammar.add_rule('AP', 'a', None, 5.0)

        self.grammar.add_rule('NP', '%s%s', ['NP', 'PP'], 0.50) # a little ambiguity
        self.grammar.add_rule('VP', '%s%s', ['VP', 'PP'], 0.50)
        self.grammar.add_rule('PP', 'p%s', ['NP'], 1.0)

        self.grammar.add_rule('VP', 'v', None, 1.0) # intransitive
        self.grammar.add_rule('VP', 'v%s', ['NP'], 1.0) # transitive
        self.grammar.add_rule('VP', 'vt%s', ['S'], 1.0) # v that S

        #self.grammar.add_rule('S', 'i%sh%s', ['S', 'S'], 1.0) 
        
    def terminals(self):
        return list('dnavtp')

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

    language = English()
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
        "id": "English",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/English.json", "w") as f:
        json.dump(result, f, indent=2)
