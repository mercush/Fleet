
from FormalLanguage import FormalLanguage
from LOTlib3.Grammar import Grammar

class MorganNewport(FormalLanguage):
    """
    From Morgan & Newport 1981, also studied in Saffran 2001, JML
    Here, we are not doing the word learning/categorization part, just assuming that the
    parts of speech are known. Note Morgan & Newport give both a CFG and a FSM, and the language
    itself is finite (18 possible strings)

    """
    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', '%s%s', ['AP', 'BP'], 1.0)
        self.grammar.add_rule('S', '%s%s%s', ['AP', 'BP', 'CP'], 1.0)
        self.grammar.add_rule('AP', 'A',   None, 1.0)
        self.grammar.add_rule('AP', 'AD',  None, 1.0) # two terminals, A,D

        self.grammar.add_rule('BP', 'E', None, 1.0)
        self.grammar.add_rule('BP', '%sF', ['CP'], 1.0)

        self.grammar.add_rule('CP', 'C', None, 1.0)
        self.grammar.add_rule('CP', 'CD', None, 1.0)


    def terminals(self):
        return list('ADECF')

    def all_strings(self):
        for g in self.grammar.enumerate():
            yield str(g)

class MorganMeierNewport(FormalLanguage):
    """
    From Morgan, Meier, & Newport with function word cues to phrase structure boundaries

    """
    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', '%s%s', ['AP', 'BP'], 1.0)
        self.grammar.add_rule('S', '%s%s%s', ['AP', 'BP', 'CP'], 1.0)
        self.grammar.add_rule('AP', 'oA',   None, 1.0)
        self.grammar.add_rule('AP', 'oAD',  None, 1.0) # two terminals, A,D

        self.grammar.add_rule('BP', 'uE', None, 1.0)
        self.grammar.add_rule('BP', 'a%sF', ['CP'], 1.0)

        self.grammar.add_rule('CP', 'iC', None, 1.0)
        self.grammar.add_rule('CP', 'iCD', None, 1.0)


    def terminals(self):
        return list('ADECFouai')

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

    language = MorganNewport()
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
        "id": "MorganNewport",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/MorganNewport.json", "w") as f:
        json.dump(result, f, indent=2)
