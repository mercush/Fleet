
from FormalLanguage import FormalLanguage
from LOTlib3.Grammar import Grammar

class BerwickPilato(FormalLanguage):
    """
    From Figure 3a of Berwick & Pilato 1987
    Ignores tense
    J = Judy
    g = gives
    G = gave
    d = does
    D = did
    e = get
    i = is
    W = was
    h = has
    H = had
    N = given
    v = giving
    V = give
    m = may
    M = might
    j = have
    b = being
    B = been
    E = be
    o = bread
    """
    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', 'J%s', ['S1'], 1.0)
        self.grammar.add_rule('S1', 'g%s', ['S4'], 1.0)
        self.grammar.add_rule('S1', 'G%s', ['S4'], 1.0)

        self.grammar.add_rule('S1', 'd%s', ['S3'], 1.0)
        self.grammar.add_rule('S1', 'D%s', ['S3'], 1.0)

        self.grammar.add_rule('S1', 'i%s', ['S6'], 1.0)
        self.grammar.add_rule('S1', 'w%s', ['S6'], 1.0)

        self.grammar.add_rule('S1', 'h%s', ['S5'], 1.0)
        self.grammar.add_rule('S1', 'H%s', ['S5'], 1.0)

        self.grammar.add_rule('S1', 'm%s', ['S2'], 1.0)
        self.grammar.add_rule('S1', 'M%s', ['S2'], 1.0)

        self.grammar.add_rule('S2', 'j%s', ['S5'], 1.0)
        self.grammar.add_rule('S2', 'E%s', ['S6'], 1.0)
        self.grammar.add_rule('S2', 'V%s', ['S4'], 1.0)

        self.grammar.add_rule('S3', 'e%s', ['S7'], 1.0)
        self.grammar.add_rule('S3', 'V%s', ['S4'], 1.0)

        self.grammar.add_rule('S4', 'o',   None, 1.0)
        self.grammar.add_rule('S4', 'o',   None, 1.0)

        self.grammar.add_rule('S5', 'N%s', ['S4'], 1.0)
        self.grammar.add_rule('S5', 'B%s', ['S6'], 1.0)

        self.grammar.add_rule('S6', 'b%s', ['S7'], 1.0)
        self.grammar.add_rule('S6', 'v%s', ['S4'], 1.0)
        self.grammar.add_rule('S6', 'N%s', ['S4'], 1.0)

        self.grammar.add_rule('S7', 'N%s', ['S4'], 1.0)


    def terminals(self):
        return list('JgGdDeiWhHNvVmMjbBEo')

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

    language = BerwickPilato()
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
        "id": "BerwickPilato",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/BerwickPilato.json", "w") as f:
        json.dump(result, f, indent=2)
