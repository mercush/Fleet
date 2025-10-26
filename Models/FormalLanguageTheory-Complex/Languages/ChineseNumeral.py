import itertools
import numpy
import random
from LOTlib3.Miscellaneous import partitions
from FormalLanguage import FormalLanguage
from LOTlib3.Grammar import Grammar
from random import random

class ChineseNumeral(FormalLanguage):
    def __init__(self):
        pass
    
    def sample_string(self):
        l = numpy.random.geometric(p=1./3.)
        out = ""
        oldn = 0
        for i in range(l):
            n = numpy.random.geometric(p=1./3.) + oldn
            out = 'a' + 'b'*n + out
            oldn = n
        return out
            
    def terminals(self):
        return list('ab')

    
# just for testing
if __name__ == '__main__':
    import json
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Generate language examples')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate (default: 11)')
    args = parser.parse_args()

    language = ChineseNumeral()
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
        "id": "ChineseNumeral",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/ChineseNumeral.json", "w") as f:
        json.dump(result, f, indent=2)
