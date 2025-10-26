
from FormalLanguage import FormalLanguage
from LOTlib3.Grammar import Grammar

# Every language uses these as X
OTHER_TERMINALS='1234567890wxyz'

class Gomez(FormalLanguage):
    """
        Gomez (2002) language 1b
    """

    def __init__(self, X):
        assert X < len(OTHER_TERMINALS)
        self.X=X

        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', 'a%sd', ['X'], 1.0)
        self.grammar.add_rule('S', 'b%se', ['X'], 1.0)

        for x in OTHER_TERMINALS[:self.X]:
            self.grammar.add_rule('X', '%s'%x, None, 1.0)

    def terminals(self):
        return list('abde'+OTHER_TERMINALS[:self.X] )

    def all_strings(self):
        for g in self.grammar.enumerate():
            yield str(g)


class Gomez2(Gomez):
    def __init__(self):
        Gomez.__init__(self, X=2)

class Gomez6(Gomez):
    def __init__(self):
        Gomez.__init__(self, X=6)

class Gomez12(Gomez):
    def __init__(self):
        Gomez.__init__(self, X=12)

# just for testing
if __name__ == '__main__':
    import json
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Generate language examples')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate (default: 11)')
    args = parser.parse_args()

    language = Gomez2()
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
        "id": "Gomez",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/Gomez.json", "w") as f:
        json.dump(result, f, indent=2)
