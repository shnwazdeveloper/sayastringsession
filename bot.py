import logging
from contextlib import suppress
from time import sleep

import env
from pyrogram import Client, idle
from pyromod import listen  # type: ignore
from pyrogram.errors import (
    AccessTokenInvalid,
    ApiIdInvalid,
    ApiIdPublishedFlood,
    FloodWait,
)


logging.basicConfig(
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(pathname)s: %(message)s",
)

def create_app() -> Client:
    return Client(
        "SayaStringSession",
        api_id=env.API_ID,
        api_hash=env.API_HASH,
        bot_token=env.BOT_TOKEN,
        plugins={"root": "SayaStringSession"},
    )


def start_bot() -> Client:
    while True:
        app = create_app()
        try:
            app.start()
            return app
        except FloodWait as exc:
            wait_for = int(getattr(exc, "value", 60)) + 5
            logging.warning(
                "Telegram requested FLOOD_WAIT for %s seconds. Waiting before retrying.",
                wait_for,
            )
            with suppress(Exception):
                app.stop()
            sleep(wait_for)
        except (ApiIdInvalid, ApiIdPublishedFlood):
            raise SystemExit("Your API_ID/API_HASH is not valid.")
        except AccessTokenInvalid:
            raise SystemExit("Your BOT_TOKEN is not valid.")


if __name__ == "__main__":
    logging.info("Starting SayaStringSession")
    app = start_bot()
    uname = app.me.username
    logging.info(f"@{uname} is now running!")
    idle()
    with suppress(Exception):
        app.stop()
    logging.info("Bot stopped.")
