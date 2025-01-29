import requests
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from DeltaMusic.resources import get_telegram_bot_token

def get_anime_streaming_url(title, episode):
    # Define the API endpoint for searching the anime
    search_url = f"https://unofficial-otakudesu-api-ruang-kreatif.vercel.app/api/search/{title}"
    
    # Make a GET request to the search API
    search_response = requests.get(search_url)
    
    # Check if the search request was successful
    if search_response.status_code == 200:
        search_data = search_response.json()
        # Extract the anime ID from the search response
        anime_id = search_data['data'][0]['id']
        
        # Define the API endpoint for fetching episode details
        episode_url = f"https://unofficial-otakudesu-api-ruang-kreatif.vercel.app/api/eps/{anime_id}/episode/{episode}"
        
        # Make a GET request to the episode API
        episode_response = requests.get(episode_url)
        
        # Check if the episode request was successful
        if episode_response.status_code == 200:
            episode_data = episode_response.json()
            # Extract the streaming URL from the episode response
            streaming_url = episode_data.get('streaming_url')
            return streaming_url
        else:
            return None
    else:
        return None

def play_anime(update: Update, context: CallbackContext):
    if len(context.args) != 2:
        update.message.reply_text("Usage: /play_anime <title> <episode>")
        return
    
    title = context.args[0]
    episode = context.args[1]
    
    # Get the streaming URL
    streaming_url = get_anime_streaming_url(title, episode)
    
    if streaming_url:
        # Send the streaming URL to the user
        update.message.reply_text(f"Playing {title} Episode {episode}: {streaming_url}")
    else:
        update.message.reply_text(f"Failed to retrieve streaming URL for {title} Episode {episode}")

def list_ongoing(update: Update, context: CallbackContext):
    ongoing_anime = get_ongoing_anime()
    update.message.reply_text(ongoing_anime)

def list_complete(update: Update, context: CallbackContext):
    complete_anime = get_complete_anime()
    update.message.reply_text(complete_anime)

def list_genre(update: Update, context: CallbackContext):
    if len(context.args) != 2:
        update.message.reply_text("Usage: /list_genre <genre_id> <page>")
        return
    
    genre_id = context.args[0]
    page = context.args[1]
    genre_anime = get_genre_anime(genre_id, page)
    update.message.reply_text(genre_anime)

def get_ongoing_anime():
    ongoing_url = "https://unofficial-otakudesu-api-ruang-kreatif.vercel.app/api/ongoing"
    response = requests.get(ongoing_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_complete_anime():
    complete_url = "https://unofficial-otakudesu-api-ruang-kreatif.vercel.app/api/complete"
    response = requests.get(complete_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_genre_anime(genre_id, page):
    genre_url = f"https://unofficial-otakudesu-api-ruang-kreatif.vercel.app/api/genres/{genre_id}/page/{page}"
    response = requests.get(genre_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    # Get the Telegram bot token from DeltaMusic resources
    bot_token = get_telegram_bot_token()
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("play_anime", play_anime))
    dp.add_handler(CommandHandler("list_ongoing", list_ongoing))
    dp.add_handler(CommandHandler("list_complete", list_complete))
    dp.add_handler(CommandHandler("list_genre", list_genre))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
