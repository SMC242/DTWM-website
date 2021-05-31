"""Makes all of the Python modules importable then exposes them to Vercel for cloud functions."""
from pathlib import Path
from sys import path as sys_path

# Paths relative to the root to add to pythonpath for importing
PATHS_TO_ADD = ["python"]


def pythonpath_add(root_dir: Path):
    """Add a directory to pythonpath."""
    def inner(dir_name: str):
        path = str(root_dir / dir_name)  # sys_path is string not Path
        sys_path.insert(0, path)
    return inner


root = Path("").absolute()
add_to_pypath = pythonpath_add(root)
for path in PATHS_TO_ADD:
    add_to_pypath(path)

# Imports here
try:
    from python.server.api import app
    print(app)
except ImportError:
    from traceback import print_exc
    print(sys_path)
    print_exc()
