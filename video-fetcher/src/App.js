import React, { useState } from 'react';

const VideoFetcher = () => {
  const [videos, setVideos] = useState([]);
  const [error, setError] = useState("");

  const fetchVideos = () => {
    // Assuming the necessary parameters (API key, channel name, dates) are set
    const apiKey = "[API_KEY]"; // Replace with actual API key or state variable
    const channelName = "@TED"; // Channel name entered by user
    const startDate = "2023-01-01T00:00:00Z"; // Start date entered by user
    const endDate = "2023-01-22T23:59:59Z"; // End date entered by user

    // Make the fetch request to the Flask backend
    fetch(`http://localhost:5000/get_videos?api_key=${apiKey}&channel_name=${channelName}&start_date=${startDate}&end_date=${endDate}`)
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          console.error(data.error);
          setError(data.error); // Show the error message on the frontend
        } else {
          setVideos(data); // Update the videos state
        }
      })
      .catch(err => {
        console.error("Fetch error:", err);
        setError("Error fetching data, please try again.");
      });
  };

  return (
    <div>
      <button onClick={fetchVideos}>Fetch Videos</button>
      {error && <div className="error">{error}</div>}
      <div>
        {videos.length > 0 ? (
          <ul>
            {videos.map((video) => (
              <li key={video.videoId}>
                <h3>{video.title}</h3>
                <p>Published on: {new Date(video.publishedAt).toLocaleDateString()}</p>
                <a href={`https://www.youtube.com/watch?v=${video.videoId}`} target="_blank" rel="noopener noreferrer">
                  Watch Video
                </a>
              </li>
            ))}
          </ul>
        ) : (
          <p>No videos found for the specified criteria.</p>
        )}
      </div>
    </div>
  );
};

export default VideoFetcher;
