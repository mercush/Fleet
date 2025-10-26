
from FormalLanguage import FormalLanguage
from LOTlib3.Grammar import Grammar

class NewportAslin(FormalLanguage):
    """
    From Newport & Aslin 2004, Learning at a distance I
    Only the 1-3 syllable word frames, Table 1, reduced to single characters
    ba=b
    te=t
    gu=g
    do=d
    pi=p
    ra=r
    ke=k
    du=u
    lo=l
    ki=i

    middles:
    di=1
    ku=2
    to=3
    pa=4
    """
    def __init__(self):
        self.grammar = Grammar(start='S')
        self.grammar.add_rule('S', 'b%st', ['MID'], 1.0) # We're going to put a probability distribution on this so that it can be evaluated like everything else (otherwise its top 25 strings are not meaningful since its all uniform!)
        self.grammar.add_rule('S', 'g%sd', ['MID'], 1.0)
        self.grammar.add_rule('S', 'p%sr', ['MID'], 1.0)
        self.grammar.add_rule('S', 'k%su', ['MID'], 1.0)
        self.grammar.add_rule('S', 'l%si', ['MID'], 1.0)

        self.grammar.add_rule('MID', '1', None, 1.0)
        self.grammar.add_rule('MID', '2', None, 1.0)
        self.grammar.add_rule('MID', '3', None, 1.0)
        self.grammar.add_rule('MID', '4', None, 1.0)


    def terminals(self):
        return list('btgdprkuli1234')

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

    language = NewportAslin()
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
        "id": "NewportAslin",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/NewportAslin.json", "w") as f:
        json.dump(result, f, indent=2)
