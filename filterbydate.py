import requests
from datetime import datetime

def get_channel_id(api_key, username=None, channel_name=None):
    """
    Fetches the YouTube channel ID based on the username or channel name.

    Parameters:
        api_key (str): Your YouTube Data API key.
        username (str): The YouTube channel's username (optional).
        channel_name (str): The YouTube channel's name (optional).

    Returns:
        str: The channel ID, or None if not found.
    """
    base_url = "https://www.googleapis.com/youtube/v3/"
    
    if username:
        # Use the "forUsername" parameter to find the channel ID by username
        url = f"{base_url}channels"
        params = {"part": "id", "forUsername": username, "key": api_key}
        response = requests.get(url, params=params).json()
        if "items" in response and response["items"]:
            return response["items"][0]["id"]
        else:
            print("Channel not found for the given username.")
            return None
    
    elif channel_name:
        # Use the Search endpoint to find the channel ID by channel name
        url = f"{base_url}search"
        params = {
            "part": "snippet",
            "q": channel_name,
            "type": "channel",
            "key": api_key
        }
        response = requests.get(url, params=params).json()
        if "items" in response and response["items"]:
            return response["items"][0]["snippet"]["channelId"]
        else:
            print("Channel not found for the given channel name.")
            return None

    else:
        print("Please provide either a username or channel name.")
        return None

<<<<<<< HEAD
API_KEY = "AIzaSyBUUX25FpJUsyt33p5zb9y3_L1V7agFVyA"
CHANNEL_ID = get_channel_id(API_KEY,None,"@SamitoFPS")
=======
API_KEY = "[API_KEY]"
CHANNEL_ID = get_channel_id(API_KEY,None,"@MOLT")
>>>>>>> 144799a820682a7928d87cb693572c06f5e7b2d0
START_DATE = "2023-01-01T00:00:00Z"  # On jan 1st 2023 - jan 31st 2023
END_DATE = "2023-01-31T23:59:59Z"

# Step 1: Get the uploads playlist ID
channel_url = "https://www.googleapis.com/youtube/v3/channels"
channel_params = {
    "part": "contentDetails",
    "id": CHANNEL_ID,
    "key": API_KEY
}

channel_response = requests.get(channel_url, params=channel_params).json()
uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

# Step 2: Fetch videos from the uploads playlist
videos = []
next_page_token = None
while True:
    playlist_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    playlist_params = {
        "part": "snippet",
        "playlistId": uploads_playlist_id,
        "maxResults": 50,
        "pageToken": next_page_token,
        "key": API_KEY
    }
    playlist_response = requests.get(playlist_url, params=playlist_params).json()
    
    for item in playlist_response["items"]:
        video_published = item["snippet"]["publishedAt"]
        if START_DATE <= video_published <= END_DATE:
            videos.append({
                "title": item["snippet"]["title"],
                "videoId": item["snippet"]["resourceId"]["videoId"],
                "publishedAt": video_published
            })
    
    next_page_token = playlist_response.get("nextPageToken")
    if not next_page_token:
        break

# Print filtered videos
for video in videos:
    print(f"Title: {video['title']}, Video ID: {video['videoId']}, Published At: {video['publishedAt']}")


