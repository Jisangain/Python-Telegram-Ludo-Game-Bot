from telegram.ext import Updater, MessageHandler, Filters
import asyncio

# Define a function to handle incoming messages
def echo(update, context):
    # Get the message text from the update
    message_text = update.message.text
    
    # Send the same message back as a reply
    update.message.reply_text(message_text)

# Create an instance of the Updater class
updater = Updater("YOUR_BOT_TOKEN")

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Register the echo function as a message handler
dispatcher.add_handler(MessageHandler(Filters.text, echo))

# Start the bot
updater.start_polling()

# Run the bot until you press Ctrl-C
updater.idle()
# Define an async function to handle incoming messages
async def echo_async(update, context):
    # Get the message text from the update
    message_text = update.message.text
    
    # Send the same message back as a reply
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message_text)

# Create an instance of the Updater class
updater = Updater("YOUR_BOT_TOKEN")

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Register the echo_async function as a message handler
dispatcher.add_handler(MessageHandler(Filters.text, echo_async))

# Start the bot
updater.start_polling()

# Run the bot until you press Ctrl-C
updater.idle()