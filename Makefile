
.PHONY : docs all test
# Generate Docs
node_modules:
	npm install

%.svg: %.mmd node_modules
	./node_modules/.bin/mmdc  -i $< -o $@

docs: $(addsuffix .svg, $(basename $(wildcard docs/*/*.mmd)))

# Tests
test:
	python -m unittest discover .

all: docs