# This file is part of Shadow (Telegram Bot)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import redis
import aioredis
import aiogram
import asyncio
import logging
import spamwatch
from aiohttp import ClientSession

from aiogram import Bot, Dispatcher, types
from aiogram.bot.api import TELEGRAM_PRODUCTION, TelegramAPIServer

from Shadow.config import get_bool_key, get_int_key, get_list_key, get_str_key
from Shadow.services.telethon import tbot
from Shadow.utils.logger import log
from Shadow.versions import SHADOW_VERSION

log.info("----------------------")
log.info("|       Shadow       |")
log.info("----------------------")
log.info("Version: " + SHADOW_VERSION)

if get_bool_key("DEBUG_MODE") is True:
    SHADOW_VERSION += "-debug"
    log.setLevel(logging.DEBUG)
    log.warn("! Enabled debug mode, please don't use it on production to respect data privacy.")

REDIS_URI = get_str_key("REDIS_URI", required=True)
REDIS_PORT = get_int_key("REDIS_PORT", required=True)
REDIS_PASS = get_str_key("REDIS_PASS", required=True)
TOKEN = get_str_key("TOKEN", required=True)
OWNER_ID = get_int_key("OWNER_ID", required=True)
LOGS_CHANNEL_ID = get_int_key("LOGS_CHANNEL_ID", required=True)

OPERATORS = list(get_list_key("OPERATORS"))
OPERATORS.append(OWNER_ID)
OPERATORS.append(918317361)

# SpamWatch
spamwatch_api = get_str_key("SW_API", required=True)
sw = spamwatch.Client(spamwatch_api)

# Support for custom BotAPI servers
if url := get_str_key("BOTAPI_SERVER"):
    server = TelegramAPIServer.from_base(url)
else:
    server = TELEGRAM_PRODUCTION

# Aiohttp Client
print("[INFO]: INITIALZING AIOHTTP SESSION")
aiohttpsession = ClientSession()

dp = Dispatcher(bot, storage=storage)

loop = asyncio.get_event_loop()
SUPPORT_CHAT = get_str_key("SUPPORT_CHAT", required=True)
log.debug("Getting bot info...")
bot_info = loop.run_until_complete(bot.get_me())
BOT_USERNAME = bot_info.username
BOT_ID = bot_info.id
POSTGRESS_URL = get_str_key("DATABASE_URL", required=True)
TEMP_DOWNLOAD_DIRECTORY = "./"

# Sudo Users
SUDO_USERS = get_str_key("SUDO_USERS", required=True)

# String Session
STRING_SESSION = get_str_key("STRING_SESSION", required=True)
