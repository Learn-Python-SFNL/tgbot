from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

def greet_user(update, context):
    logger.info('Вызван /start')
    update.message.reply_text('Hello World')

def talk_to_me(update, context):
    text=update.message.text
    logger.info(text)
    update.message.reply_text(text)

def main():

    mybot = Updater(settings.API_KEY, use_context=True)

    dp=mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот Стартовал')
    mybot.start_polling()
    mybot.idle()

if __name__=="__main__":
    main()
