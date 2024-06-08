import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, PollAnswerHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define your bot token here
BOT_TOKEN = '1250677312:AAGvNeYI6Mn6w4MmJCgn_0IXpIrKCjgtYPY'

# Dictionary to store message IDs to delete
message_store = {}

async def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hi! Use /send <user_id> <message> to send a message. Use /delete to delete the latest message sent.')

async def delete_message_after_delay(bot, chat_id, message_id, delay):
    """Delete a message after a delay."""
    await asyncio.sleep(delay)
    if chat_id in message_store and message_store[chat_id] == message_id:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        del message_store[chat_id]

async def send_message(update: Update, context: CallbackContext):
    """Send a message to a specific user and delete it after 10 seconds."""
    try:
        user_id = int(context.args[0])
        message_text = ' '.join(context.args[1:])
        bot = context.bot
        message = await bot.send_message(chat_id=user_id, text=message_text)
        
        # Store the message ID to delete it later
        message_store[user_id] = message.message_id

        # Schedule message deletion
        asyncio.create_task(delete_message_after_delay(bot, user_id, message.message_id, 10))
        
        await update.message.reply_text('Message sent and will be deleted after 10 seconds.')
    except (IndexError, ValueError):
        await update.message.reply_text('Usage: /send <user_id> <message>')

async def delete_message(update: Update, context: CallbackContext):
    """Delete the last message sent to the user."""
    user_id = update.message.chat_id
    bot = context.bot
    if user_id in message_store:
        message_id = message_store[user_id]
        await bot.delete_message(chat_id=user_id, message_id=message_id)
        del message_store[user_id]
        await update.message.reply_text('Message deleted.')
    else:
        await update.message.reply_text('No message to delete.')

async def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

from datetime import datetime, timedelta

async def create_poll(update: Update, context: CallbackContext):
    """Create a poll with a close period."""
    question = "What is your favorite color?"
    options = ["Red", "Blue", "Green"]
    
    # Calculate the close date
    close_date = datetime.utcnow() + timedelta(minutes=1)  # Close after 1 minute
    
    poll_message = await context.bot.send_poll(update.message.chat_id, question, options, is_anonymous=False, open_period=0, close_date=close_date)
    await update.message.reply_text(f"Poll created with ID: {poll_message.message_id}")

    print("KKKK", context)
    # Handle poll answers
    #async def poll_answer(update: Update, context: CallbackContext):
    #    if update.poll_answer.poll_id == poll_message.poll.id:
    #        logger.info(f"Answer: {update.poll_answer.option_ids}")

    #dispatcher = context.dispatcher
    #dispatcher.add_handler(PollAnswerHandler(poll_answer))


def main():
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("send", send_message))
    application.add_handler(CommandHandler("delete", delete_message))
    application.add_handler(CommandHandler("createpoll", create_poll))

    # log all errors
    application.add_error_handler(error)

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
