import telegram.ext
import requests

with open ('token.txt', 'r') as f:
    token = f.read()

api = "df6a9ccf303ac1478b7155b55d0c3c33"
languages = "en"

api_url = "http://api.mediastack.com/v1/news?access_key=" + api + "&languages=" + languages

def start(update, context):
    update.message.reply_text('Hello, I am PythonWorldNews_bot!')

def help(update, context):
    update.message.reply_text("""
    Available commands:

    /start - start bot
    /help - help
    """)

def getNews():
    response = requests.get(api_url)
    print(response.json())

def news(update, context):
    update.message.reply_text("This is news command")

if __name__ == '__main__':
    updater = telegram.ext.Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
    dispatcher.add_handler(telegram.ext.CommandHandler('help', help))
    dispatcher.add_handler(telegram.ext.CommandHandler('news', news))

    getNews()

    updater.start_polling()
    print("Bot started successfully!")
    updater.idle()
    print("Bot stopped")