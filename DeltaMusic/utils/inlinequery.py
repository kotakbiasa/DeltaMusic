# Copyright (C) 2025 by Alexa_Help @ Github, < https://github.com/TheTeamAlexa >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Alexa © Yukki.

""""
TheTeamAlexa is a project of Telegram bots with variety of purposes.
Copyright (c) 2021 ~ Present Team Alexa <https://github.com/TheTeamAlexa>

This program is free software: you can redistribute it and can modify
as you want or you can collabe if you have new ideas.
"""


from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

answer = []

answer.extend(
    [
        InlineQueryResultArticle(
            title="Pause",
            description="Jeda aliran yang sedang diputar di video chat.",
            thumb_url="https://telegra.ph/file/9006f077e6596772e5864.jpg",
            input_message_content=InputTextMessageContent("/pause"),
        ),
        InlineQueryResultArticle(
            title="Resume",
            description="Lanjutkan aliran yang dijeda di video chat.",
            thumb_url="https://telegra.ph/file/9006f077e6596772e5864.jpg",
            input_message_content=InputTextMessageContent("/resume"),
        ),
        InlineQueryResultArticle(
            title="Skip",
            description="Lewati aliran yang sedang diputar di video chat dan pindah ke aliran berikutnya.",
            thumb_url="https://telegra.ph/file/9006f077e6596772e5864.jpg",
            input_message_content=InputTextMessageContent("/skip"),
        ),
        InlineQueryResultArticle(
            title="End",
            description="Akhiri aliran yang sedang diputar di video chat.",
            thumb_url="https://telegra.ph/file/9006f077e6596772e5864.jpg",
            input_message_content=InputTextMessageContent("/end"),
        ),
        InlineQueryResultArticle(
            title="Shuffle",
            description="Acak lagu-lagu yang ada di daftar putar.",
            thumb_url="https://telegra.ph/file/9006f077e6596772e5864.jpg",
            input_message_content=InputTextMessageContent("/shuffle"),
        ),
        InlineQueryResultArticle(
            title="Loop",
            description="Ulangi trek yang sedang diputar di video chat.",
            thumb_url="https://telegra.ph/file/9006f077e6596772e5864.jpg",
            input_message_content=InputTextMessageContent("/loop 3"),
        ),
    ]
)
