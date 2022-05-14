try:
    from pathlib import *  # noqa: F401, F403
except ImportError:
    from ..vendor.pathlib.pathlib import *  # type: ignore # noqa: F401, F403
