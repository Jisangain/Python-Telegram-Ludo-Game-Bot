#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that works with polls. Only 3 people are allowed to interact with each
poll/quiz the bot generates. The preview command generates a closed poll/quiz, exactly like the
one the user sends the bot
"""
import asyncio
import logging
from time import time
from telegram import (
    KeyboardButton,
    KeyboardButtonPollType,
    Poll,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PollAnswerHandler,
    PollHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.INFO)

logger = logging.getLogger(__name__)


async def create_poll(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id, question, options, wait_period) -> None:
    """Sends a predefined poll"""
    print(wait_period, type(wait_period))
    message = await context.bot.send_poll(
        chat_id,
        question,
        options,
        is_anonymous=False,
        allows_multiple_answers = False,
        close_date = time() + wait_period
    )
    # Save some info about the poll the bot_data for later use in receive_poll_answer
    payload = {
        message.poll.id: {
            "message_id": message.message_id,
            "chat_id": update.effective_chat.id,
        }
    }
    context.bot_data.update(payload)
    return message.poll.id
async def receive_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(context.bot_data)
    """Summarize a users poll vote"""
    answer = update.poll_answer
    try:
        answered_poll = context.bot_data[answer.poll_id]
    except KeyError:
        return
    context.bot_data[answer.poll_id]["answer"] = answer.option_ids[0]
    return answer.option_ids[0]

async def create_poll_and_get_answer(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id, question, options, wait_period) -> None:
    # Get answer by handling create_poll and receive_poll_answer
    poll_id = await create_poll(update, context, chat_id, question, options, wait_period)
    current_time = 0
    while current_time <= wait_period:
        try:
            answer = context.bot_data[poll_id]["answer"]
            context.bot_data.pop(poll_id)
            return answer
        except:
            pass
        await asyncio.sleep(0.5)
        current_time += 0.5
    context.bot_data.pop(poll_id)
    return -1
    
async def _create_poll_and_get_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question = "What is the quesion?"
    options = ["Nothing", "Really Nothing", "Are you sure"]
    wait_period = 10
    asyncio.create_task(create_poll_and_get_answer(update, context, update.effective_chat.id, question, options, wait_period))
def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("1250677312:AAGvNeYI6Mn6w4MmJCgn_0IXpIrKCjgtYPY").build()
    #application.add_handler(CommandHandler("start", start))
    #application.add_handler(CommandHandler("poll", create_poll))
    application.add_handler(CommandHandler("poll", _create_poll_and_get_answer))
    application.add_handler(PollAnswerHandler(receive_poll_answer))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()