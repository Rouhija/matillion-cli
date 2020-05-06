### Compiling package
```sh
# Test
python setup.py develop
# Compile
python setup.py bdist_wheel
# Upload
python -m twine upload dist/*
# Upgrade
pip install matillionctl --upgrade
```

### Dependencies
- tqdm==4.45.0
- twine==3.1.1

### Reading
- [PyPi](https://dzone.com/articles/executable-package-pip-install)