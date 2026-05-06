from env import MUST_JOIN
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden


def public_join_link(chat_ref: str) -> str | None:
    chat_ref = str(chat_ref).strip()
    if not chat_ref:
        return None
    if chat_ref.startswith("@"):
        return f"https://t.me/{chat_ref[1:]}"
    if not chat_ref.lstrip("-").isdigit():
        return f"https://t.me/{chat_ref}"
    return None


@Client.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(bot: Client, msg: Message):
    if not MUST_JOIN:  # Not compulsory
        return
    try:
        try:
            await bot.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            link = public_join_link(MUST_JOIN)
            if not link:
                chat_info = await bot.get_chat(MUST_JOIN)
                link = chat_info.invite_link
            try:
                reply_kwargs = {"disable_web_page_preview": True}
                if link:
                    reply_kwargs["reply_markup"] = InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Join Channel", url=link)]]
                    )
                await msg.reply(
                    "You must join the required channel or group to use me. After joining, try again.",
                    **reply_kwargs,
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"I am not admin in the MUST_JOIN chat: {MUST_JOIN}")
