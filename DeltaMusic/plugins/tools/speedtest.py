# Copyright (C) 2025 by Delta_Help @ Github, < https://github.com/TheTeamDelta >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Delta © Yukki.

""""
TheTeamDelta is a project of Telegram bots with variety of purposes.
Copyright (c) 2021 ~ Present Team Delta <https://github.com/TheTeamDelta>

This program is free software: you can redistribute it and can modify
as you want or you can collabe if you have new ideas.
"""


import asyncio
import speedtest
from pyrogram import filters
from strings import get_command
from DeltaMusic import app
from DeltaMusic.misc import SUDOERS

# Commands
SPEEDTEST_COMMAND = get_command("SPEEDTEST_COMMAND")


async def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        await m.edit("<b>⬇️ Menjalankan Tes Kecepatan Unduh ...</b>")
        test.download()
        await m.edit("<b>⬆️ Menjalankan Tes Kecepatan Unggah ...</b>")
        test.upload()
        test.results.share()
        result = test.results.dict()
        await m.edit("<b>📤 Membagikan Hasil SpeedTest ...</b>")
    except Exception as e:
        return await m.edit(str(e))
    return result


@app.on_message(filters.command(SPEEDTEST_COMMAND) & SUDOERS)
async def speedtest_function(client, message):
    m = await message.reply_text("🚀 Menjalankan Tes Kecepatan ...")
    result = await testspeed(m)
    if isinstance(result, dict):
        output = f"""🌐 <b>Hasil SpeedTest</b>

<u><b>Klien :</b></u>
<b>ISP :</b> {result['client']['isp']}
<b>Negara :</b> {result['client']['country']}

<u><b>Server :</b></u>
<b>Nama :</b> {result['server']['name']}
<b>Negara :</b> {result['server']['country']}, {result['server']['cc']}
<b>Sponsor :</b> {result['server']['sponsor']}
<b>Latensi :</b> {result['server']['latency']} 
<b>Ping :</b> {result['ping']}
"""
        msg = await app.send_photo(
            chat_id=message.chat.id, photo=result["share"], caption=output
        )
        await m.delete()
    else:
        await m.edit("Gagal menjalankan tes kecepatan.")
