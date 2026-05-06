from pyrogram.types import Message
from pyrogram import Client, filters

from env import DATABASE_URL, OWNER_ID


SESSION = None
Users = None
num_users = None

if DATABASE_URL:
    from SayaStringSession.database import SESSION
    from SayaStringSession.database.users_sql import Users, num_users


@Client.on_message(~filters.service, group=1)
async def users_sql(_, msg: Message):
    if not DATABASE_URL or SESSION is None or Users is None or not msg.from_user:
        return
    try:
        q = SESSION.query(Users).get(int(msg.from_user.id))
        if not q:
            SESSION.add(Users(msg.from_user.id))
            SESSION.commit()
    except Exception:
        SESSION.rollback()
        raise
    finally:
        SESSION.close()


@Client.on_message(filters.private & filters.command("stats"))
async def _stats(_, msg: Message):
    if not OWNER_ID or not msg.from_user or msg.from_user.id != OWNER_ID:
        return
    if not DATABASE_URL or SESSION is None or num_users is None:
        await msg.reply("Database is not configured.", quote=True)
        return
    users = await num_users()
    await msg.reply(f"Total Users : {users}", quote=True)
