import bot
from config import settings
 
bot_telegram_api = settings['TOKEN']

bot.start(bot_telegram_api)