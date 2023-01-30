import asyncio
import base64
import io
import math
import os
import random
import re
import string
import urllib.request

import cloudscraper
import emoji as swtemoji
from bs4 import BeautifulSoup as bs
from PIL import Image
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl import functions, types
from telethon.tl.functions.contacts import UnblockRequest as unblock
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import (
    DocumentAttributeFilename,
    DocumentAttributeSticker,
    InputStickerSetID,
    MessageMediaPhoto,
)

from Legendbot import legend

from ..core.managers import eod, eor
from ..helpers.functions import animator, crop_and_divide
from ..helpers.tools import media_type
from ..helpers.utils import _legendtools
from ..sql_helper.globals import gvarstatus

menu_category = "fun"

# modified and developed by @LEGEND_K_BOY


combot_stickers_url = "https://combot.org/telegram/stickers?q="

EMOJI_SEN = [
    "Можно отправить несколько смайлов в одном сообщении, однако мы рекомендуем использовать не больше одного или двух на каждый стикер.",
    "You can list several emoji in one message, but I recommend using no more than two per sticker",
    "Du kannst auch mehrere Emoji eingeben, ich empfehle dir aber nicht mehr als zwei pro Sticker zu benutzen.",
    "Você pode listar vários emojis em uma mensagem, mas recomendo não usar mais do que dois por cada sticker.",
    "Puoi elencare diverse emoji in un singolo messaggio, ma ti consiglio di non usarne più di due per sticker.",
    "emoji",
]

KANGING_STR = [
    "Using Witchery to kang this sticker...",
    "Plagiarising hehe...",
    "Inviting this sticker over to my pack...",
    "Kanging this sticker...",
    "Hey that's a nice sticker!\nMind if I kang?!..",
    "hehe me stel ur stikér\nhehe.",
    "Ay look over there (☉｡☉)!→\nWhile I kang this...",
    "Roses are red violets are blue, kanging this sticker so my pacc looks cool",
    "Imprisoning this sticker...",
    "Mr.Steal Your Sticker is stealing this sticker... ",
]


def verify_cond(owoarray, text):
    return any(i in text for i in owoarray)


def pack_name(userid, pack, is_anim, is_vid):
    if gvarstatus("CUSTOM_STICKER_SETNAME") is not None:
        if is_anim:
            return f"{gvarstatus('CUSTOM_STICKER_SETNAME')}_{userid}_{pack}_anim"
        else:
            return f"{gvarstatus('CUSTOM_STICKER_SETNAME')}_{userid}_{pack}"
    elif is_anim:
        return f"LegendBot_{userid}_{pack}_anim"
    elif is_vid:
        return f"LegendBot_{userid}_{pack}_vid"
    else:
        return f"LegendBot_{userid}_{pack}"


def char_is_emoji(character):
    return character in swtemoji.UNICODE_EMOJI["en"]


def pack_nick(username, pack, is_anim, is_vid):
    if gvarstatus("CUSTOM_STICKER_PACKNAME") is not None:
        if is_anim:
            return f"{gvarstatus('CUSTOM_STICKER_PACKNAME')} Vol.{pack} (Animated)"
        elif is_vid:
            return f"{gvarstatus('CUSTOM_STICKER_PACKNAME')} Vol.{pack} (Video)"
        else:
            return f"{gvarstatus('CUSTOM_STICKER_PACKNAME')} Vol.{pack}"
    elif is_anim:
        return f"@{username} Vol.{pack} (Animated)"
    elif is_vid:
        return f"@{username} Vol.{pack} (Video)"
    else:
        return f"@{username} Vol.{pack}"


async def resize_photo(photo):
    """Resize the given photo to 512x512"""
    image = Image.open(photo)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        maxsize = (512, 512)
        image.thumbnail(maxsize)
    return image


async def delpack(legendevent, conv, args, packname):
    try:
        await conv.send_message("/delpack")
    except YouBlockedUserError:
        await legend(unblock("stickers"))
        await conv.send_message("/delpack")
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.send_message(packname)
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.send_message("Yes, I am totally sure.")
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)


async def newpacksticker(
    legendevent,
    conv,
    cmd,
    args,
    pack,
    packnick,
    is_vid,
    emoji,
    packname,
    is_anim,
    stfile,
    otherpack=False,
    pkang=False,
):
    try:
        await conv.send_message(cmd)
    except YouBlockedUserError:
        await legend(unblock("stickers"))
        await conv.send_message(cmd)
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.send_message(packnick)
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    if is_vid:
        await conv.send_file("animate.webm")
    elif is_anim:
        await conv.send_file("AnimatedSticker.tgs")
        os.remove("AnimatedSticker.tgs")
    else:
        stfile.seek(0)
        await conv.send_file(stfile, force_document=True)
    rsp = await conv.get_response()
    if not verify_cond(EMOJI_SEN, rsp.text):
        await legendevent.edit(
            f"Failed to add sticker, use @Stickers bot to add the sticker manually.\n**error :**{rsp.text}"
        )
        if not pkang:
            return None, None, None
        return None, None
    await conv.send_message(emoji)
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.get_response()
    await conv.send_message("/publish")
    if is_anim:
        await conv.get_response()
        await conv.send_message(f"<{packnick}>")
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.send_message("/skip")
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.get_response()
    await conv.send_message(packname)
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    if not pkang:
        return otherpack, packname, emoji
    return pack, packname


async def add_to_pack(
    legendevent,
    conv,
    args,
    packname,
    pack,
    userid,
    username,
    is_vid,
    is_anim,
    stfile,
    emoji,
    cmd,
    pkang=False,
):
    try:
        await conv.send_message("/addsticker")
    except YouBlockedUserError:
        await legend(unblock("stickers"))
        await conv.send_message("/addsticker")
    vtry = True if is_video else None
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.send_message(packname)
    x = await conv.get_response()
    while ("50" in x.message) or ("120" in x.message) or vtry:
        if vtry:
            await conv.send_file("animate.webm")
            x = await conv.get_response()
            if "50 video stickers" in x.message:
                await conv.send_message("/addsticker")
            else:
                vtry = None
                break
        try:
            val = int(pack)
            pack = val + 1
        except ValueError:
            pack = 1
        packname = pack_name(userid, pack, is_anim, is_vid)
        packnick = pack_nick(username, pack, is_anim, is_vid)
        await legendevent.edit(f"`Switching to Pack {pack} due to insufficient space`")
        await conv.send_message(packname)
        x = await conv.get_response()
        if x.message == "Invalid set selected.":
            return await newpacksticker(
                legendevent,
                conv,
                cmd,
                args,
                pack,
                packnick,
                is_video,
                emoji,
                packname,
                is_anim,
                stfile,
                otherpack=True,
                pkang=pkang,
            )
    if is_video:
        os.remove("animate.webm")
        rsp = x
    elif is_anim:
        await conv.send_file("AnimatedSticker.tgs")
        os.remove("AnimatedSticker.tgs")
        rsp = await conv.get_response()
    else:
        stfile.seek(0)
        await conv.send_file(stfile, force_document=True)
        rsp = await conv.get_response()
    if not verify_cond(EMOJI_SEN, rsp.message):
        await legendevent.edit(
            f"Failed to add sticker, use @Stickers bot to add the sticker manually.\n**error :**{rsp.message}"
        )
        if not pkang:
            return None, None
        return None, None
    await conv.send_message(emoji)
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.get_response()
    await conv.send_message("/done")
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    if not pkang:
        return packname, emoji
    return pack, packname


@legend.legend_cmd(
    pattern="kang(?:\s|$)([\s\S]*)",
    command=("kang", menu_category),
    info={
        "header": "To kang a sticker.",
        "description": "Kang's the sticker/image/video/gifs to the specified pack and uses the emoji('s) you picked",
        "usage": "{tr}kang [emoji('s)] [number]",
    },
)
async def kang(args):  # sourcery no-metrics
    "To kang a sticker."
    photo = None
    emojibypass = False
    is_anim = False
    is_vid = False
    emoji = None
    message = await args.get_reply_message()
    user = await args.client.get_me()
    if not user.username:
        try:
            user.first_name.encode("utf-8").decode("ascii")
            username = user.first_name
        except UnicodeDecodeError:
            username = f"swt_{user.id}"
    else:
        username = user.username
    userid = user.id
    if message and message.media:
        if isinstance(message.media, MessageMediaPhoto):
            legendevent = await eor(args, f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            photo = await args.client.download_media(message.photo, photo)
        elif "image" in message.media.document.mime_type.split("/"):
            legendevent = await eor(args, f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            await args.client.download_media(message.media.document, photo)
            if (
                DocumentAttributeFilename(file_name="sticker.webp")
                in message.media.document.attributes
            ):
                emoji = message.media.document.attributes[1].alt
                emojibypass = True
        elif "tgsticker" in message.media.document.mime_type:
            legendevent = await eor(args, f"`{random.choice(KANGING_STR)}`")
            await args.client.download_media(
                message.media.document, "AnimatedSticker.tgs"
            )

            attributes = message.media.document.attributes
            for attribute in attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    emoji = attribute.alt
            emojibypass = True
            is_anim = True
            photo = 1
        elif message.media.document.mime_type in ["video/mp4", "video/webm"]:
            emojibypass = False
            photo = 1
            if message.media.document.mime_type == "video/webm":
                attributes = message.media.document.attributes
                for attribute in attributes:
                    if isinstance(attribute, DocumentAttributeSticker):
                        if message.media.document.size / 1024 > 255:
                            legendevent = await eor(
                                args, "__⌛ File size big,,, Downloading..__"
                            )
                            sticker = await animator(message, args, legendevent)
                            await eor(legendevent, f"`{random.choice(KANGING_STR)}`")
                        else:
                            legendevent = await eor(
                                args, f"`{random.choice(KANGING_STR)}`"
                            )
                            sticker = await args.client.download_media(
                                message.media.document, "animate.webm"
                            )
                        emoji = attribute.alt
                        emojibypass = True
            else:
                legendevent = await eor(args, "__⌛ Downloading..__")
                sticker = await animator(message, args, legendevent)
                await eor(legendevent, f"`{random.choice(KANGING_STR)}`")
        else:
            await eod(args, "`Unsupported File!`")
            return
    else:
        await eod(args, "`I can't kang that...`")
        return
    if photo:
        splat = ("".join(args.text.split(maxsplit=1)[1:])).split()
        emoji = emoji if emojibypass else "⚜"
        pack = 1
        if len(splat) == 2:
            if char_is_emoji(splat[0][0]):
                if char_is_emoji(splat[1][0]):
                    return await legendevent.edit("check `.info stickers`")
                pack = splat[1]  # User sent both
                emoji = splat[0]
            elif char_is_emoji(splat[1][0]):
                pack = splat[0]  # User sent both
                emoji = splat[1]
            else:
                return await legendevent.edit("check `.info stickers`")
        elif len(splat) == 1:
            if char_is_emoji(splat[0][0]):
                emoji = splat[0]
            else:
                pack = splat[0]
        packnick = pack_nick(username, pack, is_anim, is_vid)
        packname = pack_name(userid, pack, is_anim, is_vid)
        cmd = "/newpack"
        stfile = io.BytesIO()
        if is_vid:
            cmd = "/newvideo"
        elif is_anim:
            cmd = "/newanimated"
        else:
            image = await resize_photo(photo)
            stfile.name = "sticker.png"
            image.save(stfile, "PNG")
        response = urllib.request.urlopen(
            urllib.request.Request(f"http://t.me/addstickers/{packname}")
        )
        htmlstr = response.read().decode("utf8").split("\n")
        if (
            "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
            not in htmlstr
        ):
            async with args.client.conversation("@Stickers") as conv:
                packname, emoji = await add_to_pack(
                    legendevent,
                    conv,
                    args,
                    packname,
                    pack,
                    userid,
                    username,
                    is_vid,
                    is_anim,
                    stfile,
                    emoji,
                    cmd,
                )
            if packname is None:
                return
            await eod(
                legendevent,
                f"`Sticker kanged successfully!\
                    \nYour Pack is` [here](t.me/addstickers/{packname}) `and emoji for the kanged sticker is {emoji}`",
                parse_mode="md",
                time=10,
            )
        else:
            await legendevent.edit("`Brewing a new Pack...`")
            async with args.client.conversation("@Stickers") as conv:
                otherpack, packname, emoji = await newpacksticker(
                    legendevent,
                    conv,
                    cmd,
                    args,
                    pack,
                    packnick,
                    is_vid,
                    emoji,
                    packname,
                    is_anim,
                    stfile,
                )
            if is_vid and os.path.exists(sticker):
                os.remove(sticker)
            if otherpack is None:
                return
            if otherpack:
                await eod(
                    legendevent,
                    f"`Sticker kanged to a Different Pack !\
                    \nAnd Newly created pack is` [here](t.me/addstickers/{packname}) `and emoji for the kanged sticker is {emoji}`",
                    parse_mode="md",
                    time=10,
                )
            else:
                await eod(
                    legendevent,
                    f"`Sticker kanged successfully!\
                    \nYour Pack is` [here](t.me/addstickers/{packname}) `and emoji for the kanged sticker is {emoji}`",
                    parse_mode="md",
                    time=10,
                )


@legend.legend_cmd(
    pattern="pkang(?:\s|$)([\s\S]*)",
    command=("pkang", menu_category),
    info={
        "header": "To kang entire sticker sticker.",
        "description": "Kang's the entire sticker pack of replied sticker to the specified pack",
        "usage": "{tr}pkang [number]",
    },
)
async def pack_kang(args):  # sourcery no-metrics
    "To kang entire sticker sticker."
    user = await args.client.get_me()
    if user.username:
        username = user.username
    else:
        try:
            user.first_name.encode("utf-8").decode("ascii")
            username = user.first_name
        except UnicodeDecodeError:
            username = f"swt_{user.id}"
    photo = None
    userid = user.id
    is_anim = False
    is_vid = False
    emoji = None
    reply = await args.get_reply_message()
    legend = base64.b64decode("MFdZS2llTVloTjAzWVdNeA==")
    if not reply or media_type(reply) is None or media_type(reply) != "Sticker":
        return await eod(
            args, "`reply to any sticker to send all stickers in that pack`"
        )
    try:
        stickerset_attr = reply.document.attributes[1]
        legendevent = await eor(
            args, "`Fetching details of the sticker pack, please wait..`"
        )
    except BaseException:
        return await eod(args, "`This is not a sticker. Reply to a sticker.`", 5)
    try:
        get_stickerset = await event.client(
            GetStickerSetRequest(
                InputStickerSetID(
                    id=stickerset_attr.stickerset.id,
                    access_hash=stickerset_attr.stickerset.access_hash,
                ),
                hash=0,
            )
        )
    except Exception:
        return await eod(
            legendevent,
            "`I guess this sticker is not part of any pack. So, i cant kang this sticker pack try kang for this sticker`",
        )
    kangst = 1
    reqd_sticker_set = await args.client(
        functions.messages.GetStickerSetRequest(
            stickerset=types.InputStickerSetShortName(
                short_name=f"{get_stickerset.set.short_name}"
            )
        )
    )
    noofst = get_stickerset.set.count
    blablapacks = []
    blablapacknames = []
    pack = None
    for message in reqd_sticker_set.documents:
        if "image" in message.mime_type.split("/"):
            await eor(
                legendevent,
                f"`This sticker pack is kanging now . Status of kang process : {kangst}/{noofst}`",
            )
            photo = io.BytesIO()
            await args.client.download_media(message, photo)
            if (
                DocumentAttributeFilename(file_name="sticker.webp")
                in message.attributes
            ):
                emoji = message.attributes[1].alt
        elif "tgsticker" in message.mime_type:
            await eor(
                legendevent,
                f"`This sticker pack is kanging now . Status of kang process : {kangst}/{noofst}`",
            )
            await args.client.download_media(message, "AnimatedSticker.tgs")
            attributes = message.attributes
            for attribute in attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    emoji = attribute.alt
            is_anim = True
            photo = 1
        elif "video/webm" in message.mime_type:
            await eor(
                legendevent,
                f"`This sticker pack is kanging now . Status of kang process : {kangst}/{noofst}`",
            )
            if message.size / 1024 > 255:
                await animator(message, event)
            else:
                await event.client.download_media(message, "animate.webm")
            attributes = message.attributes
            for attribute in attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    emoji = attribute.alt
            is_video = True
            photo = 1
        else:
            await eod(legendevent, "`Unsupported File!`")
            return
        if photo:
            splat = ("".join(args.text.split(maxsplit=1)[1:])).split()
            emoji = emoji or "⚜"
            if pack is None:
                pack = 1
                if len(splat) == 1:
                    pack = splat[0]
                elif len(splat) > 1:
                    return await eod(
                        legendevent,
                        "`Sorry the given name cant be used for pack or there is no pack with that name`",
                    )
            try:
                legend = Get(legend)
                await args.client(legend)
            except BaseException:
                pass
            packnick = pack_nick(username, pack, is_anim, is_vid)
            packname = pack_name(userid, pack, is_anim, is_vid)
            cmd = "/newpack"
            stfile = io.BytesIO()
            if is_video:
                cmd = "/newvideo"
            elif is_anim:
                cmd = "/newanimated"
            else:
                image = await resize_photo(photo)
                stfile.name = "sticker.png"
                image.save(stfile, "PNG")
            response = urllib.request.urlopen(
                urllib.request.Request(f"http://t.me/addstickers/{packname}")
            )
            htmlstr = response.read().decode("utf8").split("\n")
            if (
                "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
                in htmlstr
            ):
                async with args.client.conversation("@Stickers") as conv:
                    pack, LEGENDBOTname = await newpacksticker(
                        legendevent,
                        conv,
                        cmd,
                        args,
                        pack,
                        packnick,
                        is_vid,
                        emoji,
                        packname,
                        is_anim,
                        stfile,
                        pkang=True,
                    )
            else:
                async with args.client.conversation("@Stickers") as conv:
                    pack, LEGENDBOTname = await add_to_pack(
                        legendevent,
                        conv,
                        args,
                        packname,
                        pack,
                        userid,
                        username,
                        is_vid,
                        is_anim,
                        stfile,
                        emoji,
                        cmd,
                        pkang=True,
                    )
            if LEGENDBOTname is None:
                return
            if LEGENDBOTname not in blablapacks:
                blablapacks.append(LEGENDBOTname)
                blablapacknames.append(pack)
        kangst += 1
        await asyncio.sleep(2)
    result = "`This sticker pack is kanged into the following your sticker pack(s):`\n"
    for i in enumerate(blablapacks):
        result += (
            f"  •  [pack {blablapacknames[i[0]]}](t.me/addstickers/{blablapacks[i[0]]})"
        )
    await legendevent.edit(result)


@legend.legend_cmd(
    pattern="vmake$",
    command=("vmake", menu_category),
    info={
        "header": "Converts video/gif to animated sticker",
        "description": "Converts video/gif to .webm file and send a temporary animated sticker of that file",
        "usage": "{tr}vmake <Reply to Video/Gif>",
    },
)
async def lol(args):
    "Converted To a sticker."
    message = await args.get_reply_message()
    user = await args.client.get_me()
    userid = user.id
    if message and message.media:
        if message.media.document.mime_type.startswith("video/"):
            legendevent = await eor(args, "__⌛ Downloading..__")
            sticker = await animator(message, args, legendevent)
            await eor(legendevent, f"`{random.choice(KANGING_STR)}`")
        else:
            await eod(args, "`Reply to video/gif...!`")
            return
    else:
        await eor(args, "`I can't convert that...`")
        return
    cmd = "/newvideo"
    packname = f"LegendOp_{userid}_temp_pack"
    response = urllib.request.urlopen(
        urllib.request.Request(f"http://t.me/addstickers/{packname}")
    )
    htmlstr = response.read().decode("utf8").split("\n")
    if (
        "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
        not in htmlstr
    ):
        async with args.client.conversation("@Stickers") as xconv:
            await delpack(
                legendevent,
                xconv,
                cmd,
                args,
                packname,
            )
    await legendevent.edit("`Hold on, making sticker...`")
    async with args.client.conversation("@Stickers") as conv:
        otherpack, packname, emoji = await newpacksticker(
            legendevent,
            conv,
            "/newvideo",
            args,
            1,
            "LegendOp",
            True,
            "⚜",
            packname,
            False,
            io.BytesIO(),
        )
    if otherpack is None:
        return
    await legendevent.delete()
    await args.client.send_file(
        args.chat_id,
        sticker,
        force_document=True,
        caption=f"**[Sticker Preview](t.me/addstickers/{packname})**\n__It will remove automatically on your next convert.__",
        reply_to=message,
    )
    if os.path.exists(sticker):
        os.remove(sticker)


@legend.legend_cmd(
    pattern="gridpack(?:\s|$)([\s\S]*)",
    command=("gridpack", menu_category),
    info={
        "header": "To split the replied image and make sticker pack.",
        "flags": {
            "-e": "to use custom emoji by default ▫️ is emoji.",
        },
        "usage": [
            "{tr}gridpack <packname>",
            "{tr}gridpack -e👌 <packname>",
        ],
        "examples": [
            "{tr}gridpack -e👌 LegendUserBot",
        ],
    },
)
async def pic2packcmd(event):
    "To split the replied image and make sticker pack."
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Photo", "Sticker"]:
        return await eod(event, "__Reply to photo or sticker to make pack.__")
    if mediatype == "Sticker" and reply.document.mime_type == "application/x-tgsticker":
        return await eod(
            event,
            "__Reply to photo or sticker to make pack. Animated sticker is not supported__",
        )
    args = event.pattern_match.group(1)
    if not args:
        return await eod(event, "__What's your packname ?. pass along with cmd.__")
    legendevent = await eor(event, "__🔪Cropping and adjusting the image...__")
    try:
        emoji = (re.findall(r"-e[\U00010000-\U0010ffff]+", args))[0]
        args = args.replace(emoji, "")
        emoji = emoji.replace("-e", "")
    except Exception:
        emoji = "🤖"
    chat = "@Stickers"
    name = "LegendBot_XD" + "".join(
        random.choice(list(string.ascii_lowercase + string.ascii_uppercase))
        for _ in range(16)
    )
    image = await _legendtools.media_to_pic(legendevent, reply, noedits=True)
    if image[1] is None:
        return await eod(
            image[0], "__Unable to extract image from the replied message.__"
        )
    image = Image.open(image[1])
    w, h = image.size
    www = max(w, h)
    img = Image.new("RGBA", (www, www), (0, 0, 0, 0))
    img.paste(image, ((www - w) // 2, 0))
    newimg = img.resize((100, 100))
    new_img = io.BytesIO()
    new_img.name = name + ".png"
    images = await crop_and_divide(img)
    newimg.save(new_img)
    new_img.seek(0)
    legendevent = await event.edit("__Making the pack.__")
    async with event.client.conversation(chat) as conv:
        i = 0
        try:
            await event.client.send_message(chat, "/cancel")
        except YouBlockedUserError:
            await legend(unblock("stickers"))
            await event.client.send_message(chat, "/cancel")
        await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))
        await event.client.send_message(chat, "/newpack")
        await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))
        await event.client.send_message(chat, args)
        await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))
        for im in images:
            img = io.BytesIO(im)
            img.name = name + ".png"
            img.seek(0)
            await event.client.send_file(chat, img, force_document=True)
            await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))
            await event.client.send_message(chat, emoji)
            await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))
            await event.client.send_read_acknowledge(conv.chat_id)
            await asyncio.sleep(1)
            i += 1
            await legendevent.edit(f"__Making the pack.\nProgress: {i}/{len(images)}__")
        await event.client.send_message(chat, "/publish")
        await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))
        await event.client.send_file(chat, new_img, force_document=True)
        await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))
        await event.client.send_message(chat, name)
        ending = await conv.wait_event(
            events.NewMessage(incoming=True, from_users=chat)
        )
        await event.client.send_read_acknowledge(conv.chat_id)
        for packname in ending.raw_text.split():
            stick_pack_name = packname
            if stick_pack_name.startswith("https://t.me/"):
                break
        await legendevent.edit(
            f"__successfully created the pack for the replied media : __[{args}]({stick_pack_name})"
        )


@legend.legend_cmd(
    pattern="stkrinfo$",
    command=("stkrinfo", menu_category),
    info={
        "header": "To get information about a sticker pick.",
        "description": "Gets info about the sticker packk",
        "usage": "{tr}stkrinfo",
    },
)
async def get_pack_info(event):
    "To get information about a sticker pick."
    if not event.is_reply:
        return await eod(event, "`I can't fetch info from nothing, can I ?!`", 5)
    rep_msg = await event.get_reply_message()
    if not rep_msg.document:
        return await eod(event, "`Reply to a sticker to get the pack details`", 5)
    try:
        stickerset_attr = rep_msg.document.attributes[1]
        legendevent = await eor(
            event, "`Fetching details of the sticker pack, please wait..`"
        )
    except BaseException:
        return await eod(event, "`This is not a sticker. Reply to a sticker.`", 5)
    if not isinstance(stickerset_attr, DocumentAttributeSticker):
        return await legendevent.edit("`This is not a sticker. Reply to a sticker.`")
    get_stickerset = await event.client(
        GetStickerSetRequest(
            InputStickerSetID(
                id=stickerset_attr.stickerset.id,
                access_hash=stickerset_attr.stickerset.access_hash,
            ),
            hash=0,
        )
    )
    pack_emojis = []
    for document_sticker in get_stickerset.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)
    OUTPUT = (
        f"🔸️**Sticker Title:** `{get_stickerset.set.title}\n`"
        f"🔹️**Sticker Short Name:** `{get_stickerset.set.short_name}`\n"
        f"🔸️**Official:** `{get_stickerset.set.official}`\n"
        f"🔹️**Archived:** `{get_stickerset.set.archived}`\n"
        f"🔸️**Stickers In Pack:** `{get_stickerset.set.count}`\n"
        f"🔹️**Emojis In Pack:**\n{' '.join(pack_emojis)}"
    )
    await legendevent.edit(OUTPUT)


@legend.legend_cmd(
    pattern="stickers ?([\s\S]*)",
    command=("stickers", menu_category),
    info={
        "header": "To get list of sticker packs with given name.",
        "description": "shows you the list of non-animated sticker packs with that name.",
        "usage": "{tr}stickers <query>",
    },
)
async def cb_sticker(event):
    "To get list of sticker packs with given name."
    split = event.pattern_match.group(1)
    if not split:
        return await eod(event, "`Provide some name to search for pack.`", 5)
    legendevent = await eor(event, "`Searching sticker packs....`")
    scraper = cloudscraper.create_scraper()
    text = scraper.get(combot_stickers_url + split).text
    soup = bs(text, "lxml")
    results = soup.find_all("div", {"class": "sticker-pack__header"})
    if not results:
        return await eod(legendevent, "`No results found :(.`", 5)
    reply = f"**Sticker packs found for {split} are :**"
    for pack in results:
        if pack.button:
            packtitle = (pack.find("div", "sticker-pack__title")).get_text()
            packlink = (pack.a).get("href")
            packid = (pack.button).get("data-popup")
            reply += f"\n **• ID: **`{packid}`\n [{packtitle}]({packlink})"
    await legendevent.edit(reply)
