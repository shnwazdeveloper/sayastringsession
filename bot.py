import logging

import env
from pyrogram import Client, idle
from pyromod import listen  # type: ignore
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid


logging.basicConfig(
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(pathname)s: %(message)s",
)

app = Client(
    "SayaStringSession",
    api_id=env.API_ID,
    api_hash=env.API_HASH,
    bot_token=env.BOT_TOKEN,
    in_memory=True,
    plugins={"root": "SayaStringSession"},
)


if __name__ == "__main__":
    logging.info("Starting SayaStringSession")
    try:
        app.start()
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("Your API_ID/API_HASH is not valid.")
    except AccessTokenInvalid:
        raise Exception("Your BOT_TOKEN is not valid.")
    uname = app.me.username
    logging.info(f"@{uname} is now running!")
    idle()
    app.stop()
    logging.info("Bot stopped.")
