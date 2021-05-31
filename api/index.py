from python.server.api import app


def inject_root():
    """Make the Python folder importable."""
    from sys import path as sys_path
    from pathlib import Path
    try:
        from python.server.api import app
    except ImportError:
        root = Path().absolute()
        sys_path.append(str(root))


inject_root()
