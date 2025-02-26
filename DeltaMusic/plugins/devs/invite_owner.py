from pyrogram import filters
from pyrogram.types import Message

from DeltaMusic import app
from config import OWNER_ID


@app.on_message(filters.command("inviteme") & filters.user(OWNER_ID))
async def inviteme_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "<b>Gunakan Perintah :</b>\n/inviteme [username atau id group]"
        )
    chat = message.text.split(None, 2)[1]
    try:
        await app.add_chat_member(chat, message.from_user.id)
    except Exception as e:
        return await message.reply_text(f"<b>ERROR :</b>\n{e}")
    await message.reply_text("<b>Berhasil Bergabung Ke Group</b>")
