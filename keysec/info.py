#!/usr/bin/env python3
# encoding:utf-8


import subprocess
from tempfile import TemporaryFile

from keysec.converter import convert
from keysec.iokeys import Key, write_output


def info(key: Key) -> str:
    command = ['openssl', 'pkey', '-text', '--noout']
    command.extend(('-passin', f'pass:{key.password}')) if key.password else None
    command.append('-pubin') if key.is_public() else None
    key_str = convert(key) if key.is_ssh() else key.to_str()
    with TemporaryFile(mode='w+', encoding='utf-8') as tmp:
        write_output(text=key_str, file=tmp, close=False)
        tmp.seek(0)
        res = subprocess.run(command, capture_output=True, text=True, check=True, stdin=tmp).stdout.strip()
    res += f'\nOpenSSH comment: {key.comment}' if key.get_ssh_comment() else ''
    return res
