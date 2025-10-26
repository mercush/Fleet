
from FormalLanguage import FormalLanguage
from random import random

fib_cache = dict()
def fib(n):
    v = None
    if n not in fib_cache:
        if n <= 1:
            v = 1
        else:
            v = fib(n-1)+fib(n-2)
        fib_cache[n] = v
        return v
    else:
        return fib_cache[n]

class Fibo(FormalLanguage):
    """
    a^n : n is a fibonacci number
    """

    def __init__(self):
        self.grammar = None

    def terminals(self):
        return list('a')

    def sample_string(self): # fix that this is not CF
        n=0
        while random() < (1.0/2.0):
            n += 1
        return 'a'*fib(n)

        # just for testing
    def all_strings(self): # fix that this is not CF
        n=0
        while True:
            yield 'a'*fib(n)
            n += 1
if __name__ == '__main__':
    import json
    import os
    import argparse

    parser = argparse.ArgumentParser(description='Generate language examples')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate (default: 11)')
    args = parser.parse_args()

    language = Fibo()
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
        "id": "Fibo",
        "program": "",
        "data": examples[:args.num_examples]
    }

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/Fibo.json", "w") as f:
        json.dump(result, f, indent=2)
