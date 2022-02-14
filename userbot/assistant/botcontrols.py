import asyncio
from datetime import datetime

from telethon.errors import BadRequestError, FloodWaitError, ForbiddenError

from userbot import xrxnr

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import reply_id, time_formatter
from ..helpers.utils import _format
from ..sql_helper.bot_blacklists import check_is_black_list, get_all_bl_users
from ..sql_helper.bot_starters import del_starter_from_db, get_all_starters
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID
from .botmanagers import (
    ban_user_from_bot,
    get_user_and_reason,
    progress_str,
    unban_user_from_bot,
)

LOGS = logging.getLogger(__name__)

plugin_category = "bot"
botusername = Config.TG_BOT_USERNAME
cmhd = Config.COMMAND_HAND_LER


@xrxnr.iq_cmd(
    pattern=f"^/مساعدة$",
    from_users=Config.OWNER_ID,
)
async def bot_help(event):
    await event.reply(
        f"""**⚜️ ︙ اهلا بك في قائمه الاوامر :
الخاصه ببوت المطور :** {botusername}

**1︙** `/اذاعة`  + الرد على رساله ⤵️
⌔︙ اذاعه الرساله لجميع مراسلين بوتك عبر ارسالهم الرساله الى الخاص . 
 
**2︙** `/المستخدمين` ⤵️
⌔︙ لأضهار جميع مستخدمين البوت لديك  .

**3︙** `/حظر` + الرد على الشخص  ⤵️
⌔︙ لحضر الشخص المزعج من البوت فقط قم برد على رسالته او كتابه معرفه بجانب الامر  .

**4︙** `/فتح الحظر` + الرد على الشخص  ⤵️
⌔︙ لفتح حضر الشخص من البوت فقط قم برد على رسالته  او كتابه معرفه بجانب الامر  .

**5︙** `/فتح الحظر` + المحظورين  ⤵️
⌔︙ لأضهار قائمه المحظورين من بوتك   .
"""
    )


@xrxnr.iq_cmd(
    pattern=f"^/اذاعة$",
    from_users=Config.OWNER_ID,
)
async def bot_broadcast(event):
    replied = await event.get_reply_message()
    if not replied:
        return await event.reply("**⌔︙ يرجى الرد على الرسالة للأذاعة 📣!**")
    start_ = datetime.now()
    br_cast = await replied.reply("**⌔︙ جـاري الاذاعة لجمـيع الأعضاء 🚹**")
    blocked_users = []
    count = 0
    bot_users_count = len(get_all_starters())
    if bot_users_count == 0:
        return await event.reply("**⌔︙ لا يوجد اي شخص يستخدم بوتك**")
    users = get_all_starters()
    if users is None:
        return await event.reply("**⌔︙ هناك خطأ في فحص قائـمة  المستخدمين 🚸**")
    for user in users:
        try:
            await event.client.send_message(
                int(user.user_id), "⌔︙ 🔊 تم استلام اذاعه جديدة."
            )
            await event.client.send_message(int(user.user_id), replied)
            await asyncio.sleep(0.8)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except (BadRequestError, ValueError, ForbiddenError):
            del_starter_from_db(int(user.user_id))
        except Exception as e:
            LOGS.error(str(e))
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID, f"**⌔︙هنـاك خطـأ في الأذاعـة 🔊 🆘**\n`{str(e)}`"
                )
        else:
            count += 1
            if count % 5 == 0:
                try:
                    prog_ = (
                        "**⌔︙جـاري الأذاعـة 🔊 ..**\n\n"
                        + progress_str(
                            total=bot_users_count,
                            current=count + len(blocked_users),
                        )
                        + f"\n\n**⌔︙ بنـجاح ✔️:**  `{count}`\n"
                        + f"**⌔︙ خطأ ✖️ : **  `{len(blocked_users)}`"
                    )
                    await br_cast.edit(prog_)
                except FloodWaitError as e:
                    await asyncio.sleep(e.seconds)
    end_ = datetime.now()
    b_info = f"⌔︙ 🔊 تـم بنجاح الأذاعه الى :  <b>{count} عدد من المستخدمين 🚹.</b>"
    if len(blocked_users) != 0:
        b_info += f"\n⌔︙ 🚫  <b>{len(blocked_users)} </b> مجموع الاشخاص الذين قـامو بحـضر بوتـك 🆘."
    b_info += (
        f"\n⌔︙⏳  <code> الـوقت المسـتغرق : {time_formatter((end_ - start_).seconds)}</code>."
    )
    await br_cast.edit(b_info, parse_mode="html")


@xrxnr.iq_cmd(
    pattern=f"^/المستخدمين$",
    command=("bot_users", plugin_category),
    info={
        "header": "To get users list who started bot.",
        "description": "To get compelete list of users who started your bot",
        "usage": "{tr}bot_users",
    },
)
async def ban_starters(event):
    "To get list of users who started bot."
    ulist = get_all_starters()
    if len(ulist) == 0:
        return await edit_delete(event, "**⌔︙ لايـوجد اي شخص أستعـمل بوتـك 🚹**")
    msg = "**⌔︙ الأشخـاص الذيـن اسـتعملو بوتـك 🚻 :\n\n**"
    for user in ulist:
        msg += f"• 👤 {_format.mentionuser(user.first_name , user.user_id)}\n**⌔︙ الايدي:** `{user.user_id}`\n**⌔︙ المعرفات:** @{user.username}\n**⌔︙ التاريخ: **__{user.date}__\n\n"
    await edit_or_reply(event, msg)


@xrxnr.iq_cmd(
    pattern=f"^/حظر\s+([\s\S]*)",
    from_users=Config.OWNER_ID,
)
async def ban_botpms(event):
    user_id, reason = await get_user_and_reason(event)
    reply_to = await reply_id(event)
    if not user_id:
        return await event.client.send_message(
            event.chat_id, "**⌔︙ لايمكـنني العثـور على المسـتخدم  🚹 ⚠️**", reply_to=reply_to
        )
    if not reason:
        return await event.client.send_message(
            event.chat_id, "**⌔︙ لحـظر هـذا الشخـص قـم بكتـابة السبـب بجـانب الامـر  🔙**", reply_to=reply_to
        )
    try:
        user = await event.client.get_entity(user_id)
        user_id = user.id
    except Exception as e:
        return await event.reply(f"**⌔︙عـذرا هنـاك خطـأ 🚫 :**\n`{str(e)}`")
    if user_id == Config.OWNER_ID:
        return await event.reply("**⌔︙لاأستطيـع حظـر مالـك البـوت الشخـصي. 🛂**")
    check = check_is_black_list(user.id)
    if check:
        return await event.client.send_message(
            event.chat_id,
            f"**⌔︙ بالفعل_محظور :**\
            \n**⌔︙ هـذا المسـتخدم موجـود فـي قائمـة المحظـورين 🚫**\
            \n**⌔︙ سبب الحظر 🚫 :** `{check.reason}`\
            \n**⌔︙ التاريخ 📆 :** `{check.date}`.",
        )
    msg = await ban_user_from_bot(user, reason, reply_to)
    await event.reply(msg)


@xrxnr.iq_cmd(
     pattern=f"^/فتح الحظر(?:\s|$)([\s\S]*)",
    from_users=Config.OWNER_ID,
)
async def ban_botpms(event):
    user_id, reason = await get_user_and_reason(event)
    reply_to = await reply_id(event)
    if not user_id:
        return await event.client.send_message(
            event.chat_id, "**⌔︙ لا استطيع ايجاد المستخـدم للحـظر 🔍⚠️ .**", reply_to=reply_to
        )
    try:
        user = await event.client.get_entity(user_id)
        user_id = user.id
    except Exception as e:
        return await event.reply(f"**⌔︙عـذرا هنـاك خطـأ 🚫 :**\n`{str(e)}`")
    check = check_is_black_list(user.id)
    if not check:
        return await event.client.send_message(
            event.chat_id,
            f"**⌔︙ الغـاء الـحظر 🔓 **\
            \n⌔︙ 👤 {_format.mentionuser(user.first_name , user.id)} تـم الغـاء حـظرة مـن البـوت بنـجاح ✅",
        )
    msg = await unban_user_from_bot(user, reason, reply_to)
    await event.reply(msg)


@xrxnr.iq_cmd(
   pattern=f"^/المحظورين$",
    command=("bblist", plugin_category),
    info={
        "header": "To get users list who are banned in bot.",
        "description": "To get list of users who are banned in bot.",
        "usage": "{tr}bblist",
    },
)
async def ban_starters(event):
    "To get list of users who are banned in bot."
    ulist = get_all_bl_users()
    if len(ulist) == 0:
        return await edit_delete(event, "**⌔︙ لا يوجـد شخص محـظور في البـوت الـى الان 👤**")
    msg = "**المسـتخدميـن المحـظورين في بـوتك هـم :\n\n**"
    for user in ulist:
        msg += f"• 👤 {_format.mentionuser(user.first_name , user.chat_id)}\n**⌔︙ الايدي:** `{user.chat_id}`\n**⌔︙ المعرف:** @{user.username}\n**⌔︙ التاريخ: **{user.date}\n**⌔︙ السبب:** {user.reason}\n\n"
    await edit_or_reply(event, msg)


@xrxnr.iq_cmd(
    pattern=f"^/التكرار (تشغيل|ايقاف)$",
    command=("bot_antif", plugin_category),
    info={
        "header": "To enable or disable bot antiflood.",
        "description": "if it was turned on then after 10 messages or 10 edits of same messages in less time then your bot auto loacks them.",
        "usage": [
            "{tr}bot_antif on",
            "{tr}bot_antif off",
        ],
    },
)
async def ban_antiflood(event):
    "To enable or disable bot antiflood."
    input_str = event.pattern_match.group(1)
    if input_str == "تشغيل":
        if gvarstatus("bot_antif") is not None:
            return await edit_delete(event, "**⌔︙تـم تشغيل حظر التكـرار بالفعل ✅**")
        addgvar("bot_antif", True)
        await edit_delete(event, "**⌔︙تـم تشغيل حظر التكـرار  ✅**")
    elif input_str == "ايقاف":
        if gvarstatus("bot_antif") is None:
            return await edit_delete(event, "**⌔︙تـم تعطيل حظر التكـرار بالفعل ✅**")
        delgvar("bot_antif")
        await edit_delete(event, "**⌔︙تـم تعطيل حظر التكـرار  ✅**")
