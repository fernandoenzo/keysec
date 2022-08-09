# KeySec

[![PyPI](https://img.shields.io/pypi/v/keysec?label=latest)](https://pypi.org/project/keysec/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/keysec)
![PyPI - Status](https://img.shields.io/pypi/status/keysec)

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/fernandoenzo/keysec)
![PyPI - License](https://img.shields.io/pypi/l/keysec)

With this program you will be able to generate OpenSSL and OpenSSH keys (RSA, Ed25519) and carry out transformations between both formats.

## Table of contents

<!--ts-->

* [Installation](#installation)
* [How to use it](#how-to-use-it)
  * [Generate an Ed25519 key pair](#generate-an-ed25519-key-pair)
  * [Generate an RSA key pair](#generate-an-rsa-key-pair)
  * [Change a key pair format](#change-a-key-pair-format)
* [Packaging](#packaging)
    * [Autopackage Portable](#autopackage-portable)
    * [Autopackage Wheel](#autopackage-wheel)
    * [PyInstaller](#pyinstaller)
* [Contributing](#contributing)
* [License](#license)

<!--te-->

## Installation

Use the package manager [**pip**](https://pip.pypa.io/en/stable/) or [**pipx**](https://github.com/pypa/pipx) to install it:

```bash
pip install keysec
```

Alternatively, you can use one of the two portable versions provided on the releases page.

- The lightest one has been packaged using [**autopackage**](https://pypi.org/project/autopackage/) and will require you to have Python 3.9+ installed.
- The heavier one has been packaged using [**PyInstaller**](https://pyinstaller.org) and has no external dependencies, so it doesn't matter if you don't have Python installed, or if your version is
  lower than 3.9.

See [Packaging](#packaging) for more information.

## How to use it

The program has very few options to keep it simple, so let's see some examples.

Before we begin, let's point out that this program is capable of outputting its results to a file (`--out/-o`) or to standard output.
Similarly, it is capable of reading input data from a file (`--in/-i`) or from standard input.

This feature gives the program versatility to use linux pipes, as we will see now.

### Generate an Ed25519 key pair

Let's start creating the private key. For this example we are creating it in OpenSSL format. To make it in OpenSSH format simply replace the corresponding `--format` argument:

```commandline
keysec gen priv --algo ed25519 --format openssl --out private.key
keysec gen pub --in private.key --out public.key
```

Note: The default algorithm is already `Ed25519`, and the default format is OpenSSL, so simply writing `keysec gen priv` would be enough for the first line.

As we can see, we must first create the private key and then generate the public one from it.

In a single line, using pipes, this would be:

```commandline
keysec gen priv | tee private.key | keysec gen pub > public.key
```

### Generate an RSA key pair

Now let's do the same with a 4096-bit RSA key pair (by default the program uses 2048 bits, and these are the only two options available), but this time we will generate them in OpenSSH format

```commandline
keysec gen priv --algo rsa --bits 4096 --format openssh --out private.key
keysec gen pub --in private.key --out public.key
```

In a single line, using pipes, this would be:

```commandline
keysec gen priv --algo rsa --bits 4096 --format openssh | tee private.key | keysec gen pub --out public.key
```

### Change a key pair format

Either if we have an OpenSSL or an OpenSSH key pair, we can perform transformations between both formats by simply doing:

```commandline
keysec conv --in keyfile
```

The program will automatically detect the original format and perform the transformation to the other one.

There are also multiple help options `--help/-h` in the program. Don't forget to read them if you forget something:

```commandline
keysec -h
keysec gen -h
keysec gen priv -h
keysec gen pub -h
keysec conv -h
```

## Packaging

In this section we are going to explain how to replicate the packaging process.

### Autopackage Portable

To generate the program lightest portable version, which is available in this GitHub repository, install first `autopackage` with `pip`:

```commandline
pip install autopackage
```

Then run the following commands:

```commandline
autopackage -s setup.py -p
```

### Autopackage Wheel

To generate the program wheel, available at PyPi, first do the following:
1. In the `setup.py` file remove the `package_data` variable and also remove it from the `SetupParser` call
2. In the `setup.py` file change the `zip_safe` flag to `True`
3. In the `__main__.py` file remove lines `11` and `12`, that import the files inside the `libs` folder.

Then run:

```commandline
autopackage -s setup.py
```


### PyInstaller

To generate the program heaviest portable version, which is also available in this GitHub repository, install `pyinstaller` with `pip`:

```
pip install pyinstaller
```

Then run:

```
pyinstaller --onefile keysec.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

![PyPI - License](https://img.shields.io/pypi/l/keysec)

This program is licensed under the
[GNU General Public License v3 or later (GPLv3+)](https://choosealicense.com/licenses/gpl-3.0/)
