#!/usr/bin/env python

import argparse
import logging
import os
import sys

from example_pkg import build_logger

logger = logging.getLogger('pkg')

def parse_args(test_args=False):

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", dest="file",
                        help="file to be operated on")
    parser.add_argument("-t", "--tag", dest="tag",
                        help="name of tag")
    parser.add_argument("-v", "--verbose", dest="verbose",
                        action = "count", default = 0,
                        help="Decrease diagnostic verbosity",)
    parser.add_argument("-q", "--quiet", dest="quiet",
                        action = "count", default = 0,
                        help="Decrease diagnostic verbosity",)
    if type(test_args) is list:
        return parser.parse_known_args(test_args)
    else:
        return parser.parse_known_args()

#---.---.1--.---.--2.---.---.3--.---.--4.---.---.5--.---.--6.---.---.7--.---.--8
# Main code

def _example_script_main():
    # Parse options
    topts,targs = parse_args()

    # Setup logger
    logger = build_logger(name='example_script', opts=topts)

    if topts.file is None:
        logger.warning('NO FILE SPECIFIED')
        exit()
    
    f = os.path.expanduser(topts.file)

    # check for missing file
    if not os.path.isfile(f):
        logger.warning(f'NOT FOUND: {f}')
        exit()

    # fail out loudly
    logger.warning(f'NO ACTION PERFORMED')

if __name__=="__main__":
    _example_script_main()
