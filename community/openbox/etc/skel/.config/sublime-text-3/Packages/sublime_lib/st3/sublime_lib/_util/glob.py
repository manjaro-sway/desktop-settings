import re
from functools import lru_cache

from .._compat.typing import Callable

__all__ = ['get_glob_matcher']


GLOB_RE = re.compile(r"""(?x)(
    (?:^|/) \*\* (?:$|/)
    | (?<!\*)\*(?!\*)
    | \?
    | \[ .*? \]
)""")


@lru_cache()
def get_glob_matcher(pattern: str) -> Callable[[str], bool]:
    s = r'\A'
    if pattern.startswith('/'):
        pattern = pattern[1:]
    else:
        pattern = '**/' + pattern

    for part in GLOB_RE.split(pattern):
        if part == '':
            pass
        elif part.strip('/') == '**':
            s += r'(?:^|/)(?:(?:.*)(?:$|/))?'
        elif part == '*':
            s += r'(?:[^/]*)'
        elif part == '?':
            s += r'(?:[^/])'
        elif part[0] == '[':
            s += part
        elif '**' in part:
            raise ValueError("Invalid pattern: '**' can only be an entire path component")
        else:
            s += re.escape(part)

    expr = re.compile(s + r'\Z')
    return lambda s: (expr.search(s) is not None)
