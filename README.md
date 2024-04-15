# anstrip

[![PyPI](https://img.shields.io/pypi/v/anstrip)](https://pypi.org/project/anstrip/)

anstrip is a minimal library to strip ANSI sequences from strings.

It provides:

- `PATTERN`, the regex pattern used by the functions of anstrip
- `strip`, a function to remove all the escape sequences from a string
- `auto_strip`, a function that is similar to `strip`, except that it only removes if the output is a TTY
- `print`, a function that is similar to the built-in `print` but with sequence auto-stripping
- `printed_length`, a function that returns the length of the string as seen on the screen
