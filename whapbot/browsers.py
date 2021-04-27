import json
import urllib.request
import subprocess
from sys import platform


__all__ = ["get_latest_release", "get_current_version"]

LATEST_RELEASES = {
    "chrome": "https://chromedriver.storage.googleapis.com/LATEST_RELEASE",
    "firefox": "https://api.github.com/repos/mozilla/geckodriver/releases/latest",
    "opera": "https://api.github.com/repos/operasoftware/operachromiumdriver/releases/latest",
    "edge": "https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/"
}
LATEST_RELEASES["brave"] = LATEST_RELEASES["chrome"]

BROWSER_REGISTRY_PATHS = {
    "chrome": r"Software\Google\Chrome\BLBeacon",
    "edge": r"Software\Microsoft\Edge\BLBeacon",
    "brave": r"Software\BraveSoftware\Brave-Browser\BLBeacon"
}

MAC_BROWSER_PATHS = {
    "chrome": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    # "firefox": "/Applications/Firefox.app/Contents/MacOS/****",
    # "opera": "/Applications/Opera *****",
    "brave": "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
}


def get_latest_release(browser):
    if browser in ["chrome", "brave"]:
        version = get_chromium_driver_version(LATEST_RELEASES[browser])
    elif browser in ["firefox", "opera"]:
        version = get_github_latest_release(LATEST_RELEASES[browser])
    elif browser == "edge":
        version = get_edge_driver_latest_release(LATEST_RELEASES[browser])
    else:
        raise RuntimeError(f"Cannot get latest release for {browser} browser")
    return version


def get_current_version(browser):
    if browser in ["chrome", "brave"]:
        version = get_chromium_driver_version(LATEST_RELEASES[browser], get_chromium_current_version(browser))
    elif browser in ["firefox", "opera"]:
        version = get_latest_release(browser)
    elif browser == "edge":
        version = get_windows_browser_current_version(browser)
    else:
        raise RuntimeError(f"Cannot get the current version for {browser} browser")
    return version


def get_chromium_current_version(browser):
    if platform == 'linux':
        with subprocess.Popen(['chromium-browser', '--version'], stdout=subprocess.PIPE) as proc:
            process = proc.stdout.read().decode('utf-8')
            version = "".join(filter(lambda char: char.isdigit() or char == ".", process)).strip()
    elif platform == 'darwin':
        process = subprocess.Popen([MAC_BROWSER_PATHS[browser], '--version'],
                                   stdout=subprocess.PIPE).communicate()[0].decode("UTF-8")
        version = "".join(filter(lambda char: char.isdigit() or char == ".", process)).strip()
    else:  # win32
        version = get_windows_browser_current_version(browser)
    return version


def get_windows_browser_current_version(browser):
    assert platform == "win32"
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, BROWSER_REGISTRY_PATHS[browser], 0, winreg.KEY_READ)
        version = winreg.QueryValueEx(key, "version")[0]
    except KeyError:
        raise RuntimeError(f"Cannot detect current version for {browser.title()} browser")
    return version


def get_chromium_driver_version(api_path, full_version=""):
    api_path += f'_{full_version.split(".")[0]}' if full_version else ""
    with urllib.request.urlopen(api_path) as response:
        version = response.readlines()[0].decode("utf-8")
    return version


def get_github_latest_release(api_path):  # for firefox and opera
    with urllib.request.urlopen(api_path) as response:
        version = json.loads(response.read())["tag_name"]
    return version


def get_edge_driver_latest_release(api_path):
    with urllib.request.urlopen(api_path) as response:
        html_str = response.readlines()[-1].decode("utf-8")

        versions_idx = html_str.find(f"Version: ")
        final_idx = html_str[versions_idx:].find(f"OS {platform}") + versions_idx
        init_idx = html_str[:final_idx].rfind("version") + 7

        version = html_str[init_idx: final_idx].strip()

    return version
