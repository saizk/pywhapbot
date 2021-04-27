![whapbot_logo](images/whapbot.png?raw=true)

## Installation
```Python
pip install whapbot
```

## Simple Usage
```Python
from whapbot import WhapBot
bot = WhapBot("chrome")  # downloads current driver automatically
bot.log()  # optional
bot.send("+34123456789", "Hello world!")  # forces log
bot.quit()
```

## Download specific drivers automatically
```Python
from whapbot.install import download_driver
download_driver("firefox", version="0.29.1", root="drivers")
download_driver("opera", version="latest")
download_driver("edge", version="current")
```

## Get versions
```Python
from whapbot.utils import get_version
lversion = get_version("brave", "latest")
cversion = get_version("brave", "current")
```

## More advanced example
```Python
from whapbot import WhapBot

whapbot = WhapBot("firefox",
                  driver_path="geckodriver.exe",
                  profile_path="profiles/firefox-profile",
                  kiosk=True)  # kiosk mode (not supported on opera)

whapmsgs = [("+34696969420", "Open!"),
            ("+34696942069", "Sourcerer!")]

with whapbot as bot:  # Context manager of selenium webdriver class
    bot.get("https://github.com/saizk")
    # Selenium Webdriver command examples
    bot.driver.set_window_position(210, 210)
    assert len(bot.driver.window_handles) == 1 
    bot.driver.find_element_by_link_text("new window").click()
    bot.driver.switch_to.new_window('tab')
    
    for idx, (phone, message) in enumerate(whapmsgs):
        bot.send(phone, message, timeout=15, retries=5)  # forces log
        bot.screenshot(f"whapbot-{idx}.png")
        print(f"{idx+1}/{len(whapmsgs)} messages sent")    

# bot.quit() called by the context manager
```

## On Mac
pyarmor obfuscate --recursive src/app.py  +  PLATYPUS

sudo pyarmor pack --debug -s MacWhapBot.spec src/app.py


## pyinstaller build
pyinstaller src/app.py --onefile --windowed --name=WhapBot --icon=C:/Projects/WhapBot/images/icon.ico
pyinstaller WinWhapBot.spec


pyarmor obfuscate -O obfdist --recursive --advanced 2 src/app.py
python -m pyarmor.helper.repack -p obfdist dist/app.exe

pyarmor pack -s WinWhapBot.spec src/app.py
sudo pyarmor pack --debug -s MacWhapBot.spec src/app.py




makecert -r -pe -n "CN=github.com/saizk" -eku 1.3.6.1.5.5.7.3.1 -ss MY -a SHA512 -len 4096 C:\users\sergi\Desktop\whapbotcert.pfx (depracated)
signtool sign /f C:\Projects\WhapBot\WhapBotCert.cer C:\Projects\WhapBot\dist\WhapBot.exe

certreq -new makecert.inf WhapBotCert.cer