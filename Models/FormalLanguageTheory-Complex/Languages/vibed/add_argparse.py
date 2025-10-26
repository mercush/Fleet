#!/usr/bin/env python3
"""
Add argparse to all language files to accept --num-examples argument
"""
import os
import re

def get_language_files():
    """Get all language .py files in current directory"""
    files = []
    for f in sorted(os.listdir('.')):
        if (f.endswith('.py') and
            f not in ['FormalLanguage.py', '__init__.py', 'update_all_files.py', 'fix_remaining.py', 'generate_json.py', 'add_argparse.py'] and
            not f.startswith('.')):
            files.append(f)
    return files

def update_file(filepath):
    """Add argparse to a file"""
    with open(filepath, 'r') as f:
        content = f.read()

    # Check if argparse is already added
    if 'argparse' in content and 'num_examples' in content:
        print(f"  Skipping {filepath} - already has argparse")
        return False

    # Replace the import section in __main__ block
    # Old: import json\n    import os
    # New: import json\n    import os\n    import argparse
    content = re.sub(
        r"(if __name__ == '__main__':\s+import json\s+import os)",
        r"\1\n    import argparse",
        content
    )

    # Add argparse parsing after imports
    # Find the pattern: import argparse\n\n    language =
    # Replace with: import argparse\n\n    parser = ...\n\n    language =
    argparse_code = """

    parser = argparse.ArgumentParser(description='Generate language examples')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate (default: 11)')
    args = parser.parse_args()
"""

    content = re.sub(
        r"(import argparse)\s+language = ",
        r"\1" + argparse_code + "\n    language = ",
        content
    )

    # Replace all instances of .sample_data(11) with .sample_data(args.num_examples)
    content = re.sub(r'\.sample_data\(11\)', '.sample_data(args.num_examples)', content)

    # Replace all if len(examples) >= 11: with args.num_examples
    content = re.sub(r'if len\(examples\) >= 11:', 'if len(examples) >= args.num_examples:', content)

    # Replace examples[:11] with examples[:args.num_examples]
    content = re.sub(r'examples\[:11\]', 'examples[:args.num_examples]', content)

    with open(filepath, 'w') as f:
        f.write(content)

    return True

def main():
    files = get_language_files()
    print(f"Found {len(files)} files to update\n")

    updated = 0
    for filename in files:
        print(f"Processing {filename}...", end=' ')
        if update_file(filename):
            print("✓")
            updated += 1
        else:
            print()

    print(f"\n✓ Updated {updated}/{len(files)} files")

if __name__ == '__main__':
    main()
