## Packaging for Pypi

```bash
rm -f dist/*
python3 setup.py sdist bdist_wheel

# Test distribution
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# TBD: Real distribution
```
