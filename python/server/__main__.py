from uvicorn import run


def inject_root():
    """Make the Python folder importable."""
    from sys import path as sys_path
    from pathlib import Path
    try:
        from python.server.api import app
    except ImportError:
        root = Path().absolute()
        sys_path.append(str(root))


if __name__ == '__main__':
    inject_root()
    run("python.server.api:app", port=8000, reload=True)
