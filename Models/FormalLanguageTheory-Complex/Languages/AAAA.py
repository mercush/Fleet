
from FormalLanguage import FormalLanguage
from LOTlib3.Miscellaneous import weighted_sample

class AAAA(FormalLanguage):
    """
       The language {a,aa,aaa,aaaa}
    """

    def __init__(self):
        self.grammar = None
        self.strings = ["a", "aa", "aaa", "aaaa" ]
        self.probs   = [ 2**-len(x) for x in self.strings] # geometric distribution

    def terminals(self):
        return list('a')

    def sample_string(self): # fix that this is not CF
        return weighted_sample(self.strings, probs=self.probs)

    def all_strings(self):
        for m in self.strings:
            yield m


class AAA(FormalLanguage):

    def __init__(self):
        self.grammar = None
        self.strings = ["a", "aa", "aaa" ]
        self.probs   = [ 2**-len(x) for x in self.strings] # geometric distribution

    def terminals(self):
        return list('man')

    def sample_string(self): # fix that this is not CF
        return weighted_sample(self.strings, probs=self.probs)

    def all_strings(self):
        for m in self.strings:
            yield m


if __name__ == '__main__':
    import json
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Generate language examples')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate (default: 11)')
    args = parser.parse_args()

    language = AAAA()
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
        "id": "AAAA",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/AAAA.json", "w") as f:
        json.dump(result, f, indent=2)
