"""
VideoPlayerBot, Telegram Video Chat Bot
Copyright (c) 2021  Asm Safone <https://github.com/AsmSafone>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import asyncio
from config import REPLY_MESSAGE
from pyrogram import Client, errors
from pyrogram.handlers import InlineQueryHandler
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from youtubesearchpython import VideosSearch


buttons = [
            [
                InlineKeyboardButton("قناه البوت🙋‍♂️", url="https://t.me/SE_MO_1"),
                InlineKeyboardButton("جروب الدعم🥵", url="https://t.me/SEMO658"),
            ],
            [
                InlineKeyboardButton("كـلم سسيمو المبرمج وهيعملك بوت خاص بك❤️", url="https://t.me/S_E_M_O_E_L_K_B_E_R"),
            ]
         ]

@Client.on_inline_query()
async def search(client, query):
    answers = []
    if query.query == "SAF_ONE":
        answers.append(
            InlineQueryResultArticle(
                title="لــو عااوز بوت كلم سيمو يحبي❤️",
                input_message_content=InputTextMessageContent(f"{REPLY_MESSAGE}\n\n<b>المبرمج❤️ : \n@S_E_M_O_E_L_K_B_E_R | @SEMO658 𖤐</b>", disable_web_page_preview=True),
                reply_markup=InlineKeyboardMarkup(buttons)
                )
            )
        await query.answer(results=answers, cache_time=0)
        return
    string = query.query.lower().strip().rstrip()
    if string == "":
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text=("✍️ اكــتــب اسـم الفـيـديو!"),
            switch_pm_parameter="help",
            cache_time=0
        )
    else:
        videosSearch = VideosSearch(string.lower(), limit=50)
        for v in videosSearch.result()["result"]:
            answers.append(
                InlineQueryResultArticle(
                    title=v["title"],
                    description=("Duration: {} Views: {}").format(
                        v["duration"],
                        v["viewCount"]["short"]
                    ),
                    input_message_content=InputTextMessageContent(
                        "/stream https://www.youtube.com/watch?v={}".format(
                            v["id"]
                        )
                    ),
                    thumb_url=v["thumbnails"][0]["url"]
                )
            )
        try:
            await query.answer(
                results=answers,
                cache_time=0
            )
        except errors.QueryIdInvalid:
            await query.answer(
                results=answers,
                cache_time=0,
                switch_pm_text=("❌ لم يتم العثور على نتائج!"),
                switch_pm_parameter="",
            )


__handlers__ = [
    [
        InlineQueryHandler(
            search
        )
    ]
]
