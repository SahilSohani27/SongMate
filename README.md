# 🎵 SongMate

**SongMate** is a FastAPI-powered music companion API that lets users:
- 🎧 Download audio from YouTube videos and playlists in MP3 format using `yt-dlp`.
- 📝 Fetch song lyrics from Genius.com using advanced web scraping with **Playwright** and fallback search parsing.

The project is containerized with **Docker**, making it easy to deploy on platforms like Google Cloud Run, AWS, or Render.

---

## 🚀 Key Features

- 🔍 **Dynamic Lyrics Scraping:** Uses Playwright to scrape Genius.com directly. If blocked (e.g., CAPTCHA), falls back to DuckDuckGo search scraping.
- 🎶 **Audio Downloading:** Supports both single video and playlist downloads from YouTube, converting them into MP3.
- ⚙️ **Clean REST API:** Built with FastAPI for modular and maintainable backend development.
- 🐳 **Containerized Deployment:** Dockerized for easy portability and deployment.
- 🛡️ **Robust Error Handling:** Gracefully handles search failures, scraping blocks, and missing data.

---

## 🛠️ Tech Stack

| Component            | Technology         |
|----------------------|--------------------|
| **Backend**          | FastAPI            |
| **Lyrics Scraping**  | Playwright, DuckDuckGo (BeautifulSoup) |
| **Audio Downloads**  | yt-dlp, ffmpeg     |
| **Containerization** | Docker             |
| **Deployment Ready** | Google Cloud Run / Render / AWS |

---

## 📂 API Endpoints

| Method | Endpoint            | Description                                |
|-------|----------------------|--------------------------------------------|
| POST  | `/download/single`    | Download a single YouTube video as MP3     |
| POST  | `/download/playlist`  | Download a full playlist as MP3 zip file   |
| GET   | `/song/lyrics`        | Get lyrics of a song from Genius.com       |

---
