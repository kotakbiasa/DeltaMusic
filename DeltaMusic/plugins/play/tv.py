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

TV_STATION = {
    "Trans 7": "https://video.detik.com/trans7/smil:trans7.smil/index.m3u8",
    "TransTV": "https://video.detik.com/transtv/smil:transtv.smil/index.m3u8",
    "CNBC Indonesia": "https://live.cnbcindonesia.com/livecnbc/smil:cnbctv.smil/master.m3u8",
    "KompasTV": "http://op-group1-swiftservehd-1.dens.tv/h/h234/01.m3u8",
    "One Piece": "http://cfd-v4-service-channel-stitcher-use1-1.prd.pluto.tv/stitch/hls/channel/5f7790b3ed0c88000720b241/master.m3u8?appName=web&appVersion=unknown&clientTime=0&deviceDNT=0&deviceId=6c2a7816-30d3-11ef-9cf5-e9ddff8ff496&deviceMake=Chrome&deviceModel=web&deviceType=web&deviceVersion=unknown&includeExtendedEvents=false&serverSideAds=false&sid=4b38ba42-6f97-4a17-b657-1277978d366c",
    "CNN Indonesia": "https://live.cnnindonesia.com/livecnn/smil:cnntv.smil/master.m3u8",
    "Indosiar": "http://op-group1-swiftservehd-1.dens.tv/h/h207/02.m3u8",
    "ANTV": "http://op-group1-swiftservehd-1.dens.tv/h/h235/02.m3u8",
    "MDTV": "http://op-group1-swiftservehd-1.dens.tv/h/h223/02.m3u8",
}

def get_station_buttons():
    buttons = []
    for name in sorted(TV_STATION.keys()):
        buttons.append([InlineKeyboardButton(text=name, callback_data=f"tv_station_{name}")])
    return InlineKeyboardMarkup(buttons)


@app.on_callback_query(filters.regex(r"^tv_station_"))
async def tv_station_callback(client, callback_query):
    station_name = callback_query.data.split("_", 2)[2]
    TV_URL = TV_STATION.get(station_name)
    if TV_URL:
        await callback_query.answer()  # Answer the callback query first
        language = await get_lang(callback_query.message.chat.id)
        _ = get_string(language)
        playmode = await get_playmode(callback_query.message.chat.id)
        playty = await get_playtype(callback_query.message.chat.id)
        if playty != "Everyone":
            if callback_query.from_user and callback_query.from_user.id not in SUDOERS:
                admins = adminlist.get(callback_query.message.chat.id)
                if not admins:
                    return await callback_query.answer(_["admin_25"], show_alert=True)
                else:
                    if callback_query.from_user.id not in admins:
                        return await callback_query.answer(_["play_4"], show_alert=True)
        chat_id = callback_query.message.chat.id
        channel = None

        video = True
        mystic = await callback_query.message.reply_text(
            _["play_2"].format(channel) if channel else _["play_1"]
        )
        try:
            await stream(
                _,
                mystic,
                callback_query.from_user.id,
                TV_URL,
                chat_id,
                callback_query.from_user.mention,
                callback_query.message.chat.id,
                video=video,
                streamtype="index",
                force_play=True  # Force play without queuing
            )
        except Exception as e:
            ex_type = type(e).__name__
            err = e if ex_type == "AssistantErr" else _["general_4"].format(ex_type)
            return await mystic.edit_text(err)
        await play_logs(callback_query.message, streamtype="M3u8 or Index Link")
    else:
        await callback_query.answer("Stasiun tidak ditemukan!", show_alert=True)

@app.on_message(
    filters.command(["tvplayforce", "tv", "ctv"])
    & filters.group
    & ~BANNED_USERS
)
async def tv(client, message: Message):
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
    TV_URL = TV_STATION.get(station_name)
    if TV_URL:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
        playmode = await get_playmode(message.chat.id)
        playty = await get_playtype(message.chat.id)
        if playty != "Everyone":
            if message.from_user and message.from_user.id not in SUDOERS:
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

        video = True
        mystic = await message.reply_text(
            _["play_2"].format(channel) if channel else _["play_1"]
        )
        try:
            await stream(
                _,
                mystic,
                message.from_user.id,
                TV_URL,
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
            "Silakan pilih nama stasiun tv untuk diputar",
            reply_markup=get_station_buttons()
        )