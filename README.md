# n-grams-wikipedia
An n-gram language model based on a wikipedia dump corpus

## Downloading the corpus:

NOTE: The corpus download script will download and extract ~150GB of text files, be prepared with enough disk space.

The script also leverages the tools "pbzip2" to efficiently extract the bzip2 file. It can be installed with apt, brew, or whatever your package manager of choice.

Download and extract the files with:
```
./download_corpus.sh
```

## Dependency install

We use poetry for python package management. Install poetry if you have not already: https://python-poetry.org/docs/

Then in the base directory of the repo run:
```
poetry install
```

## Counting n-grams in the corpus

To perform n-gram counting across the corpus run:

```
poetry run naive_count
```
