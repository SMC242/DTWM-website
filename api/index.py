"""Makes all of the Python modules importable then exposes them to Vercel for cloud functions."""
from sys import path as sys_path
from pathlib import Path

try:
    from python.server.api import app
except ImportError:
    _path = Path(__file__).absolute()
    sys_path.append(str(_path.parents[1]))
    from python.server.api import app
