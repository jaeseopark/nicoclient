#### Packaging / Uploading to Pypi

```bash
rm -rf dist/* build/* nico_client.egg-info/*
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
```
