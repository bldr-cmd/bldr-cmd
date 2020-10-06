# bldr

## bldr Main Purpose is Templates

```
bldr init
echo "hello World\n" > hi.bldr-j2.txt
bldr gen.up

cat hi.txt
```

## bldr Templates are Jinja2 powered

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

## bldr Templates only apply changes

```
echo -e "NO" >> hi.txt

bldr gen.up
cat hi.txt

sed -i 's/Lets/Lets NOT/g' hi.bldr-j2.txt

bldr gen.up
cat hi.txt
```

This is a test