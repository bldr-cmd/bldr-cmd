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

cat <<EOF > hi.bldr-py.txt
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

## bldr Has a Default Local Template In .bldr/local

```
mkdir -p .bldr/local
cat <<EOF > .bldr/local/bye.bldr-j2.txt
Lets say {{ say_bye() }}

EOF

cat <<EOF > .bldr/local/bye.bldr-py.txt
def say_bye():
    return "good bye"
EOF

bldr gen.up
cat bye.txt
```

## 