## Packaging for Pypi

```bash
rm -f dist/*
python3 setup.py sdist bdist_wheel
```

## Uploading to Pypi

```bash
# Test distribution
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Real distribution
python3 -m twine dist/*
```
