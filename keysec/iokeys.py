#!/usr/bin/env python3
# encoding:utf-8


import subprocess
from argparse import ArgumentError
from getpass import getpass
from io import TextIOWrapper
from tempfile import NamedTemporaryFile, TemporaryFile
from typing import Callable, Tuple, Union

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives.serialization import Encoding, load_pem_private_key, load_pem_public_key, load_ssh_private_key, load_ssh_public_key, NoEncryption, PrivateFormat, PublicFormat

from keysec.parser import in_arg


def key_to_str(key: Union[Ed25519PrivateKey, Ed25519PublicKey, RSAPrivateKey, RSAPublicKey], str_format: Union[PrivateFormat, PublicFormat]) -> str:
    encoding = Encoding.OpenSSH if str_format is PublicFormat.OpenSSH else Encoding.PEM
    if isinstance(str_format, PrivateFormat):
        res = key.private_bytes(encoding=encoding, format=str_format, encryption_algorithm=NoEncryption())
    else:
        res = key.public_bytes(encoding=encoding, format=str_format)
    res = res.decode('utf-8').strip()
    res += '\n'
    return res


def get_ssh_comment(key: str, orig_format: Union[PrivateFormat, PublicFormat], password: str = '') -> str:
    public = key
    if orig_format is PrivateFormat.OpenSSH:
        with NamedTemporaryFile(mode='w+', encoding='utf-8') as tmp:
            write_key(key=key, output=tmp, close=False)
            public = subprocess.run(['ssh-keygen', '-y', '-P', password, '-f', tmp.name], capture_output=True, text=True, check=True).stdout
    with TemporaryFile(mode='w+', encoding='utf-8') as tmp:
        write_key(key=public, output=tmp, close=False)
        tmp.seek(0)
        info = subprocess.run(['ssh-keygen', '-l', '-f', '-'], capture_output=True, text=True, check=True, stdin=tmp).stdout
    comment = ' '.join(info.split(' ')[2:-1])
    return comment


def load_key(key: str) -> Tuple[Union[Ed25519PrivateKey, Ed25519PublicKey, RSAPrivateKey, RSAPublicKey], Union[PrivateFormat, PublicFormat], str]:
    key_bytes = key.encode('utf-8')
    loaded_key, orig_format, comment, passphrase = None, None, '', ''
    funcs = ((load_pem_private_key, PrivateFormat.PKCS8), (load_ssh_private_key, PrivateFormat.OpenSSH),
             (load_pem_public_key, PublicFormat.SubjectPublicKeyInfo), (load_ssh_public_key, PublicFormat.OpenSSH))
    for load in funcs:
        try:
            loaded_key, orig_format = load[0](key_bytes, password=None) if isinstance(load[1], PrivateFormat) else load[0](key_bytes), load[1]
            break
        except ValueError as error:
            if error.args[0] == 'Key is password-protected.':
                passphrase = getpass('Enter current key passphrase: ')
                try:
                    loaded_key, orig_format = load[0](key_bytes, password=passphrase.encode('utf-8')), load[1]
                    break
                except:
                    raise ValueError('Entered passphrase is incorrect.') from None
        except:
            pass
    if loaded_key is None:
        raise ArgumentError(argument=in_arg, message='input is not an OpenSSL or OpenSSH ASCII-encoded key')
    if orig_format in (PrivateFormat.OpenSSH, PublicFormat.OpenSSH):
        comment = get_ssh_comment(key=key, orig_format=orig_format, password=passphrase)
    return loaded_key, orig_format, comment


def write_key(key: str, output: TextIOWrapper, close=True):
    output.write(key)
    output.flush()
    if close and not output.name == '<stdout>':
        output.close()


def generate_and_write(output: TextIOWrapper,
                       func: Callable[..., str],
                       *args, **kwargs):
    key = func(*args, **kwargs)
    write_key(key=key, output=output)


def full_process(key: str,
                 output: TextIOWrapper,
                 func: Callable[[Union[Ed25519PrivateKey, Ed25519PublicKey, RSAPrivateKey, RSAPublicKey], Union[PrivateFormat, PublicFormat], str, ...], str],
                 *args, **kwargs):
    key = load_key(key=key)
    key, orig_format, comment = key[0], key[1], key[2]
    key = func(key, orig_format, comment, *args, **kwargs)
    write_key(key=key, output=output)
