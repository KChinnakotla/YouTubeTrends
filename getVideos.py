import requests

# Constants
API_KEY = "[API_KEY]"  # Replace with your YouTube Data API key
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"

def search_videos(query, published_after, published_before, max_results=50):
    """
    Searches for videos based on a query and date range.
    """
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "publishedAfter": published_after,
        "publishedBefore": published_before,
        "maxResults": max_results,
        "key": API_KEY,
    }
    response = requests.get(SEARCH_URL, params=params)
    response.raise_for_status()  # Raise an error if the request fails
    return response.json()

def get_video_statistics(video_ids):
    """
    Retrieves statistics for a list of video IDs.
    """
    params = {
        "part": "statistics",
        "id": ",".join(video_ids),
        "key": API_KEY,
    }
    response = requests.get(VIDEOS_URL, params=params)
    response.raise_for_status()
    return response.json()

def find_videos_with_high_views(query, published_after, published_before, view_threshold):
    """
    Finds videos matching the query and time range with views above the threshold.
    """
    all_videos = []
    next_page_token = None

    # Search for videos in batches
    while True:
        search_response = search_videos(query, published_after, published_before, max_results=50)
        video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]

        # Get video statistics
        if video_ids:
            stats_response = get_video_statistics(video_ids)
            for video in stats_response.get("items", []):
                view_count = int(video["statistics"].get("viewCount", 0))
                if view_count > view_threshold:
                    all_videos.append({
                        "videoId": video["id"],
                        "views": view_count,
                    })

        # Handle pagination
        next_page_token = search_response.get("nextPageToken")
        if not next_page_token:
            break

    return all_videos

# Main Execution
if __name__ == "__main__":
    QUERY = "Fortnite"
    PUBLISHED_AFTER = "2023-01-01T00:00:00Z"
    PUBLISHED_BEFORE = "2023-01-30T23:59:59Z"
    VIEW_THRESHOLD = 20_000_000

    results = find_videos_with_high_views(QUERY, PUBLISHED_AFTER, PUBLISHED_BEFORE, VIEW_THRESHOLD)
    print("Videos with over 20 million views:")
    for video in results:
        print(f"https://www.youtube.com/watch?v={video['videoId']} - {video['views']} views")

