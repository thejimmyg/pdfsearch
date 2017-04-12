# PDF Search

Three commands:

* `index.py` - Takes a directory of PDFs in the strucutre `src/<authoirty>/<file>.pdf` and indexes them, extracting individual PDF pages, PNG pages and each pages text content
* `search.py` - Searches the indexed PDFs
* `app.py` - A simple webserver to search the index, and view pages

At the moment, the authority is ignored everywhere.

## Install

```
brew install poppler
brew install imagemagick
virtualenv -p python env
env/bin/pip install PDFMiner
virtualenv -p python3 env3
env3/bin/pip install -r requirements.txt
```

## Indexing

Put files in `src/<authority>/*.pdf` then run:

```
time env3/bin/python index.py
```

The output will be in the `build` directory.

## Searching

Search the index with:

```
env3/bin/python search.py
```

## Webserver

Start the server with:

```
FLASK_APP=app.py env3/bin/flask run
```
