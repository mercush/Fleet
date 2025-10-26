#!/usr/bin/env python3
"""
Script to fix remaining language files and add JSON output capability
"""
import os
import re

MAIN_BLOCK = '''
if __name__ == '__main__':
    import json
    import os

    language = {classname}()
    data_output = language.sample_data(11)

    # Extract strings from Counter and create example list
    counter = data_output[0].output
    examples = []
    for string, count in counter.items():
        for _ in range(count):
            examples.append({{"i": [], "o": [string]}})
            if len(examples) >= 11:
                break
        if len(examples) >= 11:
            break

    # Create JSON structure
    result = {{
        "canary": "",
        "id": "{file_id}",
        "program": "",
        "data": examples[:11]
    }}

    # Write to JSON file
    os.makedirs("json", exist_ok=True)
    with open("json/{file_id}.json", "w") as f:
        json.dump(result, f, indent=2)
'''

files_to_fix = [
    ("AB.py", "AB"),
    ("ABA.py", "ABA"),
    ("ABn.py", "ABn"),
    ("ABnen.py", "ABnen"),
    ("Bach.py", "Bach3"),  # Uses Bach3 class
    ("Fibo.py", "Fibo"),
    ("Man.py", "Man"),
    ("Unequal.py", "Unequal"),
    ("WeW.py", "WeW"),
    ("XXR.py", "XXR"),
]

def main():
    for filename, classname in files_to_fix:
        if not os.path.exists(filename):
            print(f"Skipping {filename} - file not found")
            continue

        file_id = filename.replace('.py', '')

        with open(filename, 'r') as f:
            content = f.read()

        # Check if file already has the new format
        if 'json.dump(result, f, indent=2)' in content:
            print(f"Skipping {filename} - already updated")
            continue

        # Remove old __main__ block if it exists
        content = re.sub(r'\nif __name__ == [\'"]__main__[\'"]:.*$', '', content, flags=re.DOTALL)
        content = re.sub(r'\n# just for testing\s*\nif __name__ == [\'"]__main__[\'"]:.*$', '', content, flags=re.DOTALL)

        # Add new main block
        new_main = MAIN_BLOCK.format(classname=classname, file_id=file_id)
        content = content.rstrip() + new_main

        with open(filename, 'w') as f:
            f.write(content)

        print(f"✓ Fixed {filename}")

    # Fix AnBmAnBmCCC.py which has the wrong class name
    print("\nFixing AnBmAnBmCCC.py...")
    with open("AnBmAnBmCCC.py", 'r') as f:
        content = f.read()

    content = content.replace('language = AnBmAnBm()', 'language = AnBmAnBmCCC()')

    with open("AnBmAnBmCCC.py", 'w') as f:
        f.write(content)
    print("✓ Fixed AnBmAnBmCCC.py class name")

    # Fix Gomez.py to use Gomez2
    print("\nFixing Gomez.py...")
    with open("Gomez.py", 'r') as f:
        content = f.read()

    content = content.replace('language = Gomez()', 'language = Gomez2()')

    with open("Gomez.py", 'w') as f:
        f.write(content)
    print("✓ Fixed Gomez.py to use Gomez2")

    print("\n✓ Done!")

if __name__ == '__main__':
    main()
