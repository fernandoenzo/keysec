#!/usr/bin/env python3
# encoding:utf-8


from io import TextIOWrapper
from typing import Union, Callable, Tuple

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, load_pem_private_key, load_pem_public_key, load_ssh_private_key, load_ssh_public_key, PrivateFormat, PublicFormat


def key_to_str(key: Union[Ed25519PrivateKey, Ed25519PublicKey, RSAPrivateKey, RSAPublicKey], str_format: Union[PrivateFormat, PublicFormat]) -> str:
    encoding = Encoding.OpenSSH if str_format is PublicFormat.OpenSSH else Encoding.PEM
    if isinstance(str_format, PrivateFormat):
        res = key.private_bytes(encoding=encoding, format=str_format, encryption_algorithm=NoEncryption())
    else:
        res = key.public_bytes(encoding=encoding, format=str_format)
        res += b'\n' if not res.endswith(b'\n') else b''
    return res.decode('utf-8')


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
        except:
            pass
    if loaded_key is None:
        raise ValueError('The specified key is not in OpenSSL PEM nor OpenSSH format')
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


def load_and_process(key: str,
                     func: Callable[[Union[Ed25519PrivateKey, Ed25519PublicKey, RSAPrivateKey, RSAPublicKey], Union[PrivateFormat, PublicFormat], ...], str],
                     *args, **kwargs) -> str:
    key = load_key(key=key)
    key, orig_format = key[0], key[1]
    return func(key, orig_format, *args, **kwargs)


def load_process_and_write(key: str,
                           output: TextIOWrapper,
                           func: Callable[[Union[Ed25519PrivateKey, Ed25519PublicKey, RSAPrivateKey, RSAPublicKey], Union[PrivateFormat, PublicFormat], ...], str],
                           *args, **kwargs):
    key = load_and_process(key=key, func=func, *args, **kwargs)
    write_key(key=key, output=output)


def full_process(key: TextIOWrapper,
                 output: TextIOWrapper,
                 func: Callable[[Union[Ed25519PrivateKey, Ed25519PublicKey, RSAPrivateKey, RSAPublicKey], Union[PrivateFormat, PublicFormat], ...], str],
                 *args, **kwargs):
    key: str = read_key(key)
    load_process_and_write(key=key, output=output, func=func, *args, **kwargs)
