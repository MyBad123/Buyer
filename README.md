# Flake8
[Flake8](https://flake8.pycqa.org/en/latest/#) is is a great toolkit for checking your code base against coding style (PEP8), programming errors (like “library imported but unused” and “Undefined name”) and to check cyclomatic complexity.

Test everything in the current directory:
```sh
flake8 
```

Test everything in the given directory:
```sh
flake8 ./directory
```

Протестировать отдельный файл:
```sh
flake8 file.py
```