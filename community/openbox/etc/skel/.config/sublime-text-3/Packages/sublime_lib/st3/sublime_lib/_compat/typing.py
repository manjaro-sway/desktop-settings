try:
    from typing import *  # noqa: F401, F403
except ImportError:
    from .typing_stubs import *  # type: ignore # noqa: F401, F403
