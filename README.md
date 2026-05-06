# SayaStringSession

SayaStringSession is a small Telegram bot for generating Pyrogram and Telethon string sessions.

## Features

- Generate Pyrogram user string sessions
- Generate Pyrogram bot string sessions
- Generate Telethon user string sessions
- Generate Telethon bot string sessions
- Optional forced channel or group join check
- Optional PostgreSQL-backed user stats

## Deploy On Railway

1. Create a new Railway project from your `SayaStringSession` GitHub repo.
2. Add the required variables in Railway:
   - `API_ID`
   - `API_HASH`
   - `BOT_TOKEN`
3. Add optional variables if you need them:
   - `MUST_JOIN`
   - `DATABASE_URL`
   - `OWNER_ID`
4. Deploy the service.

Railway reads `railway.json` and starts the bot with:

```bash
python3 bot.py
```

## Local Setup

```bash
git clone https://github.com/shnwazdeveloper/SayaStringSession
cd SayaStringSession
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env
python3 bot.py
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.sample .env
python bot.py
```

## Environment Variables

- `API_ID` - Telegram API ID from [my.telegram.org](https://my.telegram.org/auth)
- `API_HASH` - Telegram API hash from [my.telegram.org](https://my.telegram.org/auth)
- `BOT_TOKEN` - Bot token from [@BotFather](https://t.me/BotFather)
- `MUST_JOIN` - Optional channel or group username/ID users must join before using the bot
- `DATABASE_URL` - Optional PostgreSQL URL for user stats. Leave it empty if you do not use stats.
- `OWNER_ID` - Optional Telegram user ID allowed to run `/stats`

## Notes

Only generate string sessions for accounts or bots you own. Treat generated sessions like passwords.

If Railway logs show `FLOOD_WAIT`, leave the deployment running. SayaStringSession will wait for Telegram's cooldown and retry automatically.

## Credits

- [Dan Tès](https://github.com/delivrance) for Pyrogram
- [Lonami](https://github.com/Lonami) for Telethon
