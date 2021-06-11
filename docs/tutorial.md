# bldr

## bldr Main Purpose Is Templates

```
bldr init
echo "hello World\n" > hi.bldr-j2.txt
bldr gen.up

cat hi.txt
```

## bldr Templates Are Jinja2 Powered

```
cat <<EOF > hi.bldr-j2.txt
Lets say {{ say_hello() }}

EOF

cat <<EOF > hi.bldr-j2.txt.py
def say_hello():
    return "hellow"
EOF

bldr gen.up
cat hi.txt
```

## bldr Templates Only Apply Changes

```
echo -e "NO" >> hi.txt

bldr gen.up
cat hi.txt

sed -i 's/Lets/Lets NOT/g' hi.bldr-j2.txt

bldr gen.up
cat hi.txt
```

This is a test

## bldr Has a Default Local Template In .bldr/template

```
cat <<EOF > .bldr/template/bye.bldr-j2.txt
Lets say {{ say_bye() }}

EOF

cat <<EOF > .bldr/template/bye.bldr-j2.txt.py
def say_bye():
    return "good bye"
EOF

bldr gen.up
cat bye.txt
```

## bldr Saves Inline Template to Local Template

```
ls hi.bldr-*

bldr gen.mvlocal

ls hi.bldr-*
ls .bldr/template/hi.bldr-*
```

## bldr Generators Creates File Templates in Local

```

```

## bldr can import a non bldr project as a template
```
bldr gen.import a/path/to/somethign/existing
```

To convert files to templates, use a .bldr/config/config.toml:
```
["gen.import"]
# Top level config for gen.import command
exclude_globs = ["*.sln"]

["gen.import".template_exts]
# Add extensions here to have them turned into template_exts


["gen.import".template_exts.".cs"]
    SomeModule = "TheNewModule"
    SomeModuleVerySimilar = "ANotSoSimilarModule"
    "SomeOther.Nested.Place" = "ANew.Nested.OtherPlace"
    APlugableModule = "{{ config['net_code']['module'] }}"

# This is used to render to template
["net_code"]
    module = "MyNewPlugableModule"
```