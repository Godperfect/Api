import os
import requests
import yt_dlp
from io import BytesIO

# Load API key from environment variable
API_KEY = os.getenv("YOUTUBE_API_KEY")
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


def search_video(query):
    """Search for a video on YouTube by its name."""
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 1,
        "key": API_KEY
    }

    response = requests.get(SEARCH_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch videos: {response.text}")

    data = response.json()
    if not data["items"]:
        return None

    video = data["items"][0]
    return {
        "videoId": video["id"]["videoId"],
        "title": video["snippet"]["title"]
    }


def download_audio(video_id, video_title):
    """Download audio from a YouTube video."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    audio_buffer = BytesIO()

    options = {
        "format": "bestaudio/best",
        "outtmpl": "-",
        "noplaylist": True,
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "progress_hooks": [lambda d: print(f"Status: {d['status']}")],
        "outtmpl": "-",  # Use BytesIO
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

    sanitized_title = video_title.replace("/", "-").replace("\\", "-")
    return audio_buffer, sanitized_title