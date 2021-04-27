import os
import shutil
import urllib.request
from sys import platform
from pathlib import Path
from jinja2 import Template
from urllib.error import HTTPError, URLError

from .utils import *

__all__ = ["download_driver"]

DRIVER_ROUTES = {
    "chrome": "https://chromedriver.storage.googleapis.com/{{version}}/chromedriver_{{os}}{{bits}}.{{format}}",
    "firefox": "https://github.com/mozilla/geckodriver/releases/download/{{version}}/geckodriver-{{version}}-{{os}}{{bits}}.{{format}}",
    "opera": "https://github.com/operasoftware/operachromiumdriver/releases/download/{{version}}/operadriver_{{os}}{{bits}}.{{format}}",
    "edge": "https://msedgedriver.azureedge.net/{{version}}/edgedriver_win{{bits}}.{{format}}"
    # "edge": "https://msedgedriver.azureedge.net/{{version}}/edgedriver_{{os}}{{bits}}.{{format}}",
}
DRIVER_ROUTES["brave"] = DRIVER_ROUTES["chrome"]


def download_driver(driver, version="current", root="."):
    if not os.path.exists(root):
        os.mkdir(root)

    driver_folder = f"{root}/{driver}"
    driver_path = driver_folder + f"/{driver}driver" + (".exe" if platform == "win32" else "")

    if Path(driver_path).exists():
        return
    try:
        if version in ["current", "latest"]:
            version = get_version(driver, version)
        else:
            version = fix_version(driver, version)
        url, filename = gen_url(driver, version, template=Template(DRIVER_ROUTES[driver]))
        download_url(url, filename)
        extract(filename, driver_folder)
        fix_paths(driver, driver_path)
        assert Path(driver_path).exists()

    except (HTTPError, URLError):
        raise RuntimeError(f"Cannot download {driver} driver.\n"
                           f"If the problem persist, download the driver manually.")


def download_url(url, filename):
    with urllib.request.urlopen(url) as response, open(filename, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)


def extract(filename, tgt_path):
    shutil.unpack_archive(filename, tgt_path)
    os.remove(filename)


def fix_version(driver, raw_version):
    # version = "".join(filter(lambda char: char.isdigit() or char == ".", raw_version))
    if driver == "firefox":
        return "v" + raw_version
    elif driver == "opera":
        return "v." + raw_version
    else:
        return raw_version


def fix_paths(driver, driver_path):
    src_path = search_driver(root_path=Path(driver_path).parent)

    # rename for convenience
    if driver in ["firefox", "brave", "edge"]:
        os.rename(src_path, driver_path)
        if driver == "edge":
            shutil.rmtree(f"{Path(driver_path).parent}/Driver_Notes")
    elif driver == "opera":
        shutil.move(src_path, driver_path)  # moves driver and deletes extra dir
        shutil.rmtree(src_path.parent)
    if platform in ["linux", "darwin"] and driver in ["chrome", "opera", "brave"]:
        os.chmod(driver_path, 755)  # add permissions for linux/mac drivers


def download_default_driver():
    if platform == "linux":
        download_driver(get_linux_default_browser())
    elif platform == "win32":
        download_driver(get_windows_default_browser())
    elif platform == "darwin":
        download_driver(get_mac_default_browser())
    else:
        raise RuntimeError("Unknown operating system")


def get_linux_default_browser():
    assert platform == "linux"
    try:
        import re, subprocess
        def_list = subprocess.check_output(["cat", "/usr/share/applications/defaults.list"]).decode("utf-8")
        default_browser = re.findall("http=([^\.]*)", def_list)[0].split("-")[0]

        if default_browser == "google":
            return "chrome"
        return default_browser
    except Exception:
        return "firefox"  # linux default


def get_windows_default_browser():
    assert platform == "win32"
    try:
        import winreg
        key = winreg.OpenKey(winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER),
                             r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\https\UserChoice")
        prog_id, _ = winreg.QueryValueEx(key, "ProgId")
        key = winreg.OpenKey(winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE),
                             r"SOFTWARE\Classes\{}\shell\open\command".format(prog_id))
        launch_string, _ = winreg.QueryValueEx(key, "")  # read the default value
        def_browser_path = launch_string.lower().rstrip()

        for key in DRIVER_ROUTES.keys():
            if key in def_browser_path:
                return key

        raise RuntimeError("Default browser not found or not supported")

    except FileNotFoundError:  # Just when Opera default browser
        return "opera"


def get_mac_default_browser():
    assert platform == "darwin"
    return NotImplementedError("Mac default browser function not implemented yet")


if __name__ == '__main__':
    download_default_driver()
