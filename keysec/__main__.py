#!/usr/bin/env python3
# encoding:utf-8


import collections
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

LIBS_FOLDER = Path(__file__).parent.joinpath('keysec').joinpath('libs').resolve()

tempdirs = []

for lib in LIBS_FOLDER.iterdir():
    tempdirs.append(temp_folder := TemporaryDirectory())
    with ZipFile(file=lib, mode='r') as library:
        library.extractall(temp_folder.name)

collections.deque((sys.path.insert(0, temp_folder.name) for temp_folder in tempdirs), maxlen=0)

if __name__ == '__main__':
    from keysec.keysec import main

    main()
