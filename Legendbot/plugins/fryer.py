import io
import os
from random import randint, uniform

from PIL import Image, ImageEnhance, ImageOps
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import DocumentAttributeFilename

from Legendbot import legend

from ..core.managers import eod, eor
from ..helpers.functions import delete_conv
from ..helpers.utils import media_to_pic, reply_id

menu_category = "extra"


async def deepfry(img: Image) -> Image:
    colours = (
        (randint(50, 200), randint(40, 170), randint(40, 190)),
        (randint(190, 255), randint(170, 240), randint(180, 250)),
    )
    img = img.copy().convert("RGB")
    # Crush image to hell and back
    img = img.convert("RGB")
    width, height = img.width, img.height
    img = img.resize(
        (int(width ** uniform(0.8, 0.9)), int(height ** uniform(0.8, 0.9))),
        resample=Image.LANCZOS,
    )
    img = img.resize(
        (int(width ** uniform(0.85, 0.95)), int(height ** uniform(0.85, 0.95))),
        resample=Image.BILINEAR,
    )
    img = img.resize(
        (int(width ** uniform(0.89, 0.98)), int(height ** uniform(0.89, 0.98))),
        resample=Image.BICUBIC,
    )
    img = img.resize((width, height), resample=Image.BICUBIC)
    img = ImageOps.posterize(img, randint(3, 7))
    # Generate colour overlay
    overlay = img.split()[0]
    overlay = ImageEnhance.Contrast(overlay).enhance(uniform(1.0, 2.0))
    overlay = ImageEnhance.Brightness(overlay).enhance(uniform(1.0, 2.0))
    overlay = ImageOps.colorize(overlay, colours[0], colours[1])
    # Overlay red and yellow onto main image and sharpen the hell out of it
    img = Image.blend(img, overlay, uniform(0.1, 0.4))
    img = ImageEnhance.Sharpness(img).enhance(randint(5, 300))
    return img


async def check_media(reply_message):
    if reply_message and reply_message.media:
        if reply_message.photo:
            data = reply_message.photo
        elif reply_message.document:
            if (
                DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
                in reply_message.media.document.attributes
            ):
                return False
            if (
                reply_message.gif
                or reply_message.video
                or reply_message.audio
                or reply_message.voice
            ):
                return False
            data = reply_message.media.document
        else:
            return False
    if not data or data is None:
        return False
    return data


@legend.legend_cmd(
    pattern="frybot",
    command=("frybot", menu_category),
    info={
        "header": "Fries the given sticker or image.",
        "usage": "{tr}frybot",
    },
)
async def frybot(event):
    "Fries the given sticker or image"
    reply_to = await reply_id(event)
    if not event.reply_to_msg_id:
        event = await eod(event, "Reply to any user message.")
    output = await media_to_pic(event, reply_message)
    if output[1] is None:
        return await eod(
            output[0], "__Unable to extract image from the replied message.__", 10
        )
    chat = "@image_deepfrybot"
    lolevent = await eor(event, "```Processing...```")
    async with event.client.conversation(chat) as conv:
        try:
            msg_flag = await conv.send_message("/start")
        except YouBlockedUserError:
            await eor(lolevent, "**Error:** Trying to unblock & retry, wait a sec...")
            await legend(unblock("image_deepfrybot"))
            msg_flag = await conv.send_message("/start")
        await conv.get_response()
        await event.client.send_read_acknowledge(conv.chat_id)
        await event.client.send_file(conv.chat_id, output[1])
        response = await conv.get_response()
        await event.client.send_read_acknowledge(conv.chat_id)
        await lolevent.delete()
        await event.client.send_file(event.chat_id, response, reply_to=reply_to)
        await delete_conv(event, chat, msg_flag)
        os.remove(output[1])


@legend.legend_cmd(
    pattern="deepfry(?: |$)([1-9])?",
    command=("deepfry", menu_category),
    info={
        "header": "image fryer",
        "description": "Fries the given sticker or image based on level if you dont give anything then it is default to 1",
        "usage": [
            "{tr}deepfry <1 to 9>",
            "{tr}deepfry",
        ],
    },
)
async def deepfryer(event):
    "image fryer"
    reply_to = await reply_id(event)
    input_str = event.pattern_match.group(1)
    frycount = int(input_str) if input_str else 1
    if event.is_reply:
        reply_message = await event.get_reply_message()
        data = await check_media(reply_message)
        if isinstance(data, bool):
            return await eor(event, "`I can't deep fry that!`")
    if not event.is_reply:
        return await eor(event, "`Reply to an image or sticker to deep fry it!`")
    # download last photo (highres) as byte array
    image = io.BytesIO()
    await event.client.download_media(data, image)
    image = Image.open(image)
    # fry the image
    hmm = await eor(event, "`Deep frying media…`")
    for _ in range(frycount):
        image = await deepfry(image)
    fried_io = io.BytesIO()
    fried_io.name = "image.jpeg"
    image.save(fried_io, "JPEG")
    fried_io.seek(0)
    await event.client.send_file(event.chat_id, fried_io, reply_to=reply_to)
    await hmm.delete()
