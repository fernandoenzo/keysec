#!/usr/bin/env python3
# encoding:utf-8


import collections
import sys
from pathlib import Path

from keysec.keysec import main

LIBS_FOLDER = Path(__file__).parent.joinpath('keysec').joinpath('libs').resolve()
collections.deque((sys.path.insert(0, str(lib)) for lib in LIBS_FOLDER.iterdir()), maxlen=0)

if __name__ == '__main__':
    main()
