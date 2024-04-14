"""
anstrip is a minimal library to strip ANSI sequences from strings.

It provides:
- `PATTERN`, the regex pattern used by the functions of anstrip
- `strip`, a function to remove all the escape sequences from a string
- `auto_strip`, a function that is similar to `strip`, except that it only removes if the output is a TTY
- `auto_print`, a function that is `print` but with sequence auto-stripping
- `printed_length`, a function that returns the length of the string as seen on the screen
"""

import collections.abc
import functools
import re
import sys
import typing

__all__ = [
    "PATTERN",
    "strip",
    "auto_strip",
    "auto_print",
    "printed_length",
]

_P = typing.ParamSpec("_P")

# Based on <https://github.com/chalk/ansi-regex/blob/main/index.js>
# The license of `ansi-regex` can be found in the `3rdparty` directory
PATTERN = re.compile(
    r"[\u001B\u009B][\[\]()#;?]*(?:(?:(?:(?:;[-a-zA-Z\d\/#&.:=?%@~_]+)*|[a-zA-Z\d]+(?:;[-a-zA-Z\d\/#&.:=?%@~_]*)*)?\u0007)|(?:(?:\d{1,4}(?:;\d{0,4})*)?[\dA-PR-TZcf-nq-uy=><~]))"
)


def strip(string: str) -> str:
    """
    Strip ANSI sequences from a given string.

    >>> anstrip.strip("Nothing out of the \\x1b[94mblue\\x1b[39m...")
    'Nothing out of the blue...'
    >>> anstrip.strip("\\x1b[1;31mBOLD, AND RED!\\x1b[22;39m")
    'BOLD, AND RED!'  # well not anymore
    >>> anstrip.strip("A party? I'm \\x1b[Bdown for that!")
    "A party? I'm down for that!"
    >>> anstrip.strip("Hello, mundane world.")
    'Hello, mundane world.'
    >>> anstrip.strip("")
    ''
    """

    return re.sub(PATTERN, "", string)


# The docstring is provided by the overloads (in the stubs)
def auto_strip(
    string_or_function: str | collections.abc.Callable[_P, str] | None = None,
    /,
    *,
    output: typing.TextIO | None = None,
) -> (
    str
    | collections.abc.Callable[_P, str]
    | collections.abc.Callable[
        [collections.abc.Callable[_P, str]], collections.abc.Callable[_P, str]
    ]
):
    if output is None:
        output = sys.stdout

    if isinstance(string_or_function, str):
        return string_or_function if output.isatty() else strip(string_or_function)

    def decorator(
        function: collections.abc.Callable[_P, str],
    ) -> collections.abc.Callable[_P, str]:
        @functools.wraps(function)
        def inner(*args: _P.args, **kwargs: _P.kwargs) -> str:
            return strip(function(*args, **kwargs))

        if output.isatty():
            return function
        return inner

    if string_or_function is not None:
        return decorator(string_or_function)
    return decorator


def auto_print(
    *values: object,
    sep: str | None = None,
    end: str | None = None,
    file: typing.TextIO | None = None,
    flush: bool = False,
) -> None:
    """
    Similar to the built-in function `print`, but ANSI escape sequences are
    automatically stripped if `file` is not a TTY.
    """

    def str_and_auto_strip(value: object) -> str:
        return typing.cast(str, auto_strip(str(value), output=file))

    print(*map(str_and_auto_strip, values), sep=sep, end=end, file=file, flush=flush)


def printed_length(string: str) -> int:
    """
    Return the length of the string without counting characters that are not
    actually visible (ANSI sequences).

    >>> ansi.printed_length("Nothing out of the \\x1b[94mblue\\x1b[39m...")
    26
    >>> ansi.printed_length("Hello, mundane world.")
    21
    >>> ansi.printed_length("")
    0
    """

    return len(strip(string))
