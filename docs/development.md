# Development Guide

## Development

Install hatch-conda

```shell
pip install hatch-conda
```

Create a environment for development
```shell
hatch env create dev
```

Activate the environment
```shell
hatch shell dev
```

You may need to set `PYTHONPATH=src` to run tests

run tests
```
python -m unittest
```

install locally
```
pip install -e .
```
