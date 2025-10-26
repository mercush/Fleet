import itertools
from FormalLanguage import FormalLanguage, compute_all_strings
from LOTlib3.Grammar import Grammar



class ABnen(FormalLanguage):
    #((AB)^n)^n
    
    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', 'ab%s', ['S'], 1.0)
        self.grammar.add_rule('S', 'ab', None, 2.0)

    def terminals(self):
        return list('ab')

    def sample_string(self):
         s = str(self.grammar.generate())
         return s*(len(s)//2)

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

    language = ABnen()
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
        "id": "ABnen",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/ABnen.json", "w") as f:
        json.dump(result, f, indent=2)
