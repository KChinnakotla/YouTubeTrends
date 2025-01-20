import requests

# Replace with your API key and the target video ID
API_KEY = "[API_KEY]"
VIDEO_ID = "zd7c5tQCs1I"

# Define the API URL and parameters
url = "https://www.googleapis.com/youtube/v3/videos"
params = {
    "part": "snippet,statistics,contentDetails",
    "id": VIDEO_ID,
    "key": API_KEY
}

# Make the request
response = requests.get(url, params=params)
data = response.json()

# Print the retrieved information
if "items" in data and data["items"]:
    video = data["items"][0]
    snippet = video["snippet"]
    stats = video["statistics"]
    details = video["contentDetails"]

    print("Title:", snippet["title"])
    print("Description:", snippet["description"])
    print("Published At:", snippet["publishedAt"])
    print("Channel Title:", snippet["channelTitle"])
    print("View Count:", stats.get("viewCount", "N/A"))
    print("Like Count:", stats.get("likeCount", "N/A"))
    print("Duration:", details["duration"])  # e.g., PT10M30S
else:
    print("No video found with the provided ID.")
