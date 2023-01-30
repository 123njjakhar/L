from googletrans import LANGUAGES, Translator

from Legendbot import legend

from ..core.managers import eod, eor
from ..helpers.functions.functions import getTranslate
from ..helpers.functions.utils import soft_deEmojify
from ..sql_helper.globals import addgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID

menu_category = "utils"


@legend.legend_cmd(
    pattern="tl ([\s\S]*)",
    command=("tl", menu_category),
    info={
        "header": "To translate the text to required language.",
        "note": "For langugage codes check [this link](https://da.gd/ueaQbH)",
        "usage": [
            "{tr}tl <language code> ; <text>",
            "{tr}tl <language codes>",
        ],
        "examples": "{tr}tl te ; Legenduserbot is one of the popular bot",
    },
)
async def _(event):
    "To translate the text."
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "en"
    elif ";" in input_str:
        lan, text = input_str.split(";")
    else:
        return await eod(event, "`.tl LanguageCode` as reply to a message", time=5)
    text = soft_deEmojify(text.strip())
    lan = lan.strip()
    Translator()
    try:
        translated = await getTranslate(text, dest=lan)
        after_tr_text = translated.text
        output_str = f"**TRANSLATED from {LANGUAGES[translated.src].title()} to {LANGUAGES[lan].title()}**\
                \n`{after_tr_text}`"
        await eor(event, output_str)
    except Exception as exc:
        await eod(event, f"**Error:**\n`{exc}`", time=5)


@legend.legend_cmd(
    pattern="trt(?: |$)([\s\S]*)",
    command=("trt", menu_category),
    info={
        "header": "To translate the text to required language.",
        "note": "for this command set lanuage by `{tr}lang trt <code name>` command.",
        "usage": [
            "{tr}trt",
            "{tr}trt <text>",
            "{tr}trt <lang> ; <text>",
        ],
    },
)
async def translateme(trans):
    "To translate the text to required language."
    textx = await trans.get_reply_message()
    message = trans.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        return await eor(trans, "`Give a text or reply to a message to translate!`")
    TRT_LANG = gvarstatus("TRT_LANG") or "en"
    try:
        reply_text = await getTranslate(soft_deEmojify(message), dest=TRT_LANG)
    except ValueError:
        return await eod(trans, "`Invalid destination language.`", time=5)
    source_lan = LANGUAGES[f"{reply_text.src.lower()}"]
    transl_lan = LANGUAGES[f"{reply_text.dest.lower()}"]
    reply_text = f"**From {source_lan.title()}({reply_text.src.lower()}) to {transl_lan.title()}({reply_text.dest.lower()}) :**\n`{reply_text.text}`"

    await eor(trans, reply_text)
    if BOTLOG:
        await trans.client.send_message(
            BOTLOG_CHATID,
            f"`Translated some {source_lan.title()} stuff to {transl_lan.title()} just now.`",
        )


@legend.legend_cmd(
    pattern="lang (ai|trt|tocr) ([\s\S]*)",
    command=("lang", menu_category),
    info={
        "header": "To set language for trt/ai command.",
        "description": "Check here [Language codes](https://da.gd/ueaQbH)",
        "options": {
            "trt": "default language for trt command",
            "tocr": "default language for tocr command",
            "ai": "default language for chatbot(ai)",
        },
        "usage": "{tr}lang option <language codes>",
        "examples": [
            "{tr}lang trt te",
            "{tr}lang tocr bn",
            "{tr}lang ai hi",
        ],
    },
)
async def lang(value):
    "To set language for trt comamnd."
    arg = value.pattern_match.group(2).lower()
    input_str = value.pattern_match.group(1)
    if arg not in LANGUAGES:
        return await eor(
            value,
            f"`Invalid Language code !!`\n`Available language codes for TRT`:\n\n`{LANGUAGES}`",
        )
    LANG = LANGUAGES[arg]
    if input_str == "trt":
        addgvar("TRT_LANG", arg)
        await eor(value, f"`Language for Translator changed to {LANG.title()}.`")
    elif input_str == "tocr":
        addgvar("TOCR_LANG", arg)
        await eor(value, f"`Language for Translated Ocr changed to {LANG.title()}.`")
    else:
        addgvar("AI_LANG", arg)
        await eor(value, f"`Language for chatbot is changed to {LANG.title()}.`")
    LANG = LANGUAGES[arg]

    if BOTLOG and input_str == "trt":
        await value.client.send_message(
            BOTLOG_CHATID, f"`Language for Translator changed to {LANG.title()}.`"
        )
    if BOTLOG:
        if input_str == "tocr":
            await value.client.send_message(
                BOTLOG_CHATID,
                f"`Language for Translated Ocr changed to {LANG.title()}.`",
            )
        if input_str == "ai":
            await value.client.send_message(
                BOTLOG_CHATID, f"`Language for chatbot is changed to {LANG.title()}.`"
            )
