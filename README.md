
![](images/DE_bldr_logo.png?raw=true)

# Overview

`bldr` is a utility for generating Files from Templates.  

Only changes are applied to the output file.  This allows both the Template and its resulting file to be 
iterated on.


## `bldr` Renders Templates

```
> bldr init
> echo "hello World\n" > hi.bldr-j2.txt
> bldr gen.up

> cat hi.txt
hello world
```

## `bldr` Templates Are Jinja2 Powered

```
> cat <<EOF > hi.bldr-j2.txt
Lets say {{ say_hello() }}

EOF

> cat <<EOF > hi.bldr-j2.txt.py
def say_hello():
    return "hellow"
EOF

> bldr gen.up
> cat hi.txt
Lets say hellow
```

## `bldr` Templates Only Apply Changes

```
> echo -e "NO" >> hi.txt
> bldr gen.up
> cat hi.txt
Lets say hellow
NO

> sed -i 's/Lets/Lets NOT/g' hi.bldr-j2.txt
> bldr gen.up
> cat hi.txt
Lets NOT say hellow
NO

```

See the [Tutorial](docs/tutorial.md) for more details.


# Documentation

`bldr` documentation mimics Python's Enhancment Proposals to document how various parts of the 
system works. See [README.md](docs/README.md)


# Installing

`bldr` is a python package.  If you need help setting up Python see [Python Env](docs/)

Install from Github
```
pip install git+ssh://git@github.com:bldr-cmd/bldr-cmd.git
```

Upgrading

```
pip install --upgrade git+ssh://git@github.com:bldr-cmd/bldr-cmd.git
```

# Development

## Building

```
python3 setup.py build
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

To run the Python Unit Tests
```
make test
```

## ShellSpec - Linux

Install

```
curl -fsSL https://git.io/shellspec | sh
```

Run Tests
```
shellspec
```

# License

`bldr` is created by [DE Designworks](https://dedesignworks.com/)


```
Copyright 2021 Dave Engineering LLC d.b.a. DE Design Works. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```