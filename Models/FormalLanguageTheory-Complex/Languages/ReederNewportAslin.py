
from FormalLanguage import FormalLanguage
from LOTlib3.Miscellaneous import weighted_sample
import itertools

class ReederNewportAslin(FormalLanguage):
    """
    From Reeder, Newport, & Aslin 2013 - QAXBR grammar, looking to see if you generalize
    to held-out strings

    q Q = Q words
    a A s = A words
    x X c = X words
    b B n = B words
    r R = R words

    Strings are from Table 2, starred

    """
    def __init__(self):
        strings = ['axb', 'axn', 'AxB', 'Axn', 'sxb', 'sxB', 'aXB', 'aXn', 'AXb', 'AXB', 'sXb', 'sXn', 'acb', 'acB', 'Acb', 'Acn', 'scB', 'scn']
        self.test_strings = ['axB', 'Axb', 'sxn', 'aXb', 'AXn', 'sXB','acn', 'AcB', 'scb']
        assert len(set(strings).intersection(set(self.test_strings))) == 0

        self.strings = []
        for q,r in itertools.product(['', 'q', 'Q'], ['', 'r', 'R']):
            for s in strings:
                self.strings.append( q+s+r )

    def terminals(self):
        return list('aAsbBnxXcqQrR')

    def sample_string(self):
        return weighted_sample(self.strings, probs=lambda s: pow(2.0, -len(s))) # sample inversely with length, ok?

    def all_strings(self):
        for s in self.strings:
            yield s



# just for testing
if __name__ == '__main__':
    import json
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Generate language examples')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate (default: 11)')
    args = parser.parse_args()

    language = ReederNewportAslin()
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
        "id": "ReederNewportAslin",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/ReederNewportAslin.json", "w") as f:
        json.dump(result, f, indent=2)
