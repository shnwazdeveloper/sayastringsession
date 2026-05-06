from pyrogram.types import InlineKeyboardButton


class Data:
    generate_single_button = [InlineKeyboardButton("Generate Session", callback_data="generate")]

    home_buttons = [
        generate_single_button,
        [InlineKeyboardButton(text="Home", callback_data="home")]
    ]

    generate_button = [generate_single_button]

    buttons = [
        generate_single_button,
        [
            InlineKeyboardButton("How to Use", callback_data="help"),
            InlineKeyboardButton("About", callback_data="about")
        ],
    ]

    START = """
Hi {}

Welcome to {}

I generate Pyrogram and Telethon string sessions.

Only generate sessions for accounts or bots you own.
    """

    HELP = """
**Commands**

/about - About The Bot
/help - This Message
/start - Start the Bot
/generate - Generate Session
/cancel - Cancel the process
/restart - Cancel the process
"""

    ABOUT = """
**SayaStringSession**

Telegram bot to generate Pyrogram and Telethon string sessions.

Source Code : [Click Here](https://github.com/shnwazdeveloper/SayaStringSession)

Framework : [Pyrogram](https://docs.pyrogram.org) and [Telethon](https://docs.telethon.dev)

Language : [Python](https://www.python.org)
    """
