#!/usr/bin/env python

import os
import json

# Basic function example
def foo():
    print("Hello World!")

def bar():
    return bar_(os.path.join(os.path.dirname(__file__), './data/core.json'))

# Accessing library data
def bar_(json_filename):
    with open(json_filename) as fh:
        J=json.load(fh)
    return J

# Wrapper function.  This one is referred to by
def foobar():
    foo()
    print(bar())

if __name__ == "__main__":
    foo()
    print(bar())
