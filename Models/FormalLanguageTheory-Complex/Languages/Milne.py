
from FormalLanguage import FormalLanguage
from LOTlib3.Grammar import Grammar

class Milne(FormalLanguage):
    """
    From https://www.sciencedirect.com/science/article/pii/S0306452217304645#f0025
    """
    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', '%s', ['A'], 1.0)
        
        self.grammar.add_rule('A', 'a%s', ['D'], 1.0)
        self.grammar.add_rule('A', 'a%s', ['C'], 1.0)

        self.grammar.add_rule('D', 'd%s', ['C'], 1.0)

        self.grammar.add_rule('C', 'c%s', ['G'], 1.0)
        self.grammar.add_rule('C', 'c%s', ['F'], 1.0)
        
        self.grammar.add_rule('G', 'g%s', ['F'], 1.0)

        self.grammar.add_rule('F', 'f', None, 1.0)
        self.grammar.add_rule('F', 'f%s', ['X'], 1.0) # last two states are X,Y so they aren't D,C
        
        self.grammar.add_rule('X', 'c', None, 1.0)
        self.grammar.add_rule('X', 'c%s', ['Y'], 1.0)
       
        self.grammar.add_rule('Y', 'g', None, 1.0)

    def terminals(self):
        return list('acdgf')

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

    language = Milne()
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
        "id": "Milne",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/Milne.json", "w") as f:
        json.dump(result, f, indent=2)
