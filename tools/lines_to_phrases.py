#!/usr/bin/env python
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Missing arguments")
        exit(1)

    orig = sys.argv[1]
    out = sys.argv[2]

    with open(orig, "r") as orig_file:
        with open(out, "w") as out_file:
            out_file.write("[\n")
            for line in orig_file.readlines():
                line = line[1:-2]
                out_file.write(f'{{ "phrase": "{line}", "keywords": ["testing"] }},\n')
            out_file.write("]")
