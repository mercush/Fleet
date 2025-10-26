
from FormalLanguage import FormalLanguage
from LOTlib3.Grammar import Grammar

class HudsonKamNewport(FormalLanguage):
    """
    From Hudson Kam & Newport, simplifying out words to only POS
    Goal is to investigate learning of probabilities on N+DET vs N (no det)
    Here, we do not include mass/count subcategories on nouns

    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.436.7524&rep=rep1&type=pdf


    """
    def __init__(self):
        self.grammar = Grammar(start='S')

        """
        V = transitive verb
        v = intransitive verb
        """

        self.grammar.add_rule('S', '%s%s',   ['v', 'NP'], 1.0)
        self.grammar.add_rule('S', '%s%s%s', ['V', 'NP', 'NP'], 1.0)
        self.grammar.add_rule('S', '!%s%s',  ['v', 'NP'], 1.0)
        self.grammar.add_rule('S', '!%s%s%s',  ['V', 'NP', 'NP'], 1.0)


    def terminals(self):
        return list('!vVnd')

    def all_strings(self):
        for g in self.grammar.enumerate():
            yield str(g)


class HudsonKamNewport45(HudsonKamNewport):
    def __init__(self):
        HudsonKamNewport.__init__(self)

        self.grammar.add_rule('NP', 'nd',   None, 0.45)
        self.grammar.add_rule('NP', 'n',    None, 0.55)

class HudsonKamNewport60(HudsonKamNewport):
    def __init__(self):
        HudsonKamNewport.__init__(self)

        self.grammar.add_rule('NP', 'nd',   None, 0.60)
        self.grammar.add_rule('NP', 'n',    None, 0.40)

class HudsonKamNewport75(HudsonKamNewport):
    def __init__(self):
        HudsonKamNewport.__init__(self)

        self.grammar.add_rule('NP', 'nd',   None, 0.75)
        self.grammar.add_rule('NP', 'n',    None, 0.25)


class HudsonKamNewport100(HudsonKamNewport):
    def __init__(self):
        HudsonKamNewport.__init__(self)

        self.grammar.add_rule('NP', 'nd',   None, 1.00)
        self.grammar.add_rule('NP', 'nD',   None, 1.00)

# just for testing
if __name__ == '__main__':
    import json
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Generate language examples')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate (default: 11)')
    args = parser.parse_args()

    language = HudsonKamNewport()
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
        "id": "HudsonKamNewport",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/HudsonKamNewport.json", "w") as f:
        json.dump(result, f, indent=2)
