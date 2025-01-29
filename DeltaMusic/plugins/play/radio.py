import logging

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from config import BANNED_USERS, adminlist
from strings import get_string
from DeltaMusic import app
from DeltaMusic.misc import SUDOERS
from DeltaMusic.utils.database import (
    get_assistant,
    get_cmode,
    get_lang,
    get_playmode,
    get_playtype,
)
from DeltaMusic.utils.logger import play_logs
from DeltaMusic.utils.stream.stream import stream

RADIO_STATION = {
    "The Rockin Life": "https://n10.radiojar.com/7csmg90fuqruv?rj-ttl=5&rj-tok=AAABlLLRtm0A79_IvCfOpTBeBw",
    "i-Radio": "https://n0d.radiojar.com/4ywdgup3bnzuv?rj-ttl=5&rj-tok=AAABlLLWuAUAXZtQLiTbz29MeA",
    "Radio Elshinta": "https://stream-ssl.arenastreaming.com:8000/jakarta.m3u",
    "90.4 FM": "https://stream.radiojar.com/u7d8heq3bnzuv",
    "OZ Radio": "https://streaming.ozradiojakarta.com:8443/ozjakarta",
    "Radio Sonora": "https://streaming.brol.tech/rtfmlounge",
    "Hot 93.2 FM": "https://wz.mari.co.id:1936/web_hotfm/hotfm/playlist.m3u8",
    "KISI FM": "http://live.serverstreaming.net:9340/kisifm",
    "Smart FM": "https://streaming.brol.tech/rtfmlounge",
}

def get_station_buttons():
    buttons = []
    for name in sorted(RADIO_STATION.keys()):
        buttons.append([InlineKeyboardButton(text=name, callback_data=f"radio_station_{name}")])
    return InlineKeyboardMarkup(buttons)


@app.on_message(
    filters.command(["radioplayforce", "radio", "cradio"])
    & filters.group
    & ~BANNED_USERS
)
async def radio(client, message: Message):
    msg = await message.reply_text("Mohon tunggu sebentar....")
    try:
        try:
            userbot = await get_assistant(message.chat.id)
            get = await app.get_chat_member(message.chat.id, userbot.id)
        except ChatAdminRequired:
            return await msg.edit_text(
                f"Saya tidak memiliki izin untuk mengundang pengguna melalui tautan untuk mengundang {userbot.mention} asisten ke {message.chat.title}."
            )
        if get.status == ChatMemberStatus.BANNED:
            return await msg.edit_text(
                text=f"{userbot.mention} asisten diblokir di {message.chat.title}\n\nID : `{userbot.id}`\nNama : {userbot.mention}\nUsername : @{userbot.username}\n\nSilakan buka blokir asisten dan coba lagi...",
            )
    except UserNotParticipant:
        if message.chat.username:
            invitelink = message.chat.username
            try:
                await userbot.resolve_peer(invitelink)
            except Exception as ex:
                logging.exception(ex)
        else:
            try:
                invitelink = await client.export_chat_invite_link(message.chat.id)
            except ChatAdminRequired:
                return await msg.edit_text(
                    f"Saya tidak memiliki izin untuk mengundang pengguna melalui tautan untuk mengundang {userbot.mention} asisten ke {message.chat.title}."
                )
            except InviteRequestSent:
                try:
                    await app.approve_chat_join_request(message.chat.id, userbot.id)
                except Exception as e:
                    return await msg.edit(
                        f"Gagal mengundang {userbot.mention} asisten ke {message.chat.title}.\n\n**Alasan :** `{ex}`"
                    )
            except Exception as ex:
                if "channels.JoinChannel" in str(ex) or "Username tidak ditemukan" in str(ex):
                    return await msg.edit_text(
                        f"Saya tidak memiliki izin untuk mengundang pengguna melalui tautan untuk mengundang {userbot.mention} asisten ke {message.chat.title}."
                    )
                else:
                    return await msg.edit_text(
                        f"Gagal mengundang {userbot.mention} asisten ke {message.chat.title}.\n\n**Alasan :** `{ex}`"
                    )
        if invitelink.startswith("https://t.me/+"):
            invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
        anon = await msg.edit_text(
            f"Silakan tunggu...\n\nMengundang {userbot.mention} ke {message.chat.title}."
        )
        try:
            await userbot.join_chat(invitelink)
            await asyncio.sleep(2)
            await msg.edit_text(
                f"{userbot.mention} berhasil bergabung,\n\nmemulai streaming..."
            )
        except UserAlreadyParticipant:
            pass
        except InviteRequestSent:
            try:
                await app.approve_chat_join_request(message.chat.id, userbot.id)
            except Exception as e:
                return await msg.edit(
                    f"Gagal mengundang {userbot.mention} asisten ke {message.chat.title}.\n\n**Alasan :** `{ex}`"
                )
        except Exception as ex:
            if "channels.JoinChannel" in str(ex) or "Username tidak ditemukan" in str(ex):
                return await msg.edit_text(
                    f"Saya tidak memiliki izin untuk mengundang pengguna melalui tautan untuk mengundang {userbot.mention} asisten ke {message.chat.title}."
                )
            else:
                return await msg.edit_text(
                    f"Gagal mengundang {userbot.mention} asisten ke {message.chat.title}.\n\n**Alasan :** `{ex}`"
                )

        try:
            await userbot.resolve_peer(invitelink)
        except:
            pass
    await msg.delete()
    station_name = " ".join(message.command[1:])
    RADIO_URL = RADIO_STATION.get(station_name)
    if RADIO_URL:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
        playmode = await get_playmode(message.chat.id)
        playty = await get_playtype(message.chat.id)
        if playty != "Everyone":
            if message.from_user.id not in SUDOERS:
                admins = adminlist.get(message.chat.id)
                if not admins:
                    return await message.reply_text(_["admin_25"])
                else:
                    if message.from_user.id not in admins:
                        return await message.reply_text(_["play_4"])
        if message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            try:
                chat = await app.get_chat(chat_id)
            except:
                return await message.reply_text(_["cplay_4"])
            channel = chat.title
        else:
            chat_id = message.chat.id
            channel = None

        video = None
        mystic = await message.reply_text(
            _["play_2"].format(channel) if channel else _["play_1"]
        )
        try:
            await stream(
                _,
                mystic,
                message.from_user.id,
                RADIO_URL,
                chat_id,
                message.from_user.mention,
                message.chat.id,
                video=video,
                streamtype="index",
            )
        except Exception as e:
            ex_type = type(e).__name__
            err = e if ex_type == "AssistantErr" else _["general_4"].format(ex_type)
            return await mystic.edit_text(err)
        return await play_logs(message, streamtype="M3u8 or Index Link")
    else:
        await message.reply(
            "Berikan saya nama stasiun untuk memutar radio",
            reply_markup=get_station_buttons()
        )


__MODULE__ = "Radio"
__HELP__ = f"\n/radio [nama stasiun] - untuk memutar **radio di obrolan suara**\n\nBerikut adalah beberapa nama stasiun:\n{valid_stations}"
