from pyrogram import filters
from pyrogram.types import Message
from DeltaMusic import app
from DeltaMusic.misc import SUDOERS
from config import OWNER_ID  # Menggunakan SUDOERS dari config.py

@app.on_message(filters.command("inviteme") & filters.user(SUDOERS))
async def inviteme_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "<b>Gunakan Perintah :</b>\n/inviteme [username atau ID group]"
        )

    chat = message.text.split(None, 2)[1]

    # Coba ubah menjadi angka jika mungkin (untuk ID Telegram)
    if chat.isdigit():
        chat = int(chat)

    try:
        # Pastikan ini bukan user ID agar tidak terjadi error
        chat_info = await app.get_chat(chat)
        if chat_info.type in ["private", "bot"]:
            return await message.reply_text("<b>ERROR :</b>\nTidak bisa bergabung ke chat pribadi atau bot.")

        await app.add_chat_members(chat, message.from_user.id)
        await message.reply_text("<b>Berhasil Bergabung ke Grup</b>")
    except Exception as e:
        return await message.reply_text(f"<b>ERROR :</b>\n{e}")
    
