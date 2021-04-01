# bldr

## Running

bldr requires python.  If it is not in your PATH, see "Virtual Environment" below on how to setup this

```
bldr --help
```


## Installing
```
pip install git+ssh://git@svn.daveengineering.com/bldr/bldr_cmd.git
```

## Upgrading

```
pip install --upgrade git+ssh://git@svn.daveengineering.com/bldr/bldr_cmd.git
```

## Virtual Environment - Windows

On Windows its useful to setup a VirtualEnvironment to avoid PATH issues:

```
c:\Python35\python -m venv .\venv
```
Where '35' can be replaced with which ever version of python you have installed

Once setup, run the Activate.ps1 script to setup your PowerShell Prompt:

```
.\venv\Scripts\Activate.ps1
```

## Virtual Environment - Linux

On Linux its useful to setup a VirtualEnvironment to avoid dependency issues:

```
python35 -m venv ./venv
```
Where '35' can be replaced with which ever version of python you have installed


Once setup, run the Activate.ps1 script to setup your PowerShell Prompt:
```
 . ./venv/bin/activate
```

# Changelog

* 0.2 - Initial Testing
* 0.3 - Fix verbosity