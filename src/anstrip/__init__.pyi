import collections.abc
import re
import typing

PATTERN: re.Pattern[str]

def strip(string: str) -> str: ...
@typing.overload
def auto_strip(string: str, /) -> str:
    """
    Strip the ANSI escape sequences from the provided `string` if the standard
    output is not a TTY.

    ## Example

    Consider the following program `hello.py`:

    ```py
    message = "\\x1b[1;95mHello, World!\\x1b[22;39m"
    print(repr(anstrip.auto_strip(message)))
    ```

    Running it normally:

    ```sh
    $ python hello.py
    '\\x1b[1;95mHello, World!\\x1b[22;39m'
    ```

    If we send the standard output to `echo`:

    ```sh
    $ python hello.py | xargs echo
    'Hello, World!'
    ```
    """

@typing.overload
def auto_strip(string: str, /, *, output: typing.TextIO) -> str:
    """
    Strip the ANSI escape sequences from the provided `string` if `output` is
    not a TTY.

    ## Example

    Let's set up a fake file that is not a TTY:

    >>> import io
    >>> file = io.StringIO()

    If we provide if as the output, the ANSI sequences will get stripped.

    >>> message = "\\x1b[1;95mHello, World!\\x1b[22;39m"
    >>> print(anstrip.auto_strip(message, output=file))
    Hello, World!  # neither colored nor bold!
    """

@typing.overload
def auto_strip[**P](
    function: collections.abc.Callable[P, str],
    /,
) -> collections.abc.Callable[P, str]:
    """
    Decorator that strips the ANSI escape sequences from the `function`'s
    return value if the standard output is a TTY.

    ## Example

    >>> @anstrip.auto_strip
    ... def pretty_integer(value: int) -> str:
    ...     return f"\\x1b[1;96m{value}\\x1b[22;39m"

    >>> pretty_integer(42)
    # if the standard output is a TTY
    '\\x1b[1;96m42\\x1b[22;39m'
    # if the standard output is not a TTY
    '42'
    """

@typing.overload
def auto_strip[**P](
    *, output: typing.TextIO
) -> collections.abc.Callable[
    [collections.abc.Callable[P, str]], collections.abc.Callable[P, str]
]:
    """
    Decorator that strips the ANSI escape sequences from the `function`'s
    return value if the provided `output` is a TTY.

    ## Example

    Let's set up a fake file that is not a TTY:

    >>> import io
    >>> file = io.StringIO()

    We specify that it is going to be the output of the string:

    >>> @anstrip.auto_strip(output=file)
    ... def pretty_integer(value: int) -> str:
    ...     return f"\\x1b[1;96m{value}\\x1b[22;39m"

    >>> pretty_integer(42)
    '42'
    """

def auto_print(
    *values: object,
    sep: str | None = None,
    end: str | None = None,
    file: typing.TextIO | None = None,
    flush: bool = False,
) -> None: ...
def printed_length(string: str) -> int: ...
