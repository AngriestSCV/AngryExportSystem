#!/usr/bin/env python3
import os, sys
import re
import json

def main():
    if len(sys.argv) != 3:
        print("A version for the package to use  and the path to the package.json must be specified")
        sys.exit(1)

    version = sys.argv[1]
    path = sys.argv[2]

    with open(path, "r") as ff:
        obj = json.load(ff)
        obj['version'] = version

    with open(path, "w") as ff:
        ff.write( json.dumps(obj, sort_keys=True, indent=4))
                        

if __name__ == "__main__":
    main()

