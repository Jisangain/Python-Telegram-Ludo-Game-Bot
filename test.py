#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to handle '(my_)chat_member' updates.
Greets new users & keeps track of which chats the bot is in.

Usage:
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from typing import Optional, Tuple

from telegram import Chat, ChatMember, ChatMemberUpdated, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Enable logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
import asyncio
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.INFO)

logger = logging.getLogger(__name__)

k = 0
async def f3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global k
    print("as")
    await asyncio.sleep(10)
    context.bot_data.update({k:2})
    k+=1
    print(context, context.bot_data)
    await asyncio.sleep(10)
    

async def f1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("AS")
    asyncio.create_task(f3(update, context))
async def f2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("1250677312:AAGvNeYI6Mn6w4MmJCgn_0IXpIrKCjgtYPY").build()

    application.add_handler(CommandHandler("1", f1))
    application.add_handler(CommandHandler("2", f2))
    # Handle members joining/leaving chats.
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()