from contextlib import suppress

from telethon import TelegramClient
from pyrogram.types import Message
from pyrogram import Client, filters
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid,
    AccessTokenInvalid
)

from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError,
    AccessTokenInvalidError
)

from data import Data


ask_ques = "Choose a session type."
buttons_ques = [
    [
        InlineKeyboardButton("Pyrogram", callback_data="pyrogram"),
        InlineKeyboardButton("Telethon", callback_data="telethon"),
    ],
    [
        InlineKeyboardButton("Pyrogram Bot", callback_data="pyrogram_bot"),
        InlineKeyboardButton("Telethon Bot", callback_data="telethon_bot"),
    ],
]


@Client.on_message(filters.private & ~filters.forwarded & filters.command('generate'))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bot: Client, msg: Message, telethon=False, is_bot: bool = False):
    ty = "Telethon" if telethon else "Pyrogram"
    if is_bot:
        ty += " Bot"

    await msg.reply(f"Starting {ty} session generation.")
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, "Send your `API_ID`.", filters=filters.text)
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply("`API_ID` must be a number. Start again with /generate.", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    api_hash_msg = await bot.ask(user_id, "Send your `API_HASH`.", filters=filters.text)
    if await cancelled(api_hash_msg):
        return
    api_hash = api_hash_msg.text
    if not is_bot:
        t = "Send your `PHONE_NUMBER` with country code.\nExample: `+19876543210`"
    else:
        t = "Send your `BOT_TOKEN`.\nExample: `12345:abcdefghijklmnopqrstuvwxyz`"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("Sending OTP.")
    else:
        await msg.reply("Logging in as bot.")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name=f"bot_{user_id}", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    else:
        client = Client(name=f"user_{user_id}", api_id=api_id, api_hash=api_hash, in_memory=True)

    try:
        try:
            await client.connect()
            code = None
            if not is_bot:
                if telethon:
                    code = await client.send_code_request(phone_number)
                else:
                    code = await client.send_code(phone_number)
        except (ApiIdInvalid, ApiIdInvalidError):
            await msg.reply("`API_ID` and `API_HASH` combination is invalid. Start again with /generate.", reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
        except (PhoneNumberInvalid, PhoneNumberInvalidError):
            await msg.reply("`PHONE_NUMBER` is invalid. Start again with /generate.", reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return

        try:
            phone_code_msg = None
            if not is_bot:
                phone_code_msg = await bot.ask(user_id, "Check Telegram for the OTP. If the OTP is `12345`, send it here as `1 2 3 4 5`.", filters=filters.text, timeout=600)
                if await cancelled(phone_code_msg):
                    return
        except TimeoutError:
            await msg.reply("Time limit reached after 10 minutes. Start again with /generate.", reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return

        if not is_bot:
            phone_code = phone_code_msg.text.replace(" ", "")
            try:
                if telethon:
                    await client.sign_in(phone_number, phone_code, password=None)
                else:
                    await client.sign_in(phone_number, code.phone_code_hash, phone_code)
            except (PhoneCodeInvalid, PhoneCodeInvalidError):
                await msg.reply("OTP is invalid. Start again with /generate.", reply_markup=InlineKeyboardMarkup(Data.generate_button))
                return
            except (PhoneCodeExpired, PhoneCodeExpiredError):
                await msg.reply("OTP expired. Start again with /generate.", reply_markup=InlineKeyboardMarkup(Data.generate_button))
                return
            except (SessionPasswordNeeded, SessionPasswordNeededError):
                try:
                    two_step_msg = await bot.ask(user_id, "Two-step verification is enabled. Send the password.", filters=filters.text, timeout=300)
                except TimeoutError:
                    await msg.reply("Time limit reached after 5 minutes. Start again with /generate.", reply_markup=InlineKeyboardMarkup(Data.generate_button))
                    return
                try:
                    if await cancelled(two_step_msg):
                        return
                    password = two_step_msg.text
                    if telethon:
                        await client.sign_in(password=password)
                    else:
                        await client.check_password(password=password)
                except (PasswordHashInvalid, PasswordHashInvalidError):
                    await two_step_msg.reply("Invalid password. Start again with /generate.", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
                    return
        else:
            try:
                if telethon:
                    await client.start(bot_token=phone_number)
                else:
                    await client.sign_in_bot(phone_number)
            except (AccessTokenInvalid, AccessTokenInvalidError):
                await msg.reply("`BOT_TOKEN` is invalid. Start again with /generate.", reply_markup=InlineKeyboardMarkup(Data.generate_button))
                return

        if telethon:
            string_session = client.session.save()
        else:
            string_session = await client.export_session_string()
        text = f"**{ty.upper()} STRING SESSION**\n\n`{string_session}`\n\nGenerated by SayaStringSession"
        if not is_bot:
            await client.send_message("me", text)
            delivery_note = "Please check Saved Messages."
        else:
            await bot.send_message(msg.chat.id, text)
            delivery_note = "I sent the session in this chat."
        await bot.send_message(
            msg.chat.id,
            "Successfully generated {} string session.\n\n{}".format(
                "telethon" if telethon else "pyrogram",
                delivery_note,
            ),
        )
    finally:
        with suppress(Exception):
            await client.disconnect()


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("Cancelled the process.", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("Restarted the bot.", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("Cancelled the generation process.", quote=True)
        return True
    else:
        return False
