import numpy 
from FormalLanguage import FormalLanguage
from random import random

class An2(FormalLanguage):
    # A^(n^2)

    def __init__(self):
        self.grammar = None
        
    def terminals(self):
        return list('a')
    
    def sample_string(self):
        n = numpy.random.geometric(0.5)
            
        return 'a'*(n**2)



# just for testing
if __name__ == '__main__':
    import json
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Generate language examples')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate (default: 11)')
    args = parser.parse_args()

    language = An2()
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
        "id": "An2",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/An2.json", "w") as f:
        json.dump(result, f, indent=2)
