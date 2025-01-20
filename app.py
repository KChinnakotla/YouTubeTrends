from flask import Flask, request, jsonify
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Function to get the channel ID
def get_channel_id(api_key, username=None, channel_name=None):
    base_url = "https://www.googleapis.com/youtube/v3/"
    
    if username:
        url = f"{base_url}channels"
        params = {"part": "id", "forUsername": username, "key": api_key}
        response = requests.get(url, params=params).json()
        if "items" in response and response["items"]:
            return response["items"][0]["id"]
        else:
            return None
    
    elif channel_name:
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
            return None

    return None

@app.route('/get_videos', methods=['GET'])
def get_videos():
    api_key = request.args.get('api_key')
    channel_name = request.args.get('channel_name')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Validate input parameters
    if not api_key or not channel_name or not start_date or not end_date:
        return jsonify({"error": "Missing required parameters"}), 400
    
    # Step 1: Get the channel ID
    channel_id = get_channel_id(api_key, channel_name=channel_name)
    if not channel_id:
        logging.error("Channel not found for name: %s", channel_name)
        return jsonify({"error": "Channel not found"}), 404

    # Step 2: Get the uploads playlist ID
    channel_url = "https://www.googleapis.com/youtube/v3/channels"
    channel_params = {
        "part": "contentDetails",
        "id": channel_id,
        "key": api_key
    }
    channel_response = requests.get(channel_url, params=channel_params).json()
    logging.debug(f"Channel response: {channel_response}")

    if "error" in channel_response:
        logging.error("Error in channel response: %s", channel_response["error"])
        return jsonify({"error": "Error fetching channel details"}), 500

    uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # Step 3: Fetch videos from the uploads playlist
    videos = []
    next_page_token = None
    while True:
        playlist_url = "https://www.googleapis.com/youtube/v3/playlistItems"
        playlist_params = {
            "part": "snippet",
            "playlistId": uploads_playlist_id,
            "maxResults": 50,
            "pageToken": next_page_token,
            "key": api_key
        }
        playlist_response = requests.get(playlist_url, params=playlist_params).json()
        logging.debug(f"Playlist response: {playlist_response}")

        if "error" in playlist_response:
            logging.error("Error in playlist response: %s", playlist_response["error"])
            return jsonify({"error": "Error fetching videos"}), 500

        for item in playlist_response.get("items", []):
            video_published = item["snippet"]["publishedAt"]
            if start_date <= video_published <= end_date:
                videos.append({
                    "title": item["snippet"]["title"],
                    "videoId": item["snippet"]["resourceId"]["videoId"],
                    "publishedAt": video_published
                })

        next_page_token = playlist_response.get("nextPageToken")
        if not next_page_token:
            break

    return jsonify(videos)

if __name__ == '__main__':
    app.run(debug=True)
