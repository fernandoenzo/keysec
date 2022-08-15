#!/usr/bin/env python3
# encoding:utf-8


import contextlib
import io
import os
import sys
from getpass import getpass, _raw_input

from keysec.iokeys import Key


def safe_print(text=''):
    with contextlib.ExitStack() as stack:
        try:
            fd = os.open('/dev/tty', os.O_RDWR | os.O_NOCTTY)
            tty = io.FileIO(fd, 'w+')
            stack.enter_context(tty)
            sf_input = io.TextIOWrapper(tty)
            stack.enter_context(sf_input)
            stream = sf_input
        except OSError:
            stack.close()
            stream = sys.stderr
        try:
            stream.write(text + '\n')
        except UnicodeEncodeError:
            prompt = text.encode(stream.encoding, 'replace')
            prompt = prompt.decode(stream.encoding)
            stream.write(prompt + '\n')
        stream.flush()


def safe_input(prompt='') -> str:
    with contextlib.ExitStack() as stack:
        try:
            fd = os.open('/dev/tty', os.O_RDWR | os.O_NOCTTY)
            tty = io.FileIO(fd, 'w+')
            stack.enter_context(tty)
            sf_input = io.TextIOWrapper(tty)
            stack.enter_context(sf_input)
            stream = sf_input
        except OSError:
            stack.close()
            stream, sf_input = sys.stderr, sys.stdin
        res = _raw_input(prompt=prompt, stream=stream, input=sf_input)
        stream.flush()
        return res


def edit(key: Key, comment=None, password=None) -> str:
    if password is True and key.is_private():
        password = getpass('Enter new passphrase (empty for no passphrase): ')
        password_rep = getpass('Enter same passphrase again: ')
        if password != password_rep:
            raise ValueError('Passphrases do not match.')
    else:
        password = key.password
    if comment is True and key.is_ssh():
        safe_print(f'Old comment: {key.get_ssh_comment()}')
        comment = safe_input('New comment: ')
    return key.to_str(str_format=key.orig_format, comment=comment, password=password)
