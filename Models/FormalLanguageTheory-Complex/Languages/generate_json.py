#!/usr/bin/env python3
"""
Run all language files to generate JSON outputs
"""
import os
import subprocess
import sys
import argparse

def get_language_files():
    """Get all language .py files in current directory"""
    files = []
    for f in sorted(os.listdir('.')):
        if (f.endswith('.py') and
            f not in ['FormalLanguage.py', '__init__.py', 'generate_json.py'] and
            not f.startswith('.')):
            files.append(f)
    return files

def main(num_examples=11):
    files = get_language_files()
    print(f"Found {len(files)} language files to process")
    print(f"Generating {num_examples} examples per language\n")

    successful = 0
    failed = []

    for i, filename in enumerate(files, 1):
        print(f"[{i}/{len(files)}] Processing {filename}...", end=' ')
        sys.stdout.flush()

        try:
            result = subprocess.run(
                ['python3', filename, '-n', str(num_examples)],
                capture_output=True,
                timeout=10,
                text=True
            )

            if result.returncode == 0:
                print("✓")
                successful += 1
            else:
                print("✗")
                failed.append((filename, result.stderr))
        except subprocess.TimeoutExpired:
            print("✗ (timeout)")
            failed.append((filename, "Timeout after 10 seconds"))
        except Exception as e:
            print(f"✗ ({str(e)})")
            failed.append((filename, str(e)))

    print(f"\n{'='*60}")
    print(f"Summary: {successful}/{len(files)} files processed successfully")

    if failed:
        print(f"\n{len(failed)} files failed:")
        for filename, error in failed:
            print(f"  - {filename}")
            if error:
                # Print first line of error
                error_line = error.split('\n')[0]
                print(f"    Error: {error_line}")

    # Count JSON files generated
    json_count = len([f for f in os.listdir('json') if f.endswith('.json')])
    print(f"\nJSON files generated: {json_count}")
    print(f"Location: json/")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate JSON files for all languages')
    parser.add_argument('-n', '--num-examples', type=int, default=11,
                        help='Number of examples to generate per language (default: 11)')
    args = parser.parse_args()

    main(num_examples=args.num_examples)
