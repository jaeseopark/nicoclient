# nico_client

A python client to interact with [nicovideo.jp](https://nicovideo.jp).

This client uses other existing clients such as `nicopy`, and offers a few new features as well.

## Packaging for Pypi

```bash
python3 setup.py sdist bdist_wheel

# Test distribution
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# TBD: Real distribution
```
