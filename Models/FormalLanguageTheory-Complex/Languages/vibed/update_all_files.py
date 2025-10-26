#!/usr/bin/env python3
"""
Script to update all language files to output JSON
"""
import os
import re

# Template for the __main__ block
MAIN_BLOCK_TEMPLATE = '''# just for testing
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

def get_language_files():
    """Get all language .py files in current directory"""
    files = []
    for f in os.listdir('.'):
        if (f.endswith('.py') and
            f not in ['FormalLanguage.py', '__init__.py', 'update_all_files.py'] and
            not f.startswith('.')):
            files.append(f)
    return sorted(files)

def extract_class_name(content):
    """Extract the main class name from the file"""
    # Look for class definitions
    match = re.search(r'^class\s+(\w+)\s*\(FormalLanguage\)', content, re.MULTILINE)
    if match:
        return match.group(1)
    return None

def update_file(filepath):
    """Update a single file to output JSON"""
    filename = os.path.basename(filepath)
    file_id = filename.replace('.py', '')

    print(f"Processing {filename}...")

    with open(filepath, 'r') as f:
        content = f.read()

    # Extract class name
    classname = extract_class_name(content)
    if not classname:
        print(f"  WARNING: Could not find class name in {filename}, skipping")
        return

    # Find and replace the __main__ block
    # Pattern to match everything from "if __name__ == '__main__':" to the end of file
    pattern = r'# just for testing\s*\nif __name__ == [\'"]__main__[\'"]:.*$'

    if not re.search(pattern, content, re.DOTALL):
        print(f"  WARNING: Could not find __main__ block in {filename}, skipping")
        return

    # Replace with new main block
    new_main = MAIN_BLOCK_TEMPLATE.format(classname=classname, file_id=file_id)
    new_content = re.sub(pattern, new_main, content, flags=re.DOTALL)

    # Write back
    with open(filepath, 'w') as f:
        f.write(new_content)

    print(f"  ✓ Updated {filename}")

def main():
    files = get_language_files()
    print(f"Found {len(files)} files to update\n")

    for f in files:
        if f == 'A2en.py':
            print(f"Skipping {f} (already updated)")
            continue
        update_file(f)

    print(f"\n✓ Done! Updated {len(files)-1} files")

if __name__ == '__main__':
    main()
