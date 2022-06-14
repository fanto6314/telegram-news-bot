from dotenv import load_dotenv
import telegram.ext
import requests
import datetime
import random
import json
import os

load_dotenv()

token = os.getenv('TOKEN')
api = os.getenv('API')

languages = "en"
newsTimer = 600
query = "world"
pageSize = "100"
yesterday = str(datetime.datetime.now() - datetime.timedelta(days=1))
today = str(datetime.datetime.now())
api_url = "https://newsapi.org/v2/everything?q=" + query + "&from=" + yesterday + "&to=" + today + "&sortBy=popularity&pageSize=+"+ pageSize +"&apiKey=" + api

def start(update, context):
    context.job_queue.run_repeating(news, interval=newsTimer, first=1)

def help(update, context):
    update.message.reply_text("""
    Available commands:
    /start - start bot
    /help - help
    """)

def news(context):
    response = requests.get(api_url)
    json_data = json.loads(response.text)
    i = random.randint(0, 99)
    title = json_data['articles'][i]['title']
    image = json_data['articles'][i]['urlToImage']
    description = json_data['articles'][i]['description']
    author = json_data['articles'][i]['author']
    article = json_data['articles'][i]

    if title is None:
        title = "No title"
    if image is None:
        image = "https://www.alfasolare.ru/a_solar_restyle/wp-content/themes/consultix/images/no-image-found-360x260.png"
    if description is None:
        description = "No Content"
    if author is None:
        author = "No Author"
    if article is None:
        i = random.randint(0, len(json_data['articles']))

    caption = "<a>" + title + "\n" + description + "\n Author: " + author + "</a>"
    chat_id = "800799169"

    context.bot.send_photo(
        chat_id=chat_id,
        photo=image,
        caption=caption,
        parse_mode=telegram.ParseMode.HTML
    )
        
if __name__ == '__main__':
    updater = telegram.ext.Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
    dispatcher.add_handler(telegram.ext.CommandHandler('help', help))
    if updater.start_polling():
        print("Bot started successfully!")
    if updater.idle():
        print("Bot stopped")
