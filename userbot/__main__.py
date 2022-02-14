
import sys
import userbot
from userbot import BOTLOG_CHATID, HEROKU_APP, PM_LOGGER_GROUP_ID
from telethon import functions
from .Config import Config
from .core.logger import logging
from .core.session import xrxnr
from .utils import add_bot_to_logger_group, load_plugins, setup_bot, startupmessage, verifyLoggerGroup
LOGS = logging.getLogger(
"تليثون ستارك"
)
print(
userbot.__copyright__)
print(
"المرخصة بموجب شروط " + userbot.__license__)
cmdhr = Config.COMMAND_HAND_LER
try:
    LOGS.info(
"بدء تنزيل تليثون ستارك"
)
    xrxnr.loop.run_until_complete(
setup_bot())
    LOGS.info("بدء تشغيل البوت")
except Exception as e:
    LOGS.error(
f"{str(e)}")
    sys.exit()
class CatCheck:
    def __init__(self):
        self.sucess = True
Catcheck = CatCheck()
async def startup_process():
    await verifyLoggerGroup()
    await load_plugins("plugins")
    await load_plugins("assistant")
    print(
f"<b> ⌔︙ اهلا بك لقد نصبت تليثون ستارك بنجاح 🥁 اذهب الى قناتنا لمعرفة المزيـد ⤵️. </b>\n CH : https://t.me/xrxnr "
)
    await verifyLoggerGroup()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    Catcheck.sucess = True
    return
xrxnr.loop.run_until_complete(startup_process())
def start_bot():
  try:
    xrxnr.loop.run_until_complete(
xrxnr(
functions.channels.JoinChannelRequest
(
"XRXNR"
))
)
    xrxnr.loop.run_until_complete(
xrxnr(
functions.channels.JoinChannelRequest("TelethonMusic"
)
))
    xrxnr.loop.run_until_complete(
xrxnr(
functions.channels.JoinChannelRequest(
"XRXNR"
)))
    xrxnr.loop.run_until_complete(
xrxnr(
functions.channels.JoinChannelRequest(
"XRXNR"
)))  
  except Exception as e:
    print(e)
    return False
Checker = start_bot()
if Checker == False:
    print(
"عذرا لديك حظر مؤقت حاول التنصيب غدا او بعد 24 ساعة"
)
    xrxnr.disconnect()
    sys.exit()
if len(sys.argv) not in (1, 3, 4):
    xrxnr.disconnect()
elif not Catcheck.sucess:
    if HEROKU_APP is not None:
        HEROKU_APP.restart()
else:
    try:
        xrxnr.run_until_disconnected()
    except ConnectionError:
        pass
