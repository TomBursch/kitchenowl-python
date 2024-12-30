# kitchenowl-python 
A simple wrapper around the KitchenOwl API.

This is a small python package to be used as a wrapper for the KitchenOwl API in python.

Currently, there is only support for managing shopping list items.

## Installation

```shell
python -m venv .venv
source .venv/bin/activate
pip install -e .
```
Installs all required dependencies.

## Usage

```python
from aiohttp import ClientSession
from kitchenowl_python.kitchenowl import KitchenOwl

async with ClientSession() as session:
    kitchenowl = KitchenOwl(session=session, url=url, token=token)
    await kitchenowl.test_connection()

```

## Development

### Run tests

```shell
source .venv/bin/activate
pip install -e .\[test\]
pytest .
```


