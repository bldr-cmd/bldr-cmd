# bldr-cmd


## Building

```
python3 setup.py build
```

## Documentation

The `docs` directory contains the documentation for `bldr`. See [README.md](docs/README.md)

### Testing The Script
To test the script, you can make a new virtualenv and then install your package:

```
python3 -m venv ./venv
. venv/bin/activate
pip install --editable .
```

## Bash Integration

For Bash, add this to `~/.bashrc`:
```
eval "$(_BLDR_COMPLETE=source_bash bldr)"
```
https://click.palletsprojects.com/en/7.x/bashcomplete/


More Info at
https://click.palletsprojects.com/en/7.x/setuptools/


# Testing 

## Unit Tests
## Pester - Windows

https://github.com/pester/Pester

## ShellSpec - Linux

Install

```
curl -fsSL https://git.io/shellspec | sh
```

Run Tests
```
shellspec
```

# Python Virtual Environment

## Linux 

```
python3 -m venv ./venv
```

## Windows
General form:
```
c:\Python35\python -m venv c:\path\to\myenv
```

Easy way:
From Explorer, open a command prompt in the folder you want and run:
```
c:\Python35\python -m venv .\venv
```
Replease '35' with which ever python version you have installed