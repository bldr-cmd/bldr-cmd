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
virtualenv venv
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

## ShellSpec

Install

```
curl -fsSL https://git.io/shellspec | sh
```

Run Tests
```
shellspec
```

## TODO

[ ] Dynamic commands https://stackoverflow.com/questions/53147525/is-it-possible-to-dynamically-generate-commands-in-python-click