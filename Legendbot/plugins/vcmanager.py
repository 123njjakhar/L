from telethon import functions
from telethon.errors import ChatAdminRequiredError, UserAlreadyInvitedError
from telethon.tl.types import Channel, Chat, User

from Legendbot import legend
from Legendbot.bot.core.managers import eod, eor
from Legendbot.helpers.utils import mentionuser

menu_category = "extra"


async def get_group_call(chat):
    if isinstance(chat, Channel):
        result = await legend(functions.channels.GetFullChannelRequest(channel=chat))
    elif isinstance(chat, Chat):
        result = await legend(functions.messages.GetFullChatRequest(chat_id=chat.id))
    return result.full_chat.call


async def chat_vc_checker(event, chat, edits=True):
    if isinstance(chat, User):
        await eod(event, "Voice Chats are not available in Private Chats")
        return None
    result = await get_group_call(chat)
    if not result:
        if edits:
            await eod(event, "No Group Call in this chat")
        return None
    return result


async def parse_entity(entity):
    if entity.isnumeric():
        entity = int(entity)
    return await legend.get_entity(entity)


@legend.legend_cmd(
    pattern="vcstart",
    command=("vcstart", menu_category),
    info={
        "header": "To end a stream on Voice Chat.",
        "description": "To end a stream on Voice Chat",
        "usage": "{tr}vcstart",
        "examples": "{tr}vcstart",
    },
)
async def start_vc(event):
    "To start a Voice Chat."
    vc_chat = await legend.get_entity(event.chat_id)
    gc_call = await chat_vc_checker(event, vc_chat, False)
    if gc_call:
        return await eod(event, "Group Call is already available in this chat")
    try:
        await legend(
            functions.phone.CreateGroupCallRequest(
                peer=vc_chat,
                title="LegendBot VC",
            )
        )
        await eod(event, "Started Group Call")
    except ChatAdminRequiredError:
        await eod(event, "You should be chat admin to start vc", time=20)


@legend.legend_cmd(
    pattern="vcend",
    command=("vcend", menu_category),
    info={
        "header": "To end a stream on Voice Chat.",
        "description": "To end a stream on Voice Chat",
        "usage": "{tr}vcend",
        "examples": "{tr}vcend",
    },
)
async def end_vc(event):
    "To end a Voice Chat."
    vc_chat = await legend.get_entity(event.chat_id)
    gc_call = await chat_vc_checker(event, vc_chat)
    if not gc_call:
        return
    try:
        await legend(functions.phone.DiscardGroupCallRequest(call=gc_call))
        await eod(event, "Group Call Ended")
    except ChatAdminRequiredError:
        await eod(event, "You should be chat admin to kill vc", time=20)


@legend.legend_cmd(
    pattern="vcinv ?(.*)?",
    command=("vcinv", menu_category),
    info={
        "header": "To invite users on Voice Chat.",
        "usage": "{tr}vcinv < userid/username or reply to user >",
        "examples": [
            "{tr}vcinv @djkdo",
            "{tr}vcinv userid1 userid2",
        ],
    },
)
async def inv_vc(event):
    "To invite users to vc."
    users = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    vc_chat = await legend.get_entity(event.chat_id)
    gc_call = await chat_vc_checker(event, vc_chat)
    if not gc_call:
        return
    if not users:
        if not reply:
            return await eod("Whom Should i invite")
        users = reply.from_id
    await eor(event, "Inviting User to Group Call")
    entities = str(users).split(" ")
    user_list = []
    for entity in entities:
        cc = await parse_entity(entity)
        if isinstance(cc, User):
            user_list.append(cc)
    try:
        await legend(
            functions.phone.InviteToGroupCallRequest(call=gc_call, users=user_list)
        )
        await eod(event, "Invited users to Group Call")
    except UserAlreadyInvitedError:
        return await eod(event, "User is Already Invited", time=20)


@legend.legend_cmd(
    pattern="vcinv ?(.*)?",
    command=("vcinv", menu_category),
    info={
        "header": "To invite users on Voice Chat.",
        "usage": "{tr}vcinv < userid/username or reply to user >",
        "examples": [
            "{tr}vcinv @djkdo",
            "{tr}vcinv userid1 userid2",
        ],
    },
)
async def inv_vc(event):
    "To invite users to vc."
    users = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    vc_chat = await legend.get_entity(event.chat_id)
    gc_call = await chat_vc_checker(event, vc_chat)
    if not gc_call:
        return
    if not users:
        if not reply:
            return await eod("Whom Should i invite")
        users = reply.from_id
    await eor(event, "Inviting User to Group Call")
    entities = str(users).split(" ")
    user_list = []
    for entity in entities:
        cc = await parse_entity(entity)
        if isinstance(cc, User):
            user_list.append(cc)
    try:
        await legend(
            functions.phone.InviteToGroupCallRequest(call=gc_call, users=user_list)
        )
        await eod(event, "Invited users to Group Call")
    except UserAlreadyInvitedError:
        return await eod(event, "User is Already Invited", time=20)


@legend.legend_cmd(
    pattern="vcinfo",
    command=("vcinfo", menu_category),
    info={
        "header": "To get info of Voice Chat.",
        "usage": "{tr}vcinfo",
        "examples": "{tr}vcinfo",
    },
)
async def info_vc(event):
    "Get info of VC."
    vc_chat = await legend.get_entity(event.chat_id)
    gc_call = await chat_vc_checker(event, vc_chat)
    if not gc_call:
        return
    await eor(event, "Getting Group Call Info")
    call_details = await legend(
        functions.phone.GetGroupCallRequest(call=gc_call, limit=1)
    )
    grp_call = "**Group Call Info**\n\n"
    grp_call += f"**Title :** {call_details.call.title}\n"
    grp_call += f"**Participants Count :** {call_details.call.participants_count}\n\n"

    if call_details.call.participants_count > 0:
        grp_call += "**Participants**\n"
        for user in call_details.users:
            nam = f"{user.first_name or ''} {user.last_name or ''}"
            grp_call += f"  ● {mentionuser(nam,user.id)} - `{user.id}`\n"
    await eor(event, grp_call)


@legend.legend_cmd(
    pattern="vctitle?(.*)?",
    command=("vctitle", menu_category),
    info={
        "header": "To end a stream on Voice Chat.",
        "description": "To end a stream on Voice Chat",
        "usage": "{tr}vctitle <text>",
        "examples": "{tr}vctitle CatPro",
    },
)
async def title_vc(event):
    "To change vc title."
    title = event.pattern_match.group(1)
    vc_chat = await legend.get_entity(event.chat_id)
    gc_call = await chat_vc_checker(event, vc_chat)
    if not gc_call:
        return
    if not title:
        return await eod("What should i keep as title")
    await legend(functions.phone.EditGroupCallTitleRequest(call=gc_call, title=title))
    await eod(event, f"VC title was changed to **{title}**")


@legend.legend_cmd(
    pattern="vc(|un)mute ([\s\S]*)",
    command=("vcmute", menu_category),
    info={
        "header": "To mute users on Voice Chat.",
        "description": "To mute a stream on Voice Chat",
        "usage": [
            "{tr}vcmute < userid/username or reply to user >",
        ],
        "examples": [
            "{tr}vcmute @djjkd",
            "{tr}vcmute userid1 userid2",
        ],
    },
)
async def mute_vc(event):
    "To mute users in vc."
    cmd = event.pattern_match.group(1)
    users = event.pattern_match.group(2)
    reply = await event.get_reply_message()
    vc_chat = await legend.get_entity(event.chat_id)
    gc_call = await chat_vc_checker(event, vc_chat)
    if not gc_call:
        return
    check = "Unmute" if cmd else "Mute"
    if not users:
        if not reply:
            return await eod(f"Whom Should i {check}")
        users = reply.from_id
    await eor(event, f"{check[:-1]}ing User in Group Call")
    entities = str(users).split(" ")
    user_list = []
    for entity in entities:
        cc = await parse_entity(entity)
        if isinstance(cc, User):
            user_list.append(cc)

    for user in user_list:
        await legend(
            functions.phone.EditGroupCallParticipantRequest(
                call=gc_call,
                participant=user,
                muted=bool(not cmd),
            )
        )
    await eod(event, f"{check}d users in Group Call")


@legend.legend_cmd(
    command=("vcunmute", menu_category),
    info={
        "header": "To unmute users on Voice Chat.",
        "description": "To unmute a stream on Voice Chat",
        "usage": [
            "{tr}vcunmute < userid/username or reply to user>",
        ],
        "examples": [
            "{tr}vcunmute @apro",
            "{tr}vcunmute userid1 userid2",
        ],
    },
)
async def unmute_vc(event):
    "To unmute users in vc."
