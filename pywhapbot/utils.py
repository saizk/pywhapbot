from sys import platform
from pathlib import Path

from .browsers import get_latest_release, get_current_version

__all__ = ["gen_url", "get_version", "search_driver", "get_os"]


def gen_url(driver, version, template):
    if platform == "win32" and driver in ["chrome", "brave"]:
        bits = 32
    elif platform == "darwin" and driver == "firefox":
        bits = "os"
    else:
        bits = 64

    if platform in ["linux", "darwin"] and driver == "firefox":
        file_ext = "tar.gz"
    else:
        file_ext = "zip"

    url = template.render(version=version, os=get_os(), bits=bits, format=file_ext)
    filename = url.split("/")[-1]
    return url, filename


def get_version(browser, version):
    if version == "latest":
        return get_latest_release(browser)
    elif version == "current":
        return get_current_version(browser)
    else:
        raise RuntimeError("Unknown version")


def search_driver(browser="*", root_path=Path.cwd()):
    ext = ".exe" if platform == "win32" else ""
    for path in Path(root_path).rglob(f'{browser}driver{ext}'):
        return path.absolute()


def get_os():
    if platform == "win32":
        return "win"
    elif platform == "darwin":
        return "mac"
    else:
        return "linux"
