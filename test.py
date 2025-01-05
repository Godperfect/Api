const express = require("express");
const axios = require("axios");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 3000;

// API key from .env file
const API_KEY = process.env.YOUTUBE_API_KEY;

app.get("/audio", async (req, res) => {
  const query = req.query.query;
  if (!query) {
    return res.status(400).json({ error: "Query parameter is missing" });
  }

  try {
    // Call the YouTube API
    const youtubeURL = `https://www.googleapis.com/youtube/v3/search`;
    const response = await axios.get(youtubeURL, {
      params: {
        part: "snippet",
        q: query,
        type: "video",
        maxResults: 1,
        key: API_KEY,
      },
    });

    // Log response
    console.log("YouTube API Response:", response.data);

    // Extract video ID
    const videoId = response.data.items[0]?.id?.videoId;
    if (!videoId) {
      return res.status(404).json({ error: "No video found for the query" });
    }

    res.json({ videoId, downloadLink: `https://www.youtube.com/watch?v=${videoId}` });
  } catch (error) {
    console.error("Error calling YouTube API:", error.message);
    res.status(500).json({ error: "Something went wrong", details: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
