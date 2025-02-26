from pyrogram import filters
from pyrogram.types import Message

from DeltaMusic import app
from config import OWNER_ID


@app.on_message(filters.command("ownerjoin") & filters.user(OWNER_ID))
async def invite_owner(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Berikan tautan atau username grup yang ingin Anda undang!"
        )
    try:
        link = message.text.split(None, 1)[1]
        await client.join_chat(link)
        await message.reply_text("Berhasil bergabung ke grup!")
    except Exception as e:
        await message.reply_text(f"Gagal bergabung ke grup!\n\n**Error:** {e}")
