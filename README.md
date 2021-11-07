![whapbot_logo](https://raw.githubusercontent.com/saizk/pywhapbot/master/images/whapbot.png)
![PyPI version](https://img.shields.io/pypi/v/pywhapbot)

WhatsApp Web API Wrapper for Chrome, Firefox, Opera, Brave and Edge.

## Installation
```Python
pip install pywhapbot
```

## Features
+ Automate the download of Selenium drivers
+ Send messages by phone number
+ Store WhatsApp Web sessions in all the browsers. (Edge only available on Windows)

## Simple Usage

```Python
from whapbot import WhapBot

from autoselenium import Driver

with WhapBot('chrome', root='drivers') as bot:
    bot.set_window_position(420, 420)
    bot.send("+34123456789", "Hello world!")
    bot.refresh()

```

## More advanced example

```Python
import time
from pywhapbot import WhapBot

whapbot = WhapBot(
    browser="firefox",
    driver_path="drivers/geckodriver.exe",
    profile_path="profiles/firefox-profile",
    proxy="169.210.345.10:4567",
    kiosk=True  # kiosk mode (not supported on opera)
)
whapmsgs = [("+34696969420", "Open!"),
            ("+34696942069", "Source!")]

with whapbot as bot:

    for idx, (phone, message) in enumerate(whapmsgs):
        bot.send(phone, message, timeout=15, retries=5)  # forces log
        bot.screenshot(f"whapbot-{idx}.png")
        print(f"{idx + 1}/{len(whapmsgs)} messages sent")

    time.sleep(120)

    for phone, message in whapmsgs:
        bot.open_chat_by_phone(phone)
        if bot.get_last_message_status() not in ["Read", "Leído"]:
            bot.send(message)
```

## Contribute
Would you like to contribute to this project? Here are a few starters:
- Improve documentation
- Add Testing examples
- Bug hunts and refactor
- Additional features/ More integrations