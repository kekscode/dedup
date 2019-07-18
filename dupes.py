#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import itertools
import hashlib
import multiprocessing as mp
from pathlib import Path

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format="%(asctime)s;%(levelname)s;%(message)s")
log = logging.getLogger(sys.argv[0])

def get_paths():
    '''Returns a list of pathlib Path objects from stdin and argv'''
    seed = []
    # If used inside a UNIX pipe, we read from STDIN 
    if not sys.stdin.isatty():
        for line in sys.stdin:
            p = Path(line.rstrip())
            if p.is_dir:
                seed.append(p.resolve())

    # Append arguments (if there are any)
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            p = Path(arg)
            if p.is_dir:
                seed.append(p.resolve())
    
    if len(seed) == 0:
        help = """
usage: dupes.py <path> <another_path>
usage in pipes: ls -d /usr/bin | dupes.py

The LOGLEVEL=DEBUG environment variable is supported to get debug output.
"""
        print(help)
        sys.exit(-1)
    
    return list(dict.fromkeys(seed)) # dedups the list of paths

def walk_path(path):
    for dirpath, dirnames, filenames in os.walk(path, followlinks=False):
        for file in filenames:
            yield os.path.join(dirpath, file)

def path_worker(path, hashed_files):
    for file in walk_path(path):
        fhash = file_worker(file) # runs in *only* one process
        hashed_files[file] = fhash
    return hashed_files

"""
Make a dict containing all hashes which are now keys mapping
to the paths of file duplicates and return all keys pointing to
more than 1 value
From: https://stackoverflow.com/questions/20672238/find-dictionary-keys-with-duplicate-values
"""
def get_reversed_multidict(d):
    rev_multidict = {}
    for key, value in d.items():
        rev_multidict.setdefault(value, set()).add(key)
    # Check for keys (=hashes) pointing to more than 1 value
    return [values for key, values in rev_multidict.items() if len(values) > 1]

def file_worker(file):
    try:
        with open(file, 'rb') as f:
            h = hashlib.sha256(f.read())
    except EnvironmentError as e:
       log.error("I/O or OS Error: {}".format(e))
       return e  # Add the error instead of the hash

    log.debug("working on {}".format(file)) # do something here!
    log.debug(h.hexdigest())
    return h.hexdigest()

def pprint_duplicates(duplicates):
    for dupes in duplicates:
        d = ""
        for idx, dupe in enumerate(dupes):
            if idx == len(dupes)-1: 
                d += dupe
                break
            d += dupe + " <-> "
        print(d)

if __name__ == '__main__':
    p = mp.Pool(mp.cpu_count())

    paths = get_paths()
    hashed_files = {}

    for path in paths:
        hashed_files = p.apply_async(path_worker, (path, hashed_files)).get()
    
    log.debug(hashed_files)
    duplicates = get_reversed_multidict(hashed_files)

    log.debug(duplicates) # The dupes of hazard!
    pprint_duplicates(duplicates)
