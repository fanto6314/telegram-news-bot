import telegram.ext
import requests
import json

with open ('token.txt', 'r') as f:
    token = f.read()

api = "df6a9ccf303ac1478b7155b55d0c3c33"
languages = "en"
limit = "1"
newsTimer = 10

api_url = "http://api.mediastack.com/v1/news?access_key=" + api + "&languages=" + languages + "&limit=" + limit

#TODO: fix send news every x minutes not working
def start(update, context):
    update.message.reply_text('Hello, I am PythonWorldNews_bot!')
    context.job_queue.run_repeating(news(update, context), interval=newsTimer, first=0)

def help(update, context):
    update.message.reply_text("""
    Available commands:
    /start - start bot
    /help - help
    /news - get news
    """)

def news(update, context):
    limit = 1
    response = requests.get(api_url)
    json_data = json.loads(response.text)
    for i in range(0, limit):
        #update.message.reply_text(json_data["data"][i]["image"] + json_data["data"][i]["title"])
        if(json_data["data"][i]["image"]):
            caption = "<a>" + json_data["data"][i]["title"] + "\n" + json_data["data"][i]["description"] + "\n Author: " + json_data["data"][i]["author"] + "</a>"
            chat_id = update.message.chat_id

            context.bot.send_photo(
                chat_id=chat_id,
                photo=json_data["data"][i]["image"],
                caption=caption,
                parse_mode=telegram.ParseMode.HTML
            )
        else:
            caption = "<a>" + json_data["data"][i]["title"] + "\n" + json_data["data"][i]["description"] + "\n Author: " + json_data["data"][i]["author"] + "</a>"
            chat_id = update.message.chat_id

            context.bot.send_message(
                chat_id=chat_id,
                text=caption,
                parse_mode=telegram.ParseMode.HTML
            )

# -------------------------   Main   ------------------------- #
if __name__ == '__main__':
    updater = telegram.ext.Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
    dispatcher.add_handler(telegram.ext.CommandHandler('help', help))

    if updater.start_polling():
        print("Bot started successfully!")
    if updater.idle():
        print("Bot stopped")
