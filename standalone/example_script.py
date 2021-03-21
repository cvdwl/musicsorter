#!/usr/bin/env python3
import sys,os

for pathadd in [['..'],
                ['..','example_pkg']]:
    sys.path.append(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            *pathadd))
from example_pkg.example_script import _example_script_main

####.###.1##.###.##2.########3#########4#########5#########6#########7#########8

if __name__=="__main__":
    _example_script_main()
