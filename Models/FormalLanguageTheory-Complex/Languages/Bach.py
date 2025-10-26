
from FormalLanguage import FormalLanguage
from LOTlib3.Miscellaneous import weighted_sample
import numpy 

class Bach3(FormalLanguage):
    """
       Equal numbers of a,b,c in any order
    """

    def __init__(self):
        pass 
    
    def terminals(self):
        return list('abc')

    def sample_string(self): # fix that this is not CF
        n = numpy.random.geometric(p=1./3.)
        return ''.join(numpy.random.permutation(list('abc'*n)))
    
    def all_strings(self):
        raise NotImplementedError

class Bach2(FormalLanguage):
    """
       Equal numbers of a,b,c in any order
    """

    def __init__(self):
        pass 
    
    def terminals(self):
        return list('ab')

    def sample_string(self): # fix that this is not CF
        n = numpy.random.geometric(p=1./3.)
        return ''.join(numpy.random.permutation(list('ab'*n)))
    
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

    language = Bach3()
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
        "id": "Bach",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/Bach.json", "w") as f:
        json.dump(result, f, indent=2)
