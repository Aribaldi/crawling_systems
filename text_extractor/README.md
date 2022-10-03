# Text Extractor

## Usage
```
usage: extract.py [-h] (--url URL | --path PATH)

Script for parsing text from html, pdf, doc/docx formats.

optional arguments:
  -h, --help   show this help message and exit
  --url URL    url where file is stored
  --path PATH  local path where file is stored
```

Example:

`python extract.py --path ./tests/test_examples/formula_text.docx`

## Tests

Execute `python -m unittest discover -s tests -v` from `text_extractor` directory to run all tests.
