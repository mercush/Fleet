import itertools
from FormalLanguage import FormalLanguage, compute_all_strings
from LOTlib3.Grammar import Grammar

class ABA(FormalLanguage):
    """
    Similar to Marcus ABB experiment, except we allow AAA (for simplicity)
    """

    def __init__(self):
        self.grammar = Grammar(start='S') # NOTE: This grammar does not capture the rule -- we do that in sample!
        self.grammar.add_rule('S', '%s%s', ['T','T'], 1.0)

        for t in self.terminals():
            self.grammar.add_rule('T', t, None, 1.0)

    def sample_string(self): # fix that this is not CF
        s = str(self.grammar.generate())
        return s + s[0] # copy the first  element

    def terminals(self):
        return list('gGtTnNlL') # ga gi ta ti na ni la li

    def all_strings(self):
        for t1 in self.terminals():
            for t2 in self.terminals():
                yield t1 + t2 + t1

class ABB(FormalLanguage):
    """
    Similar to Marcus ABB experiment, , except we allow AAA (for simplicity)
    """

    def __init__(self):
        self.grammar = Grammar(start='S') # NOTE: This grammar does not capture the rule -- we do that in sample!
        self.grammar.add_rule('S', '%s%s', ['T','T'], 1.0)

        for t in self.terminals():
            self.grammar.add_rule('T', t, None, 1.0)

    def sample_string(self): # fix that this is not CF
        s = str(self.grammar.generate())
        return s + s[1] # copy the second element

    def terminals(self):
        return list('gGtTnNlL') # ga gi ta ti na ni la li

    def all_strings(self):
        for t1 in self.terminals():
            for t2 in self.terminals():
                yield t1 + t2 + t2
if __name__ == '__main__':
    import json
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Generate language examples')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate (default: 11)')
    args = parser.parse_args()

    language = ABA()
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
        "id": "ABA",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/ABA.json", "w") as f:
        json.dump(result, f, indent=2)
