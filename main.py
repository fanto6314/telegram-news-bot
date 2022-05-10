from dotenv import load_dotenv
import telegram.ext
import requests
import datetime
import random
import json
import os

load_dotenv()

# Predo le variabile token e api dal file .env tramite la funzione importata "dotenv"
token = os.getenv('TOKEN')
api = os.getenv('API')

languages = "en"
newsTimer = 600 #10 minutes
query = "world"
pageSize = "100"
yesterday = str(datetime.datetime.now() - datetime.timedelta(days=1))
today = str(datetime.datetime.now())
# Url per la API Request, dove verranno presi gli articoli
api_url = "https://newsapi.org/v2/everything?q=" + query + "&from=" + yesterday + "&to=" + today + "&sortBy=popularity&pageSize=+"+ pageSize +"&apiKey=" + api

def start(update, context):
    # Metodo che esegue il metodo news() ogni tot secondi in base a quanto è impostata la variabile "newsTimer"
    context.job_queue.run_repeating(news, interval=newsTimer, first=1)

def help(update, context):
    # Manda un messaggio in chat contentete le cose tra ""
    update.message.reply_text("""
    Available commands:
    /start - start bot
    /help - help
    """)

def news(context):
    # Metodo che prende le news
    response = requests.get(api_url) # Esegue la richiesta di tipo get all'url impostato prima, e salva la risposta nella variabile "response"
    json_data = json.loads(response.text) # Trasformo il testo ritornato dalla richiesta in una variabile di tipo json
    i = random.randint(0, 99)

    # Prendo tutte le info che mi servono dal testo json (una spece di array) che ho 
    # ottenuto prima, navigo all'interno dell'array nelle posizioni di cui ho bisogno
    title = json_data['articles'][i]['title']
    image = json_data['articles'][i]['urlToImage']
    description = json_data['articles'][i]['description']
    author = json_data['articles'][i]['author']
    article = json_data['articles'][i]

    # Controllo se le variabili sopra sono di tipo "Null o None", in caso siano effettivamente le modifico assegnando
    # un valore, altrimenti il bot si blocca e crasha
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

    # Creo la variabile caption, che è il contenuto finale del messaggio mandato dal bot
    # Chat_id è l'id della mia chat con il bot per poter dire al bot di mandare messaggi in quella determinata chat
    caption = "<a>" + title + "\n" + description + "\n Author: " + author + "</a>"
    chat_id = "800799169"

    # Questo metodo di telegram manda un'immagine nella chat con id chat_id (in questo caso la mia), e come "descrizione"
    # dell'immagine mette il testo caption, che è il messaggio contenete titolo, destrizione e autore, preso dalla variabile
    # "caption" definita sopra
    context.bot.send_photo(
        chat_id=chat_id,
        photo=image,
        caption=caption,
        parse_mode=telegram.ParseMode.HTML
    )
        
# Metodo Main, che viene eseguito ogni volta runnato lo script
if __name__ == '__main__':
    # Creo la variabile updated, che è "il bot", e gli passo il token(che è il come l'usename e la pass)
    updater = telegram.ext.Updater(token, use_context=True)
    # Creo la variabile dispacher, e dico che updater.dispacher è il nostro dispacher
    dispatcher = updater.dispatcher

    # Al dispacher aggiungo un "handler", in questo caso gli handler che aggiungiamo sono dei CommandHandler
    # gli handler gestiscono i comandi, in questo caso passo una stringa ed una funzione, la stringa è il comando
    # che l'utente in chat dovra scrivere per poter eseguire la funzione data.
    dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
    dispatcher.add_handler(telegram.ext.CommandHandler('help', help))

    # Se il bot è acceso correttamente verra stampato "Bot started", altrimenti dirà bot stopped e stampera
    # eventuali errori.
    if updater.start_polling():
        print("Bot started successfully!")
    if updater.idle():
        print("Bot stopped")
