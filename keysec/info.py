#!/usr/bin/env python3
# encoding:utf-8


import subprocess
from tempfile import TemporaryFile
from typing import Union

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives.serialization import PrivateFormat, PublicFormat

from keysec.converter import convert
from keysec.iokeys import key_to_str, write_key


def info(key: Union[Ed25519PrivateKey, Ed25519PublicKey, RSAPrivateKey, RSAPublicKey], orig_format: Union[PrivateFormat, PublicFormat]) -> str:
    command = ['openssl', 'pkey', '-text', '--noout']
    command.append('-pubin') if isinstance(orig_format, PublicFormat) else None
    key = convert(key, orig_format) if orig_format in (PrivateFormat.OpenSSH, PublicFormat.OpenSSH) else key_to_str(key, orig_format)
    tmp = TemporaryFile(mode='w+')
    write_key(key=key, output=tmp, close=False)
    tmp.seek(0)
    res = subprocess.run(command, capture_output=True, text=True, check=True, stdin=tmp)
    tmp.close()
    return res.stdout
