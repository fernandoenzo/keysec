#!/usr/bin/env python3
# encoding:utf-8


from argparse import ArgumentError
from getpass import getpass
from io import TextIOWrapper
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


def read_key(priv_key: TextIOWrapper) -> str:
    return priv_key.read()


def load_key(key: str) -> Tuple[Union[Ed25519PrivateKey, Ed25519PublicKey, RSAPrivateKey, RSAPublicKey], Union[PrivateFormat, PublicFormat]]:
    key: bytes = key.encode('utf-8')
    loaded_key = None
    funcs = ((load_pem_private_key, PrivateFormat.PKCS8),
             (load_ssh_private_key, PrivateFormat.OpenSSH),
             (load_pem_public_key, PublicFormat.SubjectPublicKeyInfo),
             (load_ssh_public_key, PublicFormat.OpenSSH))
    for load in funcs:
        try:
            loaded_key = load[0](key, password=None) if isinstance(load[1], PrivateFormat) else load[0](key)
            break
        except ValueError as error:
            if error.args[0] == 'Key is password-protected.':
                passphrase = getpass('Enter current key passphrase: ')
                try:
                    loaded_key = load[0](key, password=passphrase.encode('utf-8'))
                    break
                except:
                    raise ValueError('Entered passphrase is incorrect.') from None
        except:
            pass
    if loaded_key is None:
        raise ArgumentError(argument=in_arg, message='input is not an OpenSSL or OpenSSH ASCII-encoded key')
    return loaded_key, load[1]


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


def full_process(key: TextIOWrapper,
                 output: TextIOWrapper,
                 func: Callable[[Union[Ed25519PrivateKey, Ed25519PublicKey, RSAPrivateKey, RSAPublicKey], Union[PrivateFormat, PublicFormat], ...], str],
                 *args, **kwargs):
    key = read_key(key)
    key = load_key(key=key)
    key, orig_format = key[0], key[1]
    key = func(key, orig_format, *args, **kwargs)
    write_key(key=key, output=output)
