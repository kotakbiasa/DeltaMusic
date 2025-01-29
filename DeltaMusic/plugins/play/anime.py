import requests

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

def play_anime(title, episode):
    # Get the streaming URL
    streaming_url = get_anime_streaming_url(title, episode)
    
    if streaming_url:
        # Code to play the anime using the streaming URL
        print(f"Playing {title} Episode {episode}: {streaming_url}")
        # ...existing code to handle the streaming...
    else:
        print(f"Failed to retrieve streaming URL for {title} Episode {episode}")

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
    import sys
    if len(sys.argv) < 2:
        print("Usage: python anime.py <command> [<args>]")
        return
    
    command = sys.argv[1]
    
    if command == "play":
        if len(sys.argv) != 4:
            print("Usage: python anime.py play <title> <episode>")
            return
        title = sys.argv[2]
        episode = sys.argv[3]
        play_anime(title, episode)
    elif command == "ongoing":
        ongoing_anime = get_ongoing_anime()
        print(ongoing_anime)
    elif command == "complete":
        complete_anime = get_complete_anime()
        print(complete_anime)
    elif command == "genre":
        if len(sys.argv) != 4:
            print("Usage: python anime.py genre <genre_id> <page>")
            return
        genre_id = sys.argv[2]
        page = sys.argv[3]
        genre_anime = get_genre_anime(genre_id, page)
        print(genre_anime)
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
