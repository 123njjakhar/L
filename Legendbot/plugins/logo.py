"""
Created by @Legend_K_Boy
#LegendUserBot
"""

import asyncio
import os
import random
import re
import urllib

import PIL
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from telethon.tl.types import InputMessagesFilterDocument, InputMessagesFilterPhotos

from Legendbot import legend

from ..core.managers import eod, eor
from ..helpers.functions import clippy
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import convert_toimage, mention, reply_id

# ======================================================================================================================================================================================

vars_list = {
    "lbg": "LOGO_BACKGROUND",
    "lfc": "LOGO_FONT_COLOR",
    "lfs": "LOGO_FONT_SIZE",
    "lfh": "LOGO_FONT_HEIGHT",
    "lfw": "LOGO_FONT_WIDTH",
    "lfsw": "LOGO_FONT_STROKE_WIDTH",
    "lfsc": "LOGO_FONT_STROKE_COLOR",
    "lf": "LOGO_FONT",
}

# ======================================================================================================================================================================================

menu_category = "useless"

PICS_STR = []


@legend.legend_cmd(
    pattern="(|s)logo(?: |$)([\s\S]*)",
    command=("logo", menu_category),
    info={
        "header": "Make a logo in image or sticker",
        "description": "Just a fun purpose plugin to create logo in image or in sticker.",
        "flags": {
            "s": "To create a logo in sticker instade of image.",
        },
        "usage": [
            "{tr}logo <text>",
            "{tr}slogo <text>",
            "{tr}ologo <text> <reply to image media only>",
        ],
        "examples": [
            "{tr}logo Legend",
            "{tr}slogo Legend",
            "{tr}ologo LegendBot",
        ],
    },
)
async def very(event):
    "To create a logo"
    cmd = event.pattern_match.group(1).lower()
    text = event.pattern_match.group(2)
    reply = await event.get_reply_message()
    if not text and reply:
        text = reply.text
    if not text:
        return await eod(event, "**ಠ∀ಠ Gimmi text to make logo**")
    reply_to_id = await reply_id(event)
    legendevent = await eor(event, "`Processing.....`")
    LOGO_FONT_SIZE = gvarstatus("LOGO_FONT_SIZE") or 220
    LOGO_FONT_WIDTH = gvarstatus("LOGO_FONT_WIDTH") or 2
    LOGO_FONT_HEIGHT = gvarstatus("LOGO_FONT_HEIGHT") or 2
    LOGO_FONT_COLOR = gvarstatus("LOGO_FONT_COLOR") or "red"
    LOGO_FONT_STROKE_WIDTH = gvarstatus("LOGO_FONT_STROKE_WIDTH") or 0
    LOGO_FONT_STROKE_COLOR = gvarstatus("LOGO_FONT_STROKE_COLOR") or None
    LOGO_BACKGROUND = (
        gvarstatus("LOGO_BACKGROUND")
        or "https://raw.githubusercontent.com/ITS-LEGENDBOT/RESOURCES/master/background/black.jpg"
    )
    LOGO_FONT = (
        gvarstatus("LOGO_FONT")
        or "https://github.com/ITS-LEGENDBOT/RESOURCES/blob/master/fonts/VampireWars.ttf?raw=true"
    )
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    if not os.path.exists("temp/bg_img.jpg"):
        urllib.request.urlretrieve(LOGO_BACKGROUND, "temp/bg_img.jpg")
    img = Image.open("./temp/bg_img.jpg")
    draw = ImageDraw.Draw(img)
    if not os.path.exists("temp/logo.ttf"):
        urllib.request.urlretrieve(LOGO_FONT, "temp/logo.ttf")
    font = ImageFont.truetype("temp/logo.ttf", int(LOGO_FONT_SIZE))
    image_widthz, image_heightz = img.size
    w, h = draw.textsize(text, font=font)
    h += int(h * 0.21)
    try:
        draw.text(
            (
                (image_widthz - w) / float(LOGO_FONT_WIDTH),
                (image_heightz - h) / float(LOGO_FONT_HEIGHT),
            ),
            text,
            font=font,
            fill=LOGO_FONT_COLOR,
            stroke_width=int(LOGO_FONT_STROKE_WIDTH),
            stroke_fill=LOGO_FONT_STROKE_COLOR,
        )
    except OSError:
        draw.text(
            (
                (image_widthz - w) / float(LOGO_FONT_WIDTH),
                (image_heightz - h) / float(LOGO_FONT_HEIGHT),
            ),
            text,
            font=font,
            fill=LOGO_FONT_COLOR,
            stroke_width=0,
            stroke_fill=None,
        )
    file_name = "PRO.png"
    img.save(file_name, "png")
    if cmd == "":
        await event.client.send_file(
            event.chat_id,
            file_name,
            reply_to=reply_to_id,
        )
    elif cmd == "s":
        await clippy(event.client, file_name, event.chat_id, reply_to_id)
    await legendevent.delete()
    if os.path.exists(file_name):
        os.remove(file_name)


@legend.legend_cmd(
    pattern="ologo(?: |$)([\s\S]*)",
    command=("ologo", menu_category),
    info={
        "header": "Make a logo in image or sticker",
        "description": "Just a fun purpose plugin to create logo in image or in sticker.",
        "usage": [
            "{tr}logo <text>",
            "{tr}slogo <text>",
            "{tr}ologo <text> <reply to image media only>",
        ],
        "examples": [
            "{tr}logo Legend",
        ],
    },
)
async def lg1(event):
    "To create a Random logo"
    event = await eor(event, "`Processing.....`")
    gvarstatus("LOGO_FONT_SIZE") or 220
    LOGO_FONT_WIDTH = gvarstatus("LOGO_FONT_WIDTH") or 2
    LOGO_FONT_HEIGHT = gvarstatus("LOGO_FONT_HEIGHT") or 2
    LOGO_FONT_COLOR = gvarstatus("LOGO_FONT_COLOR") or "black"
    LOGO_FONT_STROKE_WIDTH = gvarstatus("LOGO_FONT_STROKE_WIDTH") or 0
    LOGO_FONT_STROKE_COLOR = gvarstatus("LOGO_FONT_STROKE_COLOR") or None
    fnt = await get_font_file(event.client, "@Legend_Fonts")
    """
    cmd = event.pattern_match.group(1).lower()
    text = event.pattern_match.group(2)
    reply = await event.get_reply_message()
    if not text and reply:
        text = reply.text
    if not text:
        return await eod(event, "**ಠ∀ಠ Gimmi text to make logo**")
    """
    if event.reply_to_msg_id:
        rply = await event.get_reply_message()
        if rply.text:
            logo_ = rply.text
        else:
            logo_ = await rply.download_media()
    else:
        async for i in event.client.iter_messages(
            "@LegendBot_Logos", filter=InputMessagesFilterPhotos
        ):
            PICS_STR.append(i)
        pic = random.choice(PICS_STR)
        logo_ = await pic.download_media()
    text = event.pattern_match.group(1)
    if len(text) <= 8:
        font_size_ = 150
    elif len(text) >= 9:
        font_size_ = 50
    else:
        font_size_ = 130
    if not text:
        await eod(event, "**Give some text to make a logo !!**")
        return
    img = Image.open(logo_)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(fnt, font_size_)
    image_widthz, image_heightz = img.size
    w, h = draw.textsize(text, font=font)
    h += int(h * 0.21)
    image_width, image_height = img.size
    try:
        draw.text(
            (
                (image_widthz - w) / float(LOGO_FONT_WIDTH),
                (image_heightz - h) / float(LOGO_FONT_HEIGHT),
            ),
            text,
            font=font,
            fill=LOGO_FONT_COLOR,
            stroke_width=int(LOGO_FONT_STROKE_WIDTH),
            stroke_fill=LOGO_FONT_STROKE_COLOR,
        )
    except OSError:
        draw.text(
            (
                (image_widthz - w) / float(LOGO_FONT_WIDTH),
                (image_heightz - h) / float(LOGO_FONT_HEIGHT),
            ),
            text,
            font=font,
            fill=LOGO_FONT_COLOR,
            stroke_width=0,
            stroke_fill=None,
        )
    file_name = "LEGENDBOT.png"
    img.save(file_name, "png")
    await event.client.send_file(
        event.chat_id,
        file_name,
        caption=f"**Made By :** {mention}",
    )
    await event.delete()
    try:
        os.remove(file_name)
        os.remove(fnt)
        os.remove(logo_)
    except:
        pass


async def get_font_file(client, channel_id):
    font_file_message_s = await client.get_messages(
        entity=channel_id,
        filter=InputMessagesFilterDocument,
        limit=None,
    )
    font_file_message = random.choice(font_file_message_s)

    return await client.download_media(font_file_message)


@legend.legend_cmd(
    pattern="(|c)lbg(?:\s|$)([\s\S]*)",
    command=("lbg", menu_category),
    info={
        "header": "Change the background of logo",
        "description": "To change the background on which logo will created, in **bg** there few built-in backgrounds.",
        "flags": {
            "c": "Custom background for logo, can set by giving a telegraph link or reply to media.",
        },
        "usage": [
            "{tr}lbg <background color code>",
            "{tr}clbg <telegraph link / reply to media>",
        ],
        "examples": [
            "{tr}lbg red",
            "{tr}clbg https://telegra.ph/blablabla.jpg",
        ],
    },
)
async def bad(event):
    "To change background of logo"
    cmd = event.pattern_match.group(1).lower()
    input_str = event.pattern_match.group(2)
    source = requests.get(
        "https://github.com/ITS-LEGENDBOT/RESOURCES/tree/master/background"
    )
    soup = BeautifulSoup(source.text, features="html.parser")
    links = soup.find_all("a", class_="js-navigation-open Link--primary")
    bg_name = []
    lbg_list = "**Available background names are here:-**\n\n"
    for i, each in enumerate(links, start=1):
        owo = os.path.splitext(each.text)[0]
        bg_name.append(owo)
        lbg_list += f"**{i}.**  `{owo}`\n"
    if os.path.exists("./temp/bg_img.jpg"):
        os.remove("./temp/bg_img.jpg")
    if cmd == "c":
        reply_message = await event.get_reply_message()
        if not input_str and event.reply_to_msg_id and reply_message.media:
            if not os.path.isdir("./temp"):
                os.mkdir("./temp")
            output = await _legendtools.media_to_pic(event, reply_message)
            convert_toimage(output[1], filename="./temp/bg_img.jpg")
            return await eod(event, "This media is successfully set as background.")
        if not input_str.startswith("https://t"):
            return await eod(
                event, "Give a valid Telegraph picture link, Or reply to a media."
            )
        addgvar("LOGO_BACKGROUND", input_str)
        return await eod(event, f"**Background for logo changed to :-** `{input_str}`")
    if not input_str:
        return await eod(event, lbg_list, time=60)
    if input_str not in bg_name:
        legendevent = await eor(event, "`Give me a correct background name...`")
        await asyncio.sleep(1)
        await eod(legendevent, lbg_list, time=60)
    else:
        string = f"https://raw.githubusercontent.com/ITS-LEGENDBOT/RESOURCES/master/background/{input_str}.jpg"
        addgvar("LOGO_BACKGROUND", string)
        await eod(
            event, f"**Background for logo changed to :-** `{input_str}`", time=10
        )


@legend.legend_cmd(
    pattern="lf(|c|s|h|w|sc|sw)(?:\s|$)([\s\S]*)",
    command=("lf", menu_category),
    info={
        "header": "Change text style for logo.",
        "description": "Customise logo font, font size, font position like text hight or width.",
        "flags": {
            "c": "To change color of logo font.",
            "s": "To change size of logo font.",
            "h": "To change hight of logo font.",
            "w": "To change width of logo font.",
            "sw": "To change stroke width of logo font.",
            "sc": "To change stroke color of logo font.",
        },
        "usage": [
            "{tr}lf <font name>",
            "{tr}lfc <logo font color>",
            "{tr}lfs <1-1000>",
            "{tr}lfh <10-100>",
            "{tr}lfw <10-100>",
            "{tr}lfsw <10-100>",
            "{tr}lfsc <logo font stroke color>",
        ],
        "examples": [
            "{tr}lf genau-font.ttf",
            "{tr}lfc white",
            "{tr}lfs 120",
            "{tr}lfh 1",
            "{tr}lfw 8",
            "{tr}lfsw 5",
            "{tr}lfsc white",
        ],
    },
)
async def pussy(event):
    "To customise logo font"
    cmd = event.pattern_match.group(1).lower()
    input_str = event.pattern_match.group(2)
    if cmd == "":
        source = requests.get(
            "https://github.com/ITS-LEGENDBOT/RESOURCES/tree/master/fonts"
        )
        soup = BeautifulSoup(source.text, features="html.parser")
        links = soup.find_all("a", class_="js-navigation-open Link--primary")
        logo_font = []
        font_name = "**Available font names are here:-**\n\n"
        for i, each in enumerate(links, start=1):
            lol = os.path.splitext(each.text)[0]
            logo_font.append(lol)
            font_name += f"**{i}.**  `{lol}`\n"
        if not input_str:
            return await eod(event, font_name, time=80)
        if input_str not in logo_font:
            legendevent = await eor(event, "`Give me a correct font name...`")
            await asyncio.sleep(1)
            await eod(legendevent, font_name, time=80)
        else:
            if " " in input_str:
                input_str = str(input_str).replace(" ", "%20")
            string = f"https://github.com/ITS-LEGENDBOT/RESOURCES/blob/master/fonts/{input_str}.ttf?raw=true"
            if os.path.exists("temp/logo.ttf"):
                os.remove("temp/logo.ttf")
                urllib.request.urlretrieve(
                    string,
                    "temp/logo.ttf",
                )
            addgvar("LOGO_FONT", string)
            await eod(event, f"**Font for logo changed to :-** `{input_str}`", time=10)
    elif cmd in ["c", "sc"]:
        fg_name = []
        for name, code in PIL.ImageColor.colormap.items():
            fg_name.append(name)
            fg_list = str(fg_name).replace("'", "`")
        if not input_str:
            return await eod(
                event,
                f"**Available color names are here:-**\n\n{fg_list}",
                time=80,
            )
        if input_str not in fg_name:
            legendevent = await eor(event, "`Give me a correct color name...`")
            await asyncio.sleep(1)
            await eod(
                legendevent,
                f"**Available color names are here:-**\n\n{fg_list}",
                time=80,
            )
        elif cmd == "c":
            addgvar("LOGO_FONT_COLOR", input_str)
            await eod(
                event,
                f"**Foreground color for logo changed to :-** `{input_str}`",
                10,
            )
        else:
            addgvar("LOGO_FONT_STROKE_COLOR", input_str)
            await eod(
                event, f"**Stroke color for logo changed to :-** `{input_str}`", 10
            )
    else:
        legend = re.compile(r"^\-?[1-9][0-9]*\.?[0-9]*")
        isint = re.match(legend, input_str)
        if not input_str or not isint:
            return await eod(event, "**Give an integer value to set**", time=10)
        if cmd == "s":
            input_str = int(input_str)
            if input_str > 0 and input_str <= 1000:
                addgvar("LOGO_FONT_SIZE", input_str)
                await eod(event, f"**Font size is changed to :-** `{input_str}`")
            else:
                await eod(
                    event,
                    f"**Font size is between 0 - 1000, You can't set limit to :** `{input_str}`",
                )
        elif cmd == "w":
            input_str = float(input_str)
            if input_str > 0 and input_str <= 100:
                addgvar("LOGO_FONT_WIDTH", input_str)
                await eod(event, f"**Font width is changed to :-** `{input_str}`")
            else:
                await eod(
                    event,
                    f"**Font width is between 0 - 100, You can't set limit to {input_str}",
                )
        elif cmd == "h":
            input_str = float(input_str)
            if input_str > 0 and input_str <= 100:
                addgvar("LOGO_FONT_HEIGHT", input_str)
                await eod(event, f"**Font hight is changed to :-** `{input_str}`")
            else:
                await eod(
                    event,
                    f"**Font hight is between 0 - 100, You can't set limit to {input_str}",
                )
        elif cmd == "sw":
            input_str = int(input_str)
            if input_str > 0 and input_str <= 100:
                addgvar("LOGO_FONT_STROKE_WIDTH", input_str)
                await eod(
                    event, f"**Font stroke width is changed to :-** `{input_str}`"
                )
            else:
                await eod(
                    event,
                    f"**Font stroke width size is between 0 - 100, You can't set limit to :** `{input_str}`",
                )


@legend.legend_cmd(
    pattern="(g|d|r)lvar(?:\s|$)([\s\S]*)",
    command=("lvar", menu_category),
    info={
        "header": "Manage values which set for logo",
        "description": "To see which value have been set, or to delete a value , or to reset all values.",
        "flags": {
            "g": "Gets the value of the var which you set manually for logo.",
            "d": "Delete the value of the var which you set manually for logo.",
            "r": "Delete all the values of the vars which you set manually for logo & reset all changes.",
        },
        "usage": [
            "{tr}glvar <var code>",
            "{tr}dlvar <var code>",
            "{tr}rlvar",
        ],
        "examples": [
            "{tr}glvar lbg",
            "{tr}dlvar lfc",
        ],
    },
)
async def legend(event):
    "Manage all values of logo"
    cmd = event.pattern_match.group(1).lower()
    input_str = event.pattern_match.group(2)
    if input_str in vars_list.keys():
        var = vars_list[input_str]
        if cmd == "g":
            var_data = gvarstatus(var)
            await eod(event, f"📑 Value of **{var}** is  `{var_data}`", time=60)
        elif cmd == "d":
            if input_str == "lbg" and os.path.exists("./temp/bg_img.jpg"):
                os.remove("./temp/bg_img.jpg")
            if input_str == "lf" and os.path.exists("./temp/logo.ttf"):
                os.remove("./temp/logo.ttf")
            delgvar(var)
            await eod(
                event, f"📑 Value of **{var}** is now deleted & set to default.", time=60
            )
    elif not input_str and cmd == "r":
        delgvar("LOGO_BACKGROUND")
        delgvar("LOGO_FONT_COLOR")
        delgvar("LOGO_FONT")
        delgvar("LOGO_FONT_SIZE")
        delgvar("LOGO_FONT_HEIGHT")
        delgvar("LOGO_FONT_WIDTH")
        delgvar("LOGO_FONT_STROKE_COLOR")
        delgvar("LOGO_FONT_STROKE_WIDTH")
        if os.path.exists("./temp/bg_img.jpg"):
            os.remove("./temp/bg_img.jpg")
        if os.path.exists("./temp/logo.ttf"):
            os.remove("./temp/logo.ttf")
        await eod(
            event,
            "📑 Values for all vars deleted successfully & all settings reset.",
            time=20,
        )
    else:
        await eod(
            event,
            "**📑 Give correct vars name :**\n__Correct Vars code list is :__\n\n1. `lbg` : **LOGO_BACKGROUND**\n2. `lfc` : **LOGO_FONT_COLOR**\n3. `lf` : **LOGO_FONT**\n4. `lfs` : **LOGO_FONT_SIZE**\n5. `lfh` : **LOGO_FONT_HEIGHT**\n6. `lfw` : **LOGO_FONT_WIDTH**\n7. `lfsw` : **LOGO_FONT_STROKE_WIDTH**\n8. `lfsc` : **LOGO_FONT_STROKE_SCOLOUR**",
            time=60,
        )
