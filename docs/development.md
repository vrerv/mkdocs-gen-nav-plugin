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

If you are using Windows OS, it may not work by the hatch. You can activate the environment by `conda` command directly
The environment name will be similar to `mkdocs-gen-nav-plugin_dev_3.11`, you can list the conda environments first to find out the name.

```shell
conda info --envs # list all environments to find the name
conda activate mkdocs-gen-nav-plugin_dev_3.11 # activate the environment
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
