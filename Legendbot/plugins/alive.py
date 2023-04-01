import asyncio
import random
import re
import time
from datetime import datetime
from platform import python_version

from telethon import version
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery

from Legendbot import StartTime, legend, legendversion

from ..Config import Config
from ..core.managers import eor
from ..helpers.functions import check_data_base_heal_th, get_readable_time, legendalive
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import mention

menu_category = "utils"


@legend.legend_cmd(
    pattern="legend$",
    command=("legend", menu_category),
    info={
        "header": "To check bot's alive status",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}legend",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details"
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    legendevent = await eor(event, "`Checking...`")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    _, check_sgnirts = check_data_base_heal_th()
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT")
    EMOJI = gvarstatus("ALIVE_EMOJI") or "✥"
    lal = list(EMOJI.split())
    EMOTES = random.choice(lal)
    sweetie_caption = (
        "**💓 Anand Is Online 💓**\n\n" + f"{gvarstatus('ALIVE_TEMPLATE')}"
    )
    caption = sweetie_caption.format(
        ALIVE_TEXT=ALIVE_TEXT,
        EMOTES=EMOTES,
        mention=mention,
        uptime=uptime,
        telever=version.__version__,
        legendver=legendversion,
        pyver=python_version(),
        dbhealth=check_sgnirts,
        ping=ms,
    )
    try:
        results = await event.client.inline_query(Config.BOT_USERNAME, caption)
        await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
        await event.delete()
    except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
        return await eor(
            legendevent,
            f"**Media Value Error!!**\n__Change the link by __`.setdv`\n\n**__Can't get media from this link :-**__ `{LEGEND_IMG}`",
        )


"""
temp = {ALIVE_TEXT}
**{EMOTES} 𓆩𝙇𝙀𝙂𝙀𝙉𝘿 ♡ 𝘼-𝙆𝘼𝙔𓆪 :** {mention}
**{EMOTES} Stamina💦 :** `{uptime}`
"""


@legend.legend_cmd(
    pattern="alive$",
    command=("alive", menu_category),
    info={
        "header": "To check bot's alive status via inline mode",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details by your inline bot"
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    a = gvarstatus("ALIVE_EMOJI") or "✥"
    kiss = list(a.split())
    EMOJI = random.choice(kiss)
    legend_caption = "**💓 Anand Is Online 💓**\n\n"
    legend_caption += f"**{EMOJI} Stamina💦 :** {uptime}\n"
    legend_caption += f"**{EMOJI} 𓆩𝙇𝙀𝙂𝙀𝙉𝘿 ♡ 𝘼-𝙆𝘼𝙔𓆪 :** {mention}\n"
    results = await event.client.inline_query(Config.BOT_USERNAME, legend_caption)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


edit_time = 12
""" =======================CONSTANTS====================== """
file1 = "https://te.legra.ph/file/2426eab17330c6e6310ea.mp4"
file2 = "https://te.legra.ph/file/11ec9dd576ee5536125b2.jpg"
file3 = "https://te.legra.ph/file/d2a5265abdc4e73af1f94.jpg"
file4 = "https://telegra.ph/file/b6f0c65a337b1f2609d07.jpg"
file5 = "https://telegra.ph/file/af51de2749a4506d3eb43.jpg"
""" =======================CONSTANTS====================== """
pm_caption = f"**Anand Is Up**\n"
pm_caption += f"**╭────────────**\n"
pm_caption += f"┣»»»『{mention}』«««\n"
pm_caption += f"┣Lêɠêɳ̃dẞø† ~ {legendversion}\n"
pm_caption += f"┣Lêɠêɳ̃d  ~ [𓆩𝙇𝙀𝙂𝙀𝙉𝘿 ♡ 𝘼-𝙆𝘼𝙔𓆪](https://t.me/pandit_Andy)\n"
pm_caption += f"┣Support ~ [G𝖗ουρ](https://t.me/CHATTINGxGROUP)\n"
pm_caption += f"┣Řepô    ~ [Rєρο](https://graph.org/彡ᴋɪɴɢ-ᴀɴᴀɴᴅ彡-04-01)\n"
pm_caption += f"**╰────────────**\n"


@legend.legend_cmd(
    pattern="about$",
    command=("about", menu_category),
    info={
        "header": "To check bot's alive status ",
        "options": "Random Media Automatically Get It",
        "usage": [
            "{tr}about",
        ],
    },
)
async def amireallyalive(yes):
    await yes.get_chat()
    on = await borg.send_file(yes.chat_id, file=file1, caption=pm_caption)
    await asyncio.sleep(edit_time)
    ok = await borg.edit_message(yes.chat_id, on, file=file2)
    await asyncio.sleep(edit_time)
    ok2 = await borg.edit_message(yes.chat_id, ok, file=file3)

    await asyncio.sleep(edit_time)
    ok3 = await borg.edit_message(yes.chat_id, ok2, file=file4)

    await asyncio.sleep(edit_time)
    ok4 = await borg.edit_message(yes.chat_id, ok3, file=file5)

    await asyncio.sleep(edit_time)
    ok5 = await borg.edit_message(yes.chat_id, ok4, file=file4)

    await asyncio.sleep(edit_time)
    ok6 = await borg.edit_message(yes.chat_id, ok5, file=file3)

    await asyncio.sleep(edit_time)
    ok7 = await borg.edit_message(yes.chat_id, ok6, file=file2)

    await asyncio.sleep(edit_time)
    ok8 = await borg.edit_message(yes.chat_id, ok7, file=file1)

    await asyncio.sleep(edit_time)
    ok9 = await borg.edit_message(yes.chat_id, ok8, file=file2)

    await asyncio.sleep(edit_time)
    ok10 = await borg.edit_message(yes.chat_id, ok9, file=file3)

    await asyncio.sleep(edit_time)
    ok11 = await borg.edit_message(yes.chat_id, ok10, file=file4)

    await asyncio.sleep(edit_time)
    ok12 = await borg.edit_message(yes.chat_id, ok11, file=file5)

    await asyncio.sleep(edit_time)
    ok13 = await borg.edit_message(yes.chat_id, ok12, file=file1)

    await yes.delete()
    await borg.send_file(yes.chat_id, PM_IMG, caption=pm_caption)
    await yes.delete()


@legend.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await legendalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)
